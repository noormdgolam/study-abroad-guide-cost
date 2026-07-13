// Service Worker Registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/sw.js').then(function(registration) {
      console.log('ServiceWorker registration successful with scope: ', registration.scope);
    }, function(err) {
      console.log('ServiceWorker registration failed: ', err);
    });
  });
}

// Client-side Search Logic
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');

  if (searchInput && searchResults) {
    // Fetch search index
    fetch('/search_index.json')
      .then(response => response.json())
      .then(data => {
        searchInput.addEventListener('input', (e) => {
          const query = e.target.value.toLowerCase();
          searchResults.innerHTML = '';
          
          if (query.length < 2) return;
          
          const results = data.filter(item => 
            item.title.toLowerCase().includes(query) || 
            item.excerpt.toLowerCase().includes(query)
          );
          
          if (results.length === 0) {
            searchResults.innerHTML = '<p>No results found.</p>';
            return;
          }
          
          results.slice(0, 10).forEach(item => {
            const div = document.createElement('div');
            div.className = 'card';
            div.innerHTML = `
              <h3><a href="${item.url}">${item.title}</a></h3>
              <p>${item.excerpt}</p>
            `;
            searchResults.appendChild(div);
          });
        });
        
        // If query param is present on load
        const urlParams = new URLSearchParams(window.location.search);
        const q = urlParams.get('q');
        if (q) {
          searchInput.value = q;
          searchInput.dispatchEvent(new Event('input'));
        }
      });
  }
});

// Cookie Consent Logic
document.addEventListener('DOMContentLoaded', () => {
  const banner = document.getElementById('cookie-banner');
  const btn = document.getElementById('accept-cookies');
  if (banner && btn) {
    if (!localStorage.getItem('cookieConsent')) {
      banner.style.display = 'block';
    }
    btn.addEventListener('click', () => {
      localStorage.setItem('cookieConsent', 'true');
      banner.style.display = 'none';
    });
  }
});
