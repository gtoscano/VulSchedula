# VulSchedula Security Assessment — Student Checklist

**Course:** CSC 406 — Introduction to Secure Computing
**Target:** `192.168.8.147`
**Instructor:** Dr. Gregorio Toscano

---

## Objective

You have been given access to a vulnerable web application (VulSchedula) deployed on a virtual machine. Your task is to:

1. **Identify** security vulnerabilities across the entire stack (OS, network, web server, application)
2. **Fix** as many vulnerabilities as you can
3. **Document** your findings in a structured report
4. **Encrypt** your report and submit it securely

---

## Reference Material

Throughout this checklist, you will find references to the course slides. Use them to review the concepts behind each vulnerability category.

| Slide Deck | Topic | Location |
|---|---|---|
| 01-v2 | Computer Security Overview (CIA, threat modeling, design principles) | `docs/slides/01-v2.pdf` |
| 02-v2 | Cryptographic Tools (encryption, hashing, PKI, TLS) | `docs/slides/02-v2.pdf` |
| 03-v2 | User Authentication (passwords, hashing, MFA, challenge-response) | `docs/slides/03-v2.pdf` |
| 04-v2 | Access Control (DAC, MAC, RBAC, ABAC, Unix permissions) | `docs/slides/04-v2.pdf` |
| 07-v2 | Denial-of-Service (flooding, amplification, rate limiting, SYN cookies) | `docs/slides/07-v2.pdf` |
| 08-v2 | Intrusion Detection (HIDS, NIDS, Snort, honeypots) | `docs/slides/08-v2.pdf` |
| 09-v2 | Firewalls & IPS (packet filter, stateful, DMZ, iptables, ufw) | `docs/slides/09-v2.pdf` |
| 11-v2 | Software Security (input validation, injection, XSS, CSRF, encoding) | `docs/slides/11-v2.pdf` |
| 12-v2 | OS Security (hardening, users, groups, services, patching, logging) | `docs/slides/12-v2.pdf` |

Lab-specific presentations are in `docs/additional-slides/`:

| Slide Deck | Topic |
|---|---|
| session1 | Reconnaissance & Information Disclosure |
| session2 | DoS Attacks |
| session3 | Injection Attacks |
| session4 | XSS & CSRF |
| session5 | Authentication & Access Control |
| session6 | TLS, Headers & Network + Django Settings |
| session9 | OS Hardening & System-Level Security |

---

## Checklist

Use this checklist to guide your assessment. Vulnerabilities span multiple layers of the system.

### A. OS & System-Level Security

> **Review:** Slides 12-v2 (OS hardening, users, groups, services, patching), 09-v2 (firewalls, iptables, ufw), session9 (OS hardening lab)

The application runs on a Linux server. If the OS is compromised, nothing else matters — an attacker with root access can read and modify anything.

**Tips:**
- Start by listing all users who have a login shell: `grep -v 'nologin\|false' /etc/passwd`
- Check which users have UID 0: `awk -F: '$3 == 0 {print $1}' /etc/passwd`
- Look at group memberships carefully — being in the `root` group gives read access to root-owned files
- The `sudo` configuration is in `/etc/sudoers` and `/etc/sudoers.d/` — check who can escalate
- SSH is often the primary entry point for attackers — review `/etc/ssh/sshd_config` for dangerous settings like `PermitRootLogin yes` or `PermitEmptyPasswords yes`
- Attackers plant SSH keys in `~/.ssh/authorized_keys` for persistent access — check **every user's** home directory
- Run `sudo ss -tlnp` to see every listening port — ask yourself: should each service be exposed?
- VPN tunnels (Tailscale, WireGuard, ngrok) bypass your firewall entirely — check for them with `systemctl list-units` and `ip link show`
- Set up a basic firewall: `sudo ufw default deny incoming && sudo ufw allow 22/tcp && sudo ufw allow 443/tcp && sudo ufw enable`

**Checklist:**
- [ ] Audit user accounts (`/etc/passwd`, `/etc/shadow`) — who can log in?
- [ ] Check for accounts with known/weak/empty passwords
- [ ] Check for unauthorized users in privileged groups (`/etc/group`) — especially `root` and `sudo`
- [ ] Audit sudo configuration (`/etc/sudoers`, `/etc/sudoers.d/`)
- [ ] Review SSH configuration (`/etc/ssh/sshd_config`)
  - [ ] Root login settings
  - [ ] Password authentication settings
  - [ ] Empty password settings
- [ ] Audit SSH authorized keys for all users (`~/.ssh/authorized_keys`)
- [ ] Check for unauthorized VPN tunnels or network services (`ss -tlnp`, `systemctl list-units`)
- [ ] Audit open ports and running services
- [ ] Set up a firewall (`ufw`)

---

### B. Web Server (nginx) Configuration

> **Review:** Slides 07-v2 (DoS, rate limiting), 09-v2 (firewalls, connection limits), session1 (reconnaissance), session2 (DoS lab), session6 (TLS & headers lab)

nginx is the front door to your application. Misconfigurations here expose information, enable DoS attacks, and weaken browser-side protections.

**Tips:**
- Check the HTTP response headers with `curl -skI https://192.168.8.147/` — the `Server` header often reveals the exact nginx version
- Browse to `/static/` and `/media/` — if you see a file listing, `autoindex` is on
- The `server_name` directive controls which hostnames the server accepts — `server_name _` means "accept anything", which enables host header injection attacks (review session1 slides for how password reset hijacking works)
- For DoS protection, you need timeouts AND limits: `client_header_timeout` kills slowloris, `client_body_timeout` kills slow POST, `limit_req_zone` stops flooding, `client_max_body_size` caps uploads
- Security headers tell the browser how to protect the user — missing headers mean the browser has no instructions and uses unsafe defaults
- `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true` means any website can make authenticated requests to your server and read the responses

**Checklist:**
- [ ] Server version disclosure in HTTP headers (`server_tokens off;`)
- [ ] Directory listing enabled on any paths (`autoindex off;`)
- [ ] `server_name` configuration (wildcard vs specific hostname)
- [ ] Client timeouts (`client_header_timeout`, `client_body_timeout`)
- [ ] Connection limits (`limit_conn`)
- [ ] Rate limiting (`limit_req_zone`)
- [ ] Upload size limits (`client_max_body_size`)
- [ ] Security headers:
  - [ ] `Strict-Transport-Security` (HSTS) — prevents SSL stripping
  - [ ] `X-Content-Type-Options` — prevents MIME sniffing
  - [ ] `Content-Security-Policy` — restricts script sources
  - [ ] `X-Frame-Options` — prevents clickjacking
  - [ ] `Referrer-Policy` — controls URL leakage
- [ ] CORS policy (`Access-Control-Allow-Origin` should NOT be `*`)

---

### C. Django Application — Information Disclosure

> **Review:** Slides 11-v2 (path traversal, canonicalization, input validation), session1 (reconnaissance lab)

Web applications often leak sensitive information through endpoints that were meant for development, or through insufficient input validation.

**Tips:**
- Try browsing to common debug paths: `/debug/`, `/admin/`, `/api/` — see what responds
- Look for API endpoints that return data without requiring authentication — try incrementing IDs (`?id=1`, `?id=2`, ...)
- Path traversal attacks use `../` sequences to escape the intended directory — try them in any parameter that takes a filename or path
- Check if there are any files in `/static/` that shouldn't be public (IP logs, backups, credentials)
- The Django debug page (when `DEBUG=True`) returns full tracebacks with local variable values including secrets

**Checklist:**
- [ ] Check for debug/diagnostic endpoints that expose sensitive data
- [ ] Check for API endpoints that dump user data without authentication
- [ ] Check for publicly accessible files containing sensitive information
- [ ] Check for path traversal vulnerabilities (e.g., `../` in parameters)
- [ ] Check for IDOR (Insecure Direct Object Reference) in API endpoints

---

### D. Django Application — Injection

> **Review:** Slides 11-v2 (SQL injection, command injection, parameterized queries, safe OS interaction), session3 (injection lab)

Injection is when user input is interpreted as code. The two most dangerous types here are SQL injection (user input in database queries) and OS command injection (user input in shell commands).

**Tips:**
- For SQL injection, look for any endpoint that takes a search query — try adding a single quote `'` and see if the behavior changes (error, different results, or no results)
- The key indicator of SQL injection is **raw SQL with string concatenation** instead of parameterized queries or Django ORM
- For command injection, look for any endpoint that interacts with the OS (ping, diagnostic, export) — try appending `;id` or `$(whoami)` to parameters
- The fix for SQL injection is always **parameterized queries** — never concatenate user input into SQL strings
- The fix for command injection is to avoid `shell=True` in subprocess, use `shlex.quote()`, or better yet, don't pass user input to the shell at all
- Also look inside the Python code for any use of `subprocess`, `os.system`, or `os.popen` with user-controlled data

**Checklist:**
- [ ] Test search/query endpoints for SQL injection (raw SQL vs ORM)
- [ ] Test for OS command injection in any endpoint that interacts with the system
- [ ] Review code for unsanitized user input passed to `subprocess`, `os.system`, or raw SQL
- [ ] Check for any code that writes user input to files that are later executed

---

### E. Django Application — CSRF & File Upload

> **Review:** Slides 11-v2 (XSS, CSRF, output encoding), session4 (XSS & CSRF lab)

CSRF (Cross-Site Request Forgery) tricks a logged-in user's browser into making requests they didn't intend. File uploads without validation can store malicious content.

**Tips:**
- In Django, the `@csrf_exempt` decorator removes CSRF protection — search the codebase for it with `grep -r "csrf_exempt"`
- Sensitive actions (voting, uploading, deleting) should require POST requests with a CSRF token — if they work via GET, that's a vulnerability
- Test file uploads: can you upload a `.html` file? A `.php` file? Is there any file type or size restriction?
- Check if uploaded filenames are sanitized — can you use `../../` in the filename?

**Checklist:**
- [ ] Check for endpoints with `@csrf_exempt`
- [ ] Check if sensitive actions (voting, uploading) accept GET requests
- [ ] Check file upload endpoints for type/size validation
- [ ] Check for filename sanitization on uploads

---

### F. Django Application — Authentication & Access Control

> **Review:** Slides 03-v2 (authentication, passwords, MFA), 04-v2 (access control models, RBAC, least privilege), session5 (auth & access lab)

Authentication answers "who are you?" and authorization answers "are you allowed to do this?" Getting either wrong means someone is where they shouldn't be.

**Tips:**
- **IDOR (Insecure Direct Object Reference):** Try accessing API endpoints with different ID values — can you see other users' data?
- **Broken logic:** Read the voting access control code carefully — look for conditions that are always true or always false (tautologies like `A or not A`, guards set to `False`)
- **Missing authorization:** Just because a view has `@login_required` doesn't mean it checks whether the *specific* logged-in user should be allowed — authentication is not authorization
- **Poll ownership:** How does the app track who created a poll? If it uses the session (client-side), an attacker can manipulate it. If it uses a database ForeignKey, it's server-side and trustworthy
- **Backdoor accounts:** Query the database for superusers — are they all legitimate? Check how accounts are created during startup
- **Session cookies:** Check the Django settings for `SESSION_COOKIE_HTTPONLY` (can JavaScript read the cookie?) and `SESSION_COOKIE_SECURE` (is it sent over HTTP?)
- **Password policy:** Can you create an account with password `1`? That means there are no password validators

**Checklist:**
- [ ] Check for broken access control on voting (private polls accessible without auth)
- [ ] Check if any user can perform admin-only actions (e.g., closing polls)
- [ ] Check how poll ownership is tracked (session vs database)
- [ ] Check for backdoor/default accounts in the Django admin
- [ ] Check session cookie security flags
- [ ] Check password validation requirements

---

### G. Django Settings

> **Review:** Slides 12-v2 (OS hardening principles — same principles apply to application config), session6 (Django settings slides)

Django's `settings.py` controls critical security behaviors. A single misconfigured setting can undo all your other fixes.

**Tips:**
- `DEBUG = True` exposes full tracebacks to the world — always `False` in production
- `SECRET_KEY` should never be hardcoded in source code — use `os.environ.get('DJANGO_SECRET_KEY')`. If the SECRET_KEY leaks, an attacker can forge session cookies
- `ALLOWED_HOSTS = ['*']` means Django accepts requests with any `Host` header — set it to your specific hostname
- `AUTH_PASSWORD_VALIDATORS = []` means any password is accepted — add Django's built-in validators (minimum length, common password check, numeric check)
- `SESSION_COOKIE_HTTPONLY = False` means JavaScript can read the session cookie (enables cookie theft via XSS)
- `SESSION_COOKIE_SECURE = False` means the cookie is sent over unencrypted HTTP
- `X_FRAME_OPTIONS = 'ALLOWALL'` enables clickjacking — set to `'DENY'`
- `DATA_UPLOAD_MAX_MEMORY_SIZE` at 100MB enables upload-based DoS — reduce to 2-5MB
- Credentials (database passwords, Redis passwords, API keys) should be in environment variables, not in the source code

**Checklist:**
- [ ] `DEBUG` setting
- [ ] `SECRET_KEY` (hardcoded vs environment variable)
- [ ] `ALLOWED_HOSTS`
- [ ] `AUTH_PASSWORD_VALIDATORS`
- [ ] `ACCOUNT_EMAIL_VERIFICATION`
- [ ] `SESSION_COOKIE_HTTPONLY`
- [ ] `SESSION_COOKIE_SECURE`
- [ ] `X_FRAME_OPTIONS`
- [ ] `DATA_UPLOAD_MAX_MEMORY_SIZE` / `FILE_UPLOAD_MAX_MEMORY_SIZE`
- [ ] Database and cache credentials (hardcoded vs environment variables)

---

### H. Chat System

> **Review:** Slides 11-v2 (XSS — reflected, stored, DOM-based; output encoding by context; CSP), session4 (XSS & CSRF lab)

The chat system has its own set of vulnerabilities because it processes user input and renders it in the browser for other users.

**Tips:**
- **Stored XSS:** Look at how chat messages are rendered in the template — if JavaScript builds HTML strings from user data and uses `innerHTML`, any message containing `<script>` tags will execute in every viewer's browser. The fix is to use `textContent` instead of `innerHTML`, or properly escape HTML
- **Username XSS:** The same issue applies to the online users list — if usernames are inserted via `innerHTML`, a malicious username like `<img src=x onerror="alert(1)">` will execute
- **Message spoofing:** Read the chat view code carefully — are there any hidden commands that let you send messages as another user?
- **Directory traversal:** The chat system uses a `room` parameter — is it validated? Can you use `../` to read or write files outside the intended directory?

**Checklist:**
- [ ] Check for XSS in chat messages (how are messages rendered in the browser?)
- [ ] Check for XSS via usernames in online user lists
- [ ] Check for message spoofing capabilities (hidden commands)
- [ ] Check for directory traversal in room/file parameters

---

## Report Format

Your report must include the following sections:

```
1. Executive Summary
   - Total vulnerabilities found
   - Breakdown by severity (Critical, High, Medium, Low)
   - Overall risk assessment

2. Methodology
   - Tools used
   - Approach (what you scanned, tested, reviewed)

3. Findings
   For each vulnerability:
   - Title
   - Severity (Critical / High / Medium / Low)
   - Category (Injection, Auth, Config, DoS, etc.)
   - Location (endpoint, file, line number, or config)
   - Description (what the vulnerability is)
   - Proof of Concept (how you confirmed it)
   - Remediation (how to fix it)

4. Fixes Applied
   - List of vulnerabilities you fixed
   - What you changed (file, config, code)
   - How you verified the fix

5. DoS Prevention (required — see below)

6. Recommendations
   - Any additional hardening suggestions
```

Save your report as: `report_LASTNAME.md`

---

## Report Submission — Encrypted with age

> **Review:** Slides 02-v2 (public key cryptography, asymmetric encryption, key management)

Your report must be encrypted so that **only the instructor** can read it. You will use `age`, a modern encryption tool that supports SSH public keys. This uses the same asymmetric encryption concepts from Session 2 — you encrypt with the instructor's **public** key, and only the instructor's **private** key can decrypt it.

### Step 1: Install age

```bash
# Debian/Ubuntu
sudo apt install age

# macOS
brew install age
```

### Step 2: Download the instructor's public keys

```bash
curl -s https://github.com/gtoscano.keys -o instructor_keys.txt
```

### Step 3: Encrypt your report

```bash
# Encrypt using the instructor's SSH public keys
age -R instructor_keys.txt -o report_LASTNAME.md.age report_LASTNAME.md
```

This produces `report_LASTNAME.md.age` — an encrypted file that only the instructor can decrypt with his private key.

### Step 4: Verify (optional)

You can verify the file is encrypted and no longer readable:

```bash
file report_LASTNAME.md.age
# Should show: "data" or "age encrypted file"

cat report_LASTNAME.md.age
# Should show binary/unreadable content
```

### Step 5: Submit

Submit **only** the encrypted file: `report_LASTNAME.md.age`

Do **NOT** submit the plaintext report.

---

## Rubric

| Criterion | Points | Description |
|---|---|---|
| **Vulnerability Discovery** | 40 | Identify at least 60% of the vulnerabilities (29 out of 47). Each correctly identified and documented vulnerability counts. Partial credit for partially described findings. |
| **Proof of Concept** | 15 | Provide evidence for each finding: commands run, screenshots, HTTP requests/responses, or code snippets showing the vulnerability. |
| **Remediation Applied** | 20 | Actually fix vulnerabilities on the system. Show before/after evidence (config diffs, code changes, re-test results). |
| **Report Quality** | 10 | Clear writing, proper structure (follows the format above), correct severity classifications, organized by category. |
| **Encryption & Submission** | 10 | Report is correctly encrypted with `age` using the instructor's public key. Instructor can decrypt it successfully. Plaintext is not submitted. |
| **Recommendations** | 5 | Additional hardening suggestions beyond the required fixes (e.g., monitoring, logging, firewall rules, automated scanning). |
| **Total** | **100** | |

### Grading Scale

| Grade | Score | Requirement |
|---|---|---|
| A | 90-100 | Found 60%+ vulnerabilities, fixed most, excellent report |
| B | 80-89 | Found 50%+ vulnerabilities, fixed several, good report |
| C | 70-79 | Found 40%+ vulnerabilities, fixed some, adequate report |
| D | 60-69 | Found 30%+ vulnerabilities, minimal fixes, weak report |
| F | < 60 | Insufficient findings, no fixes, or unencrypted submission |

### Automatic Deductions

| Issue | Deduction |
|---|---|
| Report submitted unencrypted (plaintext) | -10 points |
| Report cannot be decrypted by instructor | -10 points |
| No proof of concept for any finding | -10 points |
| Report does not follow required format | -5 points |

---

## Important: VM Resets Every 24 Hours

The target VM (`192.168.8.147`) is **restored to its original vulnerable state every 24 hours**. This means:

- All your fixes, configuration changes, and user modifications will be wiped.
- Every student gets a fresh, identical environment to work with.
- **Document everything as you go.** Save your fixes (diffs, config files, scripts) locally so you can reproduce them and include them in your report.
- Do not rely on changes persisting — take screenshots and copy outputs immediately.

---

## DoS Prevention (Required)

> **Review:** Slides 07-v2 (DoS/DDoS attacks, flooding, amplification, rate limiting, SYN cookies), 09-v2 (firewalls, connection limits, IPS), session2 (DoS lab)

As part of your report, you must include a dedicated section explaining how to **prevent Denial of Service attacks** against this system. Specifically, address the following attack vectors:

1. **Slowloris** — an attacker opens many connections and sends partial HTTP headers slowly, exhausting worker slots so legitimate users cannot connect.
   - *Hint:* Review `client_header_timeout` in the nginx docs and session2 slides. Think about what happens when a connection sits idle sending one header line every few seconds.

2. **HTTP Flood** — an attacker sends a high volume of requests as fast as possible, overwhelming the server with no rate limiting in place.
   - *Hint:* Review slide 07-v2 on rate limiting (token bucket, leaky bucket). In nginx, look at `limit_req_zone` and `limit_req`. Also consider `fail2ban` for IP-level blocking.

3. **Slow POST** — an attacker sends the POST request body one byte at a time, tying up server workers waiting for the full body.
   - *Hint:* Similar to Slowloris but targets the request body. Review `client_body_timeout` in nginx. What happens if you set it to 10 seconds?

4. **Large Upload Flood** — an attacker uploads very large files repeatedly, consuming disk space and bandwidth.
   - *Hint:* Review `client_max_body_size` in nginx AND `DATA_UPLOAD_MAX_MEMORY_SIZE` in Django settings. What is the current limit? What should it be?

For each attack vector, explain:
- How the attack works
- Why the current system is vulnerable to it
- What specific configuration changes (nginx, Django, OS-level) would mitigate it
- The exact directives or settings you would apply

---

## Rules of Engagement

1. Only test against the assigned target (`192.168.8.147`). Do not scan or attack any other systems.
2. Do not perform destructive attacks that render the system permanently unusable for other students. The VM resets every 24 hours, but be considerate of classmates working at the same time.
3. If you break something, notify the instructor. The VM will reset within 24 hours.
4. Document everything as you go — do not rely on memory or on changes persisting on the server.
5. Collaboration is allowed for discussing techniques, but each student must submit their own independent report.

---

## Useful Tools

| Tool | Purpose | Course Reference |
|---|---|---|
| `nmap` | Port scanning and service detection | Slides 08-v2, 09-v2 |
| `curl` / `wget` | Manual HTTP requests, header inspection | Session1, session6 |
| `nikto` | Automated web server vulnerability scanner | Session1 |
| `sqlmap` | SQL injection detection and exploitation | Slides 11-v2, session3 |
| `ss` / `netstat` | Check open ports and listening services | Slides 09-v2, 12-v2 |
| `fail2ban` | Automatic IP blocking on repeated failures | Slides 07-v2, session5 |
| `ufw` | Simple firewall management | Slides 09-v2 |
| Browser DevTools (F12) | Inspect requests, cookies, headers, DOM | Session4, session6 |
| `grep` / `find` | Search configuration files and source code | Throughout |
| `age` | Encrypt your final report | Slides 02-v2 |
| `openssl s_client` | Inspect TLS certificates and protocols | Slides 02-v2, session6 |
| `lynis` | Linux security auditing | Slides 12-v2 |

---

## Vulnerability Difficulty Guide

There are **47 vulnerabilities** across the system. Here is how they break down by difficulty:

### Easy (16 vulnerabilities) — findable with `curl`, browser, or basic config review

| # | Category | What to look for |
|---|---|---|
| 1 | Nginx | Server version in HTTP response headers |
| 2 | Nginx | Directory listing on `/static/` |
| 3 | Nginx | Directory listing on `/media/` |
| 4 | App | Debug endpoint leaking secrets |
| 5 | App | API endpoint that dumps all users without auth |
| 6 | App | Publicly accessible IP tracking file |
| 7 | App | Uploaded files directory browsable |
| 8 | App | Django admin panel accessible without restriction |
| 9 | App | File upload endpoint missing CSRF protection |
| 10 | App | Voting works via GET request without CSRF token |
| 11 | Headers | Missing `Strict-Transport-Security` |
| 12 | Headers | Missing `X-Content-Type-Options` |
| 13 | Headers | Missing `Content-Security-Policy` |
| 14 | Headers | `X-Frame-Options` set to `ALLOWALL` |
| 15 | Headers | Wildcard CORS (`Access-Control-Allow-Origin: *`) |
| 16 | Settings | `DEBUG = True` (visible from error pages) |

### Medium (18 vulnerabilities) — require testing inputs, reading settings, or targeted probing

| # | Category | What to look for |
|---|---|---|
| 17 | Nginx | Host header injection (`server_name _`) |
| 18 | App | IDOR — user data accessible by iterating IDs |
| 19 | App | Path traversal via `../` in a request parameter |
| 20 | App | SQL injection — try a single quote `'` in search fields |
| 21 | App | SQL injection — destructive queries (DELETE, UPDATE) |
| 22 | App | SQL injection — privilege escalation |
| 23 | App | OS command injection — append `;id` to a parameter |
| 24 | App | OS command injection — read system files |
| 25 | App | OS command injection — dump environment variables |
| 26 | Settings | `ALLOWED_HOSTS = ['*']` |
| 27 | Settings | Hardcoded `SECRET_KEY` in source code |
| 28 | Settings | No password validators (try creating account with password `1`) |
| 29 | Settings | Email verification disabled |
| 30 | Settings | `SESSION_COOKIE_HTTPONLY = False` |
| 31 | Settings | `SESSION_COOKIE_SECURE = False` |
| 32 | Settings | Hardcoded Redis credentials in settings |
| 33 | Settings | Upload size limit set to 100MB |
| 34 | DoS | No rate limiting, no connection limits, no timeouts |

### Hard (13 vulnerabilities) — require code review, OS auditing, or deep investigation

| # | Category | What to look for |
|---|---|---|
| 35 | App | Broken access control logic in voting (code has a tautology) |
| 36 | App | Missing authorization check on an admin-only action |
| 37 | App | Poll ownership tracked via session instead of database |
| 38 | Chat | Stored XSS — look at how messages are rendered in JavaScript |
| 39 | Chat | XSS via usernames in the online users list |
| 40 | Chat | Hidden command that lets you impersonate other users |
| 41 | Chat | Directory traversal in a chat parameter |
| 42 | Code | User input written to a shell script and executed |
| 43 | OS | A system account with root-level access it shouldn't have |
| 44 | OS | Root account has a known password |
| 45 | OS | A regular user can escalate to root |
| 46 | OS | SSH allows login without a password |
| 47 | OS | An unauthorized network tunnel bypasses the firewall |

### Strategy

- **Start with Easy** — these are quick wins and will get you to 16 findings fast
- **Then Medium** — these require more testing but the checklist tips point you in the right direction
- **Then Hard** — these require reading source code and auditing the OS; tackle them last
- Finding all Easy + all Medium = **34 vulnerabilities** (72%) — already above the 60% threshold for full credit

---

## Quick Start Guide

If you're not sure where to begin, follow this order:

1. **Scan the target** — `nmap -sV -sC 192.168.8.147` to see what's running
2. **Check HTTP headers** — `curl -skI https://192.168.8.147/` to see what's exposed
3. **Browse the app** — explore every page, every form, every URL
4. **Check the OS** — SSH in, audit users, groups, services, SSH config
5. **Read the code** — look at `views.py`, `settings.py`, nginx config, templates
6. **Test for injection** — try special characters in every input field and URL parameter
7. **Document as you go** — don't wait until the end to write your report

Good luck.
