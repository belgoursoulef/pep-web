document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('demo-3d-modal');
  if (!modal) return;

  const modalTitle = document.getElementById('modal-car-title');
  const iframeContainer = modal.querySelector('.iframe-container');
  const closeBtn = modal.querySelector('.modal-close-btn');
  const backdrop = modal.querySelector('.modal-backdrop');
  
  // Cache the spinner element
  const spinner = modal.querySelector('.modal-spinner');

  // Open modal function
  function openModal(sketchfabId, carName) {
    if (!sketchfabId) return;

    // Set title
    modalTitle.textContent = carName;

    // Clear previous iframe if any (keeping spinner)
    const existingIframe = iframeContainer.querySelector('iframe');
    if (existingIframe) {
      existingIframe.remove();
    }
    
    // Show spinner
    if (spinner) {
      spinner.style.display = 'block';
    }

    // Create and insert new iframe
    const iframe = document.createElement('iframe');
    iframe.title = carName;
    iframe.frameBorder = "0";
    iframe.allowFullscreen = true;
    iframe.setAttribute('mozallowfullscreen', 'true');
    iframe.setAttribute('webkitallowfullscreen', 'true');
    iframe.allow = "autoplay; fullscreen; xr-spatial-tracking";
    iframe.setAttribute('xr-spatial-tracking', '');
    iframe.setAttribute('execution-while-out-of-viewport', '');
    iframe.setAttribute('execution-while-not-rendered', '');
    iframe.setAttribute('web-share', '');
    
    // Append parameters for autoplay, preload, etc.
    iframe.src = `https://sketchfab.com/models/${sketchfabId}/embed?autostart=1&preload=1&ui_controls=1`;

    // Hide spinner once iframe loads
    iframe.addEventListener('load', () => {
      if (spinner) {
        spinner.style.display = 'none';
      }
    });

    iframeContainer.appendChild(iframe);

    // Show modal
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden'; // Prevent scrolling background
  }

  // Close modal function
  function closeModal() {
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = ''; // Restore scrolling

    // Remove iframe to stop audio/video/processing in background
    setTimeout(() => {
      const iframe = iframeContainer.querySelector('iframe');
      if (iframe) {
        iframe.remove();
      }
    }, 400); // Wait for transition to finish
  }

  // Add event listeners to triggers
  // 1. Action CTA "Explorar" buttons and hover 3D overlays
  document.querySelectorAll('.trigger-3d-modal').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const sketchfabId = btn.getAttribute('data-sketchfab-id');
      const carName = btn.getAttribute('data-car-name');
      openModal(sketchfabId, carName);
    });
  });

  // Close triggers
  closeBtn.addEventListener('click', closeModal);
  backdrop.addEventListener('click', closeModal);

  // Close on Esc key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });
});
