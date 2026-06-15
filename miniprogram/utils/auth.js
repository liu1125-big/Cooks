/**
 * 登录认证模块
 */

const TOKEN_KEY = 'cooks_token'
const USER_KEY = 'cooks_user'

/** 获取 Token */
function getToken() {
  return wx.getStorageSync(TOKEN_KEY) || ''
}

/** 保存 Token */
function setToken(token) {
  wx.setStorageSync(TOKEN_KEY, token)
}

/** 移除 Token */
function removeToken() {
  wx.removeStorageSync(TOKEN_KEY)
}

/** 获取用户信息 */
function getUserInfo() {
  try {
    return JSON.parse(wx.getStorageSync(USER_KEY) || '{}')
  } catch (e) {
    return {}
  }
}

/** 保存用户信息 */
function setUserInfo(info) {
  wx.setStorageSync(USER_KEY, JSON.stringify(info))
}

/** 移除用户信息 */
function removeUserInfo() {
  wx.removeStorageSync(USER_KEY)
}

/** 是否已登录 */
function isLoggedIn() {
  return !!getToken()
}

/** 是否为管理员 */
function isAdmin() {
  const user = getUserInfo()
  return user.role === 'admin'
}

/** 退出登录 */
function logout() {
  removeToken()
  removeUserInfo()
  wx.reLaunch({ url: '/pages/login/login' })
}

module.exports = {
  getToken,
  setToken,
  removeToken,
  getUserInfo,
  setUserInfo,
  removeUserInfo,
  isLoggedIn,
  isAdmin,
  logout
}
