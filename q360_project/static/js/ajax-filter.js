/**
 * Q360 AJAX Filter — GET filter/axtarış formalarını tam səhifə reload-suz edir.
 *
 * İstifadə:
 *   <form method="get" data-ajax-filter data-ajax-target="#results">...</form>
 *   <div id="results"> ...cədvəl + pagination... </div>
 *
 * - Form submit olduqda URL parametrləri ilə fetch edilir, serverin qaytardığı
 *   HTML-dən yalnız hədəf konteyner çıxarılıb yerində əvəz olunur.
 * - Hədəf konteynerin İÇİNDƏKİ pagination linkləri də eyni üsulla yüklənir.
 * - history.pushState ilə URL yenilənir; back/forward düymələri işləyir.
 * - Yüklənmə zamanı konteynerə .ajax-loading sinfi verilir (spinner overlay).
 */
(function () {
    'use strict';

    var LOADING_CSS = '' +
        '.ajax-filter-wrap{position:relative}' +
        '.ajax-loading{pointer-events:none}' +
        '.ajax-loading::after{content:"";position:absolute;inset:0;' +
        'background:rgba(255,255,255,.55);z-index:5;border-radius:inherit}' +
        '.dark .ajax-loading::after{background:rgba(17,24,39,.55)}' +
        '.ajax-loading::before{content:"";position:absolute;top:50%;left:50%;z-index:6;' +
        'width:2rem;height:2rem;margin:-1rem 0 0 -1rem;border-radius:9999px;' +
        'border:3px solid #93c5fd;border-top-color:#2563eb;' +
        'animation:ajaxspin .7s linear infinite}' +
        '@keyframes ajaxspin{to{transform:rotate(360deg)}}';

    function injectStyles() {
        if (document.getElementById('ajax-filter-styles')) return;
        var s = document.createElement('style');
        s.id = 'ajax-filter-styles';
        s.textContent = LOADING_CSS;
        document.head.appendChild(s);
    }

    function getTarget(form) {
        var sel = form.getAttribute('data-ajax-target') || '#ajax-results';
        return document.querySelector(sel);
    }

    function setLoading(el, on) {
        if (!el) return;
        el.classList.add('ajax-filter-wrap');
        el.classList.toggle('ajax-loading', on);
    }

    function swapFromUrl(url, targetSel, pushUrl) {
        var target = document.querySelector(targetSel);
        if (!target) { window.location.href = url; return; }
        setLoading(target, true);
        fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(function (r) {
                if (!r.ok) throw new Error('HTTP ' + r.status);
                return r.text();
            })
            .then(function (html) {
                var doc = new DOMParser().parseFromString(html, 'text/html');
                var fresh = doc.querySelector(targetSel);
                if (fresh) {
                    target.innerHTML = fresh.innerHTML;
                } else {
                    // Hədəf tapılmadısa, tam yüklənməyə geri düş
                    window.location.href = url;
                    return;
                }
                if (pushUrl) {
                    history.pushState({ ajaxFilter: targetSel }, '', url);
                }
                setLoading(target, false);
            })
            .catch(function () {
                // Şəbəkə xətasında tam yüklənməyə geri düş
                window.location.href = url;
            });
    }

    function formUrl(form) {
        var action = form.getAttribute('action') || window.location.pathname;
        var params = new URLSearchParams(new FormData(form));
        // boş parametrləri URL-də saxlama
        var clean = new URLSearchParams();
        params.forEach(function (v, k) { if (v !== '') clean.append(k, v); });
        var qs = clean.toString();
        return action + (qs ? '?' + qs : '');
    }

    function init() {
        injectStyles();
        var forms = document.querySelectorAll('form[data-ajax-filter]');
        forms.forEach(function (form) {
            var targetSel = form.getAttribute('data-ajax-target') || '#ajax-results';

            form.addEventListener('submit', function (e) {
                e.preventDefault();
                swapFromUrl(formUrl(form), targetSel, true);
            });

            // Hədəf daxilindəki pagination/sort linklərini intersept et
            var target = getTarget(form);
            if (target) {
                target.addEventListener('click', function (e) {
                    var a = e.target.closest('a[href]');
                    if (!a) return;
                    var href = a.getAttribute('href');
                    // yalnız eyni səhifənin query-dəyişən linkləri (pagination, sort)
                    if (!href || href.startsWith('#') || a.target === '_blank') return;
                    var url = new URL(href, window.location.href);
                    if (url.pathname !== window.location.pathname) return;
                    e.preventDefault();
                    swapFromUrl(url.pathname + url.search, targetSel, true);
                });
            }
        });

        if (forms.length) {
            window.addEventListener('popstate', function () {
                var form = document.querySelector('form[data-ajax-filter]');
                if (!form) return;
                var targetSel = form.getAttribute('data-ajax-target') || '#ajax-results';
                swapFromUrl(window.location.pathname + window.location.search, targetSel, false);
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
