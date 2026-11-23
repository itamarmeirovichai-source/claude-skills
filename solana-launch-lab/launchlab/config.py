"""Settings from the environment (and an optional local `.env`). No secret is required to run."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_RPC = "https://api.mainnet-beta.solana.com"

# A Solana address is 32 bytes in base58: 32-44 characters from this alphabet.
MINT_RE = re.compile(r"[1-9A-HJ-NP-Za-km-z]{32,44}")
SYNTHETIC_PREFIX = "SYNTH"


def is_valid_mint(value: str) -> bool:
    # fullmatch, not match: `$` would accept a trailing newline
    return bool(MINT_RE.fullmatch(value or ""))


def is_synthetic_mint(value: str) -> bool:
    return (value or "").startswith(SYNTHETIC_PREFIX)


def load_dotenv(path: Path) -> dict[str, str]:
    """Minimal KEY=VALUE reader. Lines starting with # and blank lines are ignored."""
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def redact_url(url: str) -> str:
    """Hide anything in a URL that could be a credential (userinfo, path token, query string)."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return "<unparseable url>"
    host = parts.hostname or "?"
    return f"{parts.scheme}://{host}/…" if (parts.query or parts.username or len(parts.path) > 1) else f"{parts.scheme}://{host}"


@dataclass(frozen=True)
class PaperConfig:
    size_sol: float = 0.5
    latency_s: float = 8.0
    decision_delay_s: float = 90.0
    max_wait_s: float = 180.0
    fail_prob: float = 0.15
    max_attempts: int = 3
    retry_delay_s: float = 4.0
    base_fee_sol: float = 0.000005
    priority_fee_sol: float = 0.0005
    tip_sol: float = 0.0
    token_account_rent_sol: float = 0.0015
    extra_slippage_bps: float = 100.0
    max_pool_share: float = 0.02
    min_exit_liquidity_sol: float = 1.0
    max_fill_staleness_s: float = 120.0
    venue_fee_override: float | None = None  # set to replace the fee-tier table (what-if runs, tests)
    seed: int = 20261123


@dataclass(frozen=True)
class Settings:
    mode: str = "demo"
    host: str = "127.0.0.1"
    port: int = 8765
    db_path: Path = PROJECT_ROOT / "data" / "launchlab.sqlite3"
    solana_rpc_url: str = PUBLIC_RPC
    store_raw: dict[str, bool] = field(
        default_factory=lambda: {"solana_rpc": True, "dexscreener": False, "geckoterminal": False}
    )
    conflict_tolerance: float = 0.05
    stale_after_s: dict[str, float] = field(
        default_factory=lambda: {"dexscreener": 300.0, "geckoterminal": 300.0, "solana_rpc": 120.0}
    )
    paper: PaperConfig = field(default_factory=PaperConfig)

    @property
    def live_enabled(self) -> bool:
        return self.mode == "live"

    def public_dict(self) -> dict:
        """Settings safe to show in the UI or a log (RPC URL redacted)."""
        d = asdict(self)
        d["db_path"] = str(self.db_path)
        d["solana_rpc_url"] = redact_url(self.solana_rpc_url)
        return d

    def config_hash(self) -> str:
        """Stable hash of everything that affects simulated results."""
        payload = {"paper": asdict(self.paper), "conflict_tolerance": self.conflict_tolerance}
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]


def _flag(env: dict[str, str], key: str, default: bool) -> bool:
    raw = env.get(key)
    return default if raw is None else raw.strip().lower() in {"1", "true", "yes", "on"}


def _num(env: dict[str, str], key: str, default: float) -> float:
    raw = env.get(key)
    if raw is None or raw == "":
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(f"{key} must be a number, got {raw!r}") from exc


def load_settings(env: dict[str, str] | None = None, dotenv_path: Path | None = None) -> Settings:
    merged: dict[str, str] = {}
    merged.update(load_dotenv(dotenv_path if dotenv_path is not None else PROJECT_ROOT / ".env"))
    merged.update(os.environ if env is None else env)

    mode = merged.get("LAUNCHLAB_MODE", "demo").strip().lower()
    if mode not in {"demo", "live"}:
        raise ValueError("LAUNCHLAB_MODE must be 'demo' or 'live'")
    host = merged.get("LAUNCHLAB_HOST", "127.0.0.1").strip()
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("LAUNCHLAB_HOST must be a loopback address; this tool is local-only")
    db_raw = merged.get("LAUNCHLAB_DB", "")
    db_path = Path(db_raw) if db_raw else PROJECT_ROOT / "data" / "launchlab.sqlite3"
    if not db_path.is_absolute():
        db_path = PROJECT_ROOT / db_path
    defaults = PaperConfig()
    paper = PaperConfig(
        size_sol=_num(merged, "PAPER_SIZE_SOL", defaults.size_sol),
        latency_s=_num(merged, "PAPER_LATENCY_S", defaults.latency_s),
        decision_delay_s=_num(merged, "PAPER_DECISION_DELAY_S", defaults.decision_delay_s),
        fail_prob=_num(merged, "PAPER_FAIL_PROB", defaults.fail_prob),
        priority_fee_sol=_num(merged, "PAPER_PRIORITY_FEE_SOL", defaults.priority_fee_sol),
        extra_slippage_bps=_num(merged, "PAPER_EXTRA_SLIPPAGE_BPS", defaults.extra_slippage_bps),
        seed=int(_num(merged, "PAPER_SEED", defaults.seed)),
    )
    if not 0 <= paper.fail_prob < 1:
        raise ValueError("PAPER_FAIL_PROB must be in [0, 1)")
    if paper.size_sol <= 0:
        raise ValueError("PAPER_SIZE_SOL must be positive")
    return Settings(
        mode=mode,
        host=host,
        port=int(_num(merged, "LAUNCHLAB_PORT", 8765)),
        db_path=db_path,
        solana_rpc_url=merged.get("SOLANA_RPC_URL", PUBLIC_RPC).strip() or PUBLIC_RPC,
        store_raw={
            "solana_rpc": _flag(merged, "STORE_RAW_SOLANA_RPC", True),
            "dexscreener": _flag(merged, "STORE_RAW_DEXSCREENER", False),
            "geckoterminal": _flag(merged, "STORE_RAW_GECKOTERMINAL", False),
        },
        paper=paper,
    )
