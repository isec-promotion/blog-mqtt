# MQTT/シリアル通信 HDMI スイッチャー制御システム

このプロジェクトは、Raspberry Pi を使用してキーボード入力を MQTT 経由で送信し、別の Raspberry Pi で受信して HDMI スイッチャーをシリアル通信で制御するシステムです。

## プロジェクト概要

3 つの Python スクリプトで構成されています:

1. **mqtt-tx.py** - キーボードイベント送信側
2. **mqtt-rx.py** - MQTT メッセージ受信・シリアル制御側
3. **serial-switch.py** - シリアル通信テストプログラム

## ファイル説明

### mqtt-tx.py

キーボードのイベントを MQTT ブローカーに送信するプログラムです。

**機能:**

- `/dev/input/event0`からキーボードイベントを読み取り
- キー押下イベントを JSON 形式で MQTT ブローカーに送信
- TLS/SSL 暗号化通信に対応

**送信先:**

- MQTT トピック: `keyboard/movement`
- ブローカー: EMQX Cloud サーバー (ポート 8883)

**送信データ形式:**

```json
{
  "type": イベントタイプ,
  "code": キーコード,
  "value": キーの状態
}
```

### mqtt-rx.py

MQTT メッセージを受信して、HDMI スイッチャーにシリアルコマンドを送信するプログラムです。

**機能:**

- MQTT ブローカーからキーボードイベントを受信
- 特定のキー(1〜4)が押されたときに HDMI スイッチャーを制御
- `/dev/ttyUSB0`経由でシリアルコマンドを送信

**キーマッピング:**

- キー '1' (code: 2) → OUT1 VS IN1
- キー '2' (code: 3) → OUT1 VS IN2
- キー '3' (code: 4) → OUT1 VS IN3
- キー '4' (code: 5) → OUT1 VS IN4

**シリアルコマンド形式:**

```
EZS OUT{x} VS IN{y}\r\n
```

### serial-switch.py

シリアル通信で HDMI スイッチャーのチャネルを切り替えるテストプログラムです。

**機能:**

- 標準入力からキー入力(1〜4)を受け付け
- シリアルポート経由で HDMI スイッチャーにコマンドを送信
- MQTT を使わない単体動作テスト用

**使用方法:**

```bash
python serial-switch.py
```

実行後、1、2、3、4 のいずれかを入力して Enter を押すとチャネルが切り替わります。

## 必要な環境

### ハードウェア

- Raspberry Pi × 2 台
- HDMI スイッチャー (シリアル制御対応)
- USB シリアル変換ケーブル

### ソフトウェア依存関係

```bash
pip install paho-mqtt
pip install evdev
pip install pyserial
```

## セットアップ

### 1. 証明書の配置

EMQX Cloud の CA 証明書を取得し、Raspberry Pi に配置します:

```bash
/home/pi/emqxsl-ca.crt
```

### 2. MQTT 設定の変更

各スクリプトの以下の値を環境に合わせて変更してください:

```python
MQTT_BROKER = 'your-broker.emqxsl.com'  # ブローカーのアドレス
MQTT_USER = 'your-username'              # ユーザー名
MQTT_PASSWORD = 'your-password'          # パスワード
```

### 3. デバイスパスの確認

キーボードデバイスとシリアルポートのパスを確認して必要に応じて変更します:

```bash
# キーボードデバイスの確認
ls /dev/input/event*

# シリアルポートの確認
ls /dev/ttyUSB*
```

### 4. 権限の設定

デバイスへのアクセス権限を付与します:

```bash
# キーボードデバイスへのアクセス
sudo chmod 666 /dev/input/event0

# シリアルポートへのアクセス
sudo chmod 666 /dev/ttyUSB0
```

## 使用方法

### システム全体の動作

1. **送信側 Raspberry Pi**で mqtt-tx.py を実行:

```bash
python mqtt-tx.py
```

2. **受信側 Raspberry Pi**で mqtt-rx.py を実行:

```bash
python mqtt-rx.py
```

3. 送信側のキーボードで 1〜4 のキーを押すと、受信側で HDMI スイッチャーのチャネルが切り替わります。

### 単体テスト

シリアル通信のテストを行う場合:

```bash
python serial-switch.py
```

## システム構成図

```
[Raspberry Pi #1]              [MQTTブローカー]           [Raspberry Pi #2]
  キーボード                    (EMQX Cloud)                HDMIスイッチャー
      ↓                              ↓                           ↓
  mqtt-tx.py  ----MQTT送信--→  keyboard/movement  ----MQTT受信--→  mqtt-rx.py
                                                                    ↓
                                                              シリアル通信
                                                                    ↓
                                                              HDMIスイッチャー
```

## トラブルシューティング

### キーボードイベントが読み取れない

- デバイスパスを確認: `ls /dev/input/event*`
- 権限を確認: `sudo chmod 666 /dev/input/eventX`
- evdev が正しくインストールされているか確認

### シリアル通信ができない

- USB シリアル変換ケーブルが正しく接続されているか確認
- デバイスパスを確認: `ls /dev/ttyUSB*`
- ボーレートが正しいか確認 (57600bps)

### MQTT に接続できない

- ブローカーのアドレスとポートを確認
- ユーザー名とパスワードを確認
- CA 証明書のパスを確認
- ネットワーク接続を確認

## ライセンス

このプロジェクトは教育・学習目的で作成されています。

## 注意事項

- MQTT ブローカーの認証情報は公開しないでください
- 本番環境で使用する場合は、セキュリティ設定を適切に行ってください
- デバイスパスは環境によって異なる場合があります
