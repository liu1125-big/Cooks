const { get, post } = require('../../utils/request')
const auth = require('../../utils/auth')

Page({
  data: {
    categories: [],
    dishes: [],
    groupedDishes: {},
    currentCategory: '',
    searchKeyword: '',
    cartCount: 0,
    loading: false,
    recommendDish: null,
    showRecommendPopup: false
  },

  onLoad() {
    if (!auth.isLoggedIn()) {
      wx.navigateTo({ url: '/pages/login/login' })
      return
    }
    this.loadDishes()
    this.loadCartCount()
  },

  onShow() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({ selected: 0 })
    }
    this.loadCartCount()
    this.loadDishes()
  },

  async loadDishes() {
    this.setData({ loading: true })
    try {
      const query = {}
      if (this.data.searchKeyword) query.keyword = this.data.searchKeyword
      const res = await get('/dishes', query, { auth: false })
      
      // 按 category 分组
      const categories = []
      const groupedDishes = {}
      res.forEach(dish => {
        const cat = dish.category || '未分类'
        if (!groupedDishes[cat]) {
          groupedDishes[cat] = []
          categories.push(cat)
        }
        groupedDishes[cat].push(dish)
      })
      
      this.setData({ 
        dishes: res, 
        categories,
        groupedDishes,
        loading: false 
      })
    } catch (e) { 
      console.error(e)
      this.setData({ loading: false })
    }
  },

  async loadCartCount() {
    try {
      const res = await get('/cart')
      this.setData({ cartCount: res.length })
    } catch (e) { /* silent */ }
  },

  onSelectCategory(e) {
    const category = e.currentTarget.dataset.category
    this.setData({ currentCategory: category })
  },

  onSearchInput(e) {
    this.setData({ searchKeyword: e.detail.value })
  },

  onSearch() {
    this.loadDishes()
  },

  clearSearch() {
    this.setData({ searchKeyword: '' })
    this.loadDishes()
  },

  onDishTap(e) {
    const dish = e.detail.dish
    wx.navigateTo({ url: `/pages/dish-detail/dish-detail?id=${dish.id}` })
  },

  async onAddToCart(e) {
    const dish = e.detail.dish
    try {
      await post('/cart', { dish_id: dish.id })
      wx.showToast({ title: '已加入购物车', icon: 'success' })
      this.loadCartCount()
    } catch (e) { 
      if (e.detail === '该菜品已在购物车中，请勿重复添加') {
        wx.showToast({ title: '已在购物车中', icon: 'none' })
      }
    }
  },

  async onRecommend() {
    try {
      const query = {}
      if (this.data.currentCategory) query.category = this.data.currentCategory
      const dish = await get('/random', query, { auth: false })
      this.setData({ recommendDish: dish, showRecommendPopup: true })
    } catch (e) {
      wx.showToast({ title: '没有符合条件的菜品', icon: 'none' })
    }
  },
  
  closeRecommendPopup() {
    this.setData({ showRecommendPopup: false })
  },
  
  goRecommendDetail() {
    const dish = this.data.recommendDish
    if (dish) {
      this.setData({ showRecommendPopup: false })
      wx.navigateTo({ url: `/pages/dish-detail/dish-detail?id=${dish.id}` })
    }
  },

  noop() {}
})
