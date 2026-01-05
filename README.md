# Notifier SIAKAD ITS

## Setup Main Program

### 1. Clone atau Download Repository

```bash
git clone <repository-url>
cd siakad-its-event-notifier
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Setup Bot Telegram

### 1. Membuat Bot dengan BotFather

1. Buka aplikasi Telegram
2. Cari **@BotFather** di pencarian Telegram
3. Mulai chat dengan mengetik `/start`
4. Buat bot baru dengan mengetik `/newbot`
5. Masukkan nama bot
6. Masukkan username bot (harus diakhiri dengan "bot")
7. BotFather akan memberikan token seperti ini:
   ```
   Done! Congratulations on your new bot. You will find it at t.me/{username_bot}. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.
   
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
   Keep your token secure and store it safely, it can be used by anyone to control your bot.
   
   For a description of the Bot API, see this page: https://core.telegram.org/bots/api
   ```

### 2. Mendapatkan Chat ID Telegram Anda

1. Cari **@userinfobot** di pencarian Telegram
2. Mulai chat dengan mengetik `/start`
3. Bot akan memberikan informasi Anda, termasuk **Chat ID**:
   ```
   @username
   Id: 123456789
   First: Nama Anda
   Lang: en
   Registered: Check Date
   ```
4. Salin **Id** tersebut (contoh: `123456789`)

## Konfigurasi

### 1. Session ID SIAKAD ITS

1. Login ke [SIAKAD ITS](https://akademik.its.ac.id)
2. Buka Developer Tools di browser (tekan `F12` atau klik kanan → Inspect)
3. Pergi ke tab **Application** (Chrome) atau **Storage** (Firefox)
4. Di sidebar kiri, klik **Cookies** → `https://akademik.its.ac.id`
5. Cari cookie dengan nama **PHPSESSID**
6. Salin **Value** dari cookie tersebut

> **Catatan:** Session ID akan expired setelah beberapa waktu. Login ulang ke SIAKAD ITS untuk mendapatkan session ID baru.

### 2. Edit File `notif.py`

Buka file `notif.py` dan ubah konfigurasi berikut:

```python
COOKIES = {
    "PHPSESSID": "SESSION_ID_HERE"  # ← Ganti dengan session ID
}

BOT_TOKEN = "YOUR_BOT_TELEGRAM_TOKEN_HERE"  # ← Ganti dengan token bot telegram

CHAT_ID = "YOUR_CHAT_TELEGRAM_ID_HERE"  # ← Ganti dengan chat ID telegram
```

**Contoh setelah diisi:**

```python
COOKIES = {
    "PHPSESSID": "abc123def456ghi789jkl012mno345pqr"
}

BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890"

CHAT_ID = "123456789"
```

### 3. (Opsional) Ubah Interval Pengecekan

Secara default, bot akan mengecek setiap 5 menit. Untuk mengubahnya, edit baris berikut:

```python
CHECK_INTERVAL = 300  # dalam detik (300 = 5 menit)
```

> **Catatan:** Interval pengecekan dapat diubah sesuai kebutuhan. Pastikan tidak terlalu kecil interval pengecekan untuk menghindari terbanned oleh Telegram dan SIAKAD ITS.

## Menjalankan Bot

### 1. Menjalankan Langsung

```bash
python notif.py
```

### 2. Menjalankan di Background (Linux/Mac)

```bash
nohup python notif.py &
```

### 3. Menjalankan di Background (Windows)

Buat file `start.bat`:

```batch
@echo off
start /B python notif.py
```

Kemudian jalankan `start.bat`.


