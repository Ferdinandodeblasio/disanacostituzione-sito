(function () {
  // Il referto: un organo aperto alla volta
  var list = document.querySelector('.referto-list');
  if (list) {
    var buttons = list.querySelectorAll('button[aria-controls]');
    var open = function (btn) {
      buttons.forEach(function (b) {
        var on = b === btn;
        b.setAttribute('aria-expanded', on ? 'true' : 'false');
        var p = document.getElementById(b.getAttribute('aria-controls'));
        if (p) p.hidden = !on;
      });
    };
    buttons.forEach(function (b) {
      b.addEventListener('click', function () { open(b); });
    });
    var desktop = window.matchMedia('(min-width: 52.01rem)');
    var first = buttons[0];
    if (first) open(first);
  }
})();
