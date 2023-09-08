# name time price type comment

import streamlit as st
import datetime
from sqlite_sql.RolexWatchConn import RolexWatchConn



st.session_state.insert_watch_name = st.text_input("手表名称", "")
st.session_state.insert_date = st.date_input("日期", datetime.date.today())
st.session_state.insert_price = st.text_input("价格", "")
st.session_state.insert_type = st.selectbox("选择类型", ('竞价', '拿货'))
st.session_state.insert_comment = st.text_input("备注", "")
if st.button("添加"):
    return_info = RolexWatchConn.commit_insert(
        st.session_state.insert_watch_name, 
        st.session_state.insert_date, 
        st.session_state.insert_price,
        st.session_state.insert_type, 
        st.session_state.insert_comment)
    

