const { post, get } = require('../../utils/request')
const auth = require('../../utils/auth')

Page({
  data: {
    isLogin: true,
    username: '',
    password: '',
    nickname: '',
    loading: false
  },

  onInputUsername(e) { this.setData({ username: e.detail.value }) },
  onInputPassword(e) { this.setData({ password: e.detail.value }) },
  onInputNickname(e) { this.setData({ nickname: e.detail.value }) },

  switchToLogin() {
    if (!this.data.isLogin) {
      this.setData({ isLogin: true, username: '', password: '', nickname: '' })
    }
  },

  switchToRegister() {
    if (this.data.isLogin) {
      this.setData({ isLogin: false, username: '', password: '', nickname: '' })
    }
  },

  toggleMode() {
    this.setData({ isLogin: !this.data.isLogin, username: '', password: '', nickname: '' })
  },

  async handleSubmit() {
    const { isLogin, username, password, nickname } = this.data
    if (!username || !password) {
      wx.showToast({ title: '请填写用户名和密码', icon: 'none' })
      return
    }
    if (!isLogin && !nickname) {
      wx.showToast({ title: '请填写昵称', icon: 'none' })
      return
    }

    this.setData({ loading: true })
    try {
      if (isLogin) {
        const res = await post('/users/login', { username, password }, { auth: false })
        if (!res.access_token) {
          wx.showToast({ title: '登录失败，请重试', icon: 'none' })
          this.setData({ loading: false })
          return
        }
        auth.setToken(res.access_token)
        try {
          const userInfo = await get('/users/me')
          auth.setUserInfo(userInfo)
        } catch (e) {
          auth.removeToken()
          auth.removeUserInfo()
          wx.showToast({ title: '获取用户信息失败，请重新登录', icon: 'none' })
          this.setData({ loading: false })
          return
        }
        wx.switchTab({ url: '/pages/index/index' })
      } else {
        await post('/users/register', { username, password, nickname, role: 'user' }, { auth: false })
        wx.showToast({ title: '注册成功，请登录', icon: 'success' })
        this.setData({ isLogin: true, password: '' })
      }
    } catch (e) {
      // request.js 已统一处理错误提示
    } finally {
      this.setData({ loading: false })
    }
  }
})
