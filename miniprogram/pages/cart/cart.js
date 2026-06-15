const { get, post, del } = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    cartItems: [],
    totalCount: 0,
    loading: true
  },

  onShow() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({ selected: 1 })
    }
    this.loadCart()
  },

  async loadCart() {
    this.setData({ loading: true })
    try {
      const res = await get('/cart')
      this.setData({ cartItems: res, totalCount: res.length, loading: false })
    } catch (e) {
      this.setData({ loading: false })
    }
  },

  onRemoveItem(e) {
    const item = e.currentTarget.dataset.item
    wx.showModal({
      title: '提示',
      content: `确定移除 ${item.dish_name}？`,
      success: async (res) => {
        if (res.confirm) {
          try {
            await del(`/cart/${item.id}`)
            util.showSuccess('已移除')
            this.loadCart()
          } catch (err) { /* handled */ }
        }
      }
    })
  },

  async submitOrder() {
    wx.showModal({
      title: '确认下单',
      content: `确定提交 ${this.data.totalCount} 道菜的订单？`,
      success: async (res) => {
        if (res.confirm) {
          util.showLoading('提交中...')
          try {
            const result = await post('/history/submit')
            util.hideLoading()
            wx.showModal({
              title: '下单成功',
              content: `订单号：${result.order_id}\n共 ${result.total_count} 道菜`,
              showCancel: false,
              success: () => {
                this.loadCart()
              }
            })
          } catch (e) {
            util.hideLoading()
            wx.showToast({ title: e.detail || '提交失败，请重试', icon: 'none' })
          }
        }
      }
    })
  },

  clearCart() {
    wx.showModal({
      title: '提示',
      content: '确定清空购物车？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await del('/cart')
            util.showSuccess('已清空')
            this.loadCart()
          } catch (e) { /* handled */ }
        }
      }
    })
  }
})
