(function () {
  "use strict";

  const filtersRoot = document.querySelector(".pub-filters");
  if (!filtersRoot) return;

  const searchInput = document.getElementById("pub-search");
  const sortSelect = document.getElementById("pub-sort");
  const clearBtn = document.getElementById("pub-clear");
  const emptyMsg = document.querySelector(".pub-empty");
  const items = Array.from(document.querySelectorAll(".pub-item"));
  const yearHeaders = Array.from(document.querySelectorAll(".pub-year"));
  const yearLists = Array.from(document.querySelectorAll(".pub-list"));

  const state = { query: "", sort: "newest", keywords: new Set() };

  /* ===== Mobile topics toggle ===== */
  const topicToggle = document.getElementById("pub-topic-toggle");
  const keywordRow = document.querySelector(".pub-keyword-row");

  if (topicToggle && keywordRow) {
    // Desktop: start expanded; mobile: start collapsed
    if (window.innerWidth > 768) {
      keywordRow.classList.add("expanded");
      topicToggle.setAttribute("aria-expanded", "true");
    } else {
      keywordRow.classList.remove("expanded");
      topicToggle.setAttribute("aria-expanded", "false");
    }

    topicToggle.addEventListener("click", () => {
      const expanded = topicToggle.getAttribute("aria-expanded") === "true";
      topicToggle.setAttribute("aria-expanded", String(!expanded));
      keywordRow.classList.toggle("expanded", !expanded);
    });
  }

  /* ===== Keyword chips ===== */

  const keywordChips = Array.from(document.querySelectorAll(".pub-keyword-chip"));
  keywordChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const kw = chip.dataset.keyword;
      if (state.keywords.has(kw)) {
        state.keywords.delete(kw);
        chip.classList.remove("active");
      } else {
        state.keywords.add(kw);
        chip.classList.add("active");
      }
      apply();
    });
  });

  /* ===== Search & Sort ===== */

  let searchTimer = null;
  searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      state.query = searchInput.value.trim().toLowerCase();
      apply();
    }, 150);
  });

  sortSelect.addEventListener("change", () => {
    state.sort = sortSelect.value;
    apply();
  });

  clearBtn.addEventListener("click", () => {
    state.query = "";
    state.sort = "newest";
    state.keywords.clear();
    searchInput.value = "";
    sortSelect.value = "newest";
    keywordChips.forEach((c) => c.classList.remove("active"));
    apply();
  });

  function matches(item) {
    // Keyword filter: item must have ALL selected keywords
    if (state.keywords.size) {
      const itemKw = (item.dataset.keywords || "").split(",");
      for (const kw of state.keywords) {
        if (!itemKw.includes(kw)) return false;
      }
    }

    if (state.query) {
      const haystack = (
        item.dataset.title + " " +
        item.dataset.authors + " " +
        item.dataset.venue + " " +
        item.dataset.year + " " +
        item.dataset.type + " " +
        (item.dataset.keywords || "").replace(/,/g, " ")
      ).toLowerCase();
      if (!haystack.includes(state.query)) return false;
    }
    return true;
  }

  function apply() {
    let visibleTotal = 0;
    for (const item of items) {
      const show = matches(item);
      item.hidden = !show;
      if (show) visibleTotal++;
    }

    for (const list of yearLists) {
      const year = list.dataset.year;
      const hasVisible = items.some((i) => i.dataset.year === year && !i.hidden);
      list.hidden = !hasVisible;
      const header = yearHeaders.find((h) => h.dataset.year === year);
      if (header) header.hidden = !hasVisible;
    }

    for (const list of yearLists) {
      const kids = Array.from(list.querySelectorAll(".pub-item"));
      kids.sort(compareBy(state.sort));
      kids.forEach((k) => list.appendChild(k));
    }

    const parent = yearLists[0] && yearLists[0].parentNode;
    if (parent) {
      const pairs = yearHeaders
        .map((h) => ({ year: h.dataset.year, header: h, list: yearLists.find((l) => l.dataset.year === h.dataset.year) }))
        .filter((p) => p.list);
      pairs.sort((a, b) => {
        if (state.sort === "oldest") return Number(a.year) - Number(b.year);
        return Number(b.year) - Number(a.year);
      });
      pairs.forEach((p) => {
        parent.appendChild(p.header);
        parent.appendChild(p.list);
      });
      if (emptyMsg) parent.appendChild(emptyMsg);
    }

    emptyMsg.hidden = visibleTotal > 0;
  }

  function compareBy(mode) {
    if (mode === "venue") {
      return (a, b) => a.dataset.venue.localeCompare(b.dataset.venue);
    }
    if (mode === "oldest") {
      return (a, b) =>
        Number(a.dataset.year) - Number(b.dataset.year) ||
        a.dataset.venue.localeCompare(b.dataset.venue);
    }
    return () => 0;
  }

  /* ===== BibTeX copy ===== */

  const toast = document.createElement("div");
  toast.className = "pub-toast";
  document.body.appendChild(toast);
  let toastTimer = null;

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add("visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("visible"), 2000);
  }

  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".pub-btn-bibtex");
    if (!btn) return;
    e.preventDefault();
    const bibtex = btn.dataset.bibtex;
    if (!bibtex) return;

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(bibtex).then(
        () => showToast("BibTeX copied to clipboard"),
        () => showToast("Failed to copy")
      );
    } else {
      const ta = document.createElement("textarea");
      ta.value = bibtex;
      ta.style.cssText = "position:fixed;left:-9999px";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      showToast("BibTeX copied to clipboard");
    }
  });

  /* ===== Abstract toggle ===== */

  document.addEventListener("click", (e) => {
    const toggle = e.target.closest(".pub-abstract-toggle");
    if (!toggle) return;
    e.preventDefault();
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!expanded));
    const item = toggle.closest(".pub-item");
    const body = item ? item.querySelector(".pub-abstract-body") : null;
    if (body) body.classList.toggle("expanded", !expanded);
  });
})();
