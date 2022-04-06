import network

wifi=network.WLAN(network.STA_IF)
wifi.active(True)

networks = wifi.scan()

print(networks)