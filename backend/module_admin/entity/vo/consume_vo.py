from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic_validation_decorator import NotBlank, Size, Xss
from typing import Optional
from decimal import Decimal


class ConsumeModel(BaseModel):
    """
    开支记录表对应pydantic模型
    """

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(None, description='开支记录表ID')
    type_id: Optional[int] = Field(None, description='消费类型id，关联字典表（0衣1食2住3行）')
    detail: Optional[str] = Field(None, max_length=1024, description='消费明细')
    amount: Optional[Decimal] = Field(None, description='消费金额，支持更高精度')
    category: Optional[str] = Field(None, max_length=255, description='消费类别的子分类')
    currency: Optional[int] = Field(0, description='消费金额的货币类型')
    payment_id: Optional[int] = Field(None, description='支付方式，关联字典表（0现金、1银行卡、2微信、3支付宝等）')
    status: Optional[int] = Field(0, description='消费状态，关联字典表（0（完成）、1（待处理）、2（分期）等）')
    location: Optional[str] = Field(None, max_length=255, description='消费发生的地点')
    tags: Optional[str] = Field(None, max_length=255,
                                description='消费记录的标签（如“重要”、“偶然消费”、“节假日”等），支持多标签（逗号分隔）')
    user_name: Optional[str] = Field(None, max_length=255, description='消费人名称')
    consume_time: Optional[datetime] = Field(None, description='消费时间')
    year: Optional[int] = Field(None, description='消费年份')
    month: Optional[int] = Field(None, description='消费月份')
    scene: Optional[int] = Field(None, description='消费场景id，关联字典表（0旅游，1家居，2聚会，3工作）')
    create_by: Optional[str] = Field('', max_length=64, description='创建者')
    create_time: Optional[datetime] = Field(None, description='创建时间')
    update_by: Optional[str] = Field('', max_length=64, description='更新者')
    update_time: Optional[datetime] = Field(None, description='更新时间')
    remark: Optional[str] = Field(None, max_length=255, description='备注')




class ConsumeQueryModel(ConsumeModel):
    """
    通知公告管理不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class ConsumePageQueryModel(ConsumeQueryModel):
    """
    通知公告管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteConsumeModel(BaseModel):
    """
    删除通知公告模型
    """

    ids: str = Field(description='需要删除的ID列表')
