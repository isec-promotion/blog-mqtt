# mqtt-rx.py - MQTTメッセージを受信して、マウスの移動やクリックを行う
import paho.mqtt.client as mqtt
import json
import serial

# MQTTブローカーの設定
MQTT_BROKER = 'xxxx1234.ala.asia-southeast1.emqxsl.com'
MQTT_PORT = 8883
MQTT_TOPIC = 'keyboard/switch'
MQTT_USER = 'zero-2'
MQTT_PASSWORD = 'password'
MQTT_CAFILE = '/home/pi/emqxsl-ca.crt'

# シリアルポートの設定（ttyUSB0を使用）
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)

# シリアル信号を送る関数
def send_command(x, y):
    command = f'EZS OUT{x} VS IN{y}\r\n'
    ser.write(command.encode())
    print(f'Sent: {command}')

# MQTTメッセージのコールバック関数
def on_message(client, userdata, msg):
    try:
        obj = json.loads(msg.payload)
        code = obj['code']
        if code == 2:  # '1'キー
            send_command(1, 1)
        elif code == 3:  # '2'キー
            send_command(1, 2)
        elif code == 4:  # '3'キー
            send_command(1, 3)
        elif code == 5:  # '4'キー
            send_command(1, 4)
        print(f"Received: {obj}")
    except json.JSONDecodeError:
        pass

# MQTTクライアントの設定
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set(MQTT_CAFILE, tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
client.on_message = on_message

# MQTTブローカーに接続し、トピックを購読
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)

# メインループ
try:
    print("Waiting for MQTT messages...")
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
    ser.close()
    print("終了しました。")
