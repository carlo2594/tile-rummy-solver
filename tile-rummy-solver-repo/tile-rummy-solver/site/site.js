// ===== Edit this line when your Ko-fi page is ready =====
const SITE = {
  kofi: ''   // e.g. 'https://ko-fi.com/carloj'  (leave '' to keep the tip button hidden)
};
// =========================================================

document.querySelectorAll('[data-kofi]').forEach(a => {
  if (SITE.kofi) { a.href = SITE.kofi; a.hidden = false; } else { a.hidden = true; }
});
document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
