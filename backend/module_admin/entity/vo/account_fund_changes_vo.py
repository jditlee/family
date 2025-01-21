from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic_validation_decorator import NotBlank, Size, Xss
from pydantic.alias_generators import to_camel

from typing import Optional
from decimal import Decimal
from module_admin.annotation.pydantic_annotation import as_query


class AccountFundChangesModel(BaseModel):
    """
    AccountFundChanges表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(None, description='开支记录表ID')

    in_account_id: Optional[int] = Field(None, description='入账账户ID，关联finance_account表')
    out_account_id: Optional[int] = Field(None, description='出帐账户ID，关联finance_account表')
    transaction_type_id: Optional[int] = Field(None, description='交易类型（如收益入账，银证转账，基金加仓等），管理字典表')
    amount: Optional[Decimal] = Field(None, description='交易金额')
    balance_after: Optional[Decimal] = Field(None, description='交易后账户余额')



    create_by: Optional[str] = Field('', max_length=64, description='创建者')
    create_time: Optional[datetime] = Field(None, description='创建时间')
    update_by: Optional[str] = Field('', max_length=64, description='更新者')
    update_time: Optional[datetime] = Field(None, description='更新时间')
    remark: Optional[str] = Field(None, max_length=255, description='备注')


class AccountFundChangesQueryModel(AccountFundChangesModel):
    """
    不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')

@as_query
class AccountFundChangesPageQueryModel(AccountFundChangesQueryModel):
    """
    分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteAccountFundChangesModel(BaseModel):
    """
    删除模型
    """

    ids: str = Field(description='需要删除的ID列表')
