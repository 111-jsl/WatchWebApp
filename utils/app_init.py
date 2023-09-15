import streamlit as st
from database.RolexWatch import RolexWatchAPI
from database.User import UserAPI
from User.auth import Authenticate as Auth
from sqlalchemy import create_engine
from database.Base import Base


class AppInit:
    input_suggest_limit = 10
    @staticmethod
    def init():
        AppInit.cached_init()
        AppInit.no_cached_init()
    
    @staticmethod
    @st.cache_resource
    def cached_init():
        
        engine = create_engine("sqlite:///watch.sqlitedb", echo=True)
        RolexWatchAPI.init(engine)
        UserAPI.init(engine)
        Base.metadata.create_all(engine)

    
    @staticmethod
    def no_cached_init():
        if 'authentication_status' not in st.session_state:
            st.session_state.authentication_status = False
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'authentication_status' not in st.session_state:
            st.session_state.authentication_status = None
        Auth.display()

