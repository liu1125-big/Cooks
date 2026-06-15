const { get, post, put, del } = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    dishes: [],
    loading: true,
    keyword: '',
    showPopup: false,
    editMode: false,
    editId: null,
    form: { name: '', category: '', remark: '' }
  },

  onShow() {
    this.loadData()
  },

  async loadData() {
    this.setData({ loading: true })
    try {
      const query = {}
      if (this.data.keyword) query.keyword = this.data.keyword
      const res = await get('/dishes', query, { auth: false })
      this.setData({ dishes: res, loading: false })
    } catch (e) { this.setData({ loading: false }) }
  },

  onSearch(e) {
    this.setData({ keyword: e.detail.value })
    this.loadData()
  },

  openAdd() {
    this.setData({
      showPopup: true, editMode: false, editId: null,
      form: { name: '', category: '', remark: '' }
    })
  },

  openEdit(e) {
    const item = e.currentTarget.dataset.item
    this.setData({
      showPopup: true, editMode: true, editId: item.id,
      form: {
        name: item.name,
        category: item.category || '',
        remark: item.remark || ''
      }
    })
  },

  closePopup() { this.setData({ showPopup: false }) },

  noop() {},

  onInputField(e) {
    const field = e.currentTarget.dataset.field
    this.setData({ [`form.${field}`]: e.detail.value })
  },

  async handleSubmit() {
    const { editMode, editId, form } = this.data
    if (!form.name.trim()) { util.showError('请输入菜品名称'); return }
    if (!form.category.trim()) { util.showError('请输入分类'); return }

    util.showLoading()
    try {
      const data = {
        name: form.name.trim(),
        category: form.category.trim(),
        remark: form.remark || undefined
      }
      if (editMode) {
        await put(`/dishes/${editId}`, data, { silent: true })
        util.hideLoading(); util.showSuccess('更新成功')
      } else {
        await post('/dishes', data, { silent: true })
        util.hideLoading(); util.showSuccess('创建成功')
      }
      this.setData({ showPopup: false })
      this.loadData()
    } catch (e) {
      console.error('菜品提交失败:', JSON.stringify(e))
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
      content: `确定删除「${item.name}」？`,
      success: async (res) => {
        if (res.confirm) {
          util.showLoading()
          try {
            await del(`/dishes/${item.id}`)
            util.hideLoading(); util.showSuccess('删除成功')
            this.loadData()
          } catch (e) { util.hideLoading() }
        }
      }
    })
  }
})
