Component({
  properties: {
    count: { type: Number, value: 0 }
  },
  methods: {
    onTap() {
      wx.switchTab({ url: '/pages/cart/cart' })
    }
  }
})
