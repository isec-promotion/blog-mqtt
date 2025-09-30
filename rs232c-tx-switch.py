# rs232c-tx-switch.py: シリアル通信でチャンネルを切り替えるプログラム
import serial

# シリアルポートの設定（ttyUSB0を使用）
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)

def send_number(number):
    # 数字だけを送信
    ser.write(number.encode())
    print(f"Sent: {number}")

# キーボード入力を標準入力で待ち受ける
try:
    while True:
        key = input("Press 1, 2, 3, or 4 to send the channel number: ")

        if key in ['1', '2', '3', '4']:
            send_number(key)
        else:
            print("Invalid key. Please press 1, 2, 3, or 4.")

except KeyboardInterrupt:
    ser.close()  # プログラム終了時にシリアルポートを閉じる
    print("Serial connection closed")

