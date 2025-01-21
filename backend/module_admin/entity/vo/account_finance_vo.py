from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic_validation_decorator import NotBlank, Size, Xss
from pydantic.alias_generators import to_camel

from typing import Optional
from decimal import Decimal

from module_admin.annotation.pydantic_annotation import as_query

class AccountFinanceModel(BaseModel):
    """
    AccountFinance表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(None, description='开支记录表ID')

    accounr_name: Optional[str] = Field(None, description='账户名称')
    type_id: Optional[int] = Field(None, description='账户类型id,关联字典表')
    max_balance: Optional[Decimal] = Field(None, description='历史最高资金')
    principal: Optional[Decimal] = Field(None, description='账户本金')
    user_id: Optional[int] = Field(None, description='账户所属家庭成员id')

    create_by: Optional[str] = Field('', max_length=64, description='创建者')
    create_time: Optional[datetime] = Field(None, description='创建时间')
    update_by: Optional[str] = Field('', max_length=64, description='更新者')
    update_time: Optional[datetime] = Field(None, description='更新时间')
    remark: Optional[str] = Field(None, max_length=255, description='备注')


class AccountFinanceQueryModel(AccountFinanceModel):
    """
    不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')

@as_query
class AccountFinancePageQueryModel(AccountFinanceQueryModel):
    """
    分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteAccountFinanceModel(BaseModel):
    """
    删除模型
    """

    ids: str = Field(description='需要删除的ID列表')
