import streamlit as st
import datetime
import pandas as pd
import numpy as np
from io import BytesIO

from utils.app_init import AppInit
from database.RolexWatch import RolexWatchAPI, RolexWatch
from streamlit_searchbox import st_searchbox
from streamlit_tags import st_tags



AppInit.init()


query_watch_name = st_searchbox(
    RolexWatchAPI.get_name_searchbox_suggest,
    label="搜索手表名称",
    key="query_watch_name_search_box"
)

col1, col2 = st.columns(2)


with col1:
    query_start_date = st.date_input("起始日期", datetime.date(2022, 9, 1))
    query_price_low = st.number_input("高于", 0)

with col2:
    query_end_date = st.date_input("终止日期", datetime.date.today())
    query_price_high = st.number_input("低于", 1000000)

query_type = st_tags(
    label='按类型搜索',
    text='Press enter to add more',
    key='search_watch_type_tags')
query_comment = st_searchbox(
    RolexWatchAPI.get_comment_searchbox_suggest,
    label="按备注搜索",
    key="query_watch_comment_search_box"
)



rows = RolexWatchAPI.get_search_result(
    query_watch_name, query_start_date, query_end_date,
    query_price_low, query_price_high,
    query_type, query_comment
)
df = pd.DataFrame([i.to_list() for i in rows], columns=RolexWatch.to_columns())

edited_df = st.data_editor(df, use_container_width=True, hide_index=True,
                    disabled=RolexWatch.fix_columns())




col1, col2, col3 = st.columns(3)
with col1:
    if st.button("删除"):
        RolexWatchAPI.delete_search_result(
            query_watch_name, query_start_date, query_end_date,
            query_price_low, query_price_high,
            query_type, query_comment
        )
with col2:
    if st.button("确认修改"):
        edited = edited_df.to_numpy()
        update_targets = []
        for i in edited:
            update_targets.append(dict(zip(RolexWatch.to_columns_alias(), i)))
        RolexWatchAPI.bulk_update(update_targets)
with col3:
    @st.cache_data(ttl=10)
    def to_excel(df):
        in_memory_fp  = BytesIO()
        df.to_excel(in_memory_fp)
       # Write the file out to disk to demonstrate that it worked.
        in_memory_fp.seek(0, 0)
        return in_memory_fp.read()
    df_xlsx = to_excel(edited_df)
    st.download_button(label='📥下载当前数据',
                        data=df_xlsx ,
                        file_name= 'df_test.xlsx')