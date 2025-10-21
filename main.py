from funciones import *
from clases import *


bd_ventas = BD("Bd_ventas.db")

bd_ventas.iniciar_tablas()

programa_ventas = Ventas(bd_ventas)

programa_ventas.menu(programa_ventas)