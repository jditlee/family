from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.account_fund_changes_vo import DeleteAccountFundChangesModel, AccountFundChangesModel, AccountFundChangesPageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.account_fund_changes_service import AccountFundChangesService
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

account_fund_changesController = APIRouter(prefix='/money/account_fund_changes', dependencies=[Depends(LoginService.get_current_user)])


@account_fund_changesController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('money:account_fund_changes:list'))]
)
async def get_money_account_fund_changes_list(
        request: Request,
        account_fund_changes_page_query: AccountFundChangesPageQueryModel = Depends(AccountFundChangesPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    account_fund_changes_page_query_result = await AccountFundChangesService.get_account_fund_changes_list_services(query_db, account_fund_changes_page_query,
                                                                            is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=account_fund_changes_page_query_result)


@account_fund_changesController.post('', dependencies=[Depends(CheckUserInterfaceAuth('money:account_fund_changes:add'))])
@Log(title='账户资金变动记录', business_type=BusinessType.INSERT)
async def add_money_account_fund_changes(
        request: Request,
        add_account_fund_changes: AccountFundChangesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):

    add_account_fund_changes.create_by = current_user.user.user_id
    add_account_fund_changes.create_time = datetime.now()
    add_account_fund_changes.update_by = current_user.user.user_id
    add_account_fund_changes.update_time = datetime.now()
    add_account_fund_changes_result = await AccountFundChangesService.add_account_fund_changes_services(query_db, add_account_fund_changes)
    logger.info(add_account_fund_changes_result.message)

    if add_account_fund_changes_result.is_success:
        return ResponseUtil.success(msg=add_account_fund_changes_result.message)
    else:
        return ResponseUtil.failure(msg=add_account_fund_changes_result.message)

@account_fund_changesController.put('', dependencies=[Depends(CheckUserInterfaceAuth('money:account_fund_changes:edit'))])
@Log(title='账户资金变动记录', business_type=BusinessType.UPDATE)
async def edit_money_account_fund_changes(
        request: Request,
        edit_account_fund_changes: AccountFundChangesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_account_fund_changes.update_by = current_user.user.user_id
    edit_account_fund_changes.update_time = datetime.now()
    edit_account_fund_changes_result = await AccountFundChangesService.edit_account_fund_changes_services(query_db, edit_account_fund_changes)
    logger.info(edit_account_fund_changes_result.message)

    if edit_account_fund_changes_result.is_success:
        return ResponseUtil.success(msg=edit_account_fund_changes_result.message)
    else:
        return ResponseUtil.failure(msg=edit_account_fund_changes_result.message)


@account_fund_changesController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('money:account_fund_changes:remove'))])
@Log(title='账户资金变动记录', business_type=BusinessType.DELETE)
async def delete_money_account_fund_changes(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_account_fund_changes = DeleteAccountFundChangesModel(ids=ids)
    delete_account_fund_changes_result = await AccountFundChangesService.delete_account_fund_changes_services(query_db, delete_account_fund_changes)
    logger.info(delete_account_fund_changes_result.message)

    return ResponseUtil.success(msg=delete_account_fund_changes_result.message)


@account_fund_changesController.get(
    '/{id}', response_model=AccountFundChangesModel, dependencies=[Depends(CheckUserInterfaceAuth('money:account_fund_changes:query'))]
)
async def query_detail_money_account_fund_changes(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    account_fund_changes_detail_result = await AccountFundChangesService.account_fund_changes_detail_services(query_db, id)
    logger.info(f'获取账户资金变动记录id为{id}的信息成功')

    return ResponseUtil.success(data=account_fund_changes_detail_result)
