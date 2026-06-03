from machine import Pin, ADC, I2C
import network
import time
from umqtt.simple import MQTTClient

# =========================
# WIFI
# =========================
SSID = "Wokwi-GUEST"
SENHA = ""
# =========================
# MQTT
# =========================
BROKER = "test.mosquitto.org"  # Teste com outro broker
CLIENT_ID = f"sigh_mackenzie_luiz_2026"  
TOPICO_UMIDADE = b"mackenzie/luizferreira/projeto2026/umidade"
TOPICO_COMANDO = b"mackenzie/luizferreira/projeto2026/comando"
TOPICO_STATUS = b"mackenzie/luizferreira/projeto2026/status"
# =========================
# HARDWARE
# =========================
sensor = ADC(Pin(34))
sensor.atten(ADC.ATTN_11DB)
valvula = Pin(5, Pin.OUT)
valvula.value(1)  # Inicialmente desligada (HIGH)

# =========================
# LCD I2C
# =========================
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
devices = i2c.scan()
if len(devices) == 0:
    raise Exception("LCD I2C não encontrado")
addr = devices[0]
BACKLIGHT = 0x08
ENABLE = 0x04

def lcd_write(data):
    i2c.writeto(addr, bytearray([data | BACKLIGHT]))

def lcd_toggle(data):
    lcd_write(data | ENABLE)
    time.sleep_us(1)
    lcd_write(data & ~ENABLE)
    time.sleep_us(50)

def lcd_send_nibble(nibble):
    lcd_write(nibble)
    lcd_toggle(nibble)

def lcd_send_byte(byte, mode):
    high = mode | (byte & 0xF0)
    low = mode | ((byte << 4) & 0xF0)
    lcd_send_nibble(high)
    lcd_send_nibble(low)

def lcd_cmd(cmd):
    lcd_send_byte(cmd, 0)

def lcd_data(data):
    lcd_send_byte(data, 1)

def lcd_init():
    time.sleep(0.02)
    lcd_send_nibble(0x30)
    time.sleep(0.005)
    lcd_send_nibble(0x30)
    time.sleep(0.001)
    lcd_send_nibble(0x30)
    lcd_send_nibble(0x20)
    lcd_cmd(0x28)
    lcd_cmd(0x0C)
    lcd_cmd(0x06)
    lcd_cmd(0x01)
    time.sleep(0.002)

def lcd_clear():
    lcd_cmd(0x01)
    time.sleep(0.002)

def lcd_set_cursor(col, row):
    mapa = [0x80, 0xC0]
    lcd_cmd(mapa[row] + col)

def lcd_print(text):
    for c in text:
        lcd_data(ord(c))

# =========================
# WIFI
# =========================
def conecta_wifi():
    wifi = network.WLAN(network.STA_IF)
    if not wifi.active():
        wifi.active(True)
    if wifi.isconnected():
        return wifi
    lcd_clear()
    lcd_print("Conectando")
    lcd_set_cursor(0, 1)
    lcd_print("WiFi...")
    print("Conectando WiFi...")
    wifi.connect(SSID, SENHA)
    timeout = 20
    while not wifi.isconnected() and timeout > 0:
        print(".", end="")
        time.sleep(1)
        timeout -= 1
    if wifi.isconnected():
        print("\nWiFi conectado")
        print(wifi.ifconfig())
        lcd_clear()
        lcd_print("WiFi OK")
        time.sleep(2)
        return wifi
    raise Exception("Falha ao conectar WiFi")

def verifica_wifi():
    wifi = network.WLAN(network.STA_IF)
    if not wifi.isconnected():
        print("WiFi perdido")
        conecta_wifi()

# =========================
# MQTT
# =========================
client = None

def receber_msg(topico, msg):
    print("================================")
    print("Mensagem recebida")
    print("Topico:", topico)
    print("Payload:", msg)
    print("================================")
    if msg == b"ON":
        print("Valvula LIGADA")
        valvula.value(0)
    elif msg == b"OFF":
        print("Valvula DESLIGADA")
        valvula.value(1)

def conecta_mqtt():
    global client
    while True:
        try:
            lcd_clear()
            lcd_print("Conectando")
            lcd_set_cursor(0, 1)
            lcd_print("MQTT...")
            print("Conectando MQTT...")
            client = MQTTClient(
                CLIENT_ID,
                BROKER,
                keepalive=60
            )
            client.set_callback(receber_msg)
            client.connect()
            client.subscribe(TOPICO_COMANDO)
            print("MQTT conectado")
            client.publish(
                TOPICO_STATUS,
                b"ONLINE"
            )
            lcd_clear()
            lcd_print("MQTT OK")
            time.sleep(2)
            return client
        except Exception as e:
            print("Erro MQTT:", e)
            time.sleep(5)

def verifica_mensagens():
    global client
    try:
        client.check_msg()
    except Exception as e:
        print("Erro MQTT:", e)
        try:
            client.disconnect()
        except:
            pass
        conecta_mqtt()

# =========================
# Leitura do Sensor
# =========================
MOLHADO = 0     # Valor mínimo do potenciômetro
SECO = 4095     # Valor máximo do potenciômetro
UMIDADE_MINIMA = 30  # Umidade mínima para ativar os irrigadores

def ler_umidade():
    valor = sensor.read()
    umidade = (valor - MOLHADO) * 100 / (SECO - MOLHADO)
    umidade = max(0, min(100, int(umidade)))
    return umidade

# =========================
# Inicialização
# =========================
lcd_init()
conecta_wifi()
conecta_mqtt()

# =========================
# Loop Principal
# =========================
while True:
    verifica_wifi()
    verifica_mensagens()
    umidade = ler_umidade()
    print("Umidade:", umidade)
    
    if umidade < UMIDADE_MINIMA:
        lcd_clear()
        lcd_print("Ativando")
        lcd_set_cursor(0, 1)
        lcd_print("Irrigadores...")
        valvula.value(0)  # Liga os irrigadores
        client.publish(TOPICO_STATUS, b"IRRI_ON")
    else:
        lcd_clear()
        lcd_print(f"Umidade: {umidade}%")
        lcd_set_cursor(0, 1)
        lcd_print("Irrigadores OFF")
        valvula.value(1)  # Desliga os irrigadores
        client.publish(TOPICO_STATUS, b"IRRI_OFF")
    
    client.publish(TOPICO_UMIDADE, str(umidade).encode())
    time.sleep(10)  # Aguarde 10 segundos antes de enviar a próxima leitura
