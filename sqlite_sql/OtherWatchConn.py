import streamlit as st
import sqlite3
import numpy as np
import datetime
from sqlite_sql.BasicConn import ConnConfig

class OtherWatchConn(ConnConfig):
    @staticmethod
    def init():
        pass
    
    @staticmethod
    def 