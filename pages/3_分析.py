import streamlit as st
import pandas as pd
import numpy as np
from sqlite_sql.RolexWatchConn import RolexWatchConn


st.session_state.analyze_watch_name = st.text_input("分析手表名称", "")
RolexWatchConn.make_query()
RolexWatchConn.add_name(st.session_state.analyze_watch_name)
rows = RolexWatchConn.commit_query()
if len(rows) > 0:
    chart_data = pd.DataFrame({
        '日期': [pd.to_datetime(i) for i in rows[:,1]],
        '价格': [int(i) for i in rows[:,2]],
        '类型': rows[:, 3]
    })

    st.line_chart(chart_data, x = '日期', y = '价格', color = '类型')
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)