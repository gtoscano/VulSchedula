# VulSchedula – Vulnerable Scheduling App

> **Educational Use Only**  
> This project is intentionally insecure. Do **not** deploy it in production or trust its code without auditing.

**VulSchedula** is a Django‑based web application inspired by doodle‑style schedulers, designed as a hands‑on learning tool for _Introduction to Secure Computing_. It lets users create scheduling polls, share them via email, and collect votes—all while containing built‑in security pitfalls for you to discover and fix.

---

## 🎯 Educational Objectives

1. **Identify Security Vulnerabilities**  
   Audit the codebase to find flaws that could leak sensitive data.
2. **Understand Risks of Third‑Party Code**  
   Learn why you should never blindly trust or deploy unverified software.
3. **Role‑Play a Malicious Hosting Provider**  
   Exploit vulnerabilities to steal instructor‑provided credentials and document your process.

---

## 🔍 Features

- **Poll Creation:** Select multiple date/time options.
- **Poll Sharing:** Generate and email poll URLs to participants.
- **Poll Voting:** External users cast their votes on a simple web form.
- **Hidden Vulnerabilities:** Deliberate flaws that leak poll data, user credentials, or database info.

---

## 📦 Requirements

- Docker & Docker Compose  
- Bash shell  
- `msmtp` or another SMTP client configured for sending emails (optional)

---

## 🚀 Setup & Run

1. **Configure environment**  
   - Copy or create `variables.env` in the project root (see sample below).
2. **Clone repository**
   ```bash
   git clone git@github.com:gtoscano/VulSchedula.git
   cd VulSchedula
   sudo bash mod_permissions.sh
   ```
3. **(Optional) Build Docker images**
   ```bash
   docker compose build --no-cache
   ```
4. **Launch the application**
   ```bash
   docker compose up -d
   ```
5. **Verify**  
   Open `http://127.0.0.1` (or your host’s IP) in a browser.

<details>
  <summary>Sample <code>variables.env</code></summary>

  ```ini
  RABBITMQ_DEFAULT_USER=guest
  RABBITMQ_DEFAULT_PASS=guest
  AMQP_HOST=rabbitmq
  AMQP_PORT=5672
  REDIS_HOST=redis
  REDIS_PORT=6379
  POSTGRES_DB=vul_schedula
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=yourpassword
  DJANGO_SUPERUSER_USERNAME=admin
  DJANGO_SUPERUSER_PASSWORD=yourpassword
  HOST_IP=192.168.1.X
  HOST_NAME=home-vulschedula.catholic-u.ai
  CREATE_SUPERUSER=True
  RUN_INIT_SCRIPT=True
  ```
</details>

---

## 🎓 Student Tasks

### Task 1: Security Analyst
- Audit the code and document at least **five** distinct vulnerabilities (e.g., SQL injection, weak file permissions, insecure command execution).
- Explain the risk and propose how to fix each issue.

### Task 2: Mischievous Hosting Provider
- Acting as an attacker, exploit one or more vulnerabilities to **steal three** pre‑created usernames/passwords.
- Provide step‑by‑step documentation of how you executed the exploit.

Once you have the app running locally, **come see me** in my office. I’ll demonstrate exploiting one vulnerability live to guide your next steps.

---

## 🔒 Security Goals

- ✅ Only registered users can create polls.  
- ✅ Only poll creators can close their polls.  
- ✅ Private polls restrict voting and calendar downloads to invited users.  

---

**⚠️ Disclaimer:** This software is intentionally insecure and provided for educational purposes. Do **not** deploy or use it in any environment where security matters.

---

**Happy hacking!**  

