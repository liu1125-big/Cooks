Component({
  data: {
    selected: 0,
    list: [
      {
        pagePath: "/pages/index/index",
        text: "菜单",
        icon: "📋",
        iconActive: "📋"
      },
      {
        pagePath: "/pages/cart/cart",
        text: "购物车",
        icon: "🛒",
        iconActive: "🛒"
      },
      {
        pagePath: "/pages/favorites/favorites",
        text: "收藏",
        icon: "🤍",
        iconActive: "❤️"
      },
      {
        pagePath: "/pages/profile/profile",
        text: "我的",
        icon: "👤",
        iconActive: "👤"
      }
    ]
  },

  methods: {
    switchTab(e) {
      const data = e.currentTarget.dataset
      const url = data.path
      wx.switchTab({ url })
    }
  }
})
