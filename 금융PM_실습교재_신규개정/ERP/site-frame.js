(() => {
  const toggle = document.querySelector('#site-menu-toggle');
  const links = document.querySelector('#site-links');
  if (!toggle || !links) return;
  const media = matchMedia('(max-width: 720px)');
  function setOpen(open, focus = false) {
    links.dataset.open = String(open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? '메뉴 닫기' : '메뉴';
    if (focus) toggle.focus();
  }
  setOpen(!media.matches);
  toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
  links.addEventListener('click', event => { if (media.matches && event.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && media.matches && toggle.getAttribute('aria-expanded') === 'true') setOpen(false, true); });
  media.addEventListener('change', () => setOpen(!media.matches));
  const workbookTabs = document.querySelector('.wb-tabs');
  if (workbookTabs) {
    function revealCurrentTab() {
      if (!media.matches || !workbookTabs.clientWidth) return;
      const selected = workbookTabs.querySelector('[aria-current="true"]');
      if (!selected) return;
      const tab = selected.getBoundingClientRect(), rail = workbookTabs.getBoundingClientRect();
      if (tab.left < rail.left || tab.right > rail.right)
        workbookTabs.scrollBy({left:tab.left-rail.left-4,behavior:'instant'});
    }
    new MutationObserver(revealCurrentTab).observe(workbookTabs,{subtree:true,attributes:true,attributeFilter:['aria-current']});
    media.addEventListener('change',revealCurrentTab);
    revealCurrentTab();
  }
})();
