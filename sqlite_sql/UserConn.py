import streamlit as st
import sqlite3
import numpy as np
import datetime
from sqlite_sql.BasicConn import ConnConfig


class UserConn(ConnConfig):
    @staticmethod
    @st.cache_resource
    def init():
        