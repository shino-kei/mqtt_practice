# ROS特訓 

## IPアドレスとネットワークについて理解しよう

* ifconfigコマンド
* ssh(telnet)コマンド
* sftp(ftp)コマンド
* vi,nanoコマンド

## Pub/Sub型のデータ通信方法について理解する（MQTT）
### MQTTとは
MQTTでのデータ通信はPublish/Subscriber型のメッセージングによって行われます．
情報の送信者のことをPublisher，情報の受信者のことをSubscriberと呼んでいます．
両者はトピックと呼ばれる関心事の名前を共有し，Publisherはトピックを指定してメッセージを送信し，
Subscriberはトピックからメッセージを受け取ります．

PublisherとSubscriberのメッセージの伝達には，仲介者（MQTTではブローカーと呼ばれます）
が両者の間を取り持つことで成立しています．
すると，情報を受け取るSubscriberは、最初にトピックにSubScribeすると、
その後はただ待っているだけで、そのトピックに情報の更新があるたびに、メッセージを受け取ることができます．
なので，ポーリングによって，定期的にデータが来ているかを監視する必要がないため，
非同期システムを比較的簡単に構築することができることが非常に大きなメリットといえます．

メッセージの送信者であるPublisherと，送信先であるSubscriberとの間にMQTTブローカーが仲介することによって，
PublisherはSubscriberの存在を強く意識することなく，メッセージを送信することができるため，
プログラムの設計者は，外部システムとの入出力関係だけに注目すれば良くなることから，
ロボット開発（特にチーム開発）において非常に強力な武器であると言えます．実際，後述するロボット開発者向けミドルウェアである
ROS（RobotOperatingSystem）においても，このPub/Sub型のメッセージングシステムが採用されています．

ここでは，MQTTを使いながら，Pub/Sub型のメッセージングを使ったネットワーク通信のプログラミングを
実際に試しながら慣れていきましょう．

### mosquittoとは
[mosquitto](https://mosquitto.org/)とは，通信規格であるMQTTを実装したオープンソースライブラリであり，
これを使うことを簡単にMQTTブローカーをネットワーク上に構築することができます．

インストールの際は，Ubuntu標準リポジトリのmosquittoが古いものしか無いようなので，リポジトリを追加します．

    sudo add-apt-repository ppa:mosquitto-dev/mosquitto-ppa
    sudo apt-get update
    sudo apt-get install mosquitto mosquitto-clients

### pythonでMQTTクライアントを作成する
PythonでMQTTクライアント,つまりPublisherやSubscriberを実装したい場合，
[paho-mqtt](https://eclipse.org/paho/)を使うといいでしょう．

以後，想定する実行環境はUbuntu 14.04とします．

Pythonで外部ライブラリを使いたい場合，pipと呼ばれるツールがよく用いられます．
ev3devの推奨環境がPython3なので，ここではpip3でpaho-mqttをインストールすることにします．

    sudo pip3 install paho-mqtt

なお，pip3が入ってない場合は，

    sudo apt-get install python3-pip

でインストールしておいてください．

これで準備完了です．テキストエディタもしくは，vim等のエディタを開いて，プログラムを書いていきましょう．
なお，説明の都合上サンプルのプログラムをここに書いていますが，最初のうちはできればコピペせず，
実際にキーボードを叩きながら覚えることを推奨します．

### Subscriberを作成

```python

    #!/usr/bin/env python
    # -*- coding:utf-8 -*-


    import paho.mqtt.client as mqtt

    # ブローカーの設定
    host = '127.0.0.1'
    port = 1883

    FORWARD_TOPIC = 'ev3/forward'
    BACK_TOPIC = 'ev3/back'

    def on_connect(client, userdata, flags, respons_code):
        print('status {0}'.format(respons_code))

        client.subscribe(FORWARD_TOPIC) # topic名を指定
        client.subscribe(BACK_TOPIC) # topic名を指定

    def on_message(client, userdata, msg):
        print(msg.topic + ' ' + str(msg.payload))

    def on_foward(client, userdata, msg):
        print("foward: " + str(msg.payload))

        # ここにforwardトピックを受け取った時の処理を書く

    def on_back(client, userdata, msg):
        print("back : " + str(msg.payload))

        # ここにbackトピックを受け取ったときの処理を書く


    if __name__ == '__main__':

        try : 
            # mqttクライアントの生成
            client = mqtt.Client()

            ## コールバックを登録する
            # 接続時に実行される処理
            client.on_connect = on_connect
            # 何かしらのメッセージを受け取ったとき
            client.on_message = on_message

            # 各トピックに対するコールバック
            client.message_callback_add(FORWARD_TOPIC, on_foward)
            client.message_callback_add(BACK_TOPIC, on_back)

            client.connect(host, port=port, keepalive=60)

            # 待ち受け状態にする
            client.loop_forever()

        except KeyboardInterrupt  :
            print ( "KeyboardInterrupt\n" )
            client.disconnect()
        finally:
            print ("process end")

```

#### 練習問題:
次の仕様を満たすロボットを作成せよ．

要求1: 
トピック'ev3/vel'を受け取り，機体の並進方向の移動スピードを変更できる．

要求2:
トピック'ev3/steer'を受け取り，機体の操舵角指令(steer)を受け取ることができる．

ただし，steerの有効範囲は-15 < steer < 15 とし，

    steer = 15 (steer > 15)
    steer = ev3/steer が示す値
    stter = -15 (steer < -15)

要求3:
左右のモータ出力(motorL,motorR)は

    motorR = vel + steer
    motorL = vel - steer

とする．ただし，-15 < vel < 15 のときは，

    vel = 0

とする

### センサデータを送信するPublisherを作成する
メッセージをネットワーク上にPublishしたいときは，
    
    client.publish(topicname, message)

で送信します．topicnameとmessageは文字列形式で渡します．


サンプルプログラム

```python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from time import sleep
    import paho.mqtt.client as mqtt

    # MQTTブローカーのアドレスとポートを指定する
    host = '192.168.11.11'
    port = 1883

    # インスタンスの生成
    client = mqtt.Client()
    client.connect(host, port=port, keepalive=60)

    # topicの発行
    topic = 'test'
    client.publish(topic, 'message')
    sleep(0.2)

    # ブローカーと切断する
    client.disconnect()
```

#### 練習問題:
EV3超音波センサーのデータを周期10HzでPublishせよ．


### PCとEV3をMQTTで通信させよう

## ROSについて理解しよう

### Pub/Sub型のメッセージング
http://wiki.ros.org/ja/indigo/Installation/Ubuntu

### ROSのインストール
http://wiki.ros.org/ja/indigo/Installation/Ubuntu

### 自分のパッケージを作成する

## 他の人が書いたパッケージと連携しよう
* joy_teleop

## OpenCVを使って画像処理をしよう
* OpenCVを使う