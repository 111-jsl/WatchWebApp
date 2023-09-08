import streamlit as st
from sqlite_sql.BasicConn import BasicConn


def init():
    BasicConn.init_db()
    


init()




