document.addEventListener('DOMContentLoaded', () => {
  const menuBtn = document.querySelector('[data-menu-btn]');
  const nav = document.querySelector('[data-nav]');

  if (menuBtn && nav) {
    menuBtn.addEventListener('click', () => {
      const expanded = menuBtn.getAttribute('aria-expanded') === 'true';
      menuBtn.setAttribute('aria-expanded', String(!expanded));
      nav.classList.toggle('open');
    });
  }

  const resumeInput = document.querySelector('#resume');
  const fileName = document.querySelector('[data-file-name]');

  if (resumeInput && fileName) {
    resumeInput.addEventListener('change', () => {
      const selectedFile = resumeInput.files && resumeInput.files[0];
      fileName.textContent = selectedFile ? selectedFile.name : 'Choose your resume';
    });
  }
});
