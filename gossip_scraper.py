# gossip_scraper_clean.py
import utils.session
import os, json, datetime, re, time, requests
from bs4 import BeautifulSoup
from transformers import pipeline

# ---------- CONFIG ----------
HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 10
PAUSE_BETWEEN_SITES = 0.5  # seconds

# ---------- AI Summarizer ----------
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def clean_text(t):
    return re.sub(r"\s+", " ", (t or "")).strip()

def fetch_summary(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code != 200:
            return ""
        soup = BeautifulSoup(r.text, "lxml")
        paras = soup.find_all("p")
        text = " ".join(p.get_text() for p in paras)
        text = clean_text(text)
        if len(text.split()) < 40:
            return ""
        out = summarizer(text, max_length=80, min_length=30, do_sample=False)
        return out[0]["summary_text"]
    except Exception:
        return ""

# ---------- SOURCES ----------
sources = [
    {
        "name": "TMZ",
        "url": "https://www.tmz.com",
        "article_selectors": ["article", "div.tmz-article"],
        "title_selectors": ["h2", "h3", ".title"]
    },
    {
        "name": "EOnline",
        "url": "https://www.eonline.com/news",
        "article_selectors": ["div.results article", "article", ".article-card"],
        "title_selectors": ["h2", "h3", ".headline"]
    },
    {
        "name": "PageSix",
        "url": "https://pagesix.com",
        "article_selectors": ["article", "div.card"],
        "title_selectors": ["h3 a", "h2 a", "a"]
    },
    {
        "name": "DailyMail",
        "url": "https://www.dailymail.co.uk/tvshowbiz/index.html",
        "article_selectors": ["div.article", "li.fcItem"],
        "title_selectors": ["a.linkro-darkred", "h2", "h3"]
    },
    {
        "name": "People",
        "url": "https://people.com/celebrity/",
        "article_selectors": ["article", "div.cards__item"],
        "title_selectors": ["h2", "h3", "a"]
    },
    {
        "name": "USWeekly",
        "url": "https://www.usmagazine.com/celebrity-news/",
        "article_selectors": ["article", ".listing-item"],
        "title_selectors": ["h2 a", "h3 a", "a"]
    },
    {
        "name": "HollywoodLife",
        "url": "https://hollywoodlife.com",
        "article_selectors": ["article", ".post"],
        "title_selectors": ["h2 a", "h3 a", "a"]
    },
    {
        "name": "PerezHilton",
        "url": "https://perezhilton.com",
        "article_selectors": ["article", ".post"],
        "title_selectors": ["h2 a", "h3 a", "a"]
    },
]

# ---------- SCRAPE ----------
stories = []

for src in sources:
    try:
        r = requests.get(src["url"], headers=HEADERS, timeout=TIMEOUT)
        if r.status_code != 200 or not r.text.strip():
            continue
        soup = BeautifulSoup(r.text, "lxml")

        # find articles
        articles = []
        for sel in src.get("article_selectors", []):
            found = soup.select(sel)
            if found:
                articles = found
                break

        if not articles:
            continue

        count = 0
        for a in articles[:15]:
            title, link, image = "", "", ""

            for tsel in src.get("title_selectors", ["h2", "h3", "a"]):
                t = a.select_one(tsel)
                if t and clean_text(t.get_text()):
                    title = clean_text(t.get_text())
                    if t.name == "a" and t.has_attr("href"):
                        link = t["href"]
                    break

            if not link:
                a_tag = a.find("a", href=True)
                if a_tag:
                    link = a_tag["href"]

            if link.startswith("/"):
                base = src["url"].split("//")[0] + "//" + src["url"].split("//")[1].split("/")[0]
                link = base + link

            img_tag = a.find("img")
            if img_tag:
                image = img_tag.get("src") or img_tag.get("data-src") or ""

            if not title or any(x in title.lower() for x in ["share", "comment", "video", "read more"]):
                continue

            summary = ""
            if link and "http" in link:
                summary = fetch_summary(link)

            stories.append({
                "source": src["name"],
                "title": title,
                "link": link,
                "image": image,
                "summary": summary
            })

            count += 1
            if count >= 8:
                break

        time.sleep(PAUSE_BETWEEN_SITES)
    except Exception:
        time.sleep(PAUSE_BETWEEN_SITES)
        continue

# ---------- DEDUPE & SAVE ----------
unique = {}
for s in stories:
    key = (s.get("link") or s.get("title")).strip()
    if key and key not in unique:
        unique[key] = s

out = {
    "date": str(datetime.datetime.now()),
    "count": len(unique),
    "stories": list(unique.values())
}

with open("gossip.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"✅ Done — {len(unique)} gossip stories saved to gossip.json")
