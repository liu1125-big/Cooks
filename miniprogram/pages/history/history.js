const { get, del } = require('../../utils/request')
const util = require('../../utils/util')

Page({
  data: {
    historyList: [],
    groupedHistory: {},
    dates: [],
    loading: true
  },

  onShow() {
    this.loadHistory()
  },

  async loadHistory() {
    this.setData({ loading: true })
    try {
      const res = await get('/history')
      
      // 按日期分组
      const grouped = {}
      const dates = []
      res.forEach(item => {
        const dateStr = item.time ? item.time.split('T')[0] : '未知日期'
        if (!grouped[dateStr]) {
          grouped[dateStr] = []
          dates.push(dateStr)
        }
        grouped[dateStr].push(item)
      })
      
      this.setData({ 
        historyList: res, 
        groupedHistory: grouped,
        dates,
        loading: false 
      })
    } catch (e) {
      this.setData({ loading: false })
    }
  },

  goToDish(e) {
    const item = e.currentTarget.dataset.item
    wx.navigateTo({ url: `/pages/dish-detail/dish-detail?id=${item.dish_id}` })
  },

  async deleteItem(e) {
    const item = e.currentTarget.dataset.item
    wx.showModal({
      title: '提示',
      content: '确定删除此记录？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await del(`/history/${item.id}`)
            util.showSuccess('已删除')
            this.loadHistory()
          } catch (e) { /* handled */ }
        }
      }
    })
  },

  async clearAll() {
    wx.showModal({
      title: '提示',
      content: '确定清空全部历史记录？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await del('/history')
            util.showSuccess('已清空')
            this.loadHistory()
          } catch (e) { /* handled */ }
        }
      }
    })
  }
})
