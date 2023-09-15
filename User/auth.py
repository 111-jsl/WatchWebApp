import streamlit as st
from st_pages import show_pages_from_config, add_page_title, hide_pages
from streamlit_extras.switch_page_button import switch_page
from database.User import UserAPI

class Authenticate:
    
    @staticmethod
    def display():
        if st.session_state.authentication_status:
            if st.session_state.authentication_type == 'admin':
                show_pages_from_config(path='.streamlit/admin.toml')
            else:
                show_pages_from_config(path='.streamlit/user.toml')
            hide_pages(['修改密码'])
            with st.sidebar:
                Authenticate.logout()
                if st.button("修改密码"):
                    switch_page("修改密码")
        else:
            UserAPI.logout()
            show_pages_from_config(path='.streamlit/guest.toml')
            
        
    @staticmethod
    def login():
        if not st.session_state.authentication_status:
            form = st.form(key="login")
            st.session_state.username = form.text_input("用户名","")
            st.session_state.password = form.text_input("密码","",type="password")
            if form.form_submit_button("登录"):
                login_result = UserAPI.login(st.session_state.username,st.session_state.password)
                if login_result.type == 'success':
                    st.session_state.authentication_status = True
                    Authenticate.display()
                    switch_page("首页")
                login_result()
                
    @staticmethod
    def logout():
        if st.session_state.authentication_status:
            with st.sidebar:
                if st.button("登出"):
                    st.session_state.authentication_status = False
                    UserAPI.logout()
                    Authenticate.display()
                    switch_page("首页")

        
    @staticmethod
    def reset_password():
        if st.session_state.authentication_status:
            form = st.form(key="reset_password")
            st.session_state.password = form.text_input("新密码","",type="password")
            if form.form_submit_button("确认"):
                reset_result = UserAPI.reset_password(st.session_state.password)
                reset_result()
                
        
    @staticmethod
    def register():
        if not st.session_state.authentication_status:
            form = st.form(key="register")
            st.session_state.email = form.text_input("邮箱")
            st.session_state.username = form.text_input("用户名")
            st.session_state.password = form.text_input("密码",type="password")
            if form.form_submit_button("注册"):
                register_result = UserAPI.register(st.session_state.username, 
                                                   st.session_state.password,
                                                   st.session_state.email)
                register_result()
            
    @staticmethod
    def forget_password():
        if not st.session_state.authentication_status:
            form = st.form(key="forget_password")
            st.session_state.username = form.text_input("用户名")
            if form.form_submit_button("确认"):
                forget_result = UserAPI.forget_password(st.session_state.username)
                forget_result()
    
            
    @staticmethod
    def forget_username():
        if not st.session_state.authentication_status:
            form = st.form(key="forget_username")
            st.session_state.email = form.text_input("邮箱")
            if form.form_submit_button("确认"):
                forget_result = UserAPI.forget_username(st.session_state.email)
                forget_result()