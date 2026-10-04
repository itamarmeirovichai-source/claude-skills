"""Every tunable number in one place, so calibration never edits code."""

from __future__ import annotations

from dataclasses import dataclass, field, fields, replace

# Forms that indicate news (an explanation for unusual volume).
NEWS_FORMS = frozenset({"8-K", "6-K", "10-Q", "10-K", "20-F", "40-F", "PR", "NEWS"})

# Forms that put new shares into the market or register them for resale.
DILUTION_FORMS = frozenset(
    {"S-1", "S-1/A", "S-3", "S-8", "F-1", "F-3", "424B3", "424B4", "424B5", "1-A", "253G2", "D"}
)

RED_FLAG_TITLE_WORDS = (
    "name change",
    "change in control",
    "change of control",
    "reverse split",
    "reverse stock split",
    "custodian",
    "custodianship",
    "share issuance",
    "convertible note",
    "new business direction",
    "artificial intelligence",
    " ai ",
    "crypto",
    "blockchain",
)


@dataclass(frozen=True)
class Config:
    # S1 abnormal volume without news
    vol_lookback: int = 60
    vol_min_history: int = 20
    vol_ratio_trigger: float = 5.0
    vol_ratio_full: float = 50.0
    news_window_days: int = 1

    # S2 quiet accumulation
    acc_window: int = 20
    acc_min_gain: float = 0.30
    acc_min_up_share: float = 0.55
    acc_min_volume_ratio: float = 1.5
    acc_max_single_day: float = 0.25

    # S3 suspicious filings
    filing_lookback_days: int = 120
    dormant_gap_days: int = 365

    # S4 hype burst
    mention_baseline_days: int = 30
    mention_min_count: int = 5
    mention_ratio_trigger: float = 5.0
    hype_min_avg: float = 0.35

    # S5 coordinated promotion
    coord_window_days: int = 3
    coord_similarity: float = 0.6
    coord_min_authors: int = 3

    # S6 broker flow
    flow_min_new_buyers: int = 20
    flow_ratio_trigger: float = 5.0

    # S7 victim reports
    report_window_days: int = 14

    # Scoring
    weights: dict[str, float] = field(
        default_factory=lambda: {
            "S1_abnormal_volume": 0.20,
            "S2_quiet_accumulation": 0.10,
            "S3_suspicious_filings": 0.15,
            "S4_hype_burst": 0.15,
            "S5_coordinated_promotion": 0.20,
            "S6_broker_flow": 0.15,
            "S7_victim_reports": 0.05,
        }
    )
    signal_memory_days: int = 5
    alert_threshold: float = 35.0
    min_families: int = 2
    cooldown_days: int = 10

    def with_(self, **changes) -> "Config":
        return replace(self, **changes)

    @classmethod
    def field_names(cls) -> set[str]:
        return {f.name for f in fields(cls)}
