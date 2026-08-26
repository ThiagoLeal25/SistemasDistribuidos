class LogView:

    def mostrar_inicio(self, quantidade_workers, tamanho_pedaco):
        print("=" * 50)
        print("PROCESSADOR DE LOGS")
        print("=" * 50)
        print(f"Workers: {quantidade_workers}")
        print(f"Linhas por pedaço: {tamanho_pedaco}")
        print()

    def mostrar_resultado(self, resultado):
        print()
        print("=" * 50)
        print("RESULTADO FINAL")
        print("=" * 50)

        print(f"Total de registros: {resultado['total']}")
        print(f"Nível 0: {resultado['nivel_0']}")
        print(f"Nível 1: {resultado['nivel_1']}")
        print(f"Nível 2: {resultado['nivel_2']}")
        print(f"Nível 3: {resultado['nivel_3']}")

        print("=" * 50)