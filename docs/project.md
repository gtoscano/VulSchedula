# Midterm Project: Vulnerability Analysis of VulSchedula

Dear Students,

For the midterm project, you will work **in teams of three** to analyze **VulSchedula**, an intentionally insecure Django-based scheduling application designed for educational purposes.

Your objective is to **identify and analyze vulnerabilities**, understand how they can be exploited, and explain the associated security risks.

---

# Access to the System

For those who encountered difficulties creating containers previously, I have prepared one for you.

You can access it from the **third floor** by connecting to the **OpenWrt5g network** or **NachoWIFI5**

Please visit my office or ask anyone in **Pangborn 308** for the network password.

Connect **only** to the following machine:

```

192.168.2.77

```

Please **do not attempt to access or interfere with other devices**.

Login credentials:

Username:
```

gtoscano

```

The password will be provided in person.

---

# Code Injection Demonstration

To test code injection, a file named `echo_upper_case.txt` is provided.

The code included in the poll’s description field launches a server that converts received messages to uppercase.

You can verify this behavior from another computer using:

```

echo "Hello World!" | ncat 192.168.X.X 8000

```

Replace `192.168.X.X` with the IP address where VulSchedula is running.

If the injection works correctly, you should receive:

```

HELLO WORLD!

```

---

# Tasks

## Task 1 — Security Audit

Identify and document **at least three distinct vulnerabilities** in the application.

For each vulnerability explain:

- Where it appears in the system
- Why it is dangerous
- What type of vulnerability it represents
- The potential impact of exploitation

---

## Task 2 — Exploitation

Demonstrate at least **one working exploit**.

For example, you may:

- Execute injected code
- Recover credentials
- Access restricted functionality

Provide a **step-by-step explanation** of how the exploit works.

---

# Additional Things to Investigate

Some elements of the system were intentionally hidden.

## Hidden Superusers

There are **two secret superuser accounts** in the system.

One is intentionally easier to find than the other.

Your task is to determine:

- Where these accounts were created
- Why this represents a security risk

---

## Behavior Switching Code

There is a section of code that allows **switching between different injected behaviors**, such as:

- sending email notifications
- converting strings to uppercase

Find where this logic exists and explain how it works.

---

## HTTPS Fixed Strings

The code contains **hardcoded strings related to HTTPS configuration**.

Evaluate the risks associated with reusing fixed secrets or certificates in deployed systems.

---

# Optional Challenge (Extra Credit)

If you would like an additional challenge, you may attempt to **secure the system**.

For any vulnerability you identify:

- Propose a fix
- Show how the code could be modified to mitigate the issue
- Explain why the fix improves security

This portion is **optional**, but strong implementations may receive **extra credit**.

---

# Deliverables

Each team must submit:

## 1. Security Report

A document describing:

- The vulnerabilities discovered
- Exploitation methods
- Security implications

## 2. Exploit Demonstration

Evidence that at least one vulnerability can be exploited.

This may include:

- command sequences
- screenshots
- logs
- explanation of the attack process

---

# Grading Rubric

| Category | Description | Points |
|--------|-------------|-------|
| Vulnerability Identification | Correct identification and explanation of vulnerabilities (minimum of three) | 40 |
| Exploitation | Demonstration of at least one working exploit with clear explanation | 30 |
| Quality of Analysis | Depth of understanding, security reasoning, and clarity of explanations | 20 |
| Report Quality | Organization, readability, and professionalism of the report | 10 |

**Total: 100 points**

---

# Extra Credit

Additional points may be awarded for:

- Identifying more than three vulnerabilities
- Successfully securing parts of the system
- Providing particularly insightful security analysis

---

# Deadline

The deadline for submission is **two weeks after the assignment date**, at **9:00 PM**.

---

Best regards,

Gregorio Toscano  
Assistant Professor  
Department of Computer Science  
The Catholic University of America
