from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from settings import settings

# engine = create_engine(settings.database_url)
engine = create_async_engine(settings.database_url)

SessionLocal = sessionmaker(bind=engine, autoflush=False, class_=AsyncSession)

Base = declarative_base()


class Menu(Base):
    """ Menu """

    __tablename__ = "menu"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(128))
    description: str = Column(String(128))
    submenus = relationship('Submenu', backref='submenu', lazy='dynamic',
                            cascade="all, delete, delete-orphan")

    def __repr__(self):
        return '<{}>'.format(
            self.id,
            self.title,
            self.description
        )


class Submenu(Base):
    """ Submenu """

    __tablename__ = "submenu"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(128))
    description: str = Column(String(128))
    menu_id: int = Column(Integer, ForeignKey('menu.id'))
    dishes = relationship('Dish', backref='dish', lazy='dynamic',
                          cascade="all, delete, delete-orphan")

    def __repr__(self):
        return '<{}>'.format(
            self.id,
            self.title,
            self.description,
            self.menu_id
        )


class Dish(Base):
    """ Dish """

    __tablename__ = "dish"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(128))
    description: str = Column(String(128))
    price: float = Column(Float)
    submenu_id: int = Column(Integer, ForeignKey('submenu.id'))

    def __repr__(self):
        return '<{}>'.format(
            self.id,
            self.title,
            self.description,
            self.price,
            self.menu_id
        )


# Base.metadata.create_all(bind=engine)

