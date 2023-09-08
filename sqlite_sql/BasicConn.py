import streamlit as st
import sqlite3
import numpy as np
import datetime

class BasicConn:
    dbname = 'watch.db'
    @staticmethod
    @st.cache_data(ttl=600)
    def run_query(query, params):
        conn = sqlite3.connect(BasicConn.dbname)
        cur = conn.cursor()
        result = cur.execute(query, params)
        rows = result.fetchall()
        conn.commit()
        conn.close()
        return rows

    # init
    @staticmethod
    @st.cache_resource
    def init_db():
        BasicConn.table_init_RolexWatch()
        

    @staticmethod
    @st.cache_resource
    def table_init_RolexWatch():
        conn = sqlite3.connect(BasicConn.dbname)
        conn.cursor().execute(
            '''
            create table if not exists rolex_watchinfo (
                id              integer  primary key    autoincrement,
                name               text     not null,
                time               date     not null,
                price           integer     not null,
                type               text     not null,
                comment            text
            );
            '''
        )
        
        conn.commit()
        conn.close()
        
    @staticmethod
    @st.cache_resource
    def test_data_RolexWatch():
        conn = sqlite3.connect(BasicConn.dbname)
        conn.cursor().execute(
            '''
            insert into watchinfo (name, time, price, type)
            values
            ('手表1', '2023-01-03', '1000', '竞价'),
            ('手表2', '2023-01-04', '2000', '拿货');
            '''
        )
        conn.commit()
        conn.close()
        
    
    @staticmethod
    @st.cache_resource
    def table_init_OtherWatch():
        conn = sqlite3.connect(BasicConn.dbname)
        conn.cursor().execute(
            '''
            create table if not exists other_watchinfo (
                id              integer  primary key    autoincrement,
                name               text     not null,
                time               date     not null,
                price           integer     not null,
                type               text     not null,
                comment            text
            );
            '''
        )
        
        conn.commit()
        conn.close()
        
    @staticmethod
    @st.cache_resource
    def table_init_User():
        conn = sqlite3.connect(BasicConn.dbname)
        conn.cursor().execute(
            '''
            create table if not exists other_watchinfo (
                id              integer  primary key    autoincrement,
                name               text     not null,
                time               date     not null,
                price           integer     not null,
                type               text     not null,
                comment            text
            );
            '''
        )
        
        conn.commit()
        conn.close()