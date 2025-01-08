from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, LargeBinary, String, Numeric
from config.database import Base


class Consume(Base):
    """
    消费记录表：
    create table consume
(
    id           bigint auto_increment
        primary key,
    type_id      bigint                    null comment '消费类型id，关联字典表（0衣1食2住3行）',
    detail       varchar(1024)             null comment '消费明细',
    amount       decimal(15, 2)            null comment '消费金额，支持更高精度',
    category     varchar(255)              null comment '消费类别的子分类',
    currency     varchar(10) default 'CNY' null comment '消费金额的货币类型',
    payment_id   bigint                    null comment '支付方式，关联字典表（0现金、1银行卡、2微信、3支付宝等）',
    status       bigint      default 0     null comment '消费状态，关联字典表（0completed（完成）、1pending（待处理）、2installment（分期）等）',
    location     varchar(255)              null comment '消费发生的地点',
    tags         varchar(255)              null comment '消费记录的标签（如“重要”、“偶然消费”、“节假日”等），支持多标签（逗号分隔）',
    user_name    varchar(255)              null comment '消费人名称',
    consume_time datetime                  null comment '消费时间',
    year         int                       null comment '消费年份',
    month        int                       null comment '消费月份',
    scene        bigint                    null comment '消费场景id，关联字典表（0旅游，1家居，2聚会，3工作）',
    create_by    varchar(64) default ''    null comment '创建者',
    create_time  datetime                  null comment '创建时间',
    update_by    varchar(64) default ''    null comment '更新者',
    update_time  datetime                  null comment '更新时间',
    remark       text                      null comment '备注'
)
    comment '开支记录表';
    """

    __tablename__ = 'consume'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='开支记录表ID')
    type_id = Column(Integer, comment='消费类型id，关联字典表（0衣1食2住3行）')
    detail = Column(String(1024), comment='消费明细')
    amount = Column(Numeric(15, 2), nullable=True, comment='消费金额，支持更高精度')
    category = Column(String(255), comment='消费类别的子分类')
    currency = Column(String(10), default='CNY', comment='消费金额的货币类型')
    payment_id = Column(Integer, comment='支付方式，关联字典表（0现金、1银行卡、2微信、3支付宝等）')
    status = Column(Integer, default=0, comment='消费状态，关联字典表（0（完成）、1（待处理）、2（分期）等）')
    location = Column(String(255), comment='消费发生的地点')
    tags = Column(String(255), comment='消费记录的标签（如“重要”、“偶然消费”、“节假日”等），支持多标签（逗号分隔）')
    user_name = Column(String(255), comment='消费人名称')
    consume_time = Column(DateTime, comment='消费时间')
    year = Column(Integer, comment='消费年份')
    month = Column(Integer, comment='消费月份')
    scene = Column(Integer, comment='消费场景id，关联字典表（0旅游，1家居，2聚会，3工作）')
    create_by = Column(String(64), default='', comment='创建者')
    create_time = Column(DateTime, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), default='', comment='更新者')
    update_time = Column(DateTime, default=datetime.now(), comment='更新时间')
    remark = Column(String(255), comment='备注')
