import re
import requests
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin

NRP = "5025241031"
BASE = "https://progjar.web.id"
START = "/maze"

sess = requests.Session()
sess.headers.update({"NRP": NRP})

visited = set()

def interesting(text):
    if not text:
        return False
    keys = ["FOUND", "FLAG", "pattern", "alive", "next", "maze"]
    low = text.lower()
    return any(k.lower() in low for k in keys)

def extract_everything(resp):
    html = resp.text
    print(f"\n=== {resp.url} ===")
    print("STATUS:", resp.status_code)

    for k, v in resp.headers.items():
        if interesting(k) or interesting(v) or k.lower().startswith("x-"):
            print("HEADER:", k, "=", v)

    if interesting(html):
        print("BODY HIT:")
        print(html[:1500])

    soup = BeautifulSoup(html, "html.parser")

    comments = soup.find_all(string=lambda t: isinstance(t, Comment))
    for c in comments:
        if interesting(str(c)) or str(c).strip():
            print("COMMENT:", c)

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/maze"):
            links.append(href)

    return html, links

def dfs(path):
    if path in visited:
        return None
    visited.add(path)

    url = urljoin(BASE, path)
    resp = sess.get(url, timeout=15)
    html, links = extract_everything(resp)

    if "<<<YOU FOUND ME>>>" in html or "FLAG{" in html or "you found me" in html.lower():
        print("\nPOSSIBLE TARGET:", path)
        print(html)
        m = re.search(r'FLAG\{[^}]+\}', html)
        if m:
            return m.group(0)
        return "FOUND_PAGE_NO_FLAG_FORMAT"

    for link in links:
        res = dfs(link)
        if res:
            return res
    return None

result = dfs(START)
print("\nRESULT:", result)