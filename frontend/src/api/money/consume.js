import request from '@/utils/request'

// 查询公告列表
export function listConsume(query) {
  return request({
    url: '/money/consume/list',
    method: 'get',
    params: query
  })
}

// 查询公告详细
export function getConsume(consumeId) {
  return request({
    url: '/money/consume/' + consumeId,
    method: 'get'
  })
}

// 新增公告
export function addConsume(data) {
  return request({
    url: '/money/consume',
    method: 'post',
    data: data
  })
}

// 修改公告
export function updateConsume(data) {
  return request({
    url: '/money/consume',
    method: 'put',
    data: data
  })
}

// 删除公告
export function delConsume(consumeId) {
  return request({
    url: '/money/consume/' + consumeId,
    method: 'delete'
  })
}