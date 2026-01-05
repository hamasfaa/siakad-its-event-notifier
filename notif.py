import requests
import time
from bs4 import BeautifulSoup

URL = "https://akademik.its.ac.id/data_nilaipersem.php"

COOKIES = {
    "PHPSESSID": "SESSION_ID_HERE"
}

CHECK_INTERVAL = 300  # 5 menit

# Telegram
BOT_TOKEN = "YOUR_BOT_TELEGRAM_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_TELEGRAM_ID_HERE"

VALID_GRADES = {"A", "AB", "B", "BC", "C", "D", "E"}

def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()

def extract_nilai_struct(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    result = {}

    rows = soup.find_all("tr", class_=["NormalBG", "AlternateBG"])

    for tr in rows:
        tds = tr.find_all("td")
        if len(tds) != 5:
            continue

        kode = tds[0].get_text(strip=True)
        matkul = tds[1].get_text(" ", strip=True)
        nilai = tds[3].get_text(strip=True)

        result[kode] = {
            "matkul": matkul,
            "nilai": nilai
        }

    if not result:
        raise Exception("Gagal parsing data (session expired?)")

    return result

def fetch_data() -> dict:
    r = requests.get(URL, cookies=COOKIES, timeout=15)

    if "login" in r.url.lower():
        raise Exception("Session expired (redirect ke login)")

    r.raise_for_status()
    return extract_nilai_struct(r.text)

def detect_grade_changes(old: dict, new: dict) -> list:
    changes = []

    for kode, new_data in new.items():
        if kode not in old:
            continue

        old_grade = old[kode]["nilai"]
        new_grade = new_data["nilai"]

        if old_grade == "_" and new_grade in VALID_GRADES:
            changes.append({
                "kode": kode,
                "matkul": new_data["matkul"],
                "nilai": new_grade
            })

    return changes

def main():
    print("start Monitoring...")

    send_telegram_message("<b>Monitoring Nilai Akademik Aktif</b>\nSistem sedang memantau nilai kamu.")

    last_data = fetch_data()

    while True:
        time.sleep(CHECK_INTERVAL)
        try:
            current_data = fetch_data()
            changes = detect_grade_changes(last_data, current_data)

            if changes:
                msg = "<b>NILAI BARU KELUAR!</b>\n\n"
                for c in changes:
                    msg += f"• <b>{c['kode']}</b>\n"
                    msg += f"  {c['matkul']}\n"
                    msg += f"  ➜ <b>{c['nilai']}</b>\n\n"

                send_telegram_message(msg)

            last_data = current_data

        except Exception as e:
            error_msg = f"<b>Error Monitoring</b>\n{str(e)}"
            print(error_msg)
            send_telegram_message(error_msg)
            time.sleep(600)

if __name__ == "__main__":
    main()
