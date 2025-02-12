from datetime import datetime, time
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.consume_do import Consume
from module_admin.entity.vo.consume_vo import ConsumeModel, ConsumePageQueryModel
from utils.page_util import PageUtil


class ConsumeDao:
    """
    开支记录管理模块数据库操作层
    """

    @classmethod
    async def get_consume_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据开支记录id获取开支详细信息

        :param db: orm对象
        :param id: 主键id
        :return: 开支记录信息对象
        """
        consume_info = (await db.execute(select(Consume).where(Consume.id == id))).scalars().first()

        return consume_info


    @classmethod
    async def get_consume_list(cls, db: AsyncSession, query_object: ConsumePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取开支记录列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 开支记录列表信息对象
        """
        query = (
            select(Consume)
            .where(
                Consume.detail.like(f'%{query_object.detail}%') if query_object.detail else True,
                Consume.category.like(f'%{query_object.category}%') if query_object.category else True,
                Consume.location.like(f'%{query_object.location}%') if query_object.location else True,
                Consume.tags.like(f'%{query_object.tags}%') if query_object.tags else True,
                Consume.user_id == query_object.user_id if query_object.user_id else True,
                Consume.type_id == query_object.type_id if query_object.type_id else True,
                Consume.currency == query_object.currency if query_object.currency else True,
                Consume.payment_id == query_object.payment_id if query_object.payment_id else True,
                Consume.status == query_object.status if query_object.status else True,
                Consume.year == query_object.year if query_object.year else True,
                Consume.month == query_object.month if query_object.month else True,
                Consume.scene == query_object.scene if query_object.scene else True,
                Consume.acc_id == query_object.acc_id if query_object.acc_id else True,

                Consume.consume_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
            .order_by(Consume.consume_time.desc())
            .distinct()
        )
        consume_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return consume_list

    @classmethod
    async def add_consume_dao(cls, db: AsyncSession, consume: ConsumeModel):
        """
        新增开支记录数据库操作

        :param db: orm对象
        :param consume: 开支记录对象
        :return:
        """
        db_consum = Consume(**consume.model_dump())
        db.add(db_consum)
        await db.flush()

        return db_consum

    @classmethod
    async def edit_consume_dao(cls, db: AsyncSession, consume: dict):
        """
        编辑开支记录数据库操作

        :param db: orm对象
        :param consume: 需要更新的开支记录字典
        :return:
        """
        await db.execute(update(Consume), [consume])

    @classmethod
    async def delete_consume_dao(cls, db: AsyncSession, consume: ConsumeModel):
        """
        删除开支记录数据库操作

        :param db: orm对象
        :param consume: 开支记录对象
        :return:
        """
        await db.execute(delete(Consume).where(Consume.id.in_([consume.id])))
