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


class Drink(Base):
    __tablename__ = 'drinks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    composition = Column(String)
    preparation = Column(String)
    history = Column(String)
    have_photo = Column(Boolean)
    category = Column(String)
    photo_url = Column(String)
    inline_category = Column(String)


async def get_async_session():
    return AsyncSession


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_all_users():
    async_session = await get_async_session()
    async with async_session() as session:
        # Создание базового запроса
        query = select(User)
        result = await session.execute(query)
        users = result.scalars().all()
        return users


async def search_drinks(query_words: List[str], inline_category: str = None):
    async_session = await get_async_session()
    async with async_session() as session:
        # Создание базового запроса
        if inline_category == 'all':
            query = select(Drink)
        else:
            query = select(Drink).where(Drink.inline_category == inline_category)

        # Добавление условий поиска по ключевым словам, если они есть
        if query_words:
            conditions_per_word = []
            for word in query_words:
                word_condition = or_(
                    Drink.name.ilike(f'%{word}%'),
                    Drink.composition.ilike(f'%{word}%'),
                    Drink.category.ilike(f'%{word}%'),
                    Drink.preparation.ilike(f'%{word}%')
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
        drinks = result.scalars().all()
        return drinks


async def get_positions_from_db(inline_category: str = None):
    async_session = await get_async_session()
    async with async_session() as session:
        # Создание запроса
        if inline_category == 'all':
            query = select(Drink)
        else:
            query = select(Drink).where(Drink.inline_category == inline_category)

        # Выполнение запроса
        result = await session.execute(query)
        drinks = result.scalars().all()
        return drinks


async def add_excel_to_db(file_name: str, ws_name: str, inline_category: str, start_row: int = 2):
    wb = load_workbook(filename=f'./{file_name}', data_only=True)
    ws: Worksheet = wb[ws_name]

    photo_counter = 0
    async_session = await get_async_session()
    async with async_session() as session:
        for row in ws.iter_rows(min_row=start_row, values_only=True):  # Пропускаем заголовок
            name, composition, preparation, history, _, have_photo, category, photo_url = row[:8]

            if name is None or category is None:
                continue

            # Добавьте photo_file_id как аргумент при создании экземпляра Drink
            drink = Drink(name=name, composition=composition, preparation=preparation, history=history, have_photo=bool(have_photo), category=category, photo_url=photo_url if photo_url else None, inline_category=inline_category)
            session.add(drink)

        await session.commit()
