"""Guards that must hold for the whole code base: read-only, no keys, no outside scripts, no fake results."""

import ast
import re
from pathlib import Path

from launchlab.providers import solana_rpc

ROOT = Path(__file__).resolve().parent.parent
SOURCE = [p for p in (ROOT / "launchlab").rglob("*") if p.suffix in {".py", ".js", ".html", ".css"}]

# Identifiers that only appear in code that signs, submits or executes transactions, or handles keys.
FORBIDDEN = [
    r"sendTransaction", r"sendRawTransaction", r"simulateTransaction", r"signTransaction", r"signAllTransactions", r"signMessage",
    r"requestAirdrop", r"\bKeypair\b", r"secret[_ ]?key", r"private[_ ]?key", r"\bmnemonic\b", r"seed[_ ]phrase",
    r"from_secret", r"from_seed", r"wallet[-_ ]adapter", r"window\.solana", r"\bphantom\b", r"\bjito\b.*send", r"sendBundle",
    r"\bswap\s*\(", r"place_order", r"submit_order", r"execute_trade", r"\bsolders\b", r"\bsolana\.keypair\b", r"\bnacl\b", r"ed25519",
]
ALLOWED_LINES = (
    "private key or seed phrase",          # the package docstring saying it handles none
    "wallet, private key",                 # same, wrapped differently
)


def test_source_files_exist():
    assert len(SOURCE) >= 15


def test_no_signing_sending_or_key_handling_code_anywhere():
    hits = []
    for path in SOURCE:
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if any(a in line for a in ALLOWED_LINES):
                continue
            for pattern in FORBIDDEN:
                if re.search(pattern, line, re.IGNORECASE):
                    hits.append(f"{path.relative_to(ROOT)}:{n}: {pattern}")
    assert hits == []


def test_rpc_allowlist_is_read_only():
    expected = {"getAccountInfo", "getBlock", "getBlockTime", "getHealth", "getMinimumBalanceForRentExemption", "getMultipleAccounts",
                "getSignaturesForAddress", "getSlot", "getTokenAccountsByOwner", "getTokenLargestAccounts", "getTokenSupply", "getTransaction"}
    assert set(solana_rpc.READ_METHODS) == expected
    assert all(m.startswith("get") for m in solana_rpc.READ_METHODS)


def test_no_third_party_runtime_dependencies_and_no_dynamic_code():
    pyproject = (ROOT / "pyproject.toml").read_text()
    assert re.search(r"^dependencies = \[\]", pyproject, re.MULTILINE)
    allowed = {"launchlab", "__future__", "argparse", "base64", "bisect", "collections", "concurrent", "dataclasses", "datetime", "hashlib", "http",
               "json", "math", "os",
               "pathlib", "random", "re", "sqlite3", "struct", "sys", "threading", "time", "typing", "urllib"}
    for path in (ROOT / "launchlab").rglob("*.py"):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [] if node.level else [(node.module or "").split(".")[0]]   # relative imports are local by definition
            else:
                modules = []
            assert set(modules) <= allowed, f"{path.name}: imports {modules}"
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in {"eval", "exec", "compile", "__import__"}, f"{path.name}: calls {node.func.id}"


def test_dashboard_loads_nothing_from_outside_and_never_injects_html():
    for name in ("index.html", "app.js", "styles.css"):
        text = (ROOT / "launchlab" / "static" / name).read_text()
        outside = [u for u in re.findall(r"https?://[^\s\"'`)]+", text) if "www.w3.org/2000/svg" not in u]
        assert outside == [], f"{name} references {outside}"
        assert "innerHTML" not in text and "outerHTML" not in text and "document.write" not in text and "eval(" not in text
    html = (ROOT / "launchlab" / "static" / "index.html").read_text()
    assert "SYNTHETIC DEMO DATA" in html and "No wallet is connected" in html and "style=" not in html


def test_env_example_asks_for_no_secret_and_gitignore_protects_local_state():
    env = (ROOT / ".env.example").read_text()
    keys = [line.split("=")[0] for line in env.splitlines() if line and not line.startswith("#")]
    assert keys and not any(re.search(r"KEY|SECRET|TOKEN|PASSWORD|PRIVATE|MNEMONIC|WALLET", k) for k in keys)
    assert "LAUNCHLAB_MODE=demo" in env
    ignore = (ROOT / ".gitignore").read_text().split()
    assert ".env" in ignore and "data/" in ignore
    assert not (ROOT / ".env").exists()


def test_no_hard_coded_outcomes_or_success_claims_in_code():
    text = "\n".join(p.read_text(encoding="utf-8") for p in SOURCE)
    for phrase in ("guaranteed", "win rate of", "profit of $", "x from the alert", "passive income", "buy now", "strong buy"):
        assert phrase not in text.lower(), phrase
    # the three audited mints must not be baked into the application as examples or fixtures
    audited = ("CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump", "2TngN4B7XaoGSKsYvttq5bFAdM4Z4xCSnuyRwGiFpump",
               "FJKt1LxbWBpTRt9BaDEB6Wr2qL5LZzjFF5sx8rXnpump")
    for mint in audited:
        assert mint not in text
