/**
 * 通用工具函数
 */

/** 格式化日期 */
function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const h = String(d.getHours()).padStart(2, '0')
  const min = String(d.getMinutes()).padStart(2, '0')
  return `${y}-${m}-${day} ${h}:${min}`
}

/** 防抖 */
function debounce(fn, delay = 500) {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => fn.apply(this, args), delay)
  }
}

/** 难度星级文字 */
function difficultyText(level) {
  const stars = ['', '★', '★★', '★★★', '★★★★', '★★★★★']
  return stars[level] || ''
}

/** 显示加载 */
function showLoading(title = '加载中...') {
  wx.showLoading({ title, mask: true })
}

/** 隐藏加载 */
function hideLoading() {
  wx.hideLoading()
}

/** 成功提示 */
function showSuccess(title = '操作成功') {
  wx.showToast({ title, icon: 'success' })
}

/** 错误提示 */
function showError(title = '操作失败') {
  wx.showToast({ title, icon: 'none' })
}

module.exports = { formatDate, debounce, difficultyText, showLoading, hideLoading, showSuccess, showError }
