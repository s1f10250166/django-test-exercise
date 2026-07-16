// Simple theme toggle: toggles data-theme attribute on documentElement
document.addEventListener('DOMContentLoaded', function(){
  const btn = document.getElementById('themeToggle');
  if(!btn) return;
  // initialize from localStorage
  const saved = localStorage.getItem('todo-theme');
  if(saved) document.documentElement.setAttribute('data-theme', saved);
  btn.addEventListener('click', function(){
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? '' : 'dark';
    if(next) document.documentElement.setAttribute('data-theme', next);
    else document.documentElement.removeAttribute('data-theme');
    localStorage.setItem('todo-theme', next);
    btn.setAttribute('aria-pressed', next === 'dark');
  });
});
