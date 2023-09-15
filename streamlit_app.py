import streamlit as st
from utils.app_init import AppInit
from utils.random_gen import random_rgb
from streamlit_elements import elements, mui
from User.auth import Authenticate as Auth



AppInit.init()

# add_page_title() # By default this alsox adds indentation
if st.session_state["authentication_status"]:
    with elements("profile_photo"):
        with mui.Box(width="auto", textAlign="center"):
            mui.Avatar(
                st.session_state["username"][:3],
                sx={
                    "bgcolor": random_rgb(),
                    "width": 100,
                    "height": 100,
                    "margin": "auto",
                }
            )
            mui.Typography(
                "Welcome Back " + st.session_state["username"],
                sx={
                    "padding":10,
                    "fontSize": 20,
                    "color": "text.secondary"
                }
            )
else:
    Auth.login()

