from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.account_transactions_vo import DeleteAccountTransactionsModel, AccountTransactionsModel, AccountTransactionsPageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.account_transactions_service import AccountTransactionsService
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

account_transactionsController = APIRouter(prefix='/money/account_transactions', dependencies=[Depends(LoginService.get_current_user)])


@account_transactionsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('money:account_transactions:list'))]
)
async def get_money_account_transactions_list(
        request: Request,
        account_transactions_page_query: AccountTransactionsPageQueryModel = Query(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    account_transactions_page_query_result = await AccountTransactionsService.get_account_transactions_list_services(query_db, account_transactions_page_query,
                                                                            is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=account_transactions_page_query_result)


@account_transactionsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('money:account_transactions:add'))])
@Log(title='账户流水记录', business_type=BusinessType.INSERT)
async def add_money_account_transactions(
        request: Request,
        add_account_transactions: AccountTransactionsModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    if not add_account_transactions.year:
        add_account_transactions.year = add_account_transactions.account_transactions_time.year
    if not add_account_transactions.month:
        add_account_transactions.month = add_account_transactions.account_transactions_time.month
    add_account_transactions.create_by = current_user.user.user_name
    add_account_transactions.create_time = datetime.now()
    add_account_transactions.update_by = current_user.user.user_name
    add_account_transactions.update_time = datetime.now()
    add_account_transactions_result = await AccountTransactionsService.add_account_transactions_services(query_db, add_account_transactions)
    logger.info(add_account_transactions_result.message)

    return ResponseUtil.success(msg=add_account_transactions_result.message)


@account_transactionsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('money:account_transactions:edit'))])
@Log(title='账户流水记录', business_type=BusinessType.UPDATE)
async def edit_money_account_transactions(
        request: Request,
        edit_account_transactions: AccountTransactionsModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_account_transactions.update_by = current_user.user.user_name
    edit_account_transactions.update_time = datetime.now()
    edit_account_transactions_result = await AccountTransactionsService.edit_account_transactions_services(query_db, edit_account_transactions)
    logger.info(edit_account_transactions_result.message)

    return ResponseUtil.success(msg=edit_account_transactions_result.message)


@account_transactionsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('money:account_transactions:remove'))])
@Log(title='账户流水记录', business_type=BusinessType.DELETE)
async def delete_money_account_transactions(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_account_transactions = DeleteAccountTransactionsModel(ids=ids)
    delete_account_transactions_result = await AccountTransactionsService.delete_account_transactions_services(query_db, delete_account_transactions)
    logger.info(delete_account_transactions_result.message)

    return ResponseUtil.success(msg=delete_account_transactions_result.message)


@account_transactionsController.get(
    '/{id}', response_model=AccountTransactionsModel, dependencies=[Depends(CheckUserInterfaceAuth('money:account_transactions:query'))]
)
async def query_detail_money_account_transactions(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    account_transactions_detail_result = await AccountTransactionsService.account_transactions_detail_services(query_db, id)
    logger.info(f'获取账户流水记录id为{id}的信息成功')

    return ResponseUtil.success(data=account_transactions_detail_result)
