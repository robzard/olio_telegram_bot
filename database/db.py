import asyncio
import logging

from sqlalchemy import create_engine, Column, Integer, String, MetaData, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from typing import List
from sqlalchemy import or_, and_
from sqlalchemy.future import select

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from dotenv import load_dotenv

import os

from google_sheets.gs_manager import get_wsh

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

Base = declarative_base()
engine: AsyncEngine = create_async_engine(DATABASE_URL)
AsyncSession = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    is_admin = Column(String)


class MenuObject(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    composition = Column(String)
    preparation = Column(String)
    history = Column(String)
    category = Column(String)
    photo_url = Column(String)
    inline_category = Column(String)
    city = Column(String)
    price = Column(String)


async def get_async_session():
    return AsyncSession


async def create_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_all_users(admins=False):
    async_session = await get_async_session()
    async with async_session() as session:
        # Создание базового запроса
        if admins:
            query = select(User).where(User.is_admin == '1')
        else:
            query = select(User)
        result = await session.execute(query)
        users = result.scalars().all()
        return users


async def search_menu_objects(query_words: List[str], inline_category: str = None):
    async_session = await get_async_session()
    async with async_session() as session:
        # Создание базового запроса
        if inline_category == 'all':
            query = select(MenuObject)
        else:
            query = select(MenuObject).where(MenuObject.inline_category == inline_category)

        # Добавление условий поиска по ключевым словам, если они есть
        if query_words:
            conditions_per_word = []
            for word in query_words:
                word_condition = or_(
                    MenuObject.name.ilike(f'%{word}%'),
                    MenuObject.composition.ilike(f'%{word}%'),
                    MenuObject.category.ilike(f'%{word}%'),
                    MenuObject.preparation.ilike(f'%{word}%')
                )
                conditions_per_word.append(word_condition)

            query = query.filter(and_(*conditions_per_word))

        # if query_words:
        #     query = query.filter(
        #         or_(
        #             *[
        #                 or_(
        #                     Drink.name.ilike(f'%{word}%'),
        #                     Drink.composition.ilike(f'%{word}%'),
        #                     Drink.preparation.ilike(f'%{word}%')
        #                 ) for word in query_words
        #             ]
        #         )
        #     )

        # Выполнение запроса
        result = await session.execute(query)
        menu_objects = result.scalars().all()
        return menu_objects


async def get_positions_from_db(inline_category: str = None):
    async_session = await get_async_session()
    async with async_session() as session:
        # Создание запроса
        if inline_category == 'all':
            query = select(MenuObject)
        else:
            query = select(MenuObject).where(MenuObject.inline_category == inline_category)

        # Выполнение запроса
        result = await session.execute(query)
        menu_objects = result.scalars().all()
        return menu_objects


async def add_excel_to_db(wsh_name: str, inline_category: str):
    logging.info(f'Обновляю {wsh_name}')
    wsh_values = get_wsh(wsh_name)
    logging.info(f'wsh_values - {len(wsh_values)}')
    async_session = await get_async_session()
    async with async_session() as session:
        for row in wsh_values[1:]:  # Пропускаем заголовок
            name, composition, preparation, history, category, photo_url, city, price = row

            if name is None or category is None:
                continue
            logging.info(f'Добавляю в БД - {name}')
            # Добавьте photo_file_id как аргумент при создании экземпляра Drink
            menu_object = MenuObject(name=name, composition=composition, preparation=preparation, history=history, category=category, photo_url=photo_url if photo_url else None, inline_category=inline_category, city=city, price=price)
            session.add(menu_object)
        logging.info(f'Комиичу в БД')
        await session.commit()
        logging.info(f'{wsh_name} обновлено')
    await asyncio.sleep(1)