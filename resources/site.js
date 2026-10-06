(function () {
  const theme = document.querySelector('[data-resource-theme]');
  if (theme) {
    const updateThemeButton = () => {
      const dark = document.documentElement.dataset.theme === 'dark';
      theme.textContent = dark ? '☀︎' : '☾';
      theme.setAttribute('aria-pressed', String(dark));
    };
    updateThemeButton();
    theme.addEventListener('click', () => {
      const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem('tp.theme', next); } catch (_) { /* Theme still works. */ }
      updateThemeButton();
    });
  }

  const toggle = document.querySelector('[data-resource-menu]');
  const menu = document.getElementById('resource-menu');
  if (toggle && menu) {
    const closeMenu = () => {
      menu.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    };
    toggle.addEventListener('click', () => {
      const open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    menu.addEventListener('click', event => {
      if (event.target.closest('a')) closeMenu();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.classList.contains('open')) {
        closeMenu();
        toggle.focus();
      }
    });
    matchMedia('(min-width: 761px)').addEventListener('change', closeMenu);
  }
})();
