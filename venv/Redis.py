# This Python file uses the following encoding: utf-8

import redis
import logging
import threading
import time
def checkSpam(messages, name):

    thread = threading.Thread(target=Check, args=(messages, name))
    thread.start()

def Check(message, name):
    time.sleep(10)
    mes = message.split(" ")
    count = 0
    for word in mes:
        if word == 'action' or word == 'discounts':
            count += 1
    if count > 10:
        worker.base.zrem(name, message)
        worker.base.zadd(name, message, 3)
        worker.base.zincrby("spamers", name, 1)
    else:
        worker.base.zrem(name, message)
        worker.base.zadd(name, message, 2)
def matchHead(name):
    list = worker.base.smembers("Administrators")
    for names in list:
        if name == names:
            return True
    return False

def matchUsers(name):
    list = worker.base.smembers("Users")
    for names in list:
        if name == names:
            return True
    return False
class Worker:
    base = redis.Redis()

def showMessages(name):
    messages = worker.base.zrange(name, 0, -1, withscores=True)
    for message in messages:
        print(message)

def showOnline():
    print(worker.base.hget(online))

def showSpamers():
    print(worker.base.zrange("spamers", 0, -1, withscores=True))

worker = Worker()
worker.base.sadd("Administrators", "Lider")
worker.base.sadd("Users", "User")

#worker.base.sadd("Адміністратои", "Лідер")
#worker.base.sadd("Адміністраторри", "Gy")


online = "online"


print("Увійти як: 1 - звичайний користувач, 2 - адміністратор")
if(raw_input()) == "1":
    name = str(raw_input())
    if matchUsers(name):
       worker.base.hset(online, name, "true")
       print("Ласкаво просимо")
    while True:
        print("Обрати опцію: 1 - написати повідомлення, 2 - переглянути чергу повідомлень, 3 - вийти")
        choice = int(raw_input())
        if choice == 1:
            print("Ваше повідомлення: \n")
            message = raw_input()
            worker.base.zadd(name, message, 1.0)
            checkSpam(message, name)
        if choice == 2:
            showMessages(name)
        if choice == 3:
            worker.base.hset(online, name, "false")
            break

else:
    print("Увійти як адміністратор")
#print(worker.base.smembers("Адміністратори"))

    name = str(raw_input())
    if matchHead():
        print("Ласкаво просимо")
        print("Обрати опцію: 1 - подивитися користувачів в мережі, 2 - подивитися активність спаму")
        choice = int(raw_input())
        if choice == 1:
            showOnline()
        if choice == 2:
            showSpamers()

