from datetime import datetime, time
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.account_transactions_do import AccountTransactions
from module_admin.entity.vo.account_transactions_vo import AccountTransactionsModel, AccountTransactionsPageQueryModel
from utils.page_util import PageUtil


class AccountTransactionsDao:
    """
    账户流水记录管理模块数据库操作层
    """

    @classmethod
    async def get_account_transactions_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键id获取详细信息

        :param db: orm对象
        :param id: 主键id
        :return: 账户流水记录信息对象
        """
        account_transactions_info = (await db.execute(select(AccountTransactions).where(AccountTransactions.id == id))).scalars().first()

        return account_transactions_info

    @classmethod
    async def get_account_transactions_list(cls, db: AsyncSession, query_object: AccountTransactionsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 账户流水记录列表信息对象
        """
        query = (
            select(AccountTransactions)
            .where(

                AccountTransactions.account_id == query_object.account_id if query_object.account_id else True,

                AccountTransactions.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
            .order_by(AccountTransactions.id)
            .distinct()
        )
        account_transactions_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return account_transactions_list

    @classmethod
    async def add_account_transactions_dao(cls, db: AsyncSession, account_transactions: AccountTransactionsModel):
        """
        新增操作

        :param db: orm对象
        :param account_transactions: 账户流水记录对象
        :return:
        """
        db_account_transactions = AccountTransactions(**account_transactions.model_dump())
        db.add(db_account_transactions)
        await db.flush()

        return db_account_transactions

    @classmethod
    async def edit_account_transactions_dao(cls, db: AsyncSession, account_transactions: dict):
        """
        更新操作

        :param db: orm对象
        :param account_transactions: 需要更新的账户流水记录字典
        :return:
        """
        await db.execute(update(AccountTransactions), [account_transactions])

    @classmethod
    async def delete_account_transactions_dao(cls, db: AsyncSession, account_transactions: AccountTransactionsModel):
        """
        删除操作

        :param db: orm对象
        :param account_transactions: 账户流水记录对象
        :return:
        """
        await db.execute(delete(AccountTransactions).where(AccountTransactions.id.in_([account_transactions.id])))
