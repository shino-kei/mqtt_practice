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

for i in range(3):
    client.publish(topic, 'message'+str(i))
    sleep(0.2)

# ブローカーと切断する
client.disconnect()


