async function batchFetch(ids) {
  const out = [];
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const extract = () => {
    const noteId =
      location.href.match(/explore\/([a-f0-9]+)/)?.[1] ||
      location.href.match(/\/([a-f0-9]{24})(?:\?|$)/)?.[1] ||
      "";
    const noteWrap = document.querySelector(
      '.note-detail, .note-container, [class*="note-detail"]'
    );
    const root = noteWrap || document;
    const title =
      (root.querySelector("#detail-title") || root.querySelector(".title") || {})
        .innerText || "";
    const desc =
      (root.querySelector("#detail-desc") || root.querySelector(".desc") || {})
        .innerText || "";
    const tags = [...root.querySelectorAll("#hash-tag, .tag")]
      .map((e) => e.innerText.trim())
      .filter((t) => t.startsWith("#"));
    const total = (root.querySelector(".swiper-pagination") || {}).innerText || "";
    const imgs = [
      ...new Set(
        [...document.querySelectorAll('img[src*="spectrum"]')].map((i) => i.src)
      ),
    ].filter((u) => u.includes("nd_dft_wlteh_webp"));
    return {
      noteId,
      title: title.trim(),
      desc: desc.trim(),
      tags,
      carouselTotal: total.match(/\/(\d+)/)?.[1] || String(imgs.length),
      images: imgs,
    };
  };
  const clickCover = (id8) => {
    const titleA = [...document.querySelectorAll("a")].find(
      (a) =>
        a.href.includes(id8) &&
        a.textContent.trim() &&
        !a.textContent.includes("美研芒格君")
    );
    if (!titleA) return false;
    const item = titleA.closest("section") || titleA.closest('[class*="note"]');
    const cover =
      item?.querySelector("a.cover") ||
      [...(item?.querySelectorAll("a") || [])].find((a) => !a.textContent.trim());
    cover?.click();
    return !!cover;
  };
  for (const id8 of ids) {
    try {
      if (!location.href.includes("/user/profile/")) {
        document.dispatchEvent(
          new KeyboardEvent("keydown", { key: "Escape", code: "Escape", keyCode: 27, bubbles: true })
        );
        await sleep(800);
      }
      if (!clickCover(id8)) {
        window.scrollTo(0, document.body.scrollHeight);
        await sleep(800);
        if (!clickCover(id8)) {
          window.scrollTo(0, 0);
          await sleep(800);
          if (!clickCover(id8)) {
            out.push({ noteId: id8, error: "not found" });
            continue;
          }
        }
      }
      await sleep(1500);
      out.push(extract());
      document.dispatchEvent(
        new KeyboardEvent("keydown", { key: "Escape", code: "Escape", keyCode: 27, bubbles: true })
      );
      await sleep(700);
    } catch (e) {
      out.push({ noteId: id8, error: String(e) });
    }
  }
  return JSON.stringify(out);
}

batchFetch(["69fed593", "6a0039c1", "69fff736", "6a02b9c5", "6a041dc0", "6a0558ae"]);
