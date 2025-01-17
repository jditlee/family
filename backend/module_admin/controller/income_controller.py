from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.income_vo import DeleteIncomeModel, IncomeModel, IncomePageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.income_service import IncomeService
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

incomeController = APIRouter(prefix='/money/income', dependencies=[Depends(LoginService.get_current_user)])


@incomeController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('money:income:list'))]
)
async def get_money_income_list(
        request: Request,
        income_page_query: IncomePageQueryModel = Query(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    income_page_query_result = await IncomeService.get_income_list_services(query_db, income_page_query,
                                                                            is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=income_page_query_result)


@incomeController.post('', dependencies=[Depends(CheckUserInterfaceAuth('money:income:add'))])
@Log(title='收入记录', business_type=BusinessType.INSERT)
async def add_money_income(
        request: Request,
        add_income: IncomeModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    if not add_income.year:
        add_income.year = add_income.income_time.year
    if not add_income.month:
        add_income.month = add_income.income_time.month
    add_income.create_by = current_user.user.user_id
    add_income.create_time = datetime.now()
    add_income.update_by = current_user.user.user_id
    add_income.update_time = datetime.now()
    add_income_result = await IncomeService.add_income_services(query_db, add_income)
    logger.info(add_income_result.message)

    return ResponseUtil.success(msg=add_income_result.message)


@incomeController.put('', dependencies=[Depends(CheckUserInterfaceAuth('money:income:edit'))])
@Log(title='收入记录', business_type=BusinessType.UPDATE)
async def edit_money_income(
        request: Request,
        edit_income: IncomeModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_income.update_by = current_user.user.user_id
    edit_income.update_time = datetime.now()
    edit_income_result = await IncomeService.edit_income_services(query_db, edit_income)
    logger.info(edit_income_result.message)

    return ResponseUtil.success(msg=edit_income_result.message)


@incomeController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('money:income:remove'))])
@Log(title='收入记录', business_type=BusinessType.DELETE)
async def delete_money_income(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_income = DeleteIncomeModel(ids=ids)
    delete_income_result = await IncomeService.delete_income_services(query_db, delete_income)
    logger.info(delete_income_result.message)

    return ResponseUtil.success(msg=delete_income_result.message)


@incomeController.get(
    '/{id}', response_model=IncomeModel, dependencies=[Depends(CheckUserInterfaceAuth('money:income:query'))]
)
async def query_detail_money_income(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    income_detail_result = await IncomeService.income_detail_services(query_db, id)
    logger.info(f'获取收入记录id为{id}的信息成功')

    return ResponseUtil.success(data=income_detail_result)
