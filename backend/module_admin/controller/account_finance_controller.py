from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.account_finance_vo import DeleteAccountFinanceModel, AccountFinanceModel, AccountFinancePageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.account_finance_service import AccountFinanceService
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

account_financeController = APIRouter(prefix='/money/account_finance', dependencies=[Depends(LoginService.get_current_user)])


@account_financeController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('money:account_finance:list'))]
)
async def get_money_account_finance_list(
        request: Request,
        account_finance_page_query: AccountFinancePageQueryModel = Depends(AccountFinancePageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    account_finance_page_query_result = await AccountFinanceService.get_account_finance_list_services(query_db, account_finance_page_query,
                                                                            is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=account_finance_page_query_result)


@account_financeController.post('', dependencies=[Depends(CheckUserInterfaceAuth('money:account_finance:add'))])
@Log(title='账户记录', business_type=BusinessType.INSERT)
async def add_money_account_finance(
        request: Request,
        add_account_finance: AccountFinanceModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_account_finance.create_by = current_user.user.user_id
    add_account_finance.create_time = datetime.now()
    add_account_finance.update_by = current_user.user.user_id
    add_account_finance.update_time = datetime.now()
    add_account_finance_result = await AccountFinanceService.add_account_finance_services(query_db, add_account_finance)
    logger.info(add_account_finance_result.message)

    return ResponseUtil.success(msg=add_account_finance_result.message)


@account_financeController.put('', dependencies=[Depends(CheckUserInterfaceAuth('money:account_finance:edit'))])
@Log(title='账户记录', business_type=BusinessType.UPDATE)
async def edit_money_account_finance(
        request: Request,
        edit_account_finance: AccountFinanceModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_account_finance.update_by = current_user.user.user_id
    edit_account_finance.update_time = datetime.now()
    edit_account_finance_result = await AccountFinanceService.edit_account_finance_services(query_db, edit_account_finance)
    logger.info(edit_account_finance_result.message)

    return ResponseUtil.success(msg=edit_account_finance_result.message)


@account_financeController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('money:account_finance:remove'))])
@Log(title='账户记录', business_type=BusinessType.DELETE)
async def delete_money_account_finance(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_account_finance = DeleteAccountFinanceModel(ids=ids)
    delete_account_finance_result = await AccountFinanceService.delete_account_finance_services(query_db, delete_account_finance)
    logger.info(delete_account_finance_result.message)

    return ResponseUtil.success(msg=delete_account_finance_result.message)


@account_financeController.get(
    '/{id}', response_model=AccountFinanceModel, dependencies=[Depends(CheckUserInterfaceAuth('money:account_finance:query'))]
)
async def query_detail_money_account_finance(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    account_finance_detail_result = await AccountFinanceService.account_finance_detail_services(query_db, id)
    logger.info(f'获取账户记录id为{id}的信息成功')

    return ResponseUtil.success(data=account_finance_detail_result)
