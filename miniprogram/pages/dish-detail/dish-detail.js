const { get, post, del } = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    dish: null,
    isFavorited: false,
    loading: true
  },

  onLoad(options) {
    if (options.id) {
      this.loadDish(options.id)
      this.checkFavorite(options.id)
    }
  },

  async loadDish(id) {
    try {
      const dish = await get(`/dishes/${id}`, {}, { auth: false })
      this.setData({ dish, loading: false })
      wx.setNavigationBarTitle({ title: dish.name })
    } catch (e) {
      this.setData({ loading: false })
    }
  },

  async checkFavorite(id) {
    try {
      await get(`/favorites/${id}`)
      this.setData({ isFavorited: true })
    } catch (e) {
      this.setData({ isFavorited: false })
    }
  },

  async toggleFavorite() {
    const { dish, isFavorited } = this.data
    try {
      if (isFavorited) {
        await del(`/favorites/${dish.id}`)
        this.setData({ isFavorited: false })
        util.showSuccess('已取消收藏')
      } else {
        await post(`/favorites/${dish.id}`)
        this.setData({ isFavorited: true })
        util.showSuccess('收藏成功')
      }
    } catch (e) { /* handled */ }
  },

  async addToCart() {
    const { dish } = this.data
    util.showLoading('加入购物车...')
    try {
      await post('/cart', { dish_id: dish.id })
      util.hideLoading()
      util.showSuccess('已加入购物车')
    } catch (e) {
      util.hideLoading()
      if (e.detail === '该菜品已在购物车中，请勿重复添加') {
        util.showError('已在购物车中')
      }
    }
  }
})
