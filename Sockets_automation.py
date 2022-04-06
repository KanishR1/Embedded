import network
from machine import Pin
import usocket as socket
import time
import sys

def wifi_connect():
    wifi=network.WLAN(network.STA_IF)
    ssid="kanish"
    password="Ram@2002"
    wifi.active(True)
    timeout=0
    if not wifi.isconnected():
        print("connecting") 
        while (not wifi.isconnected() and timeout<5):
            print(5-timeout)
            timeout+=1
            time.sleep(1)
    if wifi.isconnected():
        print("WiFi Connected")
        print(wifi.ifconfig())
    else:
        print("WiFi not connected")
        sys.exit()


html='''<!DOCTYPE html>
<html>
<center><h2>ESP8266 WebServer </h2></center>
<form>
<center>
<h3> LED </h3>
<button name="LED" value='OFF' type='submit'> ON </button>
<button name="LED" value='ON' type='submit'> OFF </button>
</center>
'''
wifi_connect()
led=Pin(2,Pin.OUT)
led.value(0)

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#AF_INET - Internet Socket
#SOCK_STREAM - TCP protocol

Host = '' #Empty means , it will allow all IP address to connect
port = 80
s.bind((Host,port))

s.listen(5) # It will handle maximum of 5 clients at a time

while True:
    conect_socket,address=s.accept()
    print("Got a connection from" ,address)
    request=conect_socket.recv(1024)
    print("Content :",request)
    request=str(request)
    ledon=request.find('/?LED=ON')
    ledoff=request.find('/?LED=OFF')
    
    if ledon==6:
        led.value(1)
    if ledoff==6:
        led.value(0)
    response=html
    conect_socket.send(response)
    conect_socket.close()

