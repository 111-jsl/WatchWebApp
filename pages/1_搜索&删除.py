import streamlit as st
import datetime
import pandas as pd
import numpy as np

from sqlite_sql.RolexWatchConn import RolexWatchConn


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.sidebar.success("Select a demo above.")

st.session_state.query_watch_name = st.text_input("搜索手表名称", "")


col1, col2 = st.columns(2)


with col1:
    st.session_state.query_start_date = st.date_input("起始日期", datetime.date(2022, 9, 1))
    st.session_state.query_price_low = st.text_input("高于", "0")

with col2:
    st.session_state.query_end_date = st.date_input("终止日期", datetime.date(2023, 9, 2))
    st.session_state.query_price_high = st.text_input("低于", "100000")

st.session_state.query_type = st.selectbox('按类型搜索',('竞价', '拿货'))
st.session_state.query_comment = st.text_input("按备注搜索", "")

if st.button("删除"):
    RolexWatchConn.make_delete()
    RolexWatchConn.add_name(st.session_state.query_watch_name)
    RolexWatchConn.add_date(st.session_state.query_start_date, st.session_state.query_end_date)
    RolexWatchConn.add_price(st.session_state.query_price_low, st.session_state.query_price_high)
    RolexWatchConn.add_type(st.session_state.query_type)
    RolexWatchConn.add_comment(st.session_state.query_comment)
    RolexWatchConn.commit_delete()
    
        
RolexWatchConn.make_query()
RolexWatchConn.add_name(st.session_state.query_watch_name)
RolexWatchConn.add_date(st.session_state.query_start_date, st.session_state.query_end_date)
RolexWatchConn.add_price(st.session_state.query_price_low, st.session_state.query_price_high)
RolexWatchConn.add_type(st.session_state.query_type)
RolexWatchConn.add_comment(st.session_state.query_comment)
rows = RolexWatchConn.commit_query()
if len(rows) > 0:
    df = pd.DataFrame(
    rows,
    columns=['名字', '日期', '价格', '类型', '备注'])

    st.dataframe(df, use_container_width=True)