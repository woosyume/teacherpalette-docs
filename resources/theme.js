// Match the product site's preference without changing the content language.
try {
  const savedTheme = localStorage.getItem('tp.theme');
  document.documentElement.dataset.theme = savedTheme === 'dark' || savedTheme === 'light'
    ? savedTheme
    : (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
} catch (_) {
  document.documentElement.dataset.theme = 'light';
}
