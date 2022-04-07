#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ledApp.py
#  
#  
#  
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image, AsyncImage
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
import socket
from threading import *
from kivy.uix.image import Image
from kivy.cache import Cache
import pygame
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import paho.mqtt.client as mqtt
import os
#Inicio Vision
# Fin vision
broker_address="127.0.0.1"



class led(App):
    client = mqtt.Client()
    lbl = Label()
    ipAddress = "127.0.0.1"
    port = 8888
    estado = 0
    estado1 = 0
    estado2 = 0


    def build(self):

        layout = BoxLayout(orientation ='vertical')
        
        row1 = BoxLayout(orientation='vertical')
        

        lbl = Label(text ="Smart Garbage",pos_hint={'center_x':0.5,'center_y':1},font_size ='50sp',color =[0, 1, 0, 1])

        row1.add_widget(lbl)
        
#######Parte 2 -----------------------------------------------
        row2 = BoxLayout(orientation='horizontal')
       # label = Label(text ="Label is Added on screen !!:):)")
                
        btn1 = Button(background_color =(1, 0, 0, 1),size_hint = (0.4,0.9)
                      ,pos_hint={'center_x':0.5,'center_y':0.5},
                        color =(2, 1, 1, 1))
        btn2 = Button(background_color =(0, 1, 0, 1),size_hint = (0.4,0.9),
                        pos_hint={'center_x':0.5,'center_y':0.5},
                        color =(2, 1, 1, 1))
        btn3 = Button(background_color =(0, 0, 1, 1),size_hint = (0.4,0.9),
                        pos_hint={'center_x':0.5,'center_y':0.5}, color =(2, 1, 1, 1))
                      
        row2.add_widget(btn1)
        row2.add_widget(btn2)
        row2.add_widget(btn3)
        btn1.bind(on_press = self.callback)
        btn2.bind(on_press = self.callback1)
        btn3.bind(on_press = self.callback2)

        
#######Parte 3 -----------------------------------------------
        row3 = BoxLayout(orientation='horizontal')

        self.lbl = Label(text= "Temperatura del recipiente rojo")
        self.lbl1 = Label(text= "Estado del recipiente rojo")
        row3.add_widget(self.lbl)
        row3.add_widget(self.lbl1)
        
#######Parte 4 -----------------------------------------------
        row4 = BoxLayout(orientation='horizontal')
       # label = Label(text ="Label is Added on screen !!:):)")
                
        btn4 = Button(text = "Tomar fotografia",size_hint = (.5,.5),
                        background_color =(4, 1, 1, 1),
                        color =(2, 1, 1, 1))
                              
        row4.add_widget(btn4)
        btn4.bind(on_press = self.cam)
        
#######Parte Final -----------------------------------------------

    
        layout.add_widget(row1)
        layout.add_widget(row2)
        layout.add_widget(row3)
        layout.add_widget(row4)
        
        os.system('libcamera-vid -t 0 --inline --listen -o tcp://127.0.0.1:8888')

        return layout
    # callback function tells when button pressed
    def cam(self, event):
        Clock.schedule_interval(self.recv,0.05)
        
    def callback(self, event):
        print("button pressed: publishing a msg to broker")
        if(self.estado == 0):
            self.client.publish("Light/0","on")
            print("Entro a on rojo")
            self.estado = 1
        else:
            self.client.publish("Light/0","off")
            self.estado = 0
            
    def callback1(self, event):
        print("button pressed: publishing a msg to broker")
        if(self.estado1 == 0):
            self.client.publish("Light/0","on1")
            print("Entro a on verde")
            self.estado1 = 1
        else:
            self.client.publish("Light/0","off1")
            self.estado1 = 0
             
    def callback2(self, event):
        print("button pressed: publishing a msg to broker")
        if(self.estado2 == 0):
            self.client.publish("Light/0","on2")
            print("Entro a on azul")
            self.estado2 = 1
        else:
            self.client.publish("Light/0","off2")
            self.estado2 = 0           
        #Clock.schedule_interval(self.recv, 0.05)
            ###
            
    def recv(self, dt):
        clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((self.ipAddress, self.port))
        received = []
        while True:
            recvd_data = clientsocket.recv(230400)
            if not recvd_data:
                break
            else:
                received.append(recvd_data)
        dataset = ''.join(received)
        image = pygame.image.fromstring(dataset,(640, 480),"RGB") # convert received image from string
        try:
            pygame.image.save(image, "foo.jpg")
            self.ids.image_source.reload()
        except:
            pass
        
    def reconocedor(self):
        image_uri = '/home/pi/Downloads/prueba.jpg'
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = image_uri

        response = client.label_detection(image=image)

        print('Labels (and confidence score):')
        print('=' * 30)
        for label in response.label_annotations:
            print(label.description, '(%.2f%%)' % (label.score*100.))

    def on_start(self):

        def on_message(client, userdata, message):
            
            str(message.payload.decode("utf-8"))
            #os.system('libcamera-vid -t 0 --inline --listen -o tcp://127.0.0.1:8888')
            print((str(message.payload.decode("utf-8"))))
            print("message received " ,str(message.payload.decode("utf-8")))
            print("message topic=",message.topic)
            print("mess age qos=",message.qos)
            print("message retain flag=",message.retain)
            userdata['self'].lbl.text = str(message.payload.decode("utf-8"))
            
            
            
        parameters = {'self': self}
        self.client = mqtt.Client(client_id="P1", clean_session = True, userdata=parameters) #create new instance
        self.client.connect(broker_address) #connect to broker
        self.client.on_message = on_message #attach function to callback
        self.client.loop_start() #start the loop
        print("Subscribing to topic","lis/temperatura")
        self.client.subscribe("lis/temperatura")

    

def main(args):
    led().run()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
