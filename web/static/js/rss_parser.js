document.addEventListener('DOMContentLoaded', () => {
  const tickerItemsContainer = document.getElementById('ticker-items');
  if (!tickerItemsContainer) return;

  // Fetch the feed.xml asynchronously
  fetch('/static/feed.xml')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.text();
    })
    .then(str => {
      // Parse the XML string
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(str, 'text/xml');
      const items = xmlDoc.getElementsByTagName('item');
      
      let htmlContent = '';
      
      // Loop through the items and extract title & link
      for (let i = 0; i < items.length; i++) {
        const titleEl = items[i].getElementsByTagName('title')[0];
        const linkEl = items[i].getElementsByTagName('link')[0];
        
        const titleText = titleEl ? titleEl.textContent : '';
        const linkText = linkEl ? linkEl.textContent : '#';
        
        if (titleText) {
          htmlContent += `<a href="${linkText}" class="ticker-item" target="_blank" rel="noopener">${titleText}</a>`;
        }
      }
      
      // Inject the generated links inside the ticker content element
      tickerItemsContainer.innerHTML = htmlContent;
    })
    .catch(err => {
      console.error('Error loading or parsing RSS feed:', err);
      tickerItemsContainer.innerHTML = '<span class="ticker-item">Unable to load news updates.</span>';
    });
});
