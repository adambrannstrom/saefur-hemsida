// Om SAEFUR: bakgrund. Ren JavaScript, ingen server. 2026-10-25.
// Växlar var nionde sekund med övertoning, driver långsamt (CSS). Står stilla vid minskad rörelse och i dold flik.
(function () {
  var D = JSON.parse(document.getElementById('data').textContent);
  var bilder = Array.prototype.slice.call(document.querySelectorAll('.bakgrund img'));
  if (bilder.length > 1 && !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    var i = 0, timer = null;
    function rotera() {
      if (timer) clearInterval(timer);
      timer = document.hidden ? null : setInterval(function () {
        bilder[i].classList.remove('aktiv'); i = (i + 1) % bilder.length; bilder[i].classList.add('aktiv');
      }, D.vaxling * 1000);
    }
    document.addEventListener('visibilitychange', rotera);
    rotera();
  }
})();
