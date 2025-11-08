// Show loading overlay when analysis form is submitted
document.addEventListener('DOMContentLoaded', () => {
  const form    = document.getElementById('analyze-form');
  const overlay = document.getElementById('loading-overlay');
  if (form && overlay) {
    form.addEventListener('submit', () => overlay.classList.remove('hidden'));
  }
});
