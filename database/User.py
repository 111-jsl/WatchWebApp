import streamlit as st
import numpy as np
from sqlalchemy.orm import Mapped,mapped_column,sessionmaker, Session
from sqlalchemy import select, update, delete, insert, func, or_
from database.Base import Base
import datetime
from utils.pretty_alert import PrettyAlert



class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    password: Mapped[str]
    email: Mapped[str] = mapped_column(default="invalid_email")
    type: Mapped[str]
    online: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f'''
            User(
                id={self.id!r}, name={self.name!r}, date={self.date!r}, password={self.password!r},
                type={self.type!r}, online={self.online!r}
            )
            '''
    def to_list(self):
        return [self.id,self.name,self.date,self.email,self.type,self.online]
    @staticmethod
    def to_columns():
        return ['编号', '名字', '注册时间', '邮箱', '角色', '在线']
    @staticmethod
    def fix_columns():
        return ['编号', '名字', '注册时间', '邮箱', '在线']
    @staticmethod
    def to_columns_alias():
        return ['id', 'name', 'date', 'email', 'type', 'online']
    
class UserAPI:
    engine = None
    session_prototype = None
    @staticmethod
    def init(engine):
        UserAPI.engine = engine
        UserAPI.session_prototype = sessionmaker(bind=engine,
            expire_on_commit=False
            )
    @staticmethod
    def login(name,password):
        stmt = select(User).where(User.name == name, User.password == password)
        result = []
        with UserAPI.session_prototype() as session:
            result = session.scalars(stmt).all()
            session.commit()
        if len(result) == 0:
            return PrettyAlert('error', '用户名或密码错误')
        elif len(result) <= 1:
            with UserAPI.session_prototype() as session:
                session.execute(update(User).where(User.id == result[0].id).values(online=True))
                session.commit() 
            st.session_state.authentication_type = result[0].type
            return PrettyAlert('success', '登录成功')
        else:
            return PrettyAlert('error', '数据库异常：相同用户存在多个')
    
    @staticmethod
    def logout():
        with UserAPI.session_prototype() as session:
            session.execute(update(User).where(User.name == st.session_state.username).values(online=False))
            session.commit() 
        return
    
    @staticmethod
    def get_name_searchbox_suggest(searchterm):
        ans = [searchterm]
        stmt = select(User.name).distinct(User.name).where(User.name.like(searchterm + '%')).limit(10)
        with UserAPI.session_prototype() as session:
            ans += session.scalars(stmt).all()
            session.commit()
        return ans

    
    @staticmethod
    def get_search_result(
        name=None,st_date=None,en_date=None,type=None,online=None
    ):
        condis = []
        if name is not None and name != '':
            condis.append(User.name.like(name + '%'))
        if (st_date is not None and st_date != '') and (en_date is not None and en_date != ''):
            condis.append(User.date.between(st_date, en_date))
        
        if type is not None and len(type) > 0:
            condis.append(User.type.in_(type))
        if online is not None and online != '':
            condis.append(User.online == online)
       
        stmt = select(User).where(*condis)
        result = []
        with UserAPI.session_prototype() as session:
            result = np.array(session.execute(stmt).all())
            result = result[:,0]
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
            condis.append(User.name.like(name + '%'))
        if (st_date is not None and st_date != '') and (en_date is not None and en_date != ''):
            condis.append(User.date.between(st_date, en_date))
        if (st_price is not None and st_price != '') and (en_price is not None and en_price != ''):
            condis.append(User.price.between(st_price, en_price))
        if type is not None and len(type) > 0:
            condis.append(User.type.in_(type))
        if comment is not None and comment != '':
            condis.append(User.comment.like('%' + comment + '%'))
        stmt = delete(User).where(*condis)
        with UserAPI.session_prototype() as session:
            session.execute(stmt)
            session.commit()
        st.cache_data.clear()
        return

    @staticmethod
    def bulk_update(table):
        with UserAPI.session_prototype() as session:
            session.execute(update(User), table)
            session.commit()
        st.cache_data.clear()
        return

    @staticmethod
    def reset_password(password):
        if password is None or password == '':
            return PrettyAlert('error', '密码不能为空')
        update_stmt = update(User).where(User.name == st.session_state.username).values(password=password)
        with UserAPI.session_prototype() as session:
            session.execute(update_stmt)
            session.commit()
        st.cache_data.clear()
        return PrettyAlert('success', '修改成功')

    @staticmethod
    def register(name,password,email):
        if name is None or name == '':
            return PrettyAlert('error', '名称不能为空')
        if password is None or password == '':
            return PrettyAlert('error', '密码不能为空')
        if email is None or email == '':
            return PrettyAlert('error', '邮箱不能为空')
       
        select_stmt = select(User).where(or_(User.name == name, User.email == email))
        insert_stmt = insert(User).values(name=name,date=datetime.datetime.now(),password=password,type='user',online=False,email=email)
        with UserAPI.session_prototype() as session:
            select_result = session.scalars(select_stmt).all()
            if len(select_result) == 0:
                session.execute(insert_stmt)
            else:
                return PrettyAlert('error', '已存在用户')
            session.commit()
        st.cache_data.clear()
        return PrettyAlert('success', '注册成功')

    @staticmethod
    def forget_password(name):
        if name is None or name == '':
            return PrettyAlert('error', '名称不能为空')
        select_stmt = select(User).where(User.name == name)
        with UserAPI.session_prototype() as session:
            select_result = session.scalars(select_stmt).all()
            if len(select_result) == 0:
                return PrettyAlert('error', '该用户不存在')
            # send to email
            session.commit()
        return PrettyAlert('success', '已发送密码到邮箱')
    
    @staticmethod
    def forget_username(email):
        if email is None or email == '':
            return PrettyAlert('error', '邮箱不能为空')
        select_stmt = select(User).where(User.email == email)
        with UserAPI.session_prototype() as session:
            select_result = session.scalars(select_stmt).all()
            if len(select_result) == 0:
                return PrettyAlert('error', '该用户不存在')
            # send to email
            session.commit()
        return PrettyAlert('success', '已发送用户名到邮箱')