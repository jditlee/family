from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic_validation_decorator import NotBlank, Size, Xss
from pydantic.alias_generators import to_camel

from typing import Optional
from decimal import Decimal
from module_admin.annotation.pydantic_annotation import as_query


class AccountTransactionsModel(BaseModel):
    """
    AccountTransactions表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(None, description='开支记录表ID')

    account_id: Optional[int] = Field(None, description='账户ID，关联finance_account表')
    current_balance: Optional[Decimal] = Field(None, description='账户当前余额')


    create_by: Optional[str] = Field('', max_length=64, description='创建者')
    create_time: Optional[datetime] = Field(None, description='创建时间')
    update_by: Optional[str] = Field('', max_length=64, description='更新者')
    update_time: Optional[datetime] = Field(None, description='更新时间')
    remark: Optional[str] = Field(None, max_length=255, description='备注')


class AccountTransactionsQueryModel(AccountTransactionsModel):
    """
    不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')

@as_query
class AccountTransactionsPageQueryModel(AccountTransactionsQueryModel):
    """
    分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteAccountTransactionsModel(BaseModel):
    """
    删除模型
    """

    ids: str = Field(description='需要删除的ID列表')
