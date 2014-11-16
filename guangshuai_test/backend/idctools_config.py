#!/usr/bin/python
#coding=utf-8
import redis


#redis数据库参数设置
redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0)

