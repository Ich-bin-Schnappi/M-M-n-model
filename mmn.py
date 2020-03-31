# -*- coding: utf-8 -*-
'''
M/M/n model
author: Jiang Yang ZY1903240
'''

import random
import math

arrive_time = []
max_customer = 1000000
max_lenth = 1000
arr_rate = 7
tre_rate = 4

class ServerList(list):
    def __init__(self):
        list.__init__([])
    
    def findMinIdleTime(self):  #找到最先完成任务的服务器
        t = self[0].time_t
        j=0
        for i in range(len(self)):
            if t > self[i].time_t:
                t = self[i].time_t
                j=i
        return j

    def timeLast(self):  #计算总时间
        t=0
        for server in self:
            t = t if t >= server.time_t else server.time_t
        return t

    def usingRate(self):  #计算服务器平均利用率
        sum = 0
        for server in self:
            sum += server.serTimeAll/server.time_t
        return sum/len(self)

server_list = ServerList()

class Server():

    def __init__(self, item = None, rate = 1, begin_time = 0, time_last = 0):
        self.item = item
        self.rate = rate #服务率
        self.begin_time = begin_time
        self.time_last = time_last
        self.serTimeAll = 0
        self.time_t = self.begin_time
        self.idle = 1
        server_list.append(self)  #加入服务器列表

    def serve(self):
        serTime = self.randSerTime()  #随机生成服务时间
        self.time_t += serTime  #时间推进
        self.serTimeAll += serTime

    def randSerTime(self):
        return -1/self.rate*math.log(random.random())

class Customer():
    def __init__(self, server, arrive_time = 0, start_time = 0):
        self.server = server
        self.arrive_time = arrive_time  #到达时间
        #self.treat_time = -1/self.server.rate*math.log(random.random())  #服务时长
        self.start_time = start_time
        self.wait_time = self.start_time - self.arrive_time  #等待时间

class Queue(list):
    def __init__(self):
        list.__init__([])
        self.areaOfQueue = 0  #队列面积
    
    def enQueue(self, c):
        self.append(c)
        self.areaOfQueue += c.wait_time
    
    def deQueue(self):
        return self.pop(0)

def initialize():
    #arrive time
    t=0
    for i in range(max_customer):
        arrive_time.append(t)
        t -= 1/arr_rate*math.log(random.random())  #随机生成到达时间间隔

if __name__ == "__main__":
    initialize()
    
    #建立多个服务器对象，可以设定不同的开始时间和不同的服务强度
    s1 = Server(item = None, rate = tre_rate, begin_time = 0, time_last = 0)
    s2 = Server(item = None, rate = tre_rate, begin_time = 0, time_last = 0)

    queue = Queue()  #依次存放所有顾客

    lenth_all = 0
    i = 0
    while i<max_customer:
        j = server_list.findMinIdleTime()  #最先完成的服务器编号
        if arrive_time[i] > server_list[j].time_t:  #有服务器空闲的情况
            server_list[j].time_t = arrive_time[i]
        c = Customer(server_list[j], arrive_time[i], server_list[j].time_t)
        queue.enQueue(c)
        server_list[j].serve()
        i += 1
            
    aveLength = queue.areaOfQueue / server_list.timeLast()  #计算平均队长L
    aveWaitTime = queue.areaOfQueue / max_customer  #计算平均等待时间W
    usingRate = server_list.usingRate()  #服务器利用率
    
    print("Input:")
    print("The average arriving rate is", arr_rate)
    print("The average treating rate is", tre_rate)
    print("The average max number of customers is", max_customer)
    print("The average max lenth of the queue is", max_lenth)

    print("Output:")
    print("The average lenth is", aveLength)
    print("The average waiting time is", aveWaitTime)
    print("The average using rate is", usingRate)














