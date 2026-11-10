"""Reconciliation harness (protocol §5.1–5.2, overlay §4 integrity checks).

Inputs (CSV, UTF-8, header row):
  shopify_orders.csv : order_id, created_at (YYYY-MM-DD), gross_usd, status (paid|refunded|cancelled|test), tags
  payouts.csv        : order_id, payout_date, net_usd, currency_rate (ILS per USD used by the processor), fee_usd
  refunds.csv        : order_id, refund_date, amount_usd, kind (refund|chargeback)
  meta_purchases.csv : date, purchases, spend_usd   (Meta's dashboard, secondary only)
Output: one period summary and a list of integrity findings. Exit code 2 if a planted/undetected
problem remains, so a CI-style run fails loudly.

Integrity checks (every run):
  1. duplicate order ids in any file
  2. orders with status test or tag 'test'/'staff' are excluded
  3. an order with no payout within 45 days is flagged (a planted fake order must land here)
  4. a payout with no matching order is flagged (leak from another store or a typo)
  5. a payout dated before its order is flagged (future leak)
  6. refunds and chargebacks are applied to the period of the refund date, not the order date
  7. revenue is the processor's net in USD, at the processor's rate; gross is shown alongside
  8. Meta's purchases are reported next to reconciled orders, never used as the count

Plain-language: the harness is a checklist that runs the same way every day, so a number only counts
after it survived these eight questions. The operator runs it by hand first (runbook daily-numbers.md).
Run on synthetic data:  python3 -I dropshipping/phase3/reconcile.py --selftest
Run on real exports:    python3 -I dropshipping/phase3/reconcile.py --dir path/to/exports --period 2026-12
"""
import csv, sys, os, argparse, datetime as dt, random, tempfile
from collections import Counter, defaultdict

def read(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def d(s):
    return dt.date.fromisoformat(s)

def reconcile(dirpath, period):
    orders = read(os.path.join(dirpath, 'shopify_orders.csv'))
    payouts = read(os.path.join(dirpath, 'payouts.csv'))
    refunds = read(os.path.join(dirpath, 'refunds.csv'))
    meta = read(os.path.join(dirpath, 'meta_purchases.csv'))
    findings = []
    # 1 duplicates
    for name, rows in (('orders', orders), ('payouts', payouts)):
        dup = [k for k, c in Counter(r['order_id'] for r in rows).items() if c > 1]
        if dup: findings.append(f"DUPLICATE {name}: {dup}")
    # 2 exclude test/staff
    real = [o for o in orders if o['status'] != 'test' and not ({'test', 'staff'} & set(t.strip() for t in o.get('tags', '').split(';') if t))]
    excluded = len(orders) - len(real)
    by_id = {o['order_id']: o for o in real}
    pay_by_id = defaultdict(list)
    for p in payouts: pay_by_id[p['order_id']].append(p)
    # 3 no payout within 45 days (planted fake order lands here)
    today = max([d(p['payout_date']) for p in payouts] + [d(o['created_at']) for o in orders])
    for o in real:
        if o['status'] == 'paid' and not pay_by_id.get(o['order_id']):
            age = (today - d(o['created_at'])).days
            findings.append(f"NO PAYOUT {o['order_id']} (age {age}d){' <- not yet due' if age < 45 else ' <- SUSPECT: no processor record'}")
    # 4 payout without order
    for p in payouts:
        if p['order_id'] not in by_id: findings.append(f"ORPHAN PAYOUT {p['order_id']}")
    # 5 payout before order (future leak)
    for p in payouts:
        o = by_id.get(p['order_id'])
        if o and d(p['payout_date']) < d(o['created_at']): findings.append(f"FUTURE LEAK payout {p['order_id']} dated before order")
    # period sums
    in_period = lambda s: s[:7] == period
    gross = sum(float(o['gross_usd']) for o in real if in_period(o['created_at']) and o['status'] in ('paid', 'refunded'))
    net = sum(float(p['net_usd']) for p in payouts if p['order_id'] in by_id and in_period(p['payout_date']))
    fees = sum(float(p['fee_usd']) for p in payouts if p['order_id'] in by_id and in_period(p['payout_date']))
    # 6 refunds to refund period
    ref = sum(float(r['amount_usd']) for r in refunds if in_period(r['refund_date']) and r['kind'] == 'refund')
    cb = sum(float(r['amount_usd']) for r in refunds if in_period(r['refund_date']) and r['kind'] == 'chargeback')
    orders_n = sum(1 for o in real if in_period(o['created_at']) and o['status'] in ('paid', 'refunded'))
    spend = sum(float(m['spend_usd']) for m in meta if in_period(m['date']))
    meta_purch = sum(int(m['purchases']) for m in meta if in_period(m['date']))
    reconciled_rev = net - ref - cb
    roas = reconciled_rev / spend if spend else float('nan')
    summary = dict(period=period, orders=orders_n, excluded_test_or_staff=excluded, gross_usd=round(gross, 2), processor_net_usd=round(net, 2),
                   fees_usd=round(fees, 2), refunds_usd=round(ref, 2), chargebacks_usd=round(cb, 2), reconciled_revenue_usd=round(reconciled_rev, 2),
                   meta_spend_usd=round(spend, 2), reconciled_roas=round(roas, 3), meta_reported_purchases=meta_purch,
                   meta_vs_shopify_orders_ratio=round(meta_purch / orders_n, 2) if orders_n else None)
    return summary, findings

def make_synthetic(dirpath, seed=7, n=40, plant=True):
    rnd = random.Random(seed)
    start = dt.date(2026, 12, 1)
    orders, payouts, refunds, meta = [], [], [], []
    for i in range(n):
        day = start + dt.timedelta(days=rnd.randint(0, 27))
        gross = round(rnd.choice([34.9, 39.9, 44.9]), 2)
        oid = f"#{1001+i}"
        status = 'paid'
        tags = ''
        if i == 3: status, tags = 'test', 'test'
        if i in (10, 11): status = 'refunded'
        orders.append(dict(order_id=oid, created_at=day.isoformat(), gross_usd=gross, status=status, tags=tags))
        if status != 'test':
            lag = rnd.randint(1, 21)
            fee = round(gross * 0.034 + 0.38 + gross * 0.02, 2)
            payouts.append(dict(order_id=oid, payout_date=(day + dt.timedelta(days=lag)).isoformat(), net_usd=round(gross - fee, 2), currency_rate=3.17, fee_usd=fee))
        if status == 'refunded':
            refunds.append(dict(order_id=oid, refund_date=(day + dt.timedelta(days=rnd.randint(5, 25))).isoformat(), amount_usd=gross, kind=rnd.choice(['refund', 'chargeback'])))
    if plant:
        # planted fake order: appears in Shopify export, no processor record, 50 days old
        orders.append(dict(order_id='#9999', created_at=(start - dt.timedelta(days=22)).isoformat(), gross_usd=44.9, status='paid', tags=''))
        # planted future leak: payout dated before its order
        orders.append(dict(order_id='#9998', created_at='2026-12-20', gross_usd=39.9, status='paid', tags=''))
        payouts.append(dict(order_id='#9998', payout_date='2026-12-18', net_usd=37.0, currency_rate=3.17, fee_usd=2.9))
        # planted duplicate
        payouts.append(dict(payouts[0]))
    for day in range(28):
        meta.append(dict(date=(start + dt.timedelta(days=day)).isoformat(), purchases=rnd.choice([0, 1, 1, 2, 2, 3]), spend_usd=20.0))
    for name, rows in (('shopify_orders.csv', orders), ('payouts.csv', payouts), ('refunds.csv', refunds), ('meta_purchases.csv', meta)):
        with open(os.path.join(dirpath, name), 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--dir'); ap.add_argument('--period', default='2026-12'); ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        with tempfile.TemporaryDirectory() as td:
            make_synthetic(td, plant=True)
            s, f = reconcile(td, '2026-12')
            print('SUMMARY', s); print('FINDINGS'); [print(' ', x) for x in f]
            must = ['SUSPECT', 'FUTURE LEAK', 'DUPLICATE']
            caught = all(any(m in x for x in f) for m in must)
            print('planted problems caught:', caught)
            # placebo: same run without plants must produce no SUSPECT/LEAK/DUPLICATE findings
            make_synthetic(td, plant=False)
            s2, f2 = reconcile(td, '2026-12')
            clean = not any(any(m in x for x in f2) for m in must)
            print('placebo clean:', clean, '| placebo findings:', f2)
            sys.exit(0 if caught and clean else 2)
    else:
        s, f = reconcile(a.dir, a.period)
        print('SUMMARY', s); print('FINDINGS'); [print(' ', x) for x in f]
        sys.exit(2 if any('SUSPECT' in x or 'LEAK' in x or 'DUPLICATE' in x for x in f) else 0)
