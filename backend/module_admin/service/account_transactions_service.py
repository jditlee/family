from sqlalchemy.ext.asyncio import AsyncSession
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.dao.account_transactions_dao import AccountTransactionsDao
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.account_transactions_vo import DeleteAccountTransactionsModel, AccountTransactionsModel, AccountTransactionsPageQueryModel
from utils.common_util import SqlalchemyUtil, CamelCaseUtil


class AccountTransactionsService:
    """
    账户流水记录管理模块服务层
    """

    @classmethod
    async def get_account_transactions_list_services(
            cls, query_db: AsyncSession, query_object: AccountTransactionsPageQueryModel, is_page: bool = True
    ):
        """
        获取列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 账户流水记录列表信息对象
        """
        account_transactions_list_result = await AccountTransactionsDao.get_account_transactions_list(query_db, query_object, is_page)

        return account_transactions_list_result

    @classmethod
    async def add_account_transactions_services(cls, query_db: AsyncSession, page_object: AccountTransactionsModel):
        """
        新增service

        :param query_db: orm对象
        :param page_object: 账户流水记录对象
        :return: 新增账户流水记录校验结果
        """
        try:
            await AccountTransactionsDao.add_account_transactions_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_account_transactions_services(cls, query_db: AsyncSession, page_object: AccountTransactionsModel):
        """
        更新service

        :param query_db: orm对象
        :param page_object: 账户流水记录对象
        :return: 更新账户流水记录校验结果
        """
        edit_account_transactions = page_object.model_dump(exclude_unset=True)
        account_transactions_info = await cls.account_transactions_detail_services(query_db, page_object.id)
        if account_transactions_info.id:
            try:
                await AccountTransactionsDao.edit_account_transactions_dao(query_db, edit_account_transactions)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='账户流水记录不存在')

    @classmethod
    async def delete_account_transactions_services(cls, query_db: AsyncSession, page_object: DeleteAccountTransactionsModel):
        """
        删除service

        :param query_db: orm对象
        :param page_object: 账户流水记录对象
        :return: 删除账户流水记录校验结果
        """
        if page_object.ids:
            account_transactions_id_list = page_object.ids.split(',')
            try:
                for account_transactions_id in account_transactions_id_list:
                    await AccountTransactionsDao.delete_account_transactions_dao(query_db, AccountTransactionsModel(id=account_transactions_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入账户流水记录id为空')

    @classmethod
    async def account_transactions_detail_services(cls, query_db: AsyncSession, id: int):
        """
        根据id获取详细信息service

        :param query_db: orm对象
        :param id: 账户流水记录id
        :return: 账户流水记录id对应的信息
        """
        account_transactions = await AccountTransactionsDao.get_account_transactions_detail_by_id(query_db, id=id)
        if account_transactions:
            result = AccountTransactionsModel(**CamelCaseUtil.transform_result(account_transactions))
        else:
            result = AccountTransactionsModel(**dict())

        return result
