#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
#todo auto close

import os
import config
import singleton
import pymysql
import sys

class MysqlBase(singleton.Singleton):
    def __init__(self):
        """
            初始化 数据库连接信息
        """
        super(MysqlBase, self).__init__()
        self.conn = pymysql.connect(host=config.DB_HOST, user=config.DB_USERNAME, passwd=config.DB_PASSWORD, db=config.DB_DATABASE, charset='utf8')
        self.cursor = self.conn.cursor()

    def getLists(self, sql):
        """
            查询所有信息 返回全部的返回结果集合 or None tuple 
        """
        if self.__execute(sql):
            return self.cursor.fetchall()
        else:
            return None 
    
    def getListsWithDict(self, sql):
        """
            返回所有数据信息 or None dict
        """
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        if self.__execute(sql):
            return self.cursor.fetchall()
        else:
            return None 


    def getRow(self, sql):
        """
            返回一条数据信息 or None tuple 
        """
        if self.__execute(sql):
            return self.cursor.fetchone()
        else:
            return None 

    def getRowWithDict(self, sql):
        """
            返回一条数据信息 or None dict
        """
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        if self.__execute(sql):
            return self.cursor.fetchone()
        else:
            return None 

    def execUpdate(self, sql):
        """
            更新数据 返回 boolean
        """
        if self.__execute(sql):
            return True
        else:
            return False

    def execDelete(self, sql):
        """
            删除 返回 boolean
        """
        if self.__execute(sql):
            return True
        else:
            return False

    def execInsert(self, sql):
        """
            插入数据 返回 False or last_insert_id
        """
        try:
            self.cursor.execute(sql)
            last_insert_id = int(self.conn.insert_id())
            self.conn.commit()
            return last_insert_id
        except Exception as e:
            self.conn.rollback()
            return False

    def execInsertWithDict(self, table_name, items):
        """
            插入 dict 数据 返回 False or last_insert_id
        """
        sql = "INSERT INTO `%s`(`%s`) VALUES('%s')" % (table_name, '`,`'.join(items.keys()), "','".join(map(str, items.values())))
        #sql = "INSERT INTO `%s`(`%s`) VALUES('%s')" % (table_name, '`,`'.join(items.keys()), "','".join(map(lambda item: pymysql.escape_string(str(item)), items.values())))
        return self.execInsert(sql)
    
    def getRowCount(self):
        """
            获取最后影响条数
        """
        return self.cursor.rowcount
    
    def execute(self, sql):
        """
            run sql
        """
        return self.__execute(sql)

    def close(self):
        """
            关闭数据库链接
        """
        self.cursor.close()
        self.conn.close()

    def __execute(self, sql):
        """
            execute sql cat exception return boolean
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            return False
        return True

mysql = MysqlBase()
