import request from '@/utils/request'

// 查询公告列表
export function listAccountFinance(query) {
  return request({
    url: '/money/account_finance/list',
    method: 'get',
    params: query
  })
}

// 查询公告详细
export function getAccountFinance(account_financeId) {
  return request({
    url: '/money/account_finance/' + account_financeId,
    method: 'get'
  })
}

// 新增公告
export function addAccountFinance(data) {
  return request({
    url: '/money/account_finance',
    method: 'post',
    data: data
  })
}

// 修改公告
export function updateAccountFinance(data) {
  return request({
    url: '/money/account_finance',
    method: 'put',
    data: data
  })
}

// 删除公告
export function delAccountFinance(account_financeId) {
  return request({
    url: '/money/account_finance/' + account_financeId,
    method: 'delete'
  })
}