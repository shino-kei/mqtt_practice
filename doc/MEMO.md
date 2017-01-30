# ROS特訓 

## IPアドレスとネットワークについて理解しよう

* ifconfigコマンド
* ssh(telnet)コマンド
* sftp(sftp)コマンド
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
mosquittoとは，通信規格であるMQTTを実装したオープンソースライブラリであり，
これを使うことを簡単にMQTTブローカーをネットワーク上に構築することができます．


### センサデータを送信するPublisherを作成する
サンプルプログラム

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




### Subscriberを作成して，EV3を遠隔操作しよう
### PCとEV3をMQTTで通信させよう

## ROSについて理解しよう
### Pub/Sub型のメッセージング
### ROSのインストール
### 自分のパッケージを作成する

## 他の人が書いたパッケージと連携しよう
* joy_teleop

## OpenCVを使って画像処理をしよう
* OpenCVを使う