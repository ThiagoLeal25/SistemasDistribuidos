from model import LogModel


def trabalhador(fila_tarefas, fila_resultados):
    """
    Trabalhador independente.

    Recebe um pedaço do arquivo pela fila,
    processa e envia o resultado pela fila de resultados.
    """

    model = LogModel()

    while True:

        tarefa = fila_tarefas.get()

        # None significa que não existem mais tarefas
        if tarefa is None:
            break

        resultado = model.processar_linhas(tarefa)

        fila_resultados.put(resultado)