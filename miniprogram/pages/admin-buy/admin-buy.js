const { get, post, put, del } = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    buyList: [],
    stats: null,
    loading: true,
    showPopup: false,
    editMode: false,
    editId: null,
    form: { name: '', price: '', number: '', date: '' }
  },

  onLoad() {
    // 设置默认日期为今天
    const today = new Date()
    const dateStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
    this.setData({ 'form.date': dateStr })
  },

  onShow() {
    this.loadData()
    this.loadStats()
  },

  async loadData() {
    this.setData({ loading: true })
    try {
      const res = await get('/buy')
      this.setData({ buyList: res, loading: false })
    } catch (e) { this.setData({ loading: false }) }
  },

  async loadStats() {
    try {
      const daily = await get('/buy/stats/daily')
      const monthly = await get('/buy/stats/monthly')
      this.setData({ stats: { daily, monthly } })
    } catch (e) { /* silent */ }
  },

  openAdd() {
    const today = new Date()
    const dateStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
    this.setData({
      showPopup: true, editMode: false, editId: null,
      form: { name: '', price: '', number: '', date: dateStr }
    })
  },

  openEdit(e) {
    const item = e.currentTarget.dataset.item
    const dateStr = item.date || ''
    this.setData({
      showPopup: true, editMode: true, editId: item.id,
      form: {
        name: item.name,
        price: String(item.price),
        number: String(item.number),
        date: dateStr
      }
    })
  },

  closePopup() { this.setData({ showPopup: false }) },

  noop() {},

  onInputField(e) {
    const field = e.currentTarget.dataset.field
    this.setData({ [`form.${field}`]: e.detail.value })
  },

  onDateChange(e) {
    this.setData({ 'form.date': e.detail.value })
  },

  async handleSubmit() {
    const { editMode, editId, form } = this.data
    if (!form.name.trim()) { util.showError('请输入食材名称'); return }
    if (!form.price || isNaN(parseFloat(form.price))) { util.showError('请输入有效价格'); return }
    if (!form.number || isNaN(parseFloat(form.number))) { util.showError('请输入有效数量'); return }
    if (!form.date) { util.showError('请选择日期'); return }

    util.showLoading()
    try {
      const data = {
        name: form.name.trim(),
        price: parseFloat(form.price),
        number: parseFloat(form.number),
        date: form.date
      }
      if (editMode) {
        await put(`/buy/${editId}`, data, { silent: true })
        util.hideLoading(); util.showSuccess('更新成功')
      } else {
        await post('/buy', data, { silent: true })
        util.hideLoading(); util.showSuccess('创建成功')
      }
      this.setData({ showPopup: false })
      this.loadData()
      this.loadStats()
    } catch (e) {
      console.error('采购提交失败:', JSON.stringify(e))
      util.hideLoading()
      setTimeout(() => {
        util.showError(editMode ? '更新失败，请重试' : '创建失败，请重试')
      }, 300)
    }
  },

  deleteItem(e) {
    const item = e.currentTarget.dataset.item
    wx.showModal({
      title: '确认删除',
      content: `确定删除「${item.name}」的采购记录？`,
      success: async (res) => {
        if (res.confirm) {
          util.showLoading()
          try {
            await del(`/buy/${item.id}`)
            util.hideLoading(); util.showSuccess('删除成功')
            this.loadData()
            this.loadStats()
          } catch (e) { util.hideLoading() }
        }
      }
    })
  }
})
