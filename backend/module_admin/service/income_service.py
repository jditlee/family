from sqlalchemy.ext.asyncio import AsyncSession
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.dao.income_dao import IncomeDao
from module_admin.service.account_finance_service import AccountFinanceService
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.income_vo import DeleteIncomeModel, IncomeModel, IncomePageQueryModel
from utils.common_util import SqlalchemyUtil


class IncomeService:
    """
    收入记录管理模块服务层
    """

    @classmethod
    async def get_income_list_services(
            cls, query_db: AsyncSession, query_object: IncomePageQueryModel, is_page: bool = True
    ):
        """
        获取列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 收入记录列表信息对象
        """
        income_list_result = await IncomeDao.get_income_list(query_db, query_object, is_page)

        return income_list_result

    @classmethod
    async def add_income_services(cls, query_db: AsyncSession, page_object: IncomeModel):
        """
        新增service

        :param query_db: orm对象
        :param page_object: 收入记录对象
        :return: 新增收入记录校验结果
        """
        acc_info = await AccountFinanceService.account_finance_detail_services(query_db, page_object.acc_id)
        if acc_info.id:
            acc_info.principal = acc_info.principal + page_object.amount
            try:
                await AccountFinanceService.edit_account_finance_services(query_db, acc_info)
                await IncomeDao.add_income_dao(query_db, page_object)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='录入成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            return CrudResponseModel(is_success=False, message='当前收入没有关联账户信息！')

    @classmethod
    async def edit_income_services(cls, query_db: AsyncSession, page_object: IncomeModel):
        """
        更新service

        :param query_db: orm对象
        :param page_object: 收入记录对象
        :return: 更新收入记录校验结果
        """
        edit_income = page_object.model_dump(exclude_unset=True)
        income_info = await cls.income_detail_services(query_db, page_object.id)
        if income_info.id:
            if income_info.amount != page_object.amount:
                return CrudResponseModel(is_success=False, message='不允许修改收入金额！')
            if income_info.acc_id != page_object.acc_id:
                return CrudResponseModel(is_success=False, message='不允许修改收入账户！')
            try:
                await IncomeDao.edit_income_dao(query_db, edit_income)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='收入记录不存在')

    @classmethod
    async def delete_income_services(cls, query_db: AsyncSession, page_object: DeleteIncomeModel):
        """
        删除service

        :param query_db: orm对象
        :param page_object: 收入记录对象
        :return: 删除收入记录校验结果
        """
        if page_object.ids:
            income_id_list = page_object.ids.split(',')
            try:
                for income_id in income_id_list:
                    await IncomeDao.delete_income_dao(query_db, IncomeModel(id=income_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入收入记录id为空')

    @classmethod
    async def income_detail_services(cls, query_db: AsyncSession, id: int):
        """
        根据id获取详细信息service

        :param query_db: orm对象
        :param id: 收入记录id
        :return: 收入记录id对应的信息
        """
        income = await IncomeDao.get_income_detail_by_id(query_db, id=id)
        if income:
            result = IncomeModel(**SqlalchemyUtil.serialize_result(income))
        else:
            result = IncomeModel(**dict())

        return result
