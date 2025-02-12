from datetime import datetime, time
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.account_fund_changes_do import AccountFundChanges
from module_admin.entity.vo.account_fund_changes_vo import AccountFundChangesModel, AccountFundChangesPageQueryModel
from utils.page_util import PageUtil


class AccountFundChangesDao:
    """
    账户资金变动记录管理模块数据库操作层
    """

    @classmethod
    async def get_account_fund_changes_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键id获取详细信息

        :param db: orm对象
        :param id: 主键id
        :return: 账户资金变动记录信息对象
        """
        account_fund_changes_info = (await db.execute(select(AccountFundChanges).where(AccountFundChanges.id == id))).scalars().first()

        return account_fund_changes_info

    @classmethod
    async def get_account_fund_changes_list(cls, db: AsyncSession, query_object: AccountFundChangesPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 账户资金变动记录列表信息对象
        """
        query = (
            select(AccountFundChanges)
            .where(

                AccountFundChanges.in_account_id == query_object.in_account_id if query_object.in_account_id else True,
                AccountFundChanges.out_account_id == query_object.out_account_id if query_object.out_account_id else True,
                AccountFundChanges.transaction_type_id == query_object.transaction_type_id if query_object.transaction_type_id else True,

                AccountFundChanges.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
            .order_by(AccountFundChanges.create_time.desc())
            .distinct()
        )
        account_fund_changes_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return account_fund_changes_list

    @classmethod
    async def add_account_fund_changes_dao(cls, db: AsyncSession, account_fund_changes: AccountFundChangesModel):
        """
        新增操作

        :param db: orm对象
        :param account_fund_changes: 账户资金变动记录对象
        :return:
        """
        db_account_fund_changes = AccountFundChanges(**account_fund_changes.model_dump())
        db.add(db_account_fund_changes)
        await db.flush()

        return db_account_fund_changes

    @classmethod
    async def edit_account_fund_changes_dao(cls, db: AsyncSession, account_fund_changes: dict):
        """
        更新操作

        :param db: orm对象
        :param account_fund_changes: 需要更新的账户资金变动记录字典
        :return:
        """
        await db.execute(update(AccountFundChanges), [account_fund_changes])

    @classmethod
    async def delete_account_fund_changes_dao(cls, db: AsyncSession, account_fund_changes: AccountFundChangesModel):
        """
        删除操作

        :param db: orm对象
        :param account_fund_changes: 账户资金变动记录对象
        :return:
        """
        await db.execute(delete(AccountFundChanges).where(AccountFundChanges.id.in_([account_fund_changes.id])))
