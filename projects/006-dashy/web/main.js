const viewer = document.querySelector('#image-viewer');
const image = document.querySelector('#viewer-image');
const title = document.querySelector('#viewer-title');
const original = document.querySelector('#viewer-original');
const close = document.querySelector('#viewer-close');
let opener;
document.querySelectorAll('[data-image]').forEach(button => {
  button.addEventListener('click', () => {
    opener = button;
    image.src = button.dataset.image;
    image.alt = button.dataset.title;
    title.textContent = button.dataset.title;
    original.href = button.dataset.image;
    viewer.showModal();
    document.body.classList.add('viewer-open');
    close.focus();
  });
});
close.addEventListener('click', () => viewer.close());
viewer.addEventListener('click', event => {
  if (event.target === viewer) {
    const bounds = viewer.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) viewer.close();
  }
});
viewer.addEventListener('close', () => {
  document.body.classList.remove('viewer-open');
  opener?.focus();
});
