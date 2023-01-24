from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import *

Base = declarative_base()


class Menu(Base):
    """ Menu """
    __tablename__ = 'menu'
    id: int = Column(Integer(), primary_key=True, autoincrement=True, unique=True)
    title: str = Column(String(128), nullable=False)
    description: str = Column(String(256))
    # submenus_count: int = Column(Integer, default=0)
    # dishes_count: int = Column(Integer, default=0)
    submenus = relationship("Submenu",
                            back_populates='menus',
                            cascade="all, delete-orphan")

    def __repr__(self):
        return '<Menu: {}>'.format(
            self.id,
            self.title,
            self.description
        )


class Submenu(Base):
    """ Submenu """
    __tablename__ = 'submenu'
    id: int = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title: str = Column(String(128), nullable=False)
    description: str = Column(String(256))
    menu_id: int = Column(Integer, ForeignKey('menu.id'))
    menus = relationship("Menu", back_populates='submenus')
    # dishes_count: int = Column(Integer, default=0)
    dishes = relationship("Dish",
                          back_populates='submenus',
                          cascade="all, delete-orphan")

    def __repr__(self):
        return '<Submenu: {}>'.format(
            self.id,
            self.title,
            self.description,
            self.menu_id
        )


class Dish(Base):
    """ Dish """
    __tablename__ = 'dish'
    id: int = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title: str = Column(String(200))
    description: str = Column(String)
    price: float = Column(Float(round(2)))
    submenu_id: int = Column(Integer, ForeignKey('submenu.id'))
    menu_id: int = Column(Integer, ForeignKey('menu.id'))
    submenus = relationship('Submenu', back_populates='dishes')

    def __repr__(self):
        return '<Dish: {}>'.format(
            self.id,
            self.title,
            self.description,
            self.price,
            self.menu_id
        )

# Base.metadata.create_all(bind=engine)
