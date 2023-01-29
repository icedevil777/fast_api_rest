from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import *
from database import Base


class Menu(Base):
	""" Menu """
	__tablename__ = 'menu'
	id: int = Column(
		Integer(),
		primary_key=True,
		autoincrement=True,
		unique=True
	)
	title: str = Column(String(128), nullable=False)
	description: str = Column(String(256))
	submenus_count: int = Column(Integer, default=0)
	dishes_count: int = Column(Integer, default=0)
	submenus = relationship(
		"Submenu",
		back_populates='menus',
		cascade="all, delete-orphan"
	)


class Submenu(Base):
	""" Submenu """
	__tablename__ = 'submenu'
	id: int = Column(
		Integer,
		primary_key=True,
		autoincrement=True,
		unique=True
	)
	title: str = Column(String(128), nullable=False)
	description: str = Column(String(256))
	menu_id: int = Column(Integer, ForeignKey('menu.id'))
	menus = relationship("Menu", back_populates='submenus')
	dishes_count: int = Column(Integer, default=0)
	dishes = relationship(
		"Dish",
		back_populates='submenus',
		cascade="all, delete-orphan"
	)


class Dish(Base):
	""" Dish """
	__tablename__ = 'dish'
	id: int = Column(
		Integer,
		primary_key=True,
		autoincrement=True,
		unique=True
	)
	title: str = Column(String(200))
	description: str = Column(String)
	price: str = Column(String(10))
	submenu_id: int = Column(Integer, ForeignKey('submenu.id'))
	menu_id: int = Column(Integer, ForeignKey('menu.id'))
	submenus = relationship('Submenu', back_populates='dishes')
