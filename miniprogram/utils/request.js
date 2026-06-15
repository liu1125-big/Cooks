/**
 * 网络请求封装
 * 统一处理 token、错误、基础URL
 */

const auth = require('./auth')

const BASE_URL = 'http://localhost:8000'

/**
 * 发起 HTTP 请求
 * @param {string} url - 请求路径（不含基础URL）
 * @param {object} options - 配置项
 * @param {string} options.method - 请求方法 GET/POST/PUT/DELETE
 * @param {object} options.data - 请求体数据
 * @param {object} options.query - 查询参数对象
 * @param {boolean} options.auth - 是否需要认证（默认 true）
 * @param {boolean} options.silent - 是否静默（不显示错误提示）
 * @returns {Promise}
 */
function request(url, options = {}) {
  return new Promise((resolve, reject) => {
    const { method = 'GET', data, query, auth: needAuth = true, silent = false } = options

    // 拼接查询参数
    let fullUrl = BASE_URL + url
    if (query) {
      const params = Object.keys(query)
        .filter(key => query[key] !== undefined && query[key] !== null && query[key] !== '')
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(query[key])}`)
        .join('&')
      if (params) fullUrl += '?' + params
    }

    // 构建请求头
    const header = { 'Content-Type': 'application/json' }
    if (needAuth) {
      const token = auth.getToken()
      if (token) {
        header['Authorization'] = `Bearer ${token}`
      }
    }

    wx.request({
      url: fullUrl,
      method,
      data,
      header,
      success(res) {
        const { statusCode, data: resData } = res

        if (statusCode >= 200 && statusCode < 300) {
          resolve(resData)
        } else if (statusCode === 401) {
          // Token 失效，跳转登录
          auth.removeToken()
          auth.removeUserInfo()
          wx.showToast({ title: resData.detail || '登录已过期，请重新登录', icon: 'none' })
          setTimeout(() => {
            wx.reLaunch({ url: '/pages/login/login' })
          }, 1500)
          reject(resData)
        } else if (statusCode === 403) {
          if (!silent) wx.showToast({ title: resData.detail || '权限不足', icon: 'none' })
          reject(resData)
        } else {
          if (!silent) wx.showToast({ title: resData.detail || '请求失败', icon: 'none' })
          reject(resData)
        }
      },
      fail(err) {
        if (!silent) wx.showToast({ title: '网络连接失败', icon: 'none' })
        reject(err)
      }
    })
  })
}

/** GET 请求 */
function get(url, query, options = {}) {
  return request(url, { ...options, method: 'GET', query })
}

/** POST 请求 */
function post(url, data, options = {}) {
  return request(url, { ...options, method: 'POST', data })
}

/** PUT 请求 */
function put(url, data, options = {}) {
  return request(url, { ...options, method: 'PUT', data })
}

/** DELETE 请求 */
function del(url, options = {}) {
  return request(url, { ...options, method: 'DELETE' })
}

module.exports = { request, get, post, put, del, BASE_URL }
