'use strict';

// Panels remain readable without JavaScript; enhancement turns them into choices.
document.querySelectorAll('[data-switcher]').forEach(group => {
  const container = document.getElementById(group.dataset.switcher);
  if (!container) return;
  const buttons = [...group.querySelectorAll('button[data-choice]')];
  const panels = [...container.querySelectorAll('[data-panel]')];
  function select(choice) {
    if (!panels.some(panel => panel.dataset.panel === choice)) return;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.choice === choice)));
    panels.forEach(panel => { panel.hidden = panel.dataset.panel !== choice; });
  }
  buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.choice)));
  select(buttons[0].dataset.choice);
  group.hidden = false;
});

const navLinks = [...document.querySelectorAll('nav a[href^="#"]')];
const sections = navLinks.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
function updateNavigation() {
  const position = window.scrollY + 130;
  let current = sections[0];
  for (const section of sections) {
    if (section.offsetTop <= position) current = section;
  }
  navLinks.forEach(link => {
    if (current && link.hash === '#' + current.id) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}
let pending = false;
window.addEventListener('scroll', () => {
  if (pending) return;
  pending = true;
  window.requestAnimationFrame(() => { updateNavigation(); pending = false; });
}, { passive: true });
window.addEventListener('resize', updateNavigation);
window.addEventListener('load', updateNavigation);
updateNavigation();
