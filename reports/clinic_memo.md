# Memo: Where to Spend Our Security Budget

**To:** Practice leadership, Lakeview Family Medicine *(fictional 40-person clinic in Central New York)*\
**From:** Tim, security analyst\
**Date:** October 10, 2026\
**Re:** What 8,013 reported healthcare breaches say about our top three risks

---

## Bottom line

Fund three things this year: stronger email and login security, protection for our network server and backups, and a review of the vendors who handle our patient data. Underneath all three, we need a documented risk analysis, which is the first thing federal investigators ask for after a breach. The first item costs about **$3,840 a year**; the others are mostly staff time plus quotes from our IT provider.

## What the data shows

From every breach of 500+ patients reported to HHS since 2009 ([full analysis](https://notkornflakes.github.io/hhs-breach-analysis/)):

- **Hackers, not lost laptops, are now the threat.** Hacking was involved in 81% of 2025 breaches, up from 4% in 2010.
- **Network servers are the most common and the most damaging target.** 46% of breaches involved a network server, with a median of 9,967 patients affected, about three times the median for email breaches.
- **Vendors are involved in more than a third of breaches.** Breaches involving a business associate (billing, IT, EHR and similar vendors) rose from 23% in 2010–2014 to 35% in 2021–2025.
- **New York is average, not safe.** The state ranks 26th of 51 for breaches per resident, and its breaches involve hacking more often than the national pattern (63.7% vs 58.5%).

## Recommendations

| Priority | What we do | Cost | Risk it addresses |
|---|---|---|---|
| 1. Email and logins | Upgrade Microsoft 365 from Business Standard to Business Premium. Turn on multi-factor authentication for every account, phishing filtering, and managed devices. | ~$3,840/year (40 users × $8/month difference) | Phishing and stolen passwords, the usual way hackers get in |
| 2. Server and backups | Patch and restrict remote access to the server, encrypt patient data, and keep offline backups we test by restoring quarterly. | Quote from IT provider | The largest breaches, plus ransomware downtime |
| 3. Vendors | List every vendor that touches patient data, confirm a current business associate agreement, and require MFA, encryption, and prompt breach notice. | Staff time (~20 hours) | Breaches that happen outside our own network |
| Foundation | Complete and document a risk analysis every year, with owners and deadlines for each fix. | Staff time, or an outside assessment | Federal penalties after any breach |

## Why now

- **Breaches are expensive.** The average healthcare breach cost $6.64 million in IBM's 2026 study. That average comes mostly from large organizations, so ours would likely cost less, but notification, downtime, and legal costs add up quickly for a small practice.
- **Regulators fine small practices too.** In March 2026, a small New York neurology practice paid $25,000 and accepted two years of federal monitoring after a ransomware attack, over a missing risk analysis.
- **These controls are likely to become required.** Proposed HIPAA Security Rule changes would make MFA and encryption mandatory. The rule isn't final yet, but acting now puts us ahead of it.

---

*Sources: HHS OCR breach portal (downloaded Oct 10, 2026); IBM Cost of a Data Breach Report 2026; HHS press release on Comprehensive Neurology, PC (March 2026); Microsoft 365 pricing effective July 1, 2026; HHS proposed HIPAA Security Rule (January 2025).*
