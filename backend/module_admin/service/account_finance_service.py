from sqlalchemy.ext.asyncio import AsyncSession
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.dao.account_finance_dao import AccountFinanceDao
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.account_finance_vo import DeleteAccountFinanceModel, AccountFinanceModel, AccountFinancePageQueryModel
from utils.common_util import SqlalchemyUtil


class AccountFinanceService:
    """
    账户记录管理模块服务层
    """

    @classmethod
    async def get_account_finance_list_services(
            cls, query_db: AsyncSession, query_object: AccountFinancePageQueryModel, is_page: bool = True
    ):
        """
        获取列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 账户记录列表信息对象
        """
        account_finance_list_result = await AccountFinanceDao.get_account_finance_list(query_db, query_object, is_page)

        return account_finance_list_result

    @classmethod
    async def add_account_finance_services(cls, query_db: AsyncSession, page_object: AccountFinanceModel):
        """
        新增service

        :param query_db: orm对象
        :param page_object: 账户记录对象
        :return: 新增账户记录校验结果
        """
        try:
            await AccountFinanceDao.add_account_finance_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_account_finance_services(cls, query_db: AsyncSession, page_object: AccountFinanceModel):
        """
        更新service

        :param query_db: orm对象
        :param page_object: 账户记录对象
        :return: 更新账户记录校验结果
        """
        edit_account_finance = page_object.model_dump(exclude_unset=True)
        account_finance_info = await cls.account_finance_detail_services(query_db, page_object.id)
        if account_finance_info.id:
            try:
                await AccountFinanceDao.edit_account_finance_dao(query_db, edit_account_finance)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='账户记录不存在')

    @classmethod
    async def delete_account_finance_services(cls, query_db: AsyncSession, page_object: DeleteAccountFinanceModel):
        """
        删除service

        :param query_db: orm对象
        :param page_object: 账户记录对象
        :return: 删除账户记录校验结果
        """
        if page_object.ids:
            account_finance_id_list = page_object.ids.split(',')
            try:
                for account_finance_id in account_finance_id_list:
                    await AccountFinanceDao.delete_account_finance_dao(query_db, AccountFinanceModel(id=account_finance_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入账户记录id为空')

    @classmethod
    async def account_finance_detail_services(cls, query_db: AsyncSession, id: int):
        """
        根据id获取详细信息service

        :param query_db: orm对象
        :param id: 账户记录id
        :return: 账户记录id对应的信息
        """
        account_finance = await AccountFinanceDao.get_account_finance_detail_by_id(query_db, id=id)
        if account_finance:
            result = AccountFinanceModel(**SqlalchemyUtil.serialize_result(account_finance))
        else:
            result = AccountFinanceModel(**dict())

        return result
