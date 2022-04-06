from machine import Pin
import network
import time
from umqtt.robust import MQTTClient
import sys

led=Pin(2,Pin.OUT)

WIFI_SSID = "kanish"
WIFI_PASSWORD = "Ram@2002"

mqtt_client_id = bytes('client'+'12321','utf-8')

url = 'io.adafruit.com'
username= 'Kanish_R'
key = "aio_xePo60lPCZKDjzl7Oo9TfvXkAMIG"
topic="rl1"

def connect_wifi():
    wifi=network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID,WIFI_PASSWORD)
    if not wifi.isconnected():
        print("Connecting...")
        timeout=0
        while (not wifi.isconnected() and timeout < 5):
            print(5-timeout)
            timeout+=1
            time.sleep(1)
        if wifi.isconnected():
            print("Connected")
        else:
            print("Not Connected")
            sys.exit()
connect_wifi()

client=MQTTClient(client_id=mqtt_client_id,server=url,user=username,password=key,ssl=False)

try:
    client.connect()
except Exception as e:
    print("Could not connect to MQTT Server")
    sys.exit()

def cb (topic,msg):
    print("Received Data: Topic = {} , Msg = {}".format(topic,msg))
    rdata=str(msg,'utf-8')
    if rdata=="0":
        led.value(1)
    else:
        led.value(0)
toggle_feed = bytes('{:s}/feeds/{:s}'.format(username,topic),'utf-8')
client.set_callback(cb)
client.subscribe(toggle_feed)

while True:
    try:
        client.check_msg()
    except :
        client.disconnect()
        sys.exit()
        
    
            