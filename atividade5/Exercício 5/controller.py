import multiprocessing

from worker import trabalhador
from view import LogView


class LogController:

    def __init__(self, arquivo, quantidade_workers=4, tamanho_pedaco=20):

        self.arquivo = arquivo
        self.quantidade_workers = quantidade_workers
        self.tamanho_pedaco = tamanho_pedaco

        self.view = LogView()

    def executar(self):

        # Filas de mensagens
        fila_tarefas = multiprocessing.Queue()
        fila_resultados = multiprocessing.Queue()

        # Criando o pool de trabalhadores
        workers = []

        for _ in range(self.quantidade_workers):

            processo = multiprocessing.Process(
                target=trabalhador,
                args=(fila_tarefas, fila_resultados)
            )

            processo.start()
            workers.append(processo)

        self.view.mostrar_inicio(
            self.quantidade_workers,
            self.tamanho_pedaco
        )

        quantidade_tarefas = 0

        # ==========================================
        # COORDENADOR LÊ E DIVIDE O ARQUIVO
        # ==========================================

        with open(self.arquivo, "r", encoding="utf-8") as arquivo:

            pedaço = []

            for linha in arquivo:

                pedaço.append(linha)

                if len(pedaço) >= self.tamanho_pedaco:

                    fila_tarefas.put(pedaço)

                    quantidade_tarefas += 1

                    pedaço = []

            # Envia o último pedaço
            if pedaço:
                fila_tarefas.put(pedaço)
                quantidade_tarefas += 1

        # ==========================================
        # AVISA AOS WORKERS QUE ACABARAM AS TAREFAS
        # ==========================================

        for _ in range(self.quantidade_workers):
            fila_tarefas.put(None)

        # ==========================================
        # RECEBE OS RESULTADOS
        # ==========================================

        resultado_final = {
            "total": 0,
            "nivel_0": 0,
            "nivel_1": 0,
            "nivel_2": 0,
            "nivel_3": 0
        }

        for _ in range(quantidade_tarefas):

            resultado = fila_resultados.get()

            resultado_final["total"] += resultado["total"]
            resultado_final["nivel_0"] += resultado["nivel_0"]
            resultado_final["nivel_1"] += resultado["nivel_1"]
            resultado_final["nivel_2"] += resultado["nivel_2"]
            resultado_final["nivel_3"] += resultado["nivel_3"]

        # ==========================================
        # ESPERA TODOS OS WORKERS TERMINAREM
        # ==========================================

        for processo in workers:
            processo.join()

        self.view.mostrar_resultado(resultado_final)