class LogModel:

    def processar_linhas(self, linhas):
        """
        Processa um pedaço do arquivo e devolve
        somente o resumo desse pedaço.
        """

        total_registros = 0
        nivel_0 = 0
        nivel_1 = 0
        nivel_2 = 0
        nivel_3 = 0

        for linha in linhas:
            linha = linha.strip()

            if not linha:
                continue

            partes = linha.split(",")

            # Esperamos:
            # data, hora, nivel, usuario
            if len(partes) != 4:
                continue

            nivel = int(partes[2])

            total_registros += 1

            if nivel == 0:
                nivel_0 += 1
            elif nivel == 1:
                nivel_1 += 1
            elif nivel == 2:
                nivel_2 += 1
            elif nivel == 3:
                nivel_3 += 1

        return {
            "total": total_registros,
            "nivel_0": nivel_0,
            "nivel_1": nivel_1,
            "nivel_2": nivel_2,
            "nivel_3": nivel_3
        }