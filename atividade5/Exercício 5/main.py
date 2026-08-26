import multiprocessing

from controller import LogController


if __name__ == "__main__":

    multiprocessing.freeze_support()

    arquivo = "sistema.txt"

    controller = LogController(
        arquivo=arquivo,
        quantidade_workers=4,
        tamanho_pedaco=20
    )

    controller.executar()