#Proyecto billetera para criptos
import requests
from datetime import datetime #Obtener fecha y hora del sistema
diaConsulta = datetime.now () #Indica la hora actual

global registro
registro = list ()
global codigo_usuario
codigo_usuario = int (input ("¡Bienvenido! Por favor indique su numero de usuario: ")) #Solicita al usuario su código
global balance_moneda
balance_moneda = 0

monedas_list = []
precios_list = []

COINMARKET_API_KEY = "edfb80cf-4e28-402c-868f-6071813d94df" 
headers = {
  'Accepts' : 'application/json',
  'X-CMC_PRO_API_KEY' : COINMARKET_API_KEY
}

data = requests.get ("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest", headers = headers).json()

for cripto in data ["data"] :
    monedas_list.append (cripto ["symbol"])
    precios_list.append(cripto ["quote"]["USD"]["price"])

def moneda_recibida (cripto) :
    return cripto in recibir_moneda

def moneda_enviada (cripto) :
    return cripto in enviar_moneda

def moneda_consulta (cripto) :
    return cripto in consulta_cripto

recibir_moneda = tuple (monedas_list)
enviar_moneda = tuple (monedas_list)
consulta_cripto = tuple (monedas_list)
precios = tuple (precios_list)

class Transacciones : #Atributos transacciones
    transaccion_info = ()
    saldo_total_usd = 0
    recibir_moneda = ""
    enviar_moneda = ""
    recibir_cantidad = 0
    enviar_cantidad = 0

rt = Transacciones

def recibir_monto () :
    rt.recibir_moneda = input ("Ingrese la moneda a recibir: ") #Indica la moneda a recibir por el usuario
    while not moneda_recibida (rt.recibir_moneda): #Verifica cripto
        print("Moneda invalida.")
        rt.recibir_moneda = input ("Ingrese la moneda a recibir: ")
    rt.recibir_cantidad = float (input ("Ingrese la cantidad a recibir: ")) #Indica la cantidad a recibir por el usuario
    codigo_sender = int (input ("Código del usuario que envía las criptomonedas: ")) #Indica el código de usuario de quien envía las criptos
    if codigo_sender == codigo_usuario : #Verifica que el código de quien envía sea distinto al que recibe
        i = 0
        while i == 0 :
            print ("Código de usuario personal, por favor verifique el código de usuario.")
            codigo_sender = int (input ("Código del usuario que envía las criptomonedas: "))
            if codigo_sender != codigo_usuario :
                i = i + 1
    indice_moneda = monedas_list.index (rt.recibir_moneda) #Devuelve el índice en el cual se encuentra la cripto
    precio = precios_list [indice_moneda] #Busca el precio de la cripto en la lista de precios
    cantidad_fiat_recibida = rt.recibir_cantidad * precio #Indica monto en USD de cripto
    rt.transaccion_info = "Ud. recibió%6.2f"%float(rt.recibir_cantidad) + " " + rt.recibir_moneda + " del usuario " + str(codigo_sender) + " el día " + diaConsulta.strftime("%A %d/%m/%y a las %H:%M") + "." #Confirma la transacción al usuario.
    print ("Ud. recibió%6.2f"%float (rt.recibir_cantidad) + " " + rt.recibir_moneda + " del usuario " + str(codigo_sender) + " el día " + diaConsulta.strftime("%A %d/%m/%y a las %H:%M")) #Confirma la transacción al usuario.
    print ("%6.2f"%float (cantidad_fiat_recibida))
    rt.saldo_total_usd = rt.saldo_total_usd + cantidad_fiat_recibida
    print ("%6.2f"%float (rt.saldo_total_usd))
    registro.append (rt.transaccion_info) #Guarda registro de la consulta en el registro general
    archivo_registro ()

def transferir_monto () :
    rt.enviar_moneda = input ("Ingrese la moneda a enviar: ") #Indica la moneda a enviar por el usuario
    while not moneda_enviada (rt.enviar_moneda): #Verifica cripto
        print("Moneda invalida.")
        rt.enviar_moneda = input ("Ingrese la moneda a enviar: ")
    rt.enviar_cantidad = float (input ("Ingrese la cantidad a enviar: ")) #Indica la cantidad a recibir por el usuario
    indice_moneda = monedas_list.index (rt.enviar_moneda) #Devuelve el índice en el cual se encuentra la cripto
    precio = precios_list [indice_moneda] #Busca el precio de la cripto en la lista de precios
    cantidad_fiat_enviada = rt.enviar_cantidad * precio #Indica monto en USD de cripto
    if cantidad_fiat_enviada > rt.saldo_total_usd : #Verifica que el usuario tenga saldo sufiente en la cuenta para transferir
        e = 0
        while e == 0 :
            print ("Fondos insuficientes, por favor verifique la transacción e indique un nuevo monto.")
            rt.enviar_cantidad = float (input ("Ingrese la cantidad a enviar: "))
            cantidad_fiat_enviada = rt.enviar_cantidad * precio
            if cantidad_fiat_enviada <= rt.saldo_total_usd :
                e = e + 1
    codigo_destinatario = int (input ("Código del usuario destinatario de las criptomonedas: ")) #Indica el código de usuario destinatario de las criptos
    if codigo_destinatario == codigo_usuario : #Verifica que el código del destinatario sea distinto al del usuario
        i = 0
        while i == 0 :
            print ("Código de usuario personal, por favor verifique el código de usuario.")
            codigo_destinatario = int (input ("Código del usuario destinatario de las criptomonedas: "))
            if codigo_destinatario != codigo_usuario :
                i = i + 1
    rt.transaccion_info = "Ud. envió%6.2f"%float(rt.enviar_cantidad) + " " + rt.enviar_moneda + " al usuario " + str(codigo_destinatario) + " el día " + diaConsulta.strftime("%A %d/%m/%y a las %H:%M") + "." #Registra la transacción al usuario.
    print ("Ud. envió%6.2f"%float(rt.enviar_cantidad) + " " + rt.enviar_moneda + " al usuario " + str(codigo_destinatario) + " el día " + diaConsulta.strftime("%A %d/%m/%y a las %H:%M")) #Confirma la transacción al usuario.
    print ("%6.2f"%float (cantidad_fiat_enviada))
    rt.saldo_total_usd = rt.saldo_total_usd - cantidad_fiat_enviada
    print ("%6.2f"%float (rt.saldo_total_usd))
    registro.append (rt.transaccion_info) #Guarda registro de la consulta en el registro general 
    archivo_registro ()
    
def balance_cripto () :
    consulta_cripto = str (input ("Indique la criptomoneda a consultar: ")) #Solicita la cripto para consultar balance
    while not moneda_consulta (consulta_cripto): #Verifica cripto
        print("Moneda Invalida.")
        consulta_cripto = input ("Ingrese la moneda a consultar: ")
    for rt.transaccion_info in registro :
        if rt.recibir_moneda == consulta_cripto and rt.enviar_moneda == consulta_cripto :
            balance_moneda = (float (rt.recibir_cantidad) - float (rt.enviar_cantidad))
    print ("Su balance de " + consulta_cripto + " es de " + str (balance_moneda) + " al día " + diaConsulta.strftime("%A %d/%m/%y a las %H:%M")) #Muestra el balance de la criptomoneda
    rt.transaccion_info = "Ud. consultó su balance de la moneda " + consulta_cripto + " el día " + diaConsulta.strftime("%A %d/%m/%y a las %H:%M") + "." #Guarda registro de la consulta en el registro general
    registro.append (rt.transaccion_info) #Guarda registro de la consulta en el registro general
    archivo_registro ()

def balance_general () :
    print ("Su balance total es de " + str ("%6.2f"%float (rt.saldo_total_usd)) + " USD al día " + diaConsulta.strftime("%A %d/%m/%y a las %H:%M")) #Muestra el balance de la criptomoneda
    rt.transaccion_info = "Ud. consultó su balance general el día " + diaConsulta.strftime("%A %d/%m/%y a las %H:%M") + "." #Guarda registro de la consulta en el registro general
    registro.append (rt.transaccion_info) #Guarda registro de la consulta en el registro general
    archivo_registro ()

def registro_transacciones () : 
    print ("Este es el registro de todos sus movimientos:")
    archivo = open ("registro_transacciones.txt")
    print (archivo.read())
    archivo.close()
    
def salir () :
    print ("Gracias por usar la billetera, ¡hasta pronto!") #Imprime mensaje de despedida al usuario y cierra la aplicación

def archivo_registro () : #Guarda el registro en un archivo de texto
    archivo = open ("registro_transacciones.txt", "a")
    archivo.write (rt.transaccion_info + "\n")
    archivo.close()

def iniciar_billetera () : #Muestra el menú de opciones al usuario y espera por la selección del usuario
    opcion = 0 
    while opcion != 6 :
        #Preguntar opción    
        print ("Por favor seleccione una de las siguientes opciones: \n 1- Recibir criptomonedas. \n 2- Transferir criptomonedas. \n 3- Mostrar balance de criptomoneda. \n 4- Mostrar balance general. \n 5- Mostrar histórico de transacciones. \n 6- Salir del programa.")
        opcion = int (input ("Introduzca su selección: "))
        if opcion == 1 : 
            recibir_monto ()           
        elif opcion == 2 :
            transferir_monto ()            
        elif opcion == 3 :
            balance_cripto ()            
        elif opcion == 4 :
            balance_general ()
        elif opcion == 5 :
            registro_transacciones ()
        elif opcion == 6 :
            salir ()
        else :
            print ("Por favor seleccione una opción válida.") #Verifica que el usuario seleccione una opción válida

iniciar_billetera ()
