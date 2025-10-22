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
                mi_cursor.execute("CREATE TABLE IF NOT EXISTS Venta(id_venta INTERGER PRIMARY KEY,id_cliente INTERGER NOT NULL,fecha_hora DATETIME NOT NULL,total REAL NOT NULL,descuento REAL,CONSTRAINT fk_id_cliente FOREIGN KEY(id_cliente) REFERENCES Cliente(id_cliente));")
                mi_cursor.execute("CREATE TABLE IF NOT EXISTS Producto(id_producto TEXT PRIMARY KEY,nombre TEXT NOT NULL,precio REAL NOT NULL);")
                mi_cursor.execute("CREATE TABLE IF NOT EXISTS Venta_Detalle(id_producto INTERGER,id_venta TEXT,cantidad REAL NOT NULL,CONSTRAINT fk_id_producto FOREIGN KEY(id_producto) REFERENCES Producto(id_producto),CONSTRAINT fk_id_venta FOREIGN KEY(id_venta) REFERENCES Venta(id_venta),PRIMARY KEY(id_producto,id_venta));")
                print("Tablas creadas con exitosamente")
        except Error as e:
            print(e)
        except Exception as e:
            print(f"Informacion del error: {e}")

    def contador(self,tabla):
        try:
            with sqlite3.connect(self.db_nombre) as conn:
                mi_cursor = conn.cursor()
                sentencia = f"SELECT COUNT(*) FROM {tabla};"
                mi_cursor.execute(sentencia)
                registro = mi_cursor.fetchone()
                return registro[0]
        except Error as e:
            print(e)
        except Exception as e:
            print(f"Informacion del error: {e}")
        
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
    
    def insertar_producto(self,codigo,nombre,precio):
        try:
            with sqlite3.connect(self.db_nombre) as conn:
                mi_cursor = conn.cursor()
                valores = {"codigo":codigo ,"nombre": nombre,"precio": precio}
                mi_cursor.execute("INSERT INTO Producto (id_producto,nombre,precio) VALUES(:codigo, :nombre, :precio)",valores)
                conn.commit()
                print("Producto Registrado")
                print(f"Clave del producto: {codigo}")
        except Error as e:
            print(e)
        except Exception as e:
            print(f"El error obtenido es: {e}")

    def buscar_cliente(self,codigo):
        try:
            with sqlite3.connect(self.db_nombre) as conn:
                mi_cursor = conn.cursor()
                valores = {'codigo': codigo}
                mi_cursor.execute("SELECT * FROM Cliente WHERE id_cliente = :codigo", valores)
                registro = mi_cursor.fetchone()
                if registro:
                    return True
                else:
                    return False
        except Error as e:
            print(e) 
        except Exception as e:
            print(f"El error obtenido es: {e}")
    
    def buscar_producto(self,codigo):
        try:
            with sqlite3.connect(self.db_nombre) as conn:
                mi_cursor = conn.cursor()
                valores = {"codigo": codigo}
                mi_cursor.execute("SELECT * FROM Producto WHERE id_producto = :codigo;", valores)
                registro = mi_cursor.fetchone()
                if registro:
                    return True
                else:
                    return False
        except Error as e:
            print(e)
        except Exception as e:
            print(f"El error obtenido es: {e}")

    def info_productos(self, codigos):
        try:
            with sqlite3.connect(self.db_nombre) as conn:
                mi_cursor = conn.cursor()
                consulta = f"SELECT id_producto, nombre, precio FROM Producto WHERE id_producto IN ({','.join(['?']*len(codigos))})"
                mi_cursor.execute(consulta,codigos)
                registros = mi_cursor.fetchall()
                return registros
        except Error as e:
            print(e)
        except Exception as e:
            print(f"El error obtenido es: {e}")

    def registrar_venta(self, codigoV, codigoC, tiempo, total, carro, descuento = 0):
        try:
            with sqlite3.connect(self.db_nombre) as conn:
                mi_cursor = conn.cursor()
                valores = {'codigoV': codigoV, 'codigoC':codigoC, 'tiempo': tiempo,'total': total,'descuento':descuento*100}
                mi_cursor.execute("INSERT INTO Venta (id_venta,id_cliente,fecha_hora,total,descuento) VALUES (:codigoV, :codigoC, :tiempo, :total, :descuento)", valores)
                for producto, cantidad in carro.items():
                     valores2 = {'codigoV': codigoV, 'codigoP':producto, 'cantidad': cantidad}
                     mi_cursor.execute("INSERT INTO Venta_detalle (id_producto,id_venta, cantidad) VALUES (:codigoP, :codigoV, :cantidad)",valores2)
                conn.commit()
                print("Venta realizada")
        except Error as e:
            print(e)
        except Exception as e:
            print(f"El error obtenido es: {e}")
    
    def ventas_registradas(self):
        try:
            with sqlite3.connect(self.db_nombre) as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("""SELECT V.id_venta, C.nombre ||' ' ||  C.apellido_paterno ||' ' || C.apellido_materno as Cliente, V.fecha_hora,V.descuento || "%" as 'Descuento aplicado', V.total as 'Total de la venta'
                                    FROM VENTA as V
                                    INNER JOIN CLIENTE as C
                                    ON V.id_cliente = C.id_cliente;""")
                registros = mi_cursor.fetchall()
                return registros
        except Error as e:
            print(e)
        except Exception as e:
            print(f"El error obtenido es: {e}")

    def compras_cliente(self, codigo):
        try:
            with sqlite3.connect(self.db_nombre) as conn:
                mi_cursor = conn.cursor()
                valores = {"codigo": codigo}
                mi_cursor.execute("SELECT COUNT(*) FROM Venta WHERE id_cliente = :codigo", valores)
                registro = mi_cursor.fetchone()
                return registro[0]
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

            match input("Selecciona una opcion (1-5): "):
                case "1":
                    ventas.registrar_cliente()
                case "2":
                    ventas.registrar_producto()
                case "3":
                    ventas.realizar_venta()
                case "4":
                    ventas.reporte_ventas()
                case "5":
                    break
                case _:
                    print("Opcion no valida. Ingrese algun numero del 1-5")
        
    def registrar_cliente(self):
        while True:
            cliente_nom = input("Ingrese nombres del cliente (Escriba SALIR para volver al menú.): ").strip()
            if cliente_nom.upper() == "SALIR":
                return 
            cliente_ap = input("Ingrese el apellido paterno: ").strip()
            cliente_am = input("Ingrese el apellido materno (Solo presione la tecla ENTER para omitir): ").strip()
            if cliente_am == '':
                cliente_am == None
            
            cliente_tel = input("Ingrese el numero de telefono del cliente: ").strip()

            cliente_email = input("Ingrese el email del cliente: ").strip()

            codigo_cliente =  self.ventas_bd.contador("Cliente") + 1

            self.ventas_bd.insertar_cliente(codigo_cliente,cliente_nom, cliente_ap, cliente_am, cliente_tel,cliente_email)

    
    def registrar_producto(self):
        while True:
            producto_nombre = input("Ingrese el nombre del producto (Escriba SALIR para volver al menú.): ")
            if producto_nombre.upper() == "SALIR":
                return
            while True:
                try:
                    producto_precio = float(input("Ingrese el precio del producto: "))
                    break
                except ValueError:
                    print("Ingrese un valor valido")

            codigo_producto = f"{producto_nombre[0:2]}{self.ventas_bd.contador("Producto") + 1}" 

            self.ventas_bd.insertar_producto(codigo_producto,producto_nombre,producto_precio)


    def realizar_venta(self):
        while True:
            carro = {}
            print("---MENÚ DE VENTAS---")
            codigo_cliente = input("Ingrese el codigo de cliente: (Escriba SALIR para volver al menú.): ").strip()
            if codigo_cliente.upper() == "SALIR":
                return 
            if self.ventas_bd.buscar_cliente(codigo_cliente):
                print("Cliente encontrado")
                if self.ventas_bd.compras_cliente(codigo_cliente) == 0:
                    descuento = 0.45
                else:
                    descuento = 0
            else:
                print("Cliente no registrado")
                return
            while True: 
                cod_producto = input("Ingrese el codigo del producto(Presione la tecla ENTER al acabar de ingresar productos): ").strip()
                if cod_producto == '':
                    break
                if self.ventas_bd.buscar_producto(cod_producto):
                    print("Producto agregado")
                else:
                    print("Producto no encontrado")
                    continue 
                if cod_producto in carro:
                    carro[cod_producto] += 1
                else:
                    carro[cod_producto] = 1 
                info_productos = self.ventas_bd.info_productos(list(carro.keys()))
                ver_ticket(info_productos,carro, descuento)
            while True:
                opcion = input("Confirmar la compra [S/N]: ").strip().upper()
                if opcion == 'S':
                    codigo_venta = self.ventas_bd.contador("Venta") + 1
                    tiempo = datetime.now()
                    total = total_venta(info_productos,carro, descuento)
                    self.ventas_bd.registrar_venta(codigo_venta,codigo_cliente,tiempo,total,carro,descuento)
                    break
                elif opcion == 'N':
                    return 
                else:
                    print("Ingrese las opciones S o N")
    
    def reporte_ventas(self):
        registros = self.ventas_bd.ventas_registradas()
        try:
            hoja_calculo = openpyxl.Workbook()
            hoja = hoja_calculo.active
            hoja.title = "Ventas"

            encabezados = ["Id_venta","Cliente", "Fecha y hora", "Descuento aplicado", "Total de la venta"]
            hoja.append(encabezados)

            for venta in registros:
                hoja.append(venta)
            hoja_calculo.save("Ventas_registradas.xlsx")
            print("Ventas exportadas a hoja de excel")
        except Exception as e:
            print(f"El error obtenido fue: {e}")
                




            
    
