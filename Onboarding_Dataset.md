# Acme Corp — Employee Onboarding Knowledge Base (Sample)

> This is an illustrative onboarding document for a **fictional company "Acme Corp"** so the RAG pipeline has something to retrieve against. Replace this file with your own organization's onboarding docs to point the assistant at your workplace.

---

## 1. HR / Payroll

| Topic | Detail |
|------|--------|
| HRIS Portal | Acme People Portal — used for personal data, benefits, leave requests, pay stubs. |
| Payroll Cycle | Monthly; salary disbursed on the last working day of the month. |
| Time Submission | Daily timesheet entry via Acme Time Tracker. |
| Retirement Plan | Acme offers a regional retirement plan (401(k) / EPF equivalent) — enroll via the People Portal. |
| Tax & Bank Setup | Submit tax declarations and bank details within the first 5 working days. |

### Leave & Attendance
- **Annual leave:** 2 days accrued per month (24 days per year).
- **Planned PTO:** Submit at least two weeks in advance and notify your manager.
- **Sick leave:** Notify your manager via the team chat before start of the workday and log in the portal.
- **Core hours:** 10:00 AM – 4:00 PM in your local time zone.

### Performance Reviews
- Quarterly check-ins with your manager.
- Annual review drives salary adjustments and promotion progression.
- Metrics include task delivery, code-review quality, and certification progress.

---

## 2. IT / Equipment

### Initial Setup
- Standard laptop + external monitor, mouse, keyboard.
- Change the temporary password to a strong unique one (14+ chars).
- **Two-factor authentication is mandatory** via the company-approved authenticator app.
- VPN is required for accessing internal systems or client environments.

### Acceptable Use
- No personal software installs.
- No personal data storage on company devices.
- Never upload client code or internal documents to personal cloud accounts.
- Limit browsing to job-related tasks.

### Troubleshooting
- **VPN issues:** Restart, clear VPN cache, then contact the IT helpdesk channel.
- **Build server access denied:** Usually missing RBAC — ask your tech lead.
- **High-severity issues:** IT helpdesk will escalate to the IT manager.

---

## 3. Engineering / Tech

### Environment
- Visual Studio 2022 + VS Code as primary IDEs.
- Check the project's `global.json` / `package.json` for SDK versions.
- After cloning a repo, run the full build and the existing unit-test suite.

### Code Quality
- Coding standards are documented in the engineering wiki.
- Mandatory documentation comments (XML docs for C#, JSDoc for JS/TS).
- Write unit tests for every new feature or bug fix.
- Raise technical-debt tickets instead of doing unscoped refactors.

### Git Workflow
- Feature-branch model: `feature/T-XXXX-short-description`.
- Small, logical, frequent commits.
- All merges via Pull Request, linked to a task ID, reviewed by a Tech Lead.
- You are accountable for keeping CI/CD green after your merges.
- AI-assistant code (Copilot etc.) is allowed; you remain accountable for every line.

---

## 4. Delivery / Project

- **Methodology:** Two-week sprints tracked on the engineering project board.
- **Daily standup:** 15 min — yesterday, today, blockers.
- **Definition of blocker:** anything stopping productive work for 30+ minutes. Report immediately.
- **Client communication:** Never commit to scope or timelines without your Project Manager.
- **Project handoff:** PM + Tech Lead provide the project overview and first 30-day tasks.

---

## 5. Learning / Certification

- **0–90 days:** complete the mandatory cloud-fundamentals certification.
- **3–9 months:** pursue an associate-level certification matched to your role.
- Company covers the cost of pre-approved exams.
- One weekly hour is reserved for individual learning.
- You'll be paired with a peer Buddy and assigned a direct Manager.

---

## 6. General / Culture

### Communication
- Teams / Slack channels for everyday communication.
- Email for formal communication and external client correspondence.

### Escalation
- **L1:** Buddy, Tech Lead, IT Helpdesk.
- **L2:** Direct Manager, Project Manager, HR Business Partner.
- **L3:** Senior Directors / Heads of Departments.

### Values
- Engineering excellence, client partnership, continuous learning.
- Ask for help early. Report blockers — don't sit idle.
- Pre-approve expenses with your manager; file claims within 10 days.

### Quick FAQ

| Question | Answer |
|---|---|
| How many leaves per month? | 2 days/month, 24 days/year. |
| Can I install personal software on my laptop? | No, strictly prohibited. |
| Who assigns my tasks? | Your Project Manager and Tech Lead during sprint planning. |
| Where do I report a blocker? | Immediately in the team channel, then formally in the daily standup. |
| When do I get a salary review? | At the annual review, based on performance, certifications, and role proficiency. |
