// Growth Tracker — lightweight client-side analytics.
// Collects page views + goal clicks (checkout buttons) into localStorage,
// so you can see which landing gets traffic and where people click.
// Deterministic, no external servers, no personal data.

(function () {
  var SITE = (new URLSearchParams(window.location.search)).get("utm_source") || "direct";
  var PAGE = window.location.pathname;
  var KEY = "growth_tracker";

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { return {}; }
  }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} }

  function today() { return new Date().toISOString().slice(0, 10); }

  function record(event, label) {
    var d = load();
    d["pageviews"] = d["pageviews"] || {};
    d["clicks"] = d["clicks"] || {};
    var t = today();
    d["pageviews"][t] = d["pageviews"][t] || {};
    d["pageviews"][t][PAGE + "|" + SITE] = (d["pageviews"][t][PAGE + "|" + SITE] || 0) + 1;
    if (event === "click" && label) {
      d["clicks"][t] = d["clicks"][t] || {};
      d["clicks"][t][label] = (d["clicks"][t][label] || 0) + 1;
    }
    save(d);
  }

  record("view");

  // Auto-attach to all whop buy links so we capture click source without editing each.
  // Use capture phase + pointerdown so we record BEFORE the link navigates away.
  function tap(e) {
    var el = e.target;
    var a = (el && el.closest) ? el.closest("a") : null;
    if (a && a.href && a.href.indexOf("whop.com/shopgo") !== -1) {
      record("click", (a.textContent || "checkout").trim().slice(0, 40));
    }
  }
  document.addEventListener("pointerdown", tap, true);
  document.addEventListener("click", tap, true);
})();
