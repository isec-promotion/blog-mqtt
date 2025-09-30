# serial-switch.py: シリアル通信でチャンネルを切り替えるプログラム
import serial
import time

# シリアルポートの設定（ttyUSB0を使用）
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)

def send_command(x, y):
    # xとyの値を入れて、コマンドを作成
    command = f'EZS OUT{x} VS IN{y}\r\n'
    ser.write(command.encode())  # コマンドをエンコードして送信
    print(f'Sent: {command}')

# キーボード入力を標準入力で待ち受ける
try:
    while True:
        key = input("Press 1, 2, 3, or 4 to change the channel: ")
        
        if key == '1':
            send_command(1, 1)
        elif key == '2':
            send_command(1, 2)
        elif key == '3':
            send_command(1, 3)
        elif key == '4':
            send_command(1, 4)
        else:
            print("Invalid key. Please press 1, 2, 3, or 4.")

except KeyboardInterrupt:
    ser.close()  # プログラム終了時にシリアルポートを閉じる
    print("Serial connection closed")
