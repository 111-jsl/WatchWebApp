import streamlit as st
import sqlite3
import numpy as np
import datetime
from sqlite_sql.BasicConn import BasicConn


    
        
class RolexWatchConn(BasicConn):
    query = None
    params = []
    @staticmethod
    def make_query():
        RolexWatchConn.query = "select name, time, price, type, comment from watchinfo where "
        RolexWatchConn.params = []
    
    @staticmethod
    def make_delete():
        RolexWatchConn.query = "delete from watchinfo where "
        RolexWatchConn.params = []
    
    @staticmethod
    def add_name(name):
        if len(name) > 0:
            RolexWatchConn.query += f"name like ? and "
            RolexWatchConn.params.append(name + '%')
    
    @staticmethod
    def add_date(start_date, end_date):
        RolexWatchConn.query += f"time between ? and ? and "
        RolexWatchConn.params.append(start_date)
        RolexWatchConn.params.append(end_date)
        

    @staticmethod
    def add_price(start_price, end_price):
        if len(start_price) > 0 and len(end_price) > 0:
            RolexWatchConn.query += f"price >= ? and price <= ? and "
            RolexWatchConn.params.append(start_price)
            RolexWatchConn.params.append(end_price)
        
    
    @staticmethod
    def add_type(type):
        RolexWatchConn.query += f"type = ? and "
        RolexWatchConn.params.append(type)
        
        
    @staticmethod
    def add_comment(comment):
        if len(comment) > 0:
            RolexWatchConn.query += f"comment like ? and "
            RolexWatchConn.params.append('%' + comment + '%')
        
    @staticmethod
    def commit_query():
        RolexWatchConn.query = RolexWatchConn.query[:-5] + ";"
        rows = RolexWatchConn.run_query(RolexWatchConn.query, tuple(RolexWatchConn.params))
        return np.array(rows)
    
    @staticmethod
    def commit_delete():
        RolexWatchConn.query = RolexWatchConn.query[:-5] + ";"
        RolexWatchConn.run_query(RolexWatchConn.query, tuple(RolexWatchConn.params))
        st.cache_data.clear()
        
    
    @staticmethod
    def commit_insert(name, date, price, type, comment):
        if len(name) == 0:
            return "名称不能为空"
        if len(price) == 0:
            return "价格不能为空"
        if len(type) == 0:
            return "类型不能为空"
        rows = RolexWatchConn.run_query(
            '''
            select * from watchinfo where name = ? and time = ? and type = ?;
            ''',
            (name, date, type)
        )
        if len(rows) == 0:
            RolexWatchConn.run_query(
                '''
                insert into watchinfo (name, time, price, type, comment)
                values
                (?, ?, ?, ?, ?);
                ''',
                (name, date, price, type, comment)
            )
            st.cache_data.clear()
        elif len(rows) == 1:
            RolexWatchConn.run_query(
                '''
                update watchinfo 
                set price = ?, comment = ?
                where id = ?;
                ''',
                (price, comment, rows[0][0])
            )
            st.cache_data.clear()
        else:
            return "系统异常"
        return ""


