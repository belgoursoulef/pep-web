document.addEventListener('DOMContentLoaded', () => {
  const categoryButtons = document.querySelectorAll('[data-filter-category]');
  const brandButtons = document.querySelectorAll('[data-filter-brand]');
  const engineButtons = document.querySelectorAll('[data-filter-engine]');
  const carCards = document.querySelectorAll('.models-view article');
  const resultsCountText = document.getElementById('results-count');

  let activeFilters = {
    category: null, // e.g. "suv", "berline", "compacte", "break", "cabriolet", "coupe"
    brand: null,    // e.g. "BMW", "Tesla", "Audi", "Mercedes"
    engine: null    // e.g. "electric", "hybrid", "petrol", "diesel"
  };

  function updateCatalog() {
    let visibleCount = 0;
    
    carCards.forEach(card => {
      const cardCategory = card.getAttribute('data-category');
      const cardBrand = card.getAttribute('data-brand');
      const cardEngine = card.getAttribute('data-fuel');

      const categoryMatch = !activeFilters.category || cardCategory === activeFilters.category;
      const brandMatch = !activeFilters.brand || cardBrand === activeFilters.brand;
      const engineMatch = !activeFilters.engine || cardEngine === activeFilters.engine;

      if (categoryMatch && brandMatch && engineMatch) {
        // Show card with a smooth fade in
        card.style.display = 'flex';
        setTimeout(() => {
          card.style.opacity = '1';
          card.style.transform = 'scale(1)';
        }, 10);
        visibleCount++;
      } else {
        // Hide card with a smooth fade out
        card.style.opacity = '0';
        card.style.transform = 'scale(0.95)';
        setTimeout(() => {
          if (card.style.opacity === '0') {
            card.style.display = 'none';
          }
        }, 300); // matches CSS transition duration
      }
    });

    if (resultsCountText) {
      resultsCountText.innerText = visibleCount;
    }
  }

  // Categories Selection
  categoryButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const val = btn.getAttribute('data-filter-category');
      
      if (activeFilters.category === val) {
        activeFilters.category = null;
        btn.classList.remove('active');
      } else {
        categoryButtons.forEach(b => b.classList.remove('active'));
        activeFilters.category = val;
        btn.classList.add('active');
      }
      updateCatalog();
    });
  });

  // Brands Selection
  brandButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const val = btn.getAttribute('data-filter-brand');
      
      brandButtons.forEach(b => b.classList.remove('active'));
      
      if (val === 'all') {
        activeFilters.brand = null;
        btn.classList.add('active');
      } else {
        if (activeFilters.brand === val) {
          activeFilters.brand = null;
          document.querySelector('[data-filter-brand="all"]').classList.add('active');
        } else {
          activeFilters.brand = val;
          btn.classList.add('active');
        }
      }
      updateCatalog();
    });
  });

  // Engines Selection
  engineButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const val = btn.getAttribute('data-filter-engine');
      
      if (activeFilters.engine === val) {
        activeFilters.engine = null;
        btn.classList.remove('active');
      } else {
        engineButtons.forEach(b => b.classList.remove('active'));
        activeFilters.engine = val;
        btn.classList.add('active');
      }
      updateCatalog();
    });
  });

  // Initialize display properties for transition animations
  carCards.forEach(card => {
    card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    card.style.opacity = '1';
    card.style.transform = 'scale(1)';
  });
});
