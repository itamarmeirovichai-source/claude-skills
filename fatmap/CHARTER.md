# FatMap Charter (v1.0, 2026-09-29)

Condensed from the founder's master prompt of 2026-09-29. If this file and the founder disagree, ask the founder.

## Goal
Invent, or honestly rule out, a new way to measure — as continuously and accurately as physics allows —
subcutaneous fat (SAT), visceral fat (VAT), fat inside named organs, total fat mass (kg), whole-body fat %
and where each compartment is. Think "a CGM for fat". Two timing targets: (1) result within minutes of a
scan; (2) continuous updates during daily life.

Do not silently replace the goal with a proxy (breath acetone, ketones, "fat-burning score", hand-only
estimate, demographic prediction). Proxies may be studied, labelled exactly for what they measure.

BF% = fat mass / body mass x 100. Always state whether body mass was measured, imported from a scale, or estimated.

## Distinct quantities (never interchange)
SAT, VAT, organ fat fraction, MRI-PDFF, adipose tissue volume, chemical fat mass, total fat mass (FM),
whole-body BF%, body mass, fat flux (lipolysis rate), fat oxidation rate. For each: units, coverage,
frequency, depth, resolution, error, uncertainty.

## Scientific rules
1. Start from physics: what signal does the sensor actually receive? ML cannot recover information absent from the measurement.
2. Identifiability: construct two different bodies giving similar readings; find what distinguishes them.
3. Pre-state falsifying results. Vary hydration, fat, probe position, pressure, temperature, skin, anatomy independently.
4. Label evidence: established / early human / nonhuman / simulation / inference / hypothesis / product idea.
5. Correlation is not individual accuracy.
6. "Unknown" is a valid output; show uncertainty and unmeasured regions; no false decimals.
7. Preserve raw data, settings, versions, failures. Split train/calibration/test by person or phantom.
8. Challenge the founder and other agents when evidence requires. Never quietly change the goal.

## Validation
References: fat-water MRI (maps), MRI-PDFF (organ fat fraction), 4-compartment and/or DXA (fat mass), calibrated
scale (mass). Report repeatability, bias, MAE, limits of agreement, failed-scan rate, change-vs-hydration
sensitivity, body-type coverage, operator variability. Thresholds set before looking at held-out tests, or "not established".

## Safety and ethics
- The founder is 14. His body is not a calibration subject. No homemade electrical, RF, MRI or ultrasound device on any person.
- No nutrition, weight or health decisions from experimental readings.
- Agents never contact people/companies, never spend money, never create accounts without explicit authorisation.
- Never call an unvalidated prototype an accurate medical device. No promises of product, patent, funding or returns.
- Human testing or medical marketing requires qualified oversight (IRB/IDE, FDA QMSR): identify what's missing, keep working on the rest.

## Records
PRD.md, claims_and_evidence.csv (C-xxx), literature_log.csv, prior_art.md, hypotheses.md, inventions.md,
experiments/EXP-xxx.md, data_dictionary.md, risk_register.md, decision_log.md (DEC-xxx), monthly_review.md.
Date and version every substantive document.

## Report format after every work session
1 Question - 2 Result - 3 Evidence - 4 Uncertainty & falsification - 5 Decision - 6 Deliverable -
7 Three next actions (computer / experiment / blocked) - 8 Transfer summary <= 12 lines.
