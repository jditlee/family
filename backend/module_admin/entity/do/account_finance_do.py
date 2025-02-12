from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Numeric
from config.database import Base


class AccountFinance(Base):
    """
create table account_finance
(
    id           bigint auto_increment primary key,
    accounr_name varchar(255)   not null comment '账户名称',
    type_id      int            not null comment '账户类型id,关联字典表',
    max_balance  decimal(15, 2) not null default 0 comment '历史最高资金',
    principal    decimal(15, 2) not null default 0 comment '账户本金',
    user_id      bigint         not null comment '账户所属家庭成员id',
    create_by    varchar(64)             default '' null comment '创建者',
    create_time  datetime       null comment '创建时间',
    update_by    varchar(64)             default '' null comment '更新者',
    update_time  datetime       null comment '更新时间',
    remark       text           null comment '备注'
) COMMENT =' 账户表';
    """

    __tablename__ = 'account_finance'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')

    accounr_name = Column(String(255), comment='账户名称')
    type_id = Column(Integer, comment='账户类型id,关联字典表')
    max_balance = Column(Numeric(15, 2), default=0, comment='上年度最高资金')
    principal = Column(Numeric(15, 2), default=0, comment='账户本金')
    user_id = Column(Integer, comment='账户所属家庭成员id')

    create_by = Column(String(64), default='', comment='创建者')
    create_time = Column(DateTime, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), default='', comment='更新者')
    update_time = Column(DateTime, default=datetime.now(), comment='更新时间')
    remark = Column(String(255), comment='备注')

