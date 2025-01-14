from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Numeric
from config.database import Base

class AccountTransactions(Base):
    """
create table account_transactions
(
    id              bigint auto_increment primary key,
    account_id      bigint                 not null comment '账户ID，关联finance_account表',
    current_balance decimal(15, 2)         not null comment '账户当前余额',
    create_by       varchar(64) default '' null comment '创建者',
    create_time     datetime               null comment '创建时间',
    update_by       varchar(64) default '' null comment '更新者',
    update_time     datetime               null comment '更新时间',
    remark          text                   null comment '备注'
) COMMENT ='账户流水表';
    """

    __tablename__ = 'account_transactions'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')

    account_id = Column(Integer, comment='账户ID，关联finance_account表')
    current_balance = Column(Numeric(15, 2), default=0, comment='账户当前余额')

    create_by = Column(String(64), default='', comment='创建者')
    create_time = Column(DateTime, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), default='', comment='更新者')
    update_time = Column(DateTime, default=datetime.now(), comment='更新时间')
    remark = Column(String(255), comment='备注')

