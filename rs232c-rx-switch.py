# rs232c-rx-switch.py: シリアル通信でチャンネルを切り替えるプログラム
import serial
import time

# シリアルポートの設定
ser_rx = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)  # 受信用ポート
ser_hdmi = serial.Serial('/dev/ttyUSB1', 57600, timeout=1)  # HDMIスイッチャーへの送信用ポート

def send_command_to_hdmi(output, input_):
    # HDMI スイッチャーへのコマンドを生成して送信
    command = f'EZS OUT{output} VS IN{input_}\r\n'
    ser_hdmi.write(command.encode())  # コマンドをエンコードして送信
    print(f"Sent to HDMI switcher: {command}")

def receive_and_process():
    while True:
        if ser_rx.in_waiting > 0:
            # 受信用ポートからデータを読み込む
            received_data = ser_rx.read(ser_rx.in_waiting).decode().strip()
            print(f"Received: {received_data}")

            # 受信したデータに基づいてHDMIスイッチャーを制御
            if received_data in ['1', '2', '3', '4']:
                send_command_to_hdmi(1, received_data)
            else:
                print(f"Invalid data received: {received_data}")

        time.sleep(0.1)

try:
    print("Waiting for data...")
    receive_and_process()

except KeyboardInterrupt:
    ser_rx.close()  # プログラム終了時に受信用シリアルポートを閉じる
    ser_hdmi.close()  # プログラム終了時に送信用シリアルポートを閉じる
    print("Serial connections closed")

