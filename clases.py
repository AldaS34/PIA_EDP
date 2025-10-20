import sys
import datetime
import sqlite3
from sqlite3 import Error
from datetime import date, datetime, timedelta
from funciones import *
import openpyxl

class BD:
    def __init__(self,db_nombre):
        self.db_nombre = db_nombre

    def iniciar_tablas(self):
        try:
            with sqlite3.connect(self.db_nombre) as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("CREATE TABLE IF NOT EXISTS Cliente(id_cliente INTERGER PRIMARY KEY,nombre TEXT NOT NULL,apellido_paterno TEXT NOT NULL,apellido_materno TEXT,numero_telefono TEXT NOT NULL,correo TEXT NOT NULL);")
                mi_cursor.execute("CREATE TABLE IF NOT EXISTS Venta(id_venta TEXT PRIMARY KEY,id_cliente INTERGER NOT NULL,fecha_hora DATETIME NOT NULL,total REAL NOT NULL,CONSTRAINT fk_id_cliente FOREIGN KEY(id_cliente) REFERENCES Cliente(id_cliente));")
                mi_cursor.execute("CREATE TABLE IF NOT EXISTS Producto(id_producto TEXT PRIMARY KEY,nombre TEXT NOT NULL,precio REAL NOT NULL);")
                mi_cursor.execute("CREATE TABLE IF NOT EXISTS Venta_Detalle(id_producto TEXT,id_venta TEXT,cantidad REAL NOT NULL,CONSTRAINT fk_id_producto FOREIGN KEY(id_producto) REFERENCES Producto(id_producto),CONSTRAINT fk_id_venta FOREIGN KEY(id_venta) REFERENCES Venta(id_venta),PRIMARY KEY(id_producto,id_venta));")
                print("Tablas creadas con exitosamente")
        except Error as e:
            print(e)
        except Exception as e:
            print(f"Informacion del error: {e}")

    def conteo_clientes(self):
        try:
            with sqlite3.connect(self.db_nombre) as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT COUNT(*) FROM Cliente;")
                registros = mi_cursor.fetchone()
                return registros[0]
        except Error as e:
            print(e)
        except Exception as e:
            print(f"Infomacion del error: {e}")
        
    def insertar_cliente(self,codigo, nombre, apellido_pat,apellido_mat, numero, email):
        try:
            with sqlite3.connect(self.db_nombre) as conn:
                mi_cursor = conn.cursor()
                valores = {"codigo":codigo,"nombre":nombre, "apellido_pat": apellido_pat, "apellido_mat": apellido_mat, "numero": numero, "email": email}
                mi_cursor.execute("INSERT INTO Cliente (id_cliente,nombre,apellido_paterno,apellido_materno,numero_telefono,correo) VALUES(:codigo, :nombre, :apellido_pat, :apellido_mat, :numero, :email)", valores)
                conn.commit()
                print("Usuario Registrado")
                print(f"Clave del usuario registrado: {codigo}")
        except Error as e:
            print(e)
        except Exception as e:
            print(f"El error obtenido es: {e}")

class Ventas:
    def __init__(self, ventas_bd):
        self.ventas_bd = ventas_bd

    def menu(self,ventas):
        while True:
            print("---MENÚ---")
            print("1. Registrar cliente")
            print("2. Registrar producto")
            print("3. Hacer venta")
            print("4. Realizar reporte de ventas")
            print("5. Salir")

            match input("Selecciona una opcion (1-4): "):
                case "1":
                    ventas.registrar_cliente()
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    pass
                case "5":
                    pass
                case _:
                    print("Opcion no valida. Ingrese algun numero del 1-4")
        
    def registrar_cliente(self):
        while True:
            cliente_nom = input("Ingrese nombres del cliente (Escriba SALIR para volver al menú): ").strip()
            if cliente_nom.upper() == "SALIR":
                return 
            cliente_ap = input("Ingrese el apellido paterno: ").strip()
            cliente_am = input("Ingrese el apellido materno (Solo presiona la tecla ENTER para omitir): ").strip()
            if cliente_am == '':
                cliente_am == None
            
            cliente_tel = input("Ingrese el numero de telefono del cliente: ").strip()

            cliente_email = input("Ingrese el email de ").strip()

            codigo_cliente =  self.ventas_bd.conteo_clientes() + 1

            self.ventas_bd.insertar_cliente(codigo_cliente,cliente_nom, cliente_ap, cliente_am, cliente_tel,cliente_email)

            



