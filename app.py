# app.py
import os
import time
import json
import threading
import requests
from flask import Flask, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
CHAT_ID = os.environ.get("CHAT_ID", "").strip()
MW_COOKIE = os.environ.get("MW_COOKIE", "").strip()
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "20"))
STATE_FILE = "state.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MwChecker/1.0)",
    "Cookie": MW_COOKIE
}

MW_URL = "https://www.microworkers.com/locked-jobs"

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"last_ids": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def send_telegram_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("BOT_TOKEN or CHAT_ID not set!")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": True}
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print("Error sending telegram:", e)

def parse_jobs(html):
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    for a in soup.find_all("a", href=True):
        if "/dotask/info/" in a["href"]:
            job_id = a["href"].split("/dotask/info/")[1].split("_")[0]
            title = a.get_text(strip=True)
            link = "https://www.microworkers.com" + a["href"]
            jobs.append({"id": job_id, "title": title, "link": link})
    seen = set()
    unique_jobs = []
    for j in jobs:
        if j["id"] not in seen:
            seen.add(j["id"])
            unique_jobs.append(j)
    return unique_jobs

def check_loop():
    state = load_state()
    last_ids = state.get("last_ids", [])
    session = requests.Session()
    session.headers.update(HEADERS)

    while True:
        try:
            r = session.get(MW_URL, timeout=15)
            if r.status_code == 200:
                jobs = parse_jobs(r.text)
                for job in reversed(jobs):
                    if job["id"] not in last_ids:
                        msg = f"🚀 New Microworkers Task!\n\nTitle: {job['title']}\nLink: {job['link']}\nID: {job['id']}"
                        send_telegram_message(msg)
                        last_ids.append(job["id"])
                last_ids = last_ids[-200:]
                state["last_ids"] = last_ids
                save_state(state)
            else:
                print("Error fetching jobs:", r.status_code)
        except Exception as e:
            print("Loop error:", e)
        time.sleep(POLL_INTERVAL)

@app.route("/")
def home():
    return jsonify({"status": "running", "interval": POLL_INTERVAL})

def start_bg():
    t = threading.Thread(target=check_loop, daemon=True)
    t.start()

if __name__ == "__main__":
    start_bg()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    start_bg()
