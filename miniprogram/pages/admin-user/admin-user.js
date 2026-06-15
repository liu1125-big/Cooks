const { get, put, del } = require('../../utils/request')
const auth = require('../../utils/auth')
const util = require('../../utils/util')

Page({
  data: {
    users: [],
    loading: true,
    currentUserId: null,
    showRolePicker: false,
    editUser: null,
    newRole: 'user'
  },

  onShow() {
    const userInfo = auth.getUserInfo()
    this.setData({ currentUserId: userInfo.id })
    this.loadUsers()
  },

  async loadUsers() {
    this.setData({ loading: true })
    try {
      const res = await get('/users')
      this.setData({ users: res, loading: false })
    } catch (e) { this.setData({ loading: false }) }
  },

  openRolePicker(e) {
    const user = e.currentTarget.dataset.item
    this.setData({ showRolePicker: true, editUser: user, newRole: user.role })
  },

  closeRolePicker() { this.setData({ showRolePicker: false }) },

  noop() {},

  onRoleChange(e) {
    this.setData({ newRole: e.currentTarget.dataset.value })
  },

  async saveRole() {
    const { editUser, newRole } = this.data
    util.showLoading()
    try {
      await put(`/users/${editUser.id}`, { role: newRole })
      util.hideLoading()
      util.showSuccess('角色已更新')
      this.setData({ showRolePicker: false })
      this.loadUsers()
    } catch (e) { util.hideLoading() }
  },

  deleteUser(e) {
    const user = e.currentTarget.dataset.item
    if (user.id === this.data.currentUserId) {
      util.showError('不能删除自己')
      return
    }
    wx.showModal({
      title: '确认删除',
      content: `确定删除用户「${user.nickname}」？`,
      success: async (res) => {
        if (res.confirm) {
          util.showLoading()
          try {
            await del(`/users/${user.id}`)
            util.hideLoading()
            util.showSuccess('删除成功')
            this.loadUsers()
          } catch (e) { util.hideLoading() }
        }
      }
    })
  }
})
