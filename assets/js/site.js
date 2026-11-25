// PHATECO – website thử nghiệm
(function () {
  // Menu điện thoại
  var t = document.querySelector('.menu-toggle'), n = document.querySelector('nav.main');
  if (t && n) t.addEventListener('click', function () { n.classList.toggle('open'); });

  // Lọc dự án
  document.querySelectorAll('.filters button').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.filters button').forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      var f = b.getAttribute('data-f');
      document.querySelectorAll('[data-cat]').forEach(function (c) {
        c.style.display = (f === 'all' || c.getAttribute('data-cat').indexOf(f) > -1) ? '' : 'none';
      });
    });
  });

  // Gửi form về Contact Form 7 trên phateco.com (REST, không cần đăng nhập)
  document.querySelectorAll('form[data-cf7]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var id = form.getAttribute('data-cf7');
      var msg = form.querySelector('.form-msg');
      var btn = form.querySelector('[type=submit]');
      var fd = new FormData(form);
      fd.append('_wpcf7', id);
      fd.append('_wpcf7_unit_tag', 'wpcf7-f' + id + '-p0-o1');
      fd.append('_wpcf7_locale', 'vi');
      fd.append('_wpcf7_container_post', '0');
      btn.disabled = true; msg.className = 'form-msg'; msg.textContent = '';
      fetch(window.PTC.cf7Base + '/wp-json/contact-form-7/v1/contact-forms/' + id + '/feedback', { method: 'POST', body: fd })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (j.status === 'mail_sent') { msg.className = 'form-msg ok'; msg.textContent = 'Cảm ơn bạn! PHATECO đã nhận thông tin và sẽ liên hệ lại sớm.'; form.reset(); }
          else { msg.className = 'form-msg err'; msg.textContent = (j.message || 'Chưa gửi được.') + ' Bạn có thể gửi email tới admin@phateco.com.'; }
        })
        .catch(function () { msg.className = 'form-msg err'; msg.textContent = 'Không kết nối được máy chủ. Vui lòng gửi email tới admin@phateco.com hoặc gọi 0225 3 870 870.'; })
        .finally(function () { btn.disabled = false; });
    });
  });

  // Google Analytics 4 – chỉ chạy khi đã điền mã trong assets/js/config.js
  if (window.PTC && window.PTC.gaId) {
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + window.PTC.gaId; document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date()); gtag('config', window.PTC.gaId);
    // Đo các hành động quan trọng
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a'); if (!a) return;
      var h = a.getAttribute('href') || '';
      if (h.indexOf('tel:') === 0) gtag('event', 'click_call', { link_url: h });
      else if (h.indexOf('mailto:') === 0) gtag('event', 'click_email', { link_url: h });
      else if (/bao-gia|quote/.test(h)) gtag('event', 'click_quote', { link_url: h });
    });
    document.querySelectorAll('form[data-cf7]').forEach(function (f) {
      f.addEventListener('submit', function () { gtag('event', 'generate_lead', { form_id: f.getAttribute('data-cf7') }); });
    });
  }
})();
