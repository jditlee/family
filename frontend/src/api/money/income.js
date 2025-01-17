import request from '@/utils/request'

// 查询公告列表
export function listIncome(query) {
  return request({
    url: '/money/income/list',
    method: 'get',
    params: query
  })
}

// 查询公告详细
export function getIncome(incomeId) {
  return request({
    url: '/money/income/' + incomeId,
    method: 'get'
  })
}

// 新增公告
export function addIncome(data) {
  return request({
    url: '/money/income',
    method: 'post',
    data: data
  })
}

// 修改公告
export function updateIncome(data) {
  return request({
    url: '/money/income',
    method: 'put',
    data: data
  })
}

// 删除公告
export function delIncome(incomeId) {
  return request({
    url: '/money/income/' + incomeId,
    method: 'delete'
  })
}