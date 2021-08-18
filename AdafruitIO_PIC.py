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
import builtins
import tkinter as tk            #se importa libreria de GUI
from tkinter import *
import serial, time             #se importa libreria serial y cuenta de tiempo
from Adafruit_IO import Client, RequestError, Feed
'''------------------------------------------------------------------------------
-----------------------DEFINICION DE OBJETOS------------------------------------
------------------------------------------------------------------------------'''
root = Tk()                     #se le da nombre al objeto principal
root.counter = 0                #se declara una variables en el objeto
'''------------------------------------------------------------------------------
-----------------------DEFINICION DE PUERTO SERIAL-------------------------------
------------------------------------------------------------------------------'''
port1=serial.Serial()             #declarar puerto serial y braudeaje
port1.port='COM1'                 #se dice el puerto a usar
port1.baudrate = 9600             #set Baud rate to 9600
port1.bytesize = 8                # Number of data bits = 8
port1.parity   ='N'               # No parity
port1.stopbits = 1                # Number of Stop bits = 1
port1.open()                      #apertura del puerto serial                     
'''------------------------------------------------------------------------------
-------------------INTERCAMBIO DE DATOS CON ADAFRUIT-----------------------------
------------------------------------------------------------------------------'''
#---------INICIALIZACION DE COMUNICACION CON ADAFRUIT
ADAFRUIT_IO_USERNAME = "anbo_one"
ADAFRUIT_IO_KEY = "aio_FMrA69aERoZaQnj6S8twozN8ZzzU"
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)     #parametros

#---------SE MANDAN VALORES DE BOTONES DE GUI A ADAFRUIT
digital_feed = aio.feeds('botones')
aio.send_data(digital_feed.key, root.counter)
digital_data = aio.receive(digital_feed.key)
#print(f'digital signal: {digital_data.value}')

#---------SE MANDAN VALORES DE BOTONES DE PIC A ADAFRUIT
port1.flushInput()
port1.flushOutput()

#---------SE RECIBE DATO DE SLIDER DE ADAFRUIT EN GUI
adafruit_suma=aio.receive('suma-adafruit').value

'''------------------------------------------------------------------------------
-----------------------DEFINICION DE FUNCIONES-----------------------------------
------------------------------------------------------------------------------'''
#---------FUNCION PARA BOTON DE SUMA
def plus_clicked():                                          
    root.counter += 1
    if root.counter>255:           #se restringe limite superior
        root.counter=0
    if root.counter<0:             #se restringe limite inferior
        root.counter=255
    L['text'] = 'Contador: ' + str(root.counter)
    digital_feed = aio.feeds('botones')
    aio.send_data(digital_feed.key, root.counter)
    
#---------FUNCION PARA BOTON DE RESTA
def minus_clicked():                                          
    root.counter -= 1
    if root.counter<0:             #se restringe limite inferior         
        root.counter=255
    if root.counter>255:           #se restringe limite superior
        root.counter=0
    L['text'] = 'Contador: ' + str(root.counter)
    digital_feed = aio.feeds('botones')
    aio.send_data(digital_feed.key, root.counter)
#---------FUNCION PARA BOTON DE ACTUALIZAR DATO DE ADAFRUIT
def actualizar():
    adafruit_suma=aio.receive('suma-adafruit').value    #se recibe dato desde
    recibido=Label(root, text=adafruit_suma)
    recibido.place(x=160, y=220)
    slider.set(adafruit_suma)
    uart_recibido1 = port1.read_until(b',',4)
    uart_recibido2 = uart_recibido1.split(b',')
    digital_feed = aio.feeds('botones-pic')
    aio.send_data(digital_feed.key, int(uart_recibido2[0]))
    print(int(uart_recibido2[0]))
    
    
'''------------------------------------------------------------------------------
----------------------------CUERPO DE INTERFAZ-----------------------------------
------------------------------------------------------------------------------'''
#---------TITULO
titulo=tk.Label(root,text = "GUI para laboratorio 5, Electrónica Digital 2") #texto como titulo de GUI
titulo.place(x=90, y=20)
subtitulo=tk.Label(root, text="Comunicacion con Adafruit")
subtitulo.place(x=115,y=50)
#---------TITULO DE VENTANA
root.title("Electronica Digital 2")                   #le pones titulo al objeto
root.minsize(400,300)                                           #le decis el tamaño a la ventana

#---------BOTON DE SUMA
b1 = Button(root, text="Suma", command=plus_clicked)
b1.place(x=150, y=75)

#---------BOTON DE RESTA PARA ADAFRUIT
b2 = Button(root, text="Resta", command=minus_clicked)
b2.place(x=200,y=75)

#---------BOTON ACTUALIZADOR PARA ADAFRUIT
b3=Button(root, text='Actualizar', command=actualizar)
b3.place(x=160, y=250)

#---------SLIDER CON VALORES DESDE ADAFRUIT
slider=Scale(root, from_=0,to=255, )
slider.pack()
slider.place(x=160, y=110)

#---------TEXTO PARA CONTADOR
L = Label(root, text="No clicks yet.")                      
L.pack()

'''------------------------------------------------------------------------------
---------------------------------MAIN LOOP---------------------------------------
------------------------------------------------------------------------------'''
root.mainloop()
