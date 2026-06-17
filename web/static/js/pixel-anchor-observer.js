// Res.: https://css-tricks.com/styling-based-on-scroll-position/

let anchor = document.getElementById('pixel-anchor')

if (!anchor) {
  const interval = window.setInterval(() => {
    anchor = document.getElementById('pixel-anchor')
    if (anchor) {
      window.clearInterval(interval)
      createObserver(anchor)
    }
  }, 100)
}

const createObserver = anchor => {
  if ('IntersectionObserver' in window && anchor) {
    const observerCallback = entries => {
      if (entries[0].boundingClientRect.y < 0) {
        document.body.classList.add('header-not-at-top')
      } else {
        document.body.classList.remove('header-not-at-top')
      }
    }
    new window.IntersectionObserver(observerCallback).observe(anchor)
  }
}
