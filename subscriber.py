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

