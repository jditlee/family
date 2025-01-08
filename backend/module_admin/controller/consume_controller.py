from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.consume_vo import DeleteConsumeModel, ConsumeModel, ConsumePageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.consume_service import ConsumeService
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

consumeController = APIRouter(prefix='/money/consume', dependencies=[Depends(LoginService.get_current_user)])


@consumeController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('money:consume:list'))]
)
async def get_money_consume_list(
        request: Request,
        consume_page_query: ConsumePageQueryModel = Query(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    consume_page_query_result = await ConsumeService.get_consume_list_services(query_db, consume_page_query,
                                                                               is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=consume_page_query_result)


@consumeController.post('', dependencies=[Depends(CheckUserInterfaceAuth('money:consume:add'))])
@Log(title='开支记录', business_type=BusinessType.INSERT)
async def add_money_consume(
        request: Request,
        add_consume: ConsumeModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_consume.create_by = current_user.user.user_name
    add_consume.create_time = datetime.now()
    add_consume.update_by = current_user.user.user_name
    add_consume.update_time = datetime.now()
    add_consume_result = await ConsumeService.add_consume_services(query_db, add_consume)
    logger.info(add_consume_result.message)

    return ResponseUtil.success(msg=add_consume_result.message)


@consumeController.put('', dependencies=[Depends(CheckUserInterfaceAuth('money:consume:edit'))])
@Log(title='开支记录', business_type=BusinessType.UPDATE)
async def edit_money_consume(
        request: Request,
        edit_consume: ConsumeModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_consume.update_by = current_user.user.user_name
    edit_consume.update_time = datetime.now()
    edit_consume_result = await ConsumeService.edit_consume_services(query_db, edit_consume)
    logger.info(edit_consume_result.message)

    return ResponseUtil.success(msg=edit_consume_result.message)


@consumeController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('money:consume:remove'))])
@Log(title='开支记录', business_type=BusinessType.DELETE)
async def delete_money_consume(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_consume = DeleteConsumeModel(ids=ids)
    delete_consume_result = await ConsumeService.delete_consume_services(query_db, delete_consume)
    logger.info(delete_consume_result.message)

    return ResponseUtil.success(msg=delete_consume_result.message)


@consumeController.get(
    '/{id}', response_model=ConsumeModel, dependencies=[Depends(CheckUserInterfaceAuth('money:consume:query'))]
)
async def query_detail_money_consume(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    consume_detail_result = await ConsumeService.consume_detail_services(query_db, id)
    logger.info(f'获取开支记录id为{id}的信息成功')

    return ResponseUtil.success(data=consume_detail_result)
