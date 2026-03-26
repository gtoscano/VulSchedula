
# Linux Incident Response Challenge

Over the next **three weeks**, you will develop and execute the first phase of this exercise in a hostile Linux environment. You are part of a response team assigned to a system that hosts a Django-based web application. The system is experiencing abnormal behavior, and your job is to investigate, stabilize the service, and determine what is happening.

## Overall mission

Your team must operate in a hostile environment, defend the system, and coordinate under uncertainty. You should assume that the environment may already be compromised and that not every user, message, or action is trustworthy.

## First objective for this phase

The **first task** is to establish **secure communication** within your team.

You must assume that:

* the environment is hostile
* the red team may impersonate another user
* messages may be intercepted, altered, or forged
* usernames alone are not proof of identity

The **only thing you know for sure** is each teammate’s **GitHub account identity**. For the purpose of this exercise, you may assume that **GitHub accounts cannot be hacked or impersonated**.

Your team is responsible for determining how to communicate under these conditions.

## Your objectives

You must:

* establish secure communication within your team
* keep the web application available or restore its availability
* investigate suspicious activity on the system
* analyze logs and available evidence
* identify suspicious accounts, actions, or patterns
* apply reasonable defensive measures
* document your findings and actions

## Environment

You will be given access to a Linux system that includes:

* a running Django application
* a web server and application service
* system logs
* authentication logs
* network and process information
* user accounts and system configuration
* a chat system integrated into the platform

Assume that the environment is already hostile. Do not assume that all accounts, activity, messages, or behavior are trustworthy.

## Rules of communication

You are **not supposed to talk among yourselves directly**. All coordination must happen **only through the chat system provided in the platform**.

You must also assume that the chat is:

* monitored
* wired
* part of a hostile environment


## Rules of engagement

You may:

* inspect logs, services, processes, network connections, users, groups, and configuration
* apply defensive changes intended to restore or protect service
* use standard administrative and investigative commands available in the environment
* communicate with teammates only through the provided system chat

You may not:

* communicate with teammates by speaking, texting, emailing, or using any channel outside the provided chat
* destroy the system or intentionally make the service permanently unavailable
* erase evidence or remove logs
* assume that any account or message is legitimate without verification

## Deliverables

At the end of this phase, your team must submit:

1. a brief description of how you handled communication in the hostile environment
2. a summary of suspicious activity or risks identified so far
3. any defensive actions already taken
4. the evidence you relied on
5. recommendations for the next phase of the exercise

## Evaluation

You will be evaluated on:

* your ability to operate under adversarial conditions
* the quality of your investigation
* the quality of your evidence and reasoning
* your ability to stabilize or defend the service
* the clarity of your written report
* the discipline and professionalism of your coordination

## Final instruction

Treat this as a real incident in a compromised environment. Trust evidence over assumptions. Verify before acting. Communicate carefully, because the red team may observe, imitate, or manipulate what you see.
