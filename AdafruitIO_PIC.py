'''------------------------------------------------------------------------------
Autor: Andy Bonilla
Programa: laboratorio 3
Creado: 1 de agosto de 2021    
Descripcion: un laboratoria bien fumado tbh pero chilero
intefaz gráfica para el laboratorio de comunicacion SPI
-------------------------------------------------------------------------------'''

'''------------------------------------------------------------------------------
-------------------------IMPORTAR LIBRERIAS--------------------------------------
------------------------------------------------------------------------------'''
import tkinter as tk            #se importa libreria de GUI
from tkinter import *           #se importa libreria de GUI
import serial                   #se importa libreria de comunicacion serial
import io                       #se importa libreria de io
import Adafruit_IO              #se importa libreria de adafruit
from Adafruit_IO import Client, RequestError, Feed  #se crea cliente finquicio

'''------------------------------------------------------------------------------
-------------------------JALAR NUBE DE ADAFRUIT---------------------------------
------------------------------------------------------------------------------'''
ADAFRUIT_IO_USERNAME = "anbo_one"
ADAFRUIT_IO_KEY = "aio_EaPL02hEyCOLeua2tFFkq2ihgXu0"
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

'''------------------------------------------------------------------------------
-----------------------DEFINICION DE OBJETOS------------------------------------
------------------------------------------------------------------------------'''
root = Tk()                     #se le da nombre al objeto principal

'''------------------------------------------------------------------------------
-----------------------DEFINICION DE PUERTO SERIAL-------------------------------
------------------------------------------------------------------------------'''
#DEFINICION DE PUERTO SERIAL
port1=serial.Serial('COM1')                                 #declarar puerto serial y braudeaje
#port1.port('COM1')
port1.baudrate = 9600                                       #set Baud rate to 9600
port1.bytesize = 8                                          # Number of data bits = 8
port1.parity   ='N'                                         # No parity
port1.stopbits = 1                                          # Number of Stop bits = 1
#port1.open()                                                #se abre puerto serial
#variable is stored in the root object
root.counter = 0                #se declara una variables en el objeto



#Digital Feed
digital_feed = aio.feeds('botones')
aio.send_data(digital_feed.key, 16)
digital_data = aio.receive(digital_feed.key)
print(f'digital signal: {digital_data.value}')

#Analog Feed
'''analog_feed = aio.feeds('hello-analog')
aio.send_data(analog_feed.key, 100)
analog_data = aio.receive(analog_feed.key)
print(f'analog signal: {analog_data.value}')'''
