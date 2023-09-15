import streamlit as st
class PrettyAlert:
    type = "info"
    msg = ""
    def __init__(self, type, msg):
        self.type = type
        self.msg = msg
    
    def __call__(self):
        if self.type == "info":
            st.info(self.msg)
        elif self.type == "success":
            st.success(self.msg)
        elif self.type == "warning":
            st.warning(self.msg)
        elif self.type == "error":
            st.error(self.msg)
        else:
            assert 0
        