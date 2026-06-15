Component({
  properties: {
    dish: { type: Object, value: {} },
    showActions: { type: Boolean, value: true }
  },
  methods: {
    onTap() {
      this.triggerEvent('tap', { dish: this.data.dish })
    },
    onAddCart() {
      this.triggerEvent('addcart', { dish: this.data.dish })
    },
    onToggleFav() {
      this.triggerEvent('togglefav', { dish: this.data.dish })
    }
  }
})
