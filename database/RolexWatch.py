import streamlit as st
import numpy as np
from typing import Optional
from sqlalchemy.orm import Mapped,mapped_column,sessionmaker, Session
from sqlalchemy import select, update, delete, insert, func
from database.Base import Base
import datetime
from utils.pretty_alert import PrettyAlert



class RolexWatch(Base):
    __tablename__ = "rolex_watch"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    date: Mapped[datetime.date] 
    price: Mapped[int]
    type: Mapped[str]
    comment: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f'''
            RolexWatch(
                id={self.id!r}, name={self.name!r}, date={self.date!r}, price={self.price!r},
                type={self.type!r}, comment={self.comment!r}
            )
            '''
    def to_list(self):
        return [self.id,self.name,self.date,self.price,self.type,self.comment]
    @staticmethod
    def to_columns():
        return ['编号', '名字', '日期', '价格', '类型', '备注']
    @staticmethod
    def fix_columns():
        return ['编号', '名字', '日期', '类型']
    @staticmethod
    def to_columns_alias():
        return ['id', 'name', 'date', 'price', 'type', 'comment']
    
    
class RolexWatchAPI:
    engine = None
    session_prototype = None
    records_num = 0
    map_column_alias = {
        '名字': 'name',
        '日期': 'date',
        '价格': 'price',
        '类型': 'type',
        '备注': 'comment'
    }
    @staticmethod
    def init(engine):
        RolexWatchAPI.engine = engine
        RolexWatchAPI.session_prototype = sessionmaker(bind=engine,
            expire_on_commit=False
            )
        
    @staticmethod
    def bulk_update(table):
        with RolexWatchAPI.session_prototype() as session:
            session.execute(update(RolexWatch), table)
            session.commit()
        st.cache_data.clear()
        return
    
    @staticmethod
    def bulk_insert(table):
        with RolexWatchAPI.session_prototype() as session:
            session.execute(insert(RolexWatch), table)
            session.commit()
        st.cache_data.clear()
        return

    
    @staticmethod
    def get_name_searchbox_suggest(searchterm):
        ans = [searchterm]
        stmt = select(RolexWatch.name).distinct(RolexWatch.name).where(RolexWatch.name.like(searchterm + '%')).limit(10)
        with RolexWatchAPI.session_prototype() as session:
            ans += session.scalars(stmt).all()
            session.commit()
        return ans

    @staticmethod
    def get_comment_searchbox_suggest(searchterm):
        ans = [searchterm]
        stmt = select(RolexWatch.comment).distinct(RolexWatch.comment).where(RolexWatch.comment.like(searchterm + '%')).limit(10)
        with RolexWatchAPI.session_prototype() as session:
            ans += session.scalars(stmt).all()
            session.commit()
        return ans
    
    @staticmethod
    def get_search_result(
        name=None,st_date=None,en_date=None,
        st_price=None,en_price=None,
        type=None,comment=None
    ):
        condis = []
        if name is not None and name != '':
            condis.append(RolexWatch.name.like(name + '%'))
        if (st_date is not None and st_date != '') and (en_date is not None and en_date != ''):
            condis.append(RolexWatch.date.between(st_date, en_date))
        if (st_price is not None and st_price != '') and (en_price is not None and en_price != ''):
            condis.append(RolexWatch.price.between(st_price, en_price))
        if type is not None and len(type) > 0:
            condis.append(RolexWatch.type.in_(type))
        if comment is not None and comment != '':
            condis.append(RolexWatch.comment.like('%' + comment + '%'))
       
        stmt = select(RolexWatch).where(*condis)
        result = []
        with RolexWatchAPI.session_prototype() as session:
            result = session.scalars(stmt).all()
            session.commit()
        return result

    @staticmethod
    def delete_search_result(
        name=None,st_date=None,en_date=None,
        st_price=None,en_price=None,
        type=None,comment=None
    ):
        condis = []
        if name is not None and name != '':
            condis.append(RolexWatch.name.like(name + '%'))
        if (st_date is not None and st_date != '') and (en_date is not None and en_date != ''):
            condis.append(RolexWatch.date.between(st_date, en_date))
        if (st_price is not None and st_price != '') and (en_price is not None and en_price != ''):
            condis.append(RolexWatch.price.between(st_price, en_price))
        if type is not None and len(type) > 0:
            condis.append(RolexWatch.type.in_(type))
        if comment is not None and comment != '':
            condis.append(RolexWatch.comment.like('%' + comment + '%'))
        stmt = delete(RolexWatch).where(*condis)
        with RolexWatchAPI.session_prototype() as session:
            session.execute(stmt)
            session.commit()
        st.cache_data.clear()
        return

    @staticmethod
    def insert(
        name=None,date=None,price=None,
        type=None,comment=None
    ):
        if name is None or name == '':
            return PrettyAlert('error', '名称不能为空')
        if price is None or price == '':
            return PrettyAlert('error', '价格不能为空')
        if date is None or date == '':
            return PrettyAlert('error', '日期不能为空')
        if type is None or len(type) == 0:
            return PrettyAlert('error', '类型不能为空')
        type = type[0]
        select_stmt = select(RolexWatch).where(RolexWatch.name == name, RolexWatch.date == date, RolexWatch.type == type)
        update_stmt = update(RolexWatch).where(RolexWatch.name == name, RolexWatch.date == date, RolexWatch.type == type)\
            .values(price=price,comment=comment)
        insert_stmt = insert(RolexWatch).values(name=name,date=date,price=price,type=type,comment=comment)
        with RolexWatchAPI.session_prototype() as session:
            select_result = session.scalars(select_stmt).all()
            if len(select_result) > 0:
                session.execute(update_stmt)
            elif len(select_result) <= 1:
                session.execute(insert_stmt)
            else:
                return PrettyAlert('error', '数据库异常：名称、日期、类型对应多于1条的记录')
            session.commit()
        st.cache_data.clear()
        return PrettyAlert('success', '添加成功')

