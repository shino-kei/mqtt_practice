#!/usr/bin/env python
# -*- coding:utf-8 -*-


import paho.mqtt.client as mqtt

host = '127.0.0.1'
port = 1883
topic = 'test'
topic2 = 'test2'
def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))

    client.subscribe(topic) # topic名を指定
    client.subscribe(topic2) # topic名を指定

def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))

def on_topic2_received(client, userdata, msg):
    print("topic2 Reseived !! : "+ str(msg.payload))


if __name__ == '__main__':

    try : 
        # mqttクライアントの生成
        client = mqtt.Client()

        # コールバックを登録する
        client.on_connect = on_connect
        client.on_message = on_message
        client.message_callback_add(topic2, on_topic2_received)

        client.connect(host, port=port, keepalive=60)

        # 待ち受け状態にする
        client.loop_forever()

    except KeyboardInterrupt  :
        print ( "KeyboardInterrupt\n" )
        client.disconnect()
    finally:
        print ("process end")

