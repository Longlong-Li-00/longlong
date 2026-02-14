const avatar = document.querySelector('[data-avatar]');
if (avatar) {
  const img = avatar.querySelector('img');
  if (img) {
    img.addEventListener('error', () => {
      img.classList.add('is-hidden');
      avatar.classList.add('no-image');
    });
  }
}
