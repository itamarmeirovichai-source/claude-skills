# Shared brief for all PumpWatch market teams (internal working file)

PumpWatch (working name): early-warning engine that joins PUBLIC social-media / Telegram signals with market data
(price/volume) and SEC filings (EDGAR) to warn broker-dealers, trading apps, exchanges and banks about
social-media-driven pump-and-dump / "ramp-and-dump" schemes in small-cap stocks BEFORE the dump.
Signals: S1 abnormal volume without news; S2 quiet accumulation; S3 suspicious filings (offerings, name change, control change);
S4 social-mention spike + hype language; S5 identical text / repeat promoters; S6 many new small buyers (needs broker data);
S7 victim reports. Red lines: no fake identities to join closed groups, no WhatsApp scraping, no hacking/buying access,
no trading on alerts, data minimisation.
Founder: solo, Israel-based, ~$30k budget to first paying customer. Gate A = customer pain (>=3/10 calls score pain 4-5, >=1 pilot)
+ backtest on paper (signals visible >=2 days before collapse in >=10/20 cases).

House rules:
- Honesty before enthusiasm. EVERY number/claim needs a source URL inline. If not confirmed from a source you actually
  opened/searched, label it **UNVERIFIED**. Never invent URLs, customers, funding or prices.
- Plain, concise English. Markdown tables welcome.
- Company level only — never personal names, emails or phone numbers of employees.
- Date today: 2026-10-04. Note date of sources where relevant; flag stale info (>2 years old).
- Web access: WebSearch and WebFetch tools work. curl works for most sites; sec.gov needs a User-Agent header with contact info.
- Write ONLY inside /home/user/claude-skills/pumpwatch/research/. Do not git commit or push (the department head does that).
