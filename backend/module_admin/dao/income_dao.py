from datetime import datetime, time
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.income_do import Income
from module_admin.entity.vo.income_vo import IncomeModel, IncomePageQueryModel
from utils.page_util import PageUtil


class IncomeDao:
    """
    收入记录管理模块数据库操作层
    """

    @classmethod
    async def get_income_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键id获取详细信息

        :param db: orm对象
        :param id: 主键id
        :return: 收入记录信息对象
        """
        income_info = (await db.execute(select(Income).where(Income.id == id))).scalars().first()

        return income_info

    @classmethod
    async def get_income_list(cls, db: AsyncSession, query_object: IncomePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 收入记录列表信息对象
        """
        query = (
            select(Income)
            .where(
                Income.detail.like(f'%{query_object.detail}%') if query_object.detail else True,

                Income.type_id == query_object.type_id if query_object.type_id else True,
                Income.user_id == query_object.user_id if query_object.user_id else True,
                Income.year == query_object.year if query_object.year else True,
                Income.month == query_object.month if query_object.month else True,
                Income.source_id == query_object.source_id if query_object.source_id else True,
                Income.acc_id == query_object.acc_id if query_object.acc_id else True,

                Income.income_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
            .order_by(Income.income_time.desc())
            .distinct()
        )
        income_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return income_list

    @classmethod
    async def add_income_dao(cls, db: AsyncSession, income: IncomeModel):
        """
        新增操作

        :param db: orm对象
        :param income: 收入记录对象
        :return:
        """
        db_income = Income(**income.model_dump())
        db.add(db_income)
        await db.flush()

        return db_income

    @classmethod
    async def edit_income_dao(cls, db: AsyncSession, income: dict):
        """
        更新操作

        :param db: orm对象
        :param income: 需要更新的收入记录字典
        :return:
        """
        await db.execute(update(Income), [income])

    @classmethod
    async def delete_income_dao(cls, db: AsyncSession, income: IncomeModel):
        """
        删除操作

        :param db: orm对象
        :param income: 收入记录对象
        :return:
        """
        await db.execute(delete(Income).where(Income.id.in_([income.id])))
