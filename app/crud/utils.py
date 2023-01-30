from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from models import Submenu, Menu


async def add_submenus_count(menu_id: int, db: AsyncSession):
	# submenu_count = await db.execute(
	# 	(select(Submenu).where(Submenu.menu_id == menu_id)))

	# submenu_count = await db.execute(
	# 	select(func.count(Submenu.id).filter(Submenu.menu_id == menu_id)))
	# print('submenu_count', submenu_count)

	submenu_count = await db.execute(select(func.count()).select_from(Submenu).where(
		Submenu.menu_id == menu_id))

	menu = await db.execute(select(Menu).where(Menu.id == menu_id))
	menu.submenus_count = submenu_count.scalars().first()
	await db.commit()
	await db.refresh(menu)
	return None

# dishes_count = column_property(
# 	select(func.count(Dish.id))
# 	.where(Dish.submenu_id == id)
# 	.scalar_subquery()
# )


# async def create_submenu(
# 	menu_id: int,
# 	sub: UpCrMeSub,
# 	db: AsyncSession,
# ) -> BaseSubmenu:
# 	"""
# 	Create new submenu.
# 	:param menu_id:
# 	:param sub:
# 	:param db:
# 	:return:
# 	"""
# 	new_submenu = Submenu(
# 		title=sub.title,
# 		description=sub.description,
# 		menu_id=menu_id,
# 	)
# 	db.add(new_submenu)
# 	await db.commit()
# 	await db.refresh(new_submenu)
#
# 	submenu_count = await db.execute(select(func.count()).select_from(Submenu).where(
# 		Submenu.menu_id == menu_id))
# 	menu = await get_menu(menu_id, db)
# 	menu.submenus_count = submenu_count.scalars().first()
# 	db.add(menu)
# 	await db.commit()
# 	await db.refresh(menu)
# 	return new_submenu