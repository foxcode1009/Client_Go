# aqui estara el inicio de el codigo
from Main import Iniciosesion
from data_base import DDBB

# PRIMERO CREAMOS LA BASE DE DATOS Y LUEGO SE EJECUTA EL PROGRAMA
DDBB()


if __name__ == "__main__":
    # inicio sesion
    iniciar = Iniciosesion()
    iniciar.inicio()
