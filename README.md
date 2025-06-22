# 📘 Lyumi Deployment Guide

This guide explains how to run the Lyumi Discord AI bot persistently across different systems, and how to deploy it reliably on a Linux server. First of all, you need to have AnythingLLM and Ollama set up. For how to do that go [here](docker/anythingllm-ollama.md).

---

## 🧪 Local Development (Testing)

### ✅ Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 bot.py
```

### ✅ Windows (CMD):

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

### ⚠️ Note:

- Make sure your `.env` file is present and filled with valid credentials.
- Keep the terminal open during testing — the bot will shut down if closed.

---

## 🚀 Production Deployment (Linux Server)

### Recommended Tool: `systemd`

> Best for permanent background service on any Linux distribution (Ubuntu, Debian, Arch, etc.)

### 1. Create a virtual environment:

```bash
cd /path/to/lyumi-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Create a systemd service:

```bash
sudo nano /etc/systemd/system/lyumi.service
```

Paste this:

```ini
[Unit]
Description=Lyumi Discord AI Bot
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/lyumi-bot
ExecStart=/path/to/lyumi-bot/venv/bin/python3 bot.py
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

> Replace `your_username` and `path/to/lyumi-bot` accordingly.

### 3. Enable and start the service:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable lyumi
sudo systemctl start lyumi
```

### 4. View logs:

```bash
journalctl -u lyumi -f
```

### ✅ Benefits of systemd

- Bot runs **even after logout or reboot**
- Automatically restarts on crash
- Clean logging via `journalctl`

---

## 🛑 To Stop the Bot (systemd)

```bash
sudo systemctl stop lyumi
```

## ♻️ To Restart the Bot (systemd)

```bash
sudo systemctl restart lyumi
```

---

✅ Deployment complete — Lyumi is now running like a service!