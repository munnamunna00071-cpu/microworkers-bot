# Microworkers Telegram Bot (Cookie-Based)

এই বট Render সার্ভারে চলবে এবং প্রতি কয়েক সেকেন্ড অন্তর Microworkers এর Locked Jobs পেজ চেক করবে।  
নতুন কাজ মিললেই Telegram গ্রুপে মেসেজ পাঠাবে।

---

## প্রয়োজনীয় তথ্য
1. **BOT_TOKEN** – BotFather থেকে পাওয়া।
2. **CHAT_ID** – আপনার গ্রুপের chat id (`/getChat` দিয়ে বের করুন)。
3. **MW_COOKIE** – Microworkers এ লগইন অবস্থায় ব্রাউজার থেকে Cookie কপি করে দিন।

---

## Render এ ডেপ্লয় করার ধাপ
1. এই রিপো GitHub এ আপলোড করুন।
2. Render → New → Web Service → আপনার রিপো সিলেক্ট করুন।
3. Environment variables যোগ করুন:
   - `BOT_TOKEN`
   - `CHAT_ID`
   - `MW_COOKIE`
4. Build Command:
   ```
   pip install -r requirements.txt
   ```
5. Start Command:
   ```
   gunicorn app:app --bind 0.0.0.0:$PORT --workers 1
   ```
6. Deploy করুন।

---

## নোট
- Render Free plan স্লিপ করতে পারে, আপটাইম ধরে রাখতে পিং সার্ভিস ব্যবহার করুন।
- Cookie পরিবর্তন হলে `MW_COOKIE` আপডেট করুন।
