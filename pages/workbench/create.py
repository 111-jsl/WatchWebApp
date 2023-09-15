# name time price type comment

import streamlit as st
import pandas as pd
import datetime
from database.RolexWatch import RolexWatchAPI
from utils.app_init import AppInit
from streamlit_searchbox import st_searchbox
from streamlit_tags import st_tags
from streamlit_option_menu import option_menu




AppInit.init()


create_method = option_menu(None, ["手动", "Excel表格"],
    menu_icon="cast", default_index=0, orientation="horizontal")

if create_method == '手动':
    insert_watch_name = st_searchbox(
        RolexWatchAPI.get_name_searchbox_suggest,
        label="手表名称",
        key="insert_watch_name_searchbox"
    )
    insert_date = st.date_input("日期", datetime.date.today())
    insert_price = st.number_input("价格", 0)
    insert_type = st_tags(
        label='选择类型',
        text='Press enter to add more',
        key='insert_watch_type_tags',
        maxtags=1)
    insert_comment = st_searchbox(
        RolexWatchAPI.get_comment_searchbox_suggest,
        label="备注",
        key="insert_watch_comment_searchbox"
    )

    if st.button("添加"):
        return_info = RolexWatchAPI.insert(
            insert_watch_name, 
            insert_date, 
            insert_price,
            insert_type, 
            insert_comment)
elif create_method == 'Excel表格':
    uploaded_files = st.file_uploader("上传Excel文件", accept_multiple_files=True, type='xlsx')
    if st.button("上传数据库"):
        for uploaded_file in uploaded_files:
            df = pd.read_excel(uploaded_file)
            df_dict = df.to_dict('records')
            st.write(df)
            for i in range(len(df_dict)):
                new_record = {}
                for k,v in df_dict[i].items():
                    if k in RolexWatchAPI.map_column_alias:
                        new_record[RolexWatchAPI.map_column_alias[k]] = v
                df_dict[i] = new_record
            RolexWatchAPI.bulk_insert(df_dict)
