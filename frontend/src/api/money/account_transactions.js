import request from '@/utils/request'

// 查询公告列表
export function listAccountTransactions(query) {
  return request({
    url: '/money/account_transactions/list',
    method: 'get',
    params: query
  })
}

// 查询公告详细
export function getAccountTransactions(account_transactionsId) {
  return request({
    url: '/money/account_transactions/' + account_transactionsId,
    method: 'get'
  })
}

// 新增公告
export function addAccountTransactions(data) {
  return request({
    url: '/money/account_transactions',
    method: 'post',
    data: data
  })
}

// 修改公告
export function updateAccountTransactions(data) {
  return request({
    url: '/money/account_transactions',
    method: 'put',
    data: data
  })
}

// 删除公告
export function delAccountTransactions(account_transactionsId) {
  return request({
    url: '/money/account_transactions/' + account_transactionsId,
    method: 'delete'
  })
}