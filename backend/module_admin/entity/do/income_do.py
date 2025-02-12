from datetime import datetime
from sqlalchemy import Column, DateTime, Integer,  String, Numeric
from config.database import Base


class Income(Base):
    """
create table income
(
    id             bigint auto_increment primary key,
    type_id        bigint                    null comment '收入类型id，关联字典表收入类型(工资，奖金，分红)',
    detail         varchar(1024)             null comment '收入明细',
    amount         decimal(15, 2)            not null comment '收入金额',
    currency       int         default 0  not null comment '收入金额的货币类型',
    payment_method bigint                    null comment '支付方式，关联字典表（0现金、1银行卡、2微信、3支付宝等）',
    user_id        bigint                    null comment '收入人id，关联用户表主键',
    income_time    datetime                  not null comment '收入时间',
    year           int                       not null comment '收入年份',
    month          int                       not null comment '收入月份',
    source_id      bigint                    null comment '收入来源id，关联字典表收入来源（公司，店铺，某人，项目）',
    create_by      varchar(64) default ''    null comment '创建者',
    create_time    datetime                  null comment '创建时间',
    update_by      varchar(64) default ''    null comment '更新者',
    update_time    datetime                  null comment '更新时间',
    remark         text                      null comment '备注'
) COMMENT ='收入记录表';
    """

    __tablename__ = 'income'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='收入记录表ID')

    type_id = Column(Integer, comment='收入类型id，关联字典表收入类型(工资，奖金，分红)')
    acc_id = Column(Integer, comment='账户id，关联账户表主键id')
    detail = Column(String(1024), comment='收入明细')
    amount = Column(Numeric(15, 2), nullable=False, comment='收入金额')
    currency = Column(Integer, default=0, nullable=False, comment='收入金额的货币类型')
    payment_method = Column(Integer, comment='支付方式，关联字典表（0现金、1银行卡、2微信、3支付宝等）')
    user_id = Column(Integer, comment='收入人id，关联用户表主键')
    income_time = Column(DateTime, nullable=False, comment='收入时间')
    year = Column(Integer, nullable=False, comment='收入年份')
    month = Column(Integer, nullable=False, comment='收入月份')
    source_id = Column(Integer, comment='收入来源id，关联字典表收入来源（公司，店铺，某人，项目）')

    create_by = Column(String(64), default='', comment='创建者')
    create_time = Column(DateTime, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), default='', comment='更新者')
    update_time = Column(DateTime, default=datetime.now(), comment='更新时间')
    remark = Column(String(255), comment='备注')
