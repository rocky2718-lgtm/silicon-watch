#!/usr/bin/env python3
"""
fetch_rss.py — 由 GitHub Actions 執行，抓取所有 RSS 並輸出 news.json
不需要 CORS proxy，在 GitHub 伺服器端直接請求來源網站。
"""
import json, time, hashlib, re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

try:
    import feedparser
    import requests
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'feedparser', 'requests', '-q'])
    import feedparser, requests

# ── 來源設定（與 rss-sources.js 保持一致）─────────────────────────────────
SOURCES = [
    {
        "id": "technews",
        "name": "科技新報",
        "color": "#f0c060",
        "badge": "badge-technews",
        "url": "https://technews.tw/feed/",
        "categories": ["market", "process", "material"],
    },
    {
        "id": "digitimes",
        "name": "Digitimes",
        "color": "#5dc8ff",
        "badge": "badge-digitimes",
        "url": "https://www.digitimes.com/rss/rss.asp",
        "categories": ["market", "equipment", "packaging"],
    },
    {
        "id": "liberty",
        "name": "自由時報",
        "color": "#00e5aa",
        "badge": "badge-liberty",
        "url": "https://ec.ltn.com.tw/rss/business.xml",
        "categories": ["market"],
    },
    {
        "id": "ctimes",
        "name": "工商時報",
        "color": "#c0a8ff",
        "badge": "badge-ctimes",
        "url": "https://www.ctee.com.tw/rss.xml",
        "categories": ["market", "process"],
    },
    {
        "id": "tsmc",
        "name": "台積電",
        "color": "#ff8899",
        "badge": "badge-tsmc",
        "url": "https://pr.tsmc.com/tsmcpr/rss?lang=zh",
        "categories": ["tsmc", "process"],
    },
    {
        "id": "anandtech",
        "name": "AnandTech",
        "color": "#888888",
        "badge": "badge-anand",
        "url": "https://www.anandtech.com/rss/",
        "categories": ["process", "equipment"],
    },
    {
        "id": "semianalysis",
        "name": "SemiAnalysis",
        "color": "#aaddff",
        "badge": "badge-anand",
        "url": "https://www.semianalysis.com/feed",
        "categories": ["process", "market", "equipment"],
    },
    {
        "id": "eetimes",
        "name": "EE Times",
        "color": "#ffaa55",
        "badge": "badge-anand",
        "url": "https://www.eetimes.com/feed/",
        "categories": ["process", "material", "equipment"],
    },
]

# ── 半導體關鍵字（符合任一即收錄）──────────────────────────────────────────
KEYWORDS = [
    "半導體", "晶片", "晶圓", "製程", "封裝", "台積電", "tsmc", "samsung", "intel",
    "奈米", "nm ", "n2", "n3", "n4", "n5", "n7", "gaafet", "nsfet", "finfet",
    "euv", "euvl", "asml", "極紫外光", "微影", "光罩", "光阻",
    "hbm", "cowos", "soic", "chiplet", "異質整合", "3d ic",
    "矽", "介電", "high-k", "low-k", "hafnium", "ruthenium",
    "semiconductor", "wafer", "lithography", "deposition", "etching",
    "foundry", "fabless", "ic design", "記憶體", "dram", "nand", "nand flash",
    "nvidia", "amd", "qualcomm", "broadcom", "mediatek", "聯發科",
    "gate-all-around", "backside power", "2nm", "3nm", "angstrom",
]

def contains_keyword(text: str) -> bool:
    t = text.lower()
    return any(kw in t for kw in KEYWORDS)

def clean_html(html: str) -> str:
    text = re.sub(r'<[^>]+>', '', html or '')
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:300]

def parse_date(entry) -> str:
    """Return ISO8601 string or empty."""
    for attr in ('published', 'updated', 'created'):
        raw = getattr(entry, attr, None) or entry.get(attr, '')
        if raw:
            try:
                dt = parsedate_to_datetime(raw)
                return dt.astimezone(timezone.utc).isoformat()
            except Exception:
                pass
    return ''

def fetch_source(source: dict) -> list:
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; SiliconWatch/1.0; +https://github.com)',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*',
    }
    try:
        resp = requests.get(source['url'], headers=headers, timeout=15)
        resp.raise_for_status()
        feed = feedparser.parse(resp.content)
    except Exception as e:
        print(f"  ✕ {source['name']}: {e}")
        return []

    articles = []
    for entry in feed.entries[:30]:
        title   = (entry.get('title') or '').strip()
        link    = entry.get('link') or ''
        summary = clean_html(
            entry.get('summary') or
            entry.get('description') or
            (entry.get('content') or [{}])[0].get('value', '')
        )
        date = parse_date(entry)

        if not title:
            continue
        if not contains_keyword(title + ' ' + summary):
            continue

        uid = hashlib.md5(link.encode()).hexdigest()[:12]
        articles.append({
            "id":       uid,
            "title":    title,
            "link":     link,
            "summary":  summary,
            "date":     date,
            "sourceId": source['id'],
            "cats":     source['categories'],
        })

    print(f"  ✓ {source['name']}: {len(articles)} 篇符合")
    return articles

def main():
    print(f"\n=== Silicon Watch RSS Fetch — {datetime.now(timezone.utc).isoformat()} ===\n")

    all_articles = []
    seen_links   = set()

    for source in SOURCES:
        print(f"抓取 {source['name']} ({source['url']})")
        articles = fetch_source(source)
        for a in articles:
            if a['link'] not in seen_links:
                all_articles.append(a)
                seen_links.add(a['link'])
        time.sleep(0.5)   # 禮貌性延遲，避免連續請求

    # 依日期排序（最新在前）
    all_articles.sort(key=lambda a: a['date'] or '', reverse=True)

    # 輸出 news.json
    output = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "count":   len(all_articles),
        "sources": [{"id": s["id"], "name": s["name"], "color": s["color"], "badge": s["badge"], "url": s["url"]} for s in SOURCES],
        "articles": all_articles,
    }
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n=== 完成：共 {len(all_articles)} 篇，已寫入 news.json ===\n")

if __name__ == '__main__':
    main()
