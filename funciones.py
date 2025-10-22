def nulificador(valor):
    if valor == '':
        return None
    
def ver_ticket(datos_venta, cantidad, descuento = 0):
        total = 0
        descuento_aplicado = 0
        print("Datos de venta")
        print(f"{"Codigo":^1} {"Producto":^10} {"Precio":^20} {"Cantidad":^25} {"Importe":^15}")

        for datos in datos_venta:
            print(f"{datos[0]:^1} {datos[1]:^15} {datos[2]:^15} {cantidad[datos[0]]:^35} {cantidad[datos[0]]*datos[2]:^5}")
            total += cantidad[datos[0]]*datos[2]
        if descuento > 0:
            print(f"{"Descuendo":>75} {descuento*100}%")
            descuento_aplicado = total * (descuento)
        print(f"{"Total":>75} {total - descuento_aplicado}")
        
def total_venta(datos_venta, carro, descuento = 0):
    total = 0
    for datos in datos_venta:
          total += carro[datos[0]]*datos[2]
    descuento_aplicado = total * descuento
    return total - descuento_aplicado