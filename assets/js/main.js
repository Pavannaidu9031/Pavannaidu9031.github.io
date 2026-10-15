(function () {
  "use strict";

  var doc = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---------- language ---------- */
  var enTitle = document.title;

  function applyLang(lang) {
    var zh = lang === "zh";
    doc.lang = zh ? "zh-Hant" : "en";
    document.title = zh ? doc.getAttribute("data-title-zh") || enTitle : enTitle;
    document.querySelectorAll("[data-zh]").forEach(function (el) {
      if (!el.hasAttribute("data-en")) el.setAttribute("data-en", el.textContent);
      el.textContent = el.getAttribute(zh ? "data-zh" : "data-en");
    });
    document.querySelectorAll("[data-zh-placeholder]").forEach(function (el) {
      if (!el.hasAttribute("data-en-placeholder")) el.setAttribute("data-en-placeholder", el.placeholder);
      el.placeholder = el.getAttribute(zh ? "data-zh-placeholder" : "data-en-placeholder");
    });
    document.querySelectorAll("[data-lang-btn]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-lang-btn") === lang));
    });
    splitWords();
  }

  document.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-lang-btn]");
    if (!b) return;
    var lang = b.getAttribute("data-lang-btn");
    store.set("lang", lang);
    applyLang(lang);
  });

  /* ---------- word-by-word reveal ---------- */
  function splitWords() {
    document.querySelectorAll(".reveal-words").forEach(function (el) {
      var text = el.getAttribute(doc.lang === "zh-Hant" ? "data-zh" : "data-en") || el.textContent;
      var parts;
      if (doc.lang === "zh-Hant" && window.Intl && Intl.Segmenter) {
        parts = Array.from(new Intl.Segmenter("zh-Hant", { granularity: "word" }).segment(text), function (s) { return s.segment; });
      } else {
        parts = text.split(/(\s+)/);
      }
      el.textContent = "";
      parts.forEach(function (w, i) {
        if (/^\s+$/.test(w)) { el.appendChild(document.createTextNode(w)); return; }
        var m = document.createElement("span");
        m.className = "mask";
        var s = document.createElement("span");
        s.textContent = w;
        s.style.transitionDelay = Math.min(i * 0.012, 0.6) + "s";
        m.appendChild(s);
        el.appendChild(m);
      });
    });
  }

  /* ---------- reveal on scroll ---------- */
  function observeReveals() {
    var els = document.querySelectorAll(".reveal, .reveal-words");
    if (!("IntersectionObserver" in window) || reduce) {
      els.forEach(function (el) { el.setAttribute("data-in", ""); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.setAttribute("data-in", ""); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------- preloader (first page of a visit only) ---------- */
  function preloader() {
    var el = document.querySelector("[data-preloader]");
    if (!el || !doc.classList.contains("hello")) return;
    try { sessionStorage.setItem("seen-hello", "1"); } catch (e) {}
    var words = ["Hello", "你好", "నమస్కారం", "Hello"];
    var word = el.querySelector("[data-preloader-word]");
    var i = 0;
    var timer = setInterval(function () {
      i++;
      if (i < words.length) { word.textContent = words[i]; return; }
      clearInterval(timer);
      el.setAttribute("data-done", "");
      setTimeout(function () { doc.classList.remove("hello"); }, 1100);
    }, 260);
  }

  /* ---------- menu ---------- */
  function menu() {
    var panel = document.getElementById("site-menu");
    var openers = document.querySelectorAll("[data-menu-open]");
    function set(open) {
      if (open) { panel.hidden = false; document.body.setAttribute("data-menu-open", ""); }
      else document.body.removeAttribute("data-menu-open");
      openers.forEach(function (b) { b.setAttribute("aria-expanded", String(open)); });
      if (open) { var first = panel.querySelector("a"); if (first) setTimeout(function () { first.focus(); }, 300); }
    }
    openers.forEach(function (b) {
      b.addEventListener("click", function () { set(!document.body.hasAttribute("data-menu-open")); });
    });
    document.querySelectorAll("[data-menu-close]").forEach(function (b) { b.addEventListener("click", function () { set(false); }); });
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") set(false); });
    panel.addEventListener("click", function (ev) { if (ev.target.closest("a")) set(false); });
  }

  /* ---------- magnetic buttons ---------- */
  function magnetic() {
    if (!finePointer || reduce) return;
    document.querySelectorAll(".magnetic").forEach(function (m) {
      var inner = m.firstElementChild;
      m.addEventListener("mousemove", function (ev) {
        var r = m.getBoundingClientRect();
        var x = ev.clientX - r.left - r.width / 2;
        var y = ev.clientY - r.top - r.height / 2;
        m.style.transform = "translate(" + x * 0.35 + "px," + y * 0.35 + "px)";
        if (inner) inner.style.transform = "translate(" + x * 0.1 + "px," + y * 0.1 + "px)";
      });
      m.addEventListener("mouseleave", function () {
        m.style.transition = "transform .7s cubic-bezier(.22,1,.36,1)";
        m.style.transform = "";
        if (inner) { inner.style.transition = m.style.transition; inner.style.transform = ""; }
        setTimeout(function () { m.style.transition = ""; if (inner) inner.style.transition = ""; }, 700);
      });
    });
  }

  /* ---------- hover preview for work rows ---------- */
  function preview() {
    if (!finePointer) return;
    var modal = document.querySelector("[data-preview]");
    var cursor = document.querySelector("[data-cursor]");
    if (!modal || !cursor) return;
    var slider = modal.querySelector("[data-preview-slider]");
    var target = { x: 0, y: 0 }, pos = { x: 0, y: 0 }, cpos = { x: 0, y: 0 };
    var running = false;
    function tick() {
      pos.x += (target.x - pos.x) * 0.12; pos.y += (target.y - pos.y) * 0.12;
      cpos.x += (target.x - cpos.x) * 0.25; cpos.y += (target.y - cpos.y) * 0.25;
      modal.style.left = pos.x + "px"; modal.style.top = pos.y + "px";
      cursor.style.left = cpos.x + "px"; cursor.style.top = cpos.y + "px";
      if (running) requestAnimationFrame(tick);
    }
    window.addEventListener("mousemove", function (ev) {
      target.x = ev.clientX; target.y = ev.clientY;
      if (!running) { running = true; pos.x = cpos.x = target.x; pos.y = cpos.y = target.y; requestAnimationFrame(tick); }
    });
    document.querySelectorAll("[data-preview-index]").forEach(function (link) {
      link.addEventListener("mouseenter", function () {
        var i = Number(link.getAttribute("data-preview-index"));
        slider.style.transform = "translateY(" + i * -100 + "%)";
        modal.setAttribute("data-on", ""); cursor.setAttribute("data-on", "");
      });
      link.addEventListener("mouseleave", function () {
        modal.removeAttribute("data-on"); cursor.removeAttribute("data-on");
      });
    });
  }

  /* ---------- scroll-driven bits ---------- */
  function scrollFx() {
    var marquee = document.querySelector("[data-marquee]");
    var burger = document.querySelector("[data-burger]");
    var rows = document.querySelectorAll("[data-slide]");
    var parallax = document.querySelectorAll("[data-parallax]");
    var cap = document.querySelector("[data-cap]");
    var gallery = document.querySelector(".gallery");
    var x = 0, dir = -1, lastY = window.scrollY;

    function onScroll() {
      var y = window.scrollY;
      if (y !== lastY) dir = y > lastY ? -1 : 1;
      lastY = y;
      if (burger) burger.toggleAttribute("data-show", y > 120);
      var vh = window.innerHeight;
      if (gallery && !reduce) {
        var r = gallery.getBoundingClientRect();
        var prog = (vh - r.top) / (vh + r.height);
        rows.forEach(function (row) {
          var d = Number(row.getAttribute("data-slide"));
          row.style.transform = "translateX(" + d * (prog - 0.5) * 16 + "vw)";
        });
      }
      if (!reduce) parallax.forEach(function (el) {
        var r = el.getBoundingClientRect();
        var off = Math.max(-60, Math.min(60, (r.top + r.height / 2 - vh / 2) * Number(el.getAttribute("data-parallax"))));
        el.style.translate = "0 " + off.toFixed(1) + "px";
      });
      if (cap) {
        var fr = cap.parentElement.getBoundingClientRect();
        var p = Math.min(Math.max((vh - fr.top) / vh, 0), 1);
        cap.style.setProperty("--cap", (1 - p).toFixed(3));
      }
    }

    function loop() {
      if (marquee) {
        x += 0.045 * dir;
        if (x <= -50) x += 50;
        if (x > 0) x -= 50;
        marquee.style.transform = "translateX(" + x + "%)";
        requestAnimationFrame(loop);
      }
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    onScroll();
    if (marquee && !reduce) requestAnimationFrame(loop);
  }

  /* ---------- live clock (Taipei) ---------- */
  function clock() {
    var els = document.querySelectorAll("[data-clock]");
    if (!els.length) return;
    var fmt;
    try { fmt = new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Taipei", hour: "2-digit", minute: "2-digit", hour12: false }); }
    catch (e) { return; }
    function set() { var s = fmt.format(new Date()); els.forEach(function (el) { el.textContent = s; }); }
    set();
    setInterval(set, 15000);
  }

  /* ---------- work page filter + view ---------- */
  function work() {
    var root = document.querySelector("[data-work]");
    if (!root) return;
    var chips = root.querySelectorAll("[data-filter]");
    var views = root.querySelectorAll("[data-view]");
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        var f = c.getAttribute("data-filter");
        chips.forEach(function (o) { o.setAttribute("aria-pressed", String(o === c)); });
        root.querySelectorAll(".row").forEach(function (r) {
          r.hidden = f !== "all" && r.getAttribute("data-group") !== f;
        });
      });
    });
    function setView(v) {
      root.setAttribute("data-mode", v);
      views.forEach(function (o) { o.setAttribute("aria-pressed", String(o.getAttribute("data-view") === v)); });
    }
    views.forEach(function (b) {
      b.addEventListener("click", function () { var v = b.getAttribute("data-view"); setView(v); store.set("work-view", v); });
    });
    if (store.get("work-view") === "grid") setView("grid");
  }

  /* ---------- contact form → email app ---------- */
  function contact() {
    var form = document.querySelector("[data-contact-form]");
    if (!form) return;
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var to = form.getAttribute("data-email");
      if (!to) return;
      var d = new FormData(form);
      var subject = (d.get("topic") || "Hello") + " — " + d.get("name");
      var body = d.get("message") + "\n\n" + d.get("name") + (d.get("org") ? "\n" + d.get("org") : "") + "\n" + d.get("email");
      window.location.href = "mailto:" + to + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    });
  }

  /* ---------- copy email ---------- */
  function copyButtons() {
    document.querySelectorAll("[data-copy]").forEach(function (b) {
      b.addEventListener("click", function () {
        var label = b.querySelector("span") || b;
        var text = b.getAttribute("data-copy");
        function done() {
          var old = label.textContent;
          label.textContent = b.getAttribute(doc.lang === "zh-Hant" ? "data-copied-zh" : "data-copied-en");
          b.setAttribute("data-done", "");
          setTimeout(function () { label.textContent = old; b.removeAttribute("data-done"); }, 1600);
        }
        if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () { window.prompt("Email", text); });
        else window.prompt("Email", text);
      });
    });
  }

  function init() {
    preloader();
    var saved = store.get("lang");
    if (saved === "zh") applyLang("zh"); else splitWords();
    observeReveals();
    menu();
    magnetic();
    preview();
    scrollFx();
    clock();
    work();
    contact();
    copyButtons();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
