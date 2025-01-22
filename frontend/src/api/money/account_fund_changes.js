import request from '@/utils/request'

// 查询公告列表
export function listAccountFundChanges(query) {
  return request({
    url: '/money/account_fund_changes/list',
    method: 'get',
    params: query
  })
}

// 查询公告详细
export function getAccountFundChanges(accountFundChangesId) {
  return request({
    url: '/money/account_fund_changes/' + accountFundChangesId,
    method: 'get'
  })
}

// 新增公告
export function addAccountFundChanges(data) {
  return request({
    url: '/money/account_fund_changes',
    method: 'post',
    data: data
  })
}

// 修改公告
export function updateAccountFundChanges(data) {
  return request({
    url: '/money/account_fund_changes',
    method: 'put',
    data: data
  })
}

// 删除公告
export function delAccountFundChanges(accountFundChangesId) {
  return request({
    url: '/money/account_fund_changes/' + accountFundChangesId,
    method: 'delete'
  })
}