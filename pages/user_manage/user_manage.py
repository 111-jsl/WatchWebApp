import streamlit as st
import numpy as np
from utils.app_init import AppInit
from streamlit_searchbox import st_searchbox
from database.User import UserAPI, User
from streamlit_elements import elements, mui, html
from utils.random_gen import random_rgb
import pandas as pd

AppInit.init()

query_user_name = st_searchbox(
    UserAPI.get_name_searchbox_suggest,
    label="搜索用户名称",
    key="query_user_name_search_box"
)
rows = UserAPI.get_search_result()


df = pd.DataFrame([i.to_list() for i in rows], columns=User.to_columns())

edited_df = st.data_editor(df, use_container_width=True, hide_index=True,
                           disabled=User.fix_columns())

if st.button("确认修改"):
    edited = edited_df.to_numpy()
    update_targets = []
    for i in edited:
        update_targets.append(dict(zip(User.to_columns_alias(), i)))
    UserAPI.bulk_update(update_targets)
