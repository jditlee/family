from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Numeric
from config.database import Base

class AccountFundChanges(Base):
    """
create table account_fund_changes
(
    id                  bigint auto_increment primary key,
    in_account_id       bigint                 null comment '入账账户ID，关联finance_account表',
    out_account_id      bigint                 null comment '出帐账户ID，关联finance_account表',
    transaction_type_id int                    not null comment '交易类型（如收益入账，银证转账，基金加仓等），管理字典表',
    amount              decimal(15, 2)         not null comment '交易金额',
    balance_after       decimal(15, 2)         not null comment '交易后账户余额',
    create_by           varchar(64) default '' null comment '创建者',
    create_time         datetime               null comment '创建时间',
    update_by           varchar(64) default '' null comment '更新者',
    update_time         datetime               null comment '更新时间',
    remark              text                   null comment '备注'
) COMMENT ='资金变动记录表';
    """

    __tablename__ = 'account_fund_changes'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')

    in_account_id = Column(Integer, comment='入账账户ID，关联finance_account表')
    out_account_id = Column(Integer, comment='出帐账户ID，关联finance_account表')
    transaction_type_id = Column(Integer, comment='交易类型（如收益入账，银证转账，基金加仓等），管理字典表')

    amount = Column(Numeric(15, 2), default=0, comment='交易金额')
    balance_after = Column(Numeric(15, 2), default=0, comment='交易后账户余额')

    create_by = Column(String(64), default='', comment='创建者')
    create_time = Column(DateTime, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), default='', comment='更新者')
    update_time = Column(DateTime, default=datetime.now(), comment='更新时间')
    remark = Column(String(255), comment='备注')
