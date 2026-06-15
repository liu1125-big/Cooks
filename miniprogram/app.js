const auth = require('./utils/auth')

App({
  onLaunch() {
    // 检查登录状态
    if (!auth.isLoggedIn()) {
      // 未登录，跳转到登录页
      wx.navigateTo({ url: '/pages/login/login' })
    }
  },

  globalData: {
    userInfo: null
  }
})
