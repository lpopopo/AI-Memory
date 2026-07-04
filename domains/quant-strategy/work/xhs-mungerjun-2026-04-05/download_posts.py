#!/usr/bin/env python3
"""Download Apr-May 2026 Xiaohongshu posts from posts-data.json."""

import json
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA_FILE = BASE / "posts-data.json"
PREV_SYNC = BASE.parent / "xhs-mungerjun-2026-07-04"


def download_image(url: str, dest: Path) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return {"status": resp.status, "bytes": len(data), "file": str(dest), "url": url}


def copy_existing(note_id: str, post_dir: Path) -> bool:
    src = PREV_SYNC / f"xhs-{note_id[:8]}"
    if not src.exists():
        return False
    post_dir.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        dest = post_dir / f.name
        if not dest.exists():
            dest.write_bytes(f.read_bytes())
    return True


def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        payload = json.load(f)

    results = []
    for post in payload["posts"]:
        note_id = post["noteId"]
        short = note_id[:8]
        post_dir = BASE / f"xhs-{short}"
        if copy_existing(note_id, post_dir):
            print(f"  [{short}] copied from previous sync")
        else:
            post_dir.mkdir(parents=True, exist_ok=True)

        md_path = post_dir / "content.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# {post['title']}\n\n")
            f.write(f"- 博主: 美研芒格君 / Kay2289123\n")
            f.write(f"- 帖子ID: {note_id}\n")
            f.write(f"- 发布日期(推算): {post.get('publishedDate', 'unknown')}\n")
            f.write(f"- 链接: {post['url']}\n")
            f.write(f"- 轮播图: {post.get('carouselTotal', len(post['images']))} 张\n")
            f.write(f"- 标签: {', '.join(post.get('tags', []))}\n\n")
            f.write("## 正文\n\n")
            f.write(post["desc"].replace("\t", ""))
            f.write("\n")

        image_records = []
        for i, url in enumerate(post["images"], 1):
            dest = post_dir / f"{i:02d}.webp"
            if dest.exists() and dest.stat().st_size > 1000:
                image_records.append({
                    "i": i, "status": "cached", "bytes": dest.stat().st_size,
                    "file": str(dest), "url": url
                })
                continue
            try:
                rec = download_image(url, dest)
                rec["i"] = i
                image_records.append(rec)
                print(f"  [{short}] img {i}/{len(post['images'])} OK")
            except Exception as e:
                image_records.append({"i": i, "status": "error", "error": str(e), "url": url})
                print(f"  [{short}] img {i} FAILED: {e}")

        with open(post_dir / "image-urls.json", "w", encoding="utf-8") as f:
            json.dump(image_records, f, ensure_ascii=False, indent=2)

        results.append({
            "noteId": note_id,
            "title": post["title"],
            "publishedDate": post.get("publishedDate"),
            "dir": str(post_dir),
            "imagesDownloaded": sum(1 for r in image_records if r.get("status") in (200, "cached")),
            "totalImages": len(post["images"]),
        })

    with open(BASE / "download-summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nDone: {len(results)} posts -> {BASE}")


if __name__ == "__main__":
    main()
