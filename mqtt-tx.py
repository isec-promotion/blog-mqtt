# mqtt-tx.py: キーボードのイベントをMQTTブローカーに送信するプログラム
import evdev
import paho.mqtt.client as mqtt
import json

# MQTTブローカーの設定
MQTT_BROKER = 'xxxx1234.ala.asia-southeast1.emqxsl.com'
MQTT_PORT = 8883
MQTT_TOPIC = 'keyboard/movement'
MQTT_USER = 'zero-1'
MQTT_PASSWORD = 'password'
MQTT_CAFILE = '/home/pi/emqxsl-ca.crt'

# MQTTクライアントの設定
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set(MQTT_CAFILE, tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# デバイスのevent番号を指定（キーボードのイベントデバイス）
device = evdev.InputDevice('/dev/input/event0')

# キーボードイベントの読み取りと送信
try:
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            # データの送信 (JSON形式)
            data = json.dumps({'type': event.type, 'code': event.code, 'value': event.value})
            client.publish(MQTT_TOPIC, data)
            print(f"Sent: {data}")  # 送信したデータを表示
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.disconnect()
