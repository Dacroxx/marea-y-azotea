/* Static magazine: no upload, editor, local storage, or implied persistence. */
'use strict';
(() => {
  const photos = JSON.parse(document.getElementById('published-photos').textContent);
  const cards = [...document.querySelectorAll('#archive-grid .photo-card')];
  const axisCategory = Object.fromEntries([...document.querySelectorAll('[data-axis]')].map(section => [section.dataset.axis, section.querySelector('h2').textContent]));
  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  let selection = photos;
  let viewerSelection = photos;
  let viewerIndex = 0;
  let returnFocus = null;
  const dialog = document.getElementById('lightbox');
  const image = document.getElementById('lightbox-image');
  const fallback = document.getElementById('lightbox-fallback');
  const count = document.getElementById('gallery-count');

  function setFilter(key) {
    selection = key === 'all' ? photos : photos.filter(photo => photo.primaryCategory === axisCategory[key]);
    const ids = new Set(selection.map(photo => photo.sourceId));
    cards.forEach(card => { card.hidden = !ids.has(card.dataset.sourceId); });
    filterButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === key)));
    const active = filterButtons.find(button => button.dataset.filter === key);
    const label = key === 'all' ? 'Todas' : axisCategory[key];
    count.textContent = `${selection.length} de ${photos.length} fotografías · ${label}`;
    document.getElementById('gallery-empty').hidden = selection.length !== 0;
    if (!active) throw new Error('Unknown gallery filter');
  }

  document.querySelectorAll('.image-open img').forEach(img => {
    const showFallback = () => {
      img.hidden = true;
      img.nextElementSibling.hidden = false;
    };
    img.addEventListener('error', showFallback);
    // A response can fail before this deferred script runs.
    if (img.complete && img.naturalWidth === 0) showFallback();
  });

  function renderViewer() {
    const photo = viewerSelection[viewerIndex];
    image.hidden = false;
    fallback.hidden = true;
    image.alt = photo.visualDescription;
    image.src = `https://drive.google.com/thumbnail?id=${encodeURIComponent(photo.sourceId)}&sz=w1600`;
    document.getElementById('lightbox-name').textContent = photo.originalName;
    document.getElementById('lightbox-category').textContent = photo.primaryCategory;
    document.getElementById('lightbox-description').textContent = photo.visualDescription;
    document.getElementById('lightbox-count').textContent = `${viewerIndex + 1} / ${viewerSelection.length}`;
    document.getElementById('lightbox-drive').href = `https://drive.google.com/file/d/${photo.sourceId}/view`;
    document.getElementById('lightbox-prev').disabled = viewerSelection.length < 2;
    document.getElementById('lightbox-next').disabled = viewerSelection.length < 2;
  }

  image.addEventListener('error', () => { image.hidden = true; fallback.hidden = false; });
  function step(delta) {
    viewerIndex = (viewerIndex + delta + viewerSelection.length) % viewerSelection.length;
    renderViewer();
  }
  filterButtons.forEach(button => button.addEventListener('click', () => setFilter(button.dataset.filter)));
  document.querySelectorAll('[data-gallery-filter]').forEach(link => link.addEventListener('click', () => {
    setFilter(link.dataset.galleryFilter);
  }));
  document.querySelectorAll('[data-open]').forEach(button => button.addEventListener('click', () => {
    viewerSelection = button.closest('#archive-grid') ? selection : photos;
    viewerIndex = viewerSelection.findIndex(photo => photo.sourceId === button.dataset.open);
    if (viewerIndex < 0) return;
    returnFocus = button;
    renderViewer();
    dialog.showModal();
    document.getElementById('lightbox-close').focus();
  }));
  document.getElementById('lightbox-prev').addEventListener('click', () => step(-1));
  document.getElementById('lightbox-next').addEventListener('click', () => step(1));
  document.getElementById('lightbox-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      step(event.key === 'ArrowLeft' ? -1 : 1);
    }
  });
  dialog.addEventListener('click', event => {
    const bounds = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
  });
  dialog.addEventListener('close', () => { if (returnFocus?.isConnected) returnFocus.focus(); });

  function preparePrint() {
    // Native Ctrl+P also loads the whole selection, not just the active filter.
    document.querySelectorAll('.image-open img').forEach(img => { img.loading = 'eager'; });
  }
  window.addEventListener('beforeprint', preparePrint);
  document.getElementById('print-button').addEventListener('click', async () => {
    const button = document.getElementById('print-button');
    button.disabled = true;
    button.textContent = 'Preparando imágenes…';
    preparePrint();
    const settled = Promise.all([...document.querySelectorAll('.image-open img')].map(img => img.decode().catch(() => {})));
    await Promise.race([settled, new Promise(resolve => setTimeout(resolve, 10000))]);
    button.disabled = false;
    button.textContent = 'Imprimir / PDF';
    window.print();
  });
})();
