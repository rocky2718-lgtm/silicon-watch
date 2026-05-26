# Silicon Watch · 半導體資訊中樞

> GitHub Actions 每 2 小時在伺服器端抓取 RSS，存成 `news.json`。  
> 前端直接讀取靜態 JSON，**載入速度 < 200ms**，無需 CORS proxy。

## 架構

```
GitHub Actions (每 2 小時)
  └── fetch_rss.py          ← Python 直接抓 RSS，無需 proxy
        └── news.json       ← 存回 repo，commit 並 push

GitHub Pages
  └── index.html            ← fetch('news.json')，秒顯
```

## 部署步驟（5 分鐘完成）

### 1. 建立 Repository 並推送

```bash
cd silicon-watch
git init
git add .
git commit -m "init: silicon watch"
git remote add origin https://github.com/你的帳號/silicon-watch.git
git branch -M main
git push -u origin main
```

### 2. 啟用 GitHub Pages

Repository → **Settings** → **Pages** → Source 選 **GitHub Actions** → 儲存

### 3. 確認 Actions 權限

Settings → **Actions** → General → **Workflow permissions** → 選 **Read and write permissions** → 儲存

### 4. 手動觸發第一次抓取

Actions → **Fetch RSS & Deploy** → **Run workflow** → 等約 1 分鐘

完成後網址：`https://你的帳號.github.io/silicon-watch/`

---

## 新增 RSS 來源

只需編輯 `fetch_rss.py` 的 `SOURCES` 列表：

```python
{
    "id": "mysite",
    "name": "我的來源",
    "color": "#ff6600",
    "badge": "badge-anand",
    "url": "https://example.com/feed.xml",
    "categories": ["market"],
},
```

commit 推上去後，Actions 自動更新。

## 檔案說明

| 檔案 | 說明 |
|------|------|
| `index.html` | 前端頁面，只 fetch `news.json` |
| `fetch_rss.py` | GitHub Actions 執行的 RSS 爬蟲 |
| `news.json` | Actions 自動產生，不需手動編輯 |
| `.github/workflows/deploy.yml` | 排程：每 2 小時抓取 + 部署 |

## 速度比較

| 方法 | 每次開頁等待 |
|------|------------|
| 舊版（CORS proxy）| 5–15 秒 |
| **新版（news.json）** | **< 200ms** |
