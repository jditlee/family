from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic_validation_decorator import NotBlank, Size, Xss
from typing import Optional
from decimal import Decimal


class IncomeModel(BaseModel):
    """
    收入记录表对应pydantic模型
    """

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(None, description='开支记录表ID')
    type_id: Optional[int] = Field(None, description='收入类型id，关联字典表收入类型(工资，奖金，分红)')
    detail: Optional[str] = Field(None, max_length=1024, description='收入明细')
    amount: Optional[Decimal] = Field(None, nullable=False, description='收入金额')
    currency: Optional[int] = Field(0, max_length=10, description='收入金额的货币类型')
    payment_method: Optional[int] = Field(None, description='支付方式，关联字典表（0现金、1银行卡、2微信、3支付宝等）')
    user_id: Optional[int] = Field(None, description='收入人id，关联用户表主键')
    income_time: Optional[datetime] = Field(None, description='收入时间')
    year: Optional[int] = Field(None, description='收入年份')
    month: Optional[int] = Field(None, description='收入月份')
    source_id: Optional[int] = Field(None, description='收入来源id，关联字典表收入来源（公司，店铺，某人，项目）')
    create_by: Optional[str] = Field('', max_length=64, description='创建者')
    create_time: Optional[datetime] = Field(None, description='创建时间')
    update_by: Optional[str] = Field('', max_length=64, description='更新者')
    update_time: Optional[datetime] = Field(None, description='更新时间')
    remark: Optional[str] = Field(None, max_length=255, description='备注')


class IncomeQueryModel(IncomeModel):
    """
    通知公告管理不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class IncomePageQueryModel(IncomeQueryModel):
    """
    通知公告管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteIncomeModel(BaseModel):
    """
    删除通知公告模型
    """

    ids: str = Field(description='需要删除的ID列表')
