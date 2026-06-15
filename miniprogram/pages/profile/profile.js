const auth = require('../../utils/auth')
const { get } = require('../../utils/request')

Page({
  data: {
    userInfo: null,
    isAdmin: false
  },

  onShow() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({ selected: 3 })
    }
    if (!auth.isLoggedIn()) {
      wx.navigateTo({ url: '/pages/login/login' })
      return
    }
    this.loadUserInfo()
  },

  async loadUserInfo() {
    try {
      const info = await get('/users/me')
      auth.setUserInfo(info)
      this.setData({ userInfo: info, isAdmin: info.role === 'admin' })
    } catch (e) {
      const cached = auth.getUserInfo()
      this.setData({ userInfo: cached, isAdmin: cached.role === 'admin' })
    }
  },

  goHistory() {
    wx.navigateTo({ url: '/pages/history/history' })
  },

  goAdminDish() {
    wx.navigateTo({ url: '/pages/admin-dish/admin-dish' })
  },

  goAdminBuy() {
    wx.navigateTo({ url: '/pages/admin-buy/admin-buy' })
  },

  goAdminUser() {
    wx.navigateTo({ url: '/pages/admin-user/admin-user' })
  },

  handleLogout() {
    wx.showModal({
      title: '提示',
      content: '确定退出登录？',
      success(res) {
        if (res.confirm) {
          auth.logout()
        }
      }
    })
  }
})
