from datetime import datetime, time
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.account_finance_do import AccountFinance
from module_admin.entity.vo.account_finance_vo import AccountFinanceModel, AccountFinancePageQueryModel
from utils.page_util import PageUtil


class AccountFinanceDao:
    """
    账户记录管理模块数据库操作层
    """

    @classmethod
    async def get_account_finance_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键id获取详细信息

        :param db: orm对象
        :param id: 主键id
        :return: 账户记录信息对象
        """
        account_finance_info = (await db.execute(select(AccountFinance).where(AccountFinance.id == id))).scalars().first()

        return account_finance_info

    @classmethod
    async def get_account_finance_list(cls, db: AsyncSession, query_object: AccountFinancePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 账户记录列表信息对象
        """
        query = (
            select(AccountFinance)
            .where(
                AccountFinance.accounr_name.like(f'%{query_object.accounr_name}%') if query_object.accounr_name else True,

                AccountFinance.type_id == query_object.type_id if query_object.type_id else True,
                AccountFinance.user_id == query_object.user_id if query_object.user_id else True,

                AccountFinance.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
            .order_by(AccountFinance.create_time.desc())
            .distinct()
        )
        account_finance_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return account_finance_list

    @classmethod
    async def add_account_finance_dao(cls, db: AsyncSession, account_finance: AccountFinanceModel):
        """
        新增操作

        :param db: orm对象
        :param account_finance: 账户记录对象
        :return:
        """
        db_account_finance = AccountFinance(**account_finance.model_dump())
        db.add(db_account_finance)
        await db.flush()

        return db_account_finance

    @classmethod
    async def edit_account_finance_dao(cls, db: AsyncSession, account_finance: dict):
        """
        更新操作

        :param db: orm对象
        :param account_finance: 需要更新的账户记录字典
        :return:
        """
        await db.execute(update(AccountFinance), [account_finance])

    @classmethod
    async def delete_account_finance_dao(cls, db: AsyncSession, account_finance: AccountFinanceModel):
        """
        删除操作

        :param db: orm对象
        :param account_finance: 账户记录对象
        :return:
        """
        await db.execute(delete(AccountFinance).where(AccountFinance.id.in_([account_finance.id])))
