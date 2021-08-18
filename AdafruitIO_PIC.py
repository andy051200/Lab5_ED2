'''------------------------------------------------------------------------------
Autor: Andy Bonilla
Programa: laboratorio 5
Creado: 16 de agosto de 2021    
Descripcion: un laboratoria bien fumado tbh pero chilero
intefaz gráfica para el laboratorio de comunicacion SPI
-------------------------------------------------------------------------------'''


'''------------------------------------------------------------------------------
-------------------------IMPORTAR LIBRERIAS--------------------------------------
------------------------------------------------------------------------------'''
import tkinter as tk            #se importa libreria de GUI
from tkinter import *
#import serial, time             #se importa libreria serial y cuenta de tiempo
from Adafruit_IO import Client, RequestError, Feed
'''------------------------------------------------------------------------------
-----------------------DEFINICION DE OBJETOS------------------------------------
------------------------------------------------------------------------------'''
root = Tk()                     #se le da nombre al objeto principal
root.counter = 0                #se declara una variables en el objeto
'''------------------------------------------------------------------------------
-----------------------DEFINICION DE PUERTO SERIAL-------------------------------
------------------------------------------------------------------------------'''
'''
port1=serial.Serial()             #declarar puerto serial y braudeaje
port1.port='COM1'                 #se dice el puerto a usar
port1.baudrate = 9600             #set Baud rate to 9600
port1.bytesize = 8                # Number of data bits = 8
port1.parity   ='N'               # No parity
port1.stopbits = 1                # Number of Stop bits = 1
port1.open()                      #apertura del puerto serial                 '''     
'''------------------------------------------------------------------------------
-----------------------DEFINICION DE ADAFRUIT-----------------------------------
------------------------------------------------------------------------------'''
ADAFRUIT_IO_USERNAME = "anbo_one"                       #usuario
ADAFRUIT_IO_KEY = "aio_EaPL02hEyCOLeua2tFFkq2ihgXu0"    #contraseña
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)     #parametros

#---------
digital_feed = aio.feeds('botones')
aio.send_data(digital_feed.key, root.counter)
digital_data = aio.receive(digital_feed.key)
#print(f'digital signal: {digital_data.value}')

#uart_recibido = port1.read_until(b'\r', size=4)      
#uart_recibido=int(uart_recibido)   
#print(uart_recibido)


#-------mandar datos desde el pic para adafruit
'''digital_feed = aio.feeds('botones-pic')
aio.send_data(digital_feed.key, uart_recibido)
digital_data = aio.receive(digital_feed.key)'''


'''------------------------------------------------------------------------------
-----------------------DEFINICION DE FUNCIONES-----------------------------------
------------------------------------------------------------------------------'''
def plus_clicked():                                          #se define funcion para sumar
    root.counter += 1
    if root.counter>255:                             #se restringe rango superior
        root.counter=0
    if root.counter<0:
        root.counter=255
    L['text'] = 'Contador: ' + str(root.counter)
    aio.send_data(digital_feed.key, root.counter)
    

def minus_clicked():                                          #se define funcion para sumar
    root.counter -= 1
    if root.counter<0:
        root.counter=255
    if root.counter>255:
        root.counter=0
    L['text'] = 'Contador: ' + str(root.counter)
    aio.send_data(digital_feed.key, root.counter)

'''------------------------------------------------------------------------------
----------------------------CUERPO DE INTERFAZ-----------------------------------
------------------------------------------------------------------------------'''
#TITULO
titulo=tk.Label(root,text = "GUI para laboratorio 5, Electrónica Digital 2") #texto como titulo de GUI
titulo.place(x=90, y=20)
subtitulo=tk.Label(root, text="Comunicacion con Adafruit")
subtitulo.place(x=115,y=50)
#titulo de la ventana
root.title("GUI Lab5, Electronica Digital 2")                   #le pones titulo al objeto
root.minsize(400,300)                                           #le decis el tamaño a la ventana

#boton de suma
b1 = Button(root, text="Suma", command=plus_clicked)
b1.place(x=150, y=75)

#boton de resta 
b2 = Button(root, text="Resta", command=minus_clicked)
b2.place(x=200,y=75)

slider=Scale(root, from_=0,to=100)
slider.pack()
slider.place(x=160, y=110)
'''
#POTENCIOMETROS
#prueba=port1.read()
label_pots=tk.Label(root, text=port1.read())
label_pots.place(x=135, y=150)
#print(port1.read())

#texto indicador
label1 = tk.Label(root, text = "Valor potenciometro 1")        #texto para el cuadro de texto
label1.place(x=70,y=110)                                       #ubicacion del texto para contador
pot1=tk.LabelFrame(root, text=port1.read())
pot1.place(x=70,y=125)'''

#POTENCIOMETRO2
#texto indicador
'''label2 = tk.Label(root, text = "Valor potenciometro 2")        #texto para el cuadro de texto
label2.place(x=210,y=110)                                      #ubicacion del texto para contador
pot2=tk.LabelFrame(root, text="wenas")
pot2.place(x=260, y=110)'''
L = Label(root, text="No clicks yet.")                      
L.pack()

'''------------------------------------------------------------------------------
---------------------------------MAIN LOOP---------------------------------------
------------------------------------------------------------------------------'''
root.mainloop()
#loop para que siempre esté mandando el pic para adafruit
'''while 1:
    digital_feed = aio.feeds('botones-pic')
    aio.send_data(digital_feed.key, uart_recibido)
    digital_data = aio.receive(digital_feed.key)'''

