const { get, del } = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    favorites: [],
    loading: true
  },

  onShow() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({ selected: 2 })
    }
    this.loadFavorites()
  },

  async loadFavorites() {
    this.setData({ loading: true })
    try {
      const res = await get('/favorites')
      this.setData({ favorites: res, loading: false })
    } catch (e) {
      this.setData({ loading: false })
    }
  },

  async removeFavorite(item) {
    wx.showModal({
      title: '提示',
      content: `确定取消收藏 ${item.dish_name}？`,
      success: async (res) => {
        if (res.confirm) {
          try {
            await del(`/favorites/${item.dish_id}`)
            util.showSuccess('已取消收藏')
            this.loadFavorites()
          } catch (e) { /* handled */ }
        }
      }
    })
  },

  goToDetail(e) {
    const item = e.currentTarget.dataset.item
    wx.navigateTo({ url: `/pages/dish-detail/dish-detail?id=${item.dish_id}` })
  }
})
