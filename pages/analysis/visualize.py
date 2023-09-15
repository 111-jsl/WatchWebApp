import streamlit as st
import pandas as pd
import numpy as np
from database.RolexWatch import RolexWatchAPI
from utils.app_init import AppInit
from streamlit_searchbox import st_searchbox


AppInit.init()


analyze_watch_name = st_searchbox(
    RolexWatchAPI.get_name_searchbox_suggest,
    label="分析手表名称",
    key="analyze_watch_name_search_box"
)
rows = np.array([])
if analyze_watch_name is not None and analyze_watch_name != '':
    rows = np.array(RolexWatchAPI.get_search_result(name=analyze_watch_name))
if len(rows) > 0:
    chart_data = pd.DataFrame({
        '日期': [pd.to_datetime(i) for i in rows[:,1]],
        '价格': [int(i) for i in rows[:,2]],
        '类型': rows[:, 3]
    })

    st.line_chart(chart_data, x = '日期', y = '价格', color = '类型')
