import sys
import datetime
import sqlite3
from sqlite3 import Error
from datetime import date, datetime, timedelta
from funciones import *
from clases import *
import openpyxl


bd_ventas = BD("Bd_ventas.db")

bd_ventas.iniciar_tablas()

programa_ventas = Ventas(bd_ventas)

programa_ventas.menu(programa_ventas)