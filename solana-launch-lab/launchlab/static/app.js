/* Solana Launch Lab dashboard. Vanilla JS, no dependencies.
   Every value that comes from data is inserted with textContent — never as HTML. */
"use strict";

const $ = (sel) => document.querySelector(sel);
const SVG = "http://www.w3.org/2000/svg";
const state = { status: null, view: "tokens", mint: null, asOf: null, book: "demo" };

function h(tag, attrs, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === "class") el.className = v;
    else if (k === "text") el.textContent = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v === true ? "" : v);
  }
  for (const c of children.flat()) if (c !== null && c !== undefined && c !== false) el.append(c.nodeType ? c : document.createTextNode(String(c)));
  return el;
}
function s(tag, attrs, text) {
  const el = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs || {})) el.setAttribute(k, v);
  if (text !== undefined) el.textContent = text;
  return el;
}
const unknown = (why) => h("span", { class: "unknown", title: why || "not available from the data sources" }, "unknown");
const fmtTime = (t) => (t == null ? null : new Date(t * 1000).toISOString().replace("T", " ").replace(/\.\d+Z$/, "Z"));
function fmtNum(x, digits = 2) {
  if (x == null || Number.isNaN(x)) return null;
  const a = Math.abs(x);
  if (a !== 0 && a < 0.001) return x.toExponential(3);
  if (a >= 1e9) return (x / 1e9).toFixed(2) + "B";
  if (a >= 1e6) return (x / 1e6).toFixed(2) + "M";
  if (a >= 1e4) return (x / 1e3).toFixed(1) + "K";
  return x.toLocaleString("en-US", { maximumFractionDigits: digits, minimumFractionDigits: a < 10 ? Math.min(digits, 2) : 0 });
}
const fmtPct = (x, d = 1) => (x == null ? null : (x * 100).toFixed(d) + "%");
const fmtSol = (x, d = 4) => (x == null ? null : (x >= 0 ? "+" : "−") + Math.abs(x).toFixed(d) + " SOL");
const short = (a) => (a && a.length > 16 ? a.slice(0, 6) + "…" + a.slice(-6) : a);
function fmtAge(seconds) {
  if (seconds == null) return null;
  if (seconds < 90) return Math.round(seconds) + " s";
  if (seconds < 5400) return Math.round(seconds / 60) + " min";
  if (seconds < 172800) return (seconds / 3600).toFixed(1) + " h";
  return Math.round(seconds / 86400) + " d";
}
const cell = (value, cls) => h("td", { class: cls || "" }, value == null ? unknown() : value);

async function api(path, body) {
  const opts = body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  const res = await fetch(path, opts);
  const data = await res.json().catch(() => ({ error: "the server returned something that is not JSON" }));
  if (!res.ok) throw new Error(data.error || "request failed (" + res.status + ")");
  return data;
}
function setMessage(id, text, isError) {
  const el = $(id);
  el.textContent = text || "";
  el.classList.toggle("error", Boolean(isError));
}
function showBanner(synthetic) { $("#synthetic-banner").hidden = !synthetic; }

/* ---------- tooltip ---------- */
const tip = $("#tooltip");
function showTip(evt, strong, sub) {
  tip.replaceChildren(h("b", { text: strong }), sub || "");
  tip.hidden = false;
  const x = Math.min(evt.clientX + 14, window.innerWidth - tip.offsetWidth - 8);
  tip.style.left = x + "px";
  tip.style.top = evt.clientY + 14 + "px";
}
const hideTip = () => { tip.hidden = true; };

/* ---------- charts ---------- */
function lineChart(points, opts) {
  // points: [{x, y}] sorted by x. opts: {yLabel, xFmt, yFmt, markers:[{x,label}], asOf, title}
  const hasMarkers = Boolean(opts.markers && opts.markers.length);
  const W = 760, H = hasMarkers ? 270 : 240, m = { l: 62, r: 14, t: hasMarkers ? 54 : 18, b: 26 };
  const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, class: "chart", role: "img", "aria-label": opts.title });
  if (points.length < 2) { svg.append(s("text", { x: W / 2, y: H / 2, "text-anchor": "middle" }, "not enough data points to draw")); return svg; }
  const xs = points.map((p) => p.x), ys = points.map((p) => p.y);
  const x0 = Math.min(...xs), x1 = Math.max(...xs);
  let y0 = Math.min(...ys, opts.zero ? 0 : Infinity), y1 = Math.max(...ys, opts.zero ? 0 : -Infinity);
  if (y0 === y1) { y0 -= Math.abs(y0) * 0.1 || 1; y1 += Math.abs(y1) * 0.1 || 1; }
  const pad = (y1 - y0) * 0.06; y0 -= opts.zero ? pad : Math.min(pad, y0 > 0 ? y0 : pad); y1 += pad;
  const X = (x) => m.l + ((x - x0) / (x1 - x0 || 1)) * (W - m.l - m.r);
  const Y = (y) => H - m.b - ((y - y0) / (y1 - y0)) * (H - m.t - m.b);
  for (let i = 0; i <= 3; i++) {
    const yv = y0 + ((y1 - y0) * i) / 3;
    svg.append(s("line", { x1: m.l, x2: W - m.r, y1: Y(yv), y2: Y(yv), class: "gridline" }));
    svg.append(s("text", { x: m.l - 6, y: Y(yv) + 4, "text-anchor": "end" }, opts.yFmt(yv)));
  }
  if (opts.zero) svg.append(s("line", { x1: m.l, x2: W - m.r, y1: Y(0), y2: Y(0), class: "axis" }));
  svg.append(s("text", { x: m.l, y: H - 6 }, opts.xFmt(x0)));
  svg.append(s("text", { x: W - m.r, y: H - 6, "text-anchor": "end" }, opts.xFmt(x1)));
  svg.append(s("text", { x: m.l, y: 11 }, opts.yLabel));
  svg.append(s("path", { class: "line", d: points.map((p, i) => (i ? "L" : "M") + X(p.x).toFixed(1) + " " + Y(p.y).toFixed(1)).join(" ") }));
  // event markers: labels sit in up to three rows above the plot so neighbours never overprint
  let lastX = -Infinity, row = 0;
  for (const mk of (opts.markers || []).filter((k) => k.x >= x0 && k.x <= x1).sort((a, b) => a.x - b.x)) {
    row = X(mk.x) - lastX < 90 ? (row + 1) % 3 : 0;
    lastX = X(mk.x);
    const labelY = 24 + row * 12, right = X(mk.x) > W - 110;
    svg.append(s("line", { x1: X(mk.x), x2: X(mk.x), y1: labelY + 3, y2: H - m.b, class: "marker" }));
    svg.append(s("text", { x: X(mk.x) + (right ? -4 : 4), y: labelY, class: "marker-label", "text-anchor": right ? "end" : "start" }, mk.label));
  }
  if (opts.asOf != null && opts.asOf < x1) {
    svg.append(s("rect", { x: X(opts.asOf), y: m.t, width: W - m.r - X(opts.asOf), height: H - m.t - m.b, class: "shade" }));
    svg.append(s("line", { x1: X(opts.asOf), x2: X(opts.asOf), y1: m.t, y2: H - m.b, class: "asof" }));
    svg.append(s("text", { x: X(opts.asOf) + 4, y: H - m.b - 5, class: "marker-label" }, "not yet known →"));
  }
  const cross = s("line", { y1: m.t, y2: H - m.b, class: "cross", visibility: "hidden" });
  const dot = s("circle", { r: 4.5, class: "dot", visibility: "hidden" });
  const hit = s("rect", { x: m.l, y: m.t, width: W - m.l - m.r, height: H - m.t - m.b, fill: "transparent", tabindex: 0 });
  const at = (evt) => {
    const box = svg.getBoundingClientRect();
    const xv = x0 + (((evt.clientX - box.left) / box.width) * W - m.l) / (W - m.l - m.r) * (x1 - x0);
    let best = points[0];
    for (const p of points) if (Math.abs(p.x - xv) < Math.abs(best.x - xv)) best = p;
    cross.setAttribute("x1", X(best.x)); cross.setAttribute("x2", X(best.x)); cross.setAttribute("visibility", "visible");
    dot.setAttribute("cx", X(best.x)); dot.setAttribute("cy", Y(best.y)); dot.setAttribute("visibility", "visible");
    showTip(evt, opts.yFmt(best.y), opts.xFmt(best.x) + (best.note ? " · " + best.note : ""));
  };
  hit.addEventListener("pointermove", at);
  hit.addEventListener("pointerleave", () => { cross.setAttribute("visibility", "hidden"); dot.setAttribute("visibility", "hidden"); hideTip(); });
  svg.append(cross, dot, hit);
  return svg;
}
function barChart(rows, title) {
  // rows: [{label, count}] in a fixed order; one series, so no legend.
  const W = 760, H = 220, m = { l: 14, r: 14, t: 22, b: 34 };
  const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, class: "chart", role: "img", "aria-label": title });
  const max = Math.max(1, ...rows.map((r) => r.count));
  const slot = (W - m.l - m.r) / rows.length;
  svg.append(s("line", { x1: m.l, x2: W - m.r, y1: H - m.b, y2: H - m.b, class: "axis" }));
  rows.forEach((r, i) => {
    const bh = (r.count / max) * (H - m.t - m.b);
    const x = m.l + i * slot + 6, w = slot - 12, y = H - m.b - bh;
    if (r.count > 0) {
      const bar = s("path", { class: "bar", tabindex: 0, d: `M${x} ${H - m.b} V${y + 4} Q${x} ${y} ${x + 4} ${y} H${x + w - 4} Q${x + w} ${y} ${x + w} ${y + 4} V${H - m.b} Z` });
      const show = (evt) => showTip(evt.clientX ? evt : { clientX: 40, clientY: 40 }, r.count + " position" + (r.count === 1 ? "" : "s"), "net return " + r.label);
      bar.addEventListener("pointermove", show); bar.addEventListener("focus", show);
      bar.addEventListener("pointerleave", hideTip); bar.addEventListener("blur", hideTip);
      svg.append(bar);
    }
    svg.append(s("text", { x: x + w / 2, y: y - 5, "text-anchor": "middle", class: "bar-label" }, String(r.count)));
    svg.append(s("text", { x: x + w / 2, y: H - m.b + 15, "text-anchor": "middle" }, r.label));
  });
  return svg;
}

/* ---------- status / header ---------- */
async function loadStatus() {
  const st = await api("/api/status");
  state.status = st;
  $("#notice").textContent = st.notice;
  const pill = $("#mode-pill");
  pill.textContent = st.live_enabled ? "LIVE MODE · read-only public data" : "DEMO MODE · no network calls";
  const chain = $("#chain-pill");
  chain.textContent = st.event_log.ok ? `event log intact · ${st.event_log.count} entries` : `EVENT LOG BROKEN at entry ${st.event_log.first_bad_id}`;
  chain.classList.toggle("pill-bad", !st.event_log.ok);
  for (const id of ["#fetch-live", "#discover-live"]) {
    $(id).disabled = !st.live_enabled;
    $(id).title = st.live_enabled ? "Read-only requests to public data providers" : "Live connectors are off. Start with --live or LAUNCHLAB_MODE=live.";
  }
  return st;
}

/* ---------- tokens ---------- */
function badge(isSynthetic) {
  return isSynthetic ? h("span", { class: "badge badge-synthetic", text: "SYNTHETIC" }) : h("span", { class: "badge badge-live", text: "LIVE DATA" });
}
async function loadTokens() {
  const q = $("#search-input").value.trim(), scope = $("#scope-select").value;
  const data = await api(`/api/tokens?scope=${encodeURIComponent(scope)}&q=${encodeURIComponent(q)}`);
  const table = $("#tokens-table");
  table.replaceChildren(h("thead", {}, h("tr", {}, ["Source", "Symbol", "Mint", "Launch (UTC)", "Launch time source", "Observations", "Last data (UTC)", "Paper decision"].map((t) => h("th", { text: t })))));
  const body = h("tbody");
  for (const t of data.tokens) {
    body.append(h("tr", { class: "clickable", tabindex: 0, onclick: () => openToken(t.mint), onkeydown: (e) => { if (e.key === "Enter") openToken(t.mint); } },
      h("td", {}, badge(t.is_synthetic)), cell(t.symbol), h("td", { class: "mono", title: t.mint, text: short(t.mint) }),
      cell(fmtTime(t.launch_time), "mono"), cell(t.launch_source), h("td", { class: "num", text: t.n_obs }), cell(fmtTime(t.last_observed), "mono"), cell(t.decision)));
  }
  table.append(body);
  showBanner(data.tokens.some((t) => t.is_synthetic));
  setMessage("#tokens-message", data.tokens.length ? `${data.tokens.length} token(s) shown. Search matches an exact mint only.` :
    (q ? "This exact mint is not in the local store. In live mode, use “Fetch live public data”." : "No tokens stored yet."));
  return data;
}
function marketTable(d) {
  const now = d.token.is_synthetic ? null : d.now;
  const head = ["Provider", "Venue", "Price", "FDV", "Market cap", "Liquidity", "24h volume", "Observed (UTC)", "Data age", "Flags"];
  const rows = d.market.map((o) => {
    const p = o.payload, flags = [];
    if (o.is_synthetic) flags.push("synthetic");
    if (o.stale) flags.push("stale");
    if (o.missing.length) flags.push("missing: " + o.missing.join(", "));
    const withDef = (v, def) => (v == null ? h("td", { class: "num" }, unknown(def)) : h("td", { class: "num" }, v, h("span", { class: "def", text: def || "" })));
    return h("tr", {}, cell(o.provider), cell(p.venue === "curve" ? "bonding curve" : p.venue === "pool" ? "AMM pool" : null),
      withDef(p.price_sol == null ? (p.price_usd == null ? null : "$" + fmtNum(p.price_usd, 8)) : fmtNum(p.price_sol, 10) + " SOL", p.price_usd == null ? "" : "$" + fmtNum(p.price_usd, 8)),
      withDef(p.fdv_usd == null ? null : "$" + fmtNum(p.fdv_usd), p.fdv_definition),
      withDef(p.market_cap_usd == null ? null : "$" + fmtNum(p.market_cap_usd), p.market_cap_definition),
      withDef(p.liquidity_usd == null ? null : "$" + fmtNum(p.liquidity_usd), p.liquidity_definition || p.reserve_model),
      cell(p.volume_24h_usd == null ? null : "$" + fmtNum(p.volume_24h_usd), "num"), cell(fmtTime(o.observed_at), "mono"),
      cell(now == null ? "synthetic clock" : fmtAge(now - o.observed_at)), h("td", {}, flags.length ? flags.map((f) => h("span", { class: "badge badge-flag", text: f })) : "—"));
  });
  return h("div", { class: "table-wrap" }, h("table", { class: "data" }, h("thead", {}, h("tr", {}, head.map((t) => h("th", { text: t })))),
    h("tbody", {}, rows.length ? rows : h("tr", {}, h("td", { colspan: head.length }, unknown("no market observation stored at this point in time"))))));
}
function levelChip(c) {
  const map = { high: ["level-high", "HIGH"], elevated: ["level-elevated", "ELEVATED"], low: ["level-low", "NO FLAG"], "n/a": ["level-na", "UNKNOWN"] };
  const [cls, label] = map[c.level] || map["n/a"];
  return h("span", { class: "level " + cls, text: label });
}
function riskPanel(r) {
  const sum = r.summary;
  const comps = r.components.map((c) => h("div", { class: "component" },
    h("div", {}, levelChip(c), h("div", { class: "component-name", text: c.name })),
    h("div", {}, h("ul", {}, c.evidence.map((e) => h("li", { text: e }))), c.note ? h("p", { class: "note", text: c.note }) : null,
      h("p", { class: "meta", text: `status: ${c.status} · confidence: ${c.confidence} · source: ${c.source || "—"} · observed: ${fmtTime(c.observed_at) || "—"}` }))));
  return h("div", { class: "panel" },
    h("div", { class: "panel-head" }, h("h2", { text: "Risk components" }),
      h("span", { class: "muted", text: `${sum.high} high · ${sum.elevated} elevated · ${sum.low} no flag · ${sum.unknown} unknown · ${fmtPct(sum.completeness, 0)} of checks computable` })),
    h("p", { class: "muted", text: r.disclaimer }), comps);
}
function signalPanel(d) {
  const blocks = d.signals.map((sg) => {
    const pos = d.positions.find((p) => p.signal_id === sg.id);
    const kv = h("dl", { class: "kv" },
      h("dt", { text: "Book" }), h("dd", { text: sg.book }), h("dt", { text: "Decision" }), h("dd", { text: sg.decision.toUpperCase() + " · ruleset " + sg.ruleset }),
      h("dt", { text: "Decided as of" }), h("dd", { class: "mono", text: fmtTime(sg.as_of) }),
      h("dt", { text: "Reasons" }), h("dd", {}, sg.reasons.length ? h("ul", {}, sg.reasons.map((x) => h("li", { text: x }))) : "all structural checks passed (this is not a buy signal)"),
      h("dt", { text: "Features hash" }), h("dd", { class: "mono", text: sg.features_hash.slice(0, 24) + "…" }));
    if (pos) {
      kv.append(h("dt", { text: "Paper position" }), h("dd", { text: `${pos.status}${pos.exit_reason ? " — " + pos.exit_reason : ""}` }),
        h("dt", { text: "Cost / proceeds" }), h("dd", { class: "mono", text: `${pos.cost_sol.toFixed(4)} SOL / ${pos.proceeds_sol.toFixed(4)} SOL` }),
        h("dt", { text: "Gross / fees / net" }), h("dd", { class: "mono", text: `${fmtSol(pos.gross_pnl_sol)} / ${pos.fees_sol.toFixed(4)} SOL / ${fmtSol(pos.net_pnl_sol)}` }));
      for (const f of pos.fills) kv.append(h("dt", { text: "Fill · " + f.side }), h("dd", { text: `${fmtTime(f.filled_at)} · ${fmtNum(f.price_sol, 10)} SOL/token · model: ${f.model}` }));
    }
    return kv;
  });
  return h("div", { class: "panel" }, h("h2", { text: "Signals and paper position" }),
    blocks.length ? blocks : h("p", { class: "muted", text: "No signal recorded for this token yet. Run “Update paper book”." }));
}
async function openToken(mint, asOf) {
  state.mint = mint; state.asOf = asOf ?? null;
  const d = await api(`/api/token?mint=${encodeURIComponent(mint)}` + (state.asOf ? `&as_of=${state.asOf}` : ""));
  const t = d.token, box = $("#token-detail");
  showBanner(t.is_synthetic);
  const markers = [];
  if (t.launch_time) markers.push({ x: t.launch_time, label: "launch" });
  for (const sg of d.signals) markers.push({ x: sg.as_of, label: sg.decision === "candidate" ? "decision" : "rejected" });
  for (const p of d.positions) for (const f of p.fills) markers.push({ x: f.filled_at, label: f.side === "buy" ? "paper buy" : "paper sell" });
  const chart = lineChart(d.series.map((p) => ({ x: p.t, y: p.price_sol, note: p.provider })), {
    title: "Price in SOL over time", yLabel: "price (SOL per token)", xFmt: fmtTime, yFmt: (v) => fmtNum(v, 10), markers, asOf: state.asOf });
  const range = d.time_range;
  const slider = range && range.last > range.first ? h("input", { type: "range", min: range.first, max: range.last, step: 1, value: state.asOf ?? range.last, "aria-label": "Replay: show only what was known at this time" }) : null;
  const readout = h("span", { class: "mono", text: state.asOf ? "as of " + fmtTime(state.asOf) : "showing all stored data" });
  if (slider) {
    slider.addEventListener("input", () => { readout.textContent = "as of " + fmtTime(Number(slider.value)); });
    slider.addEventListener("change", () => openToken(mint, Number(slider.value) >= range.last ? null : Number(slider.value)));
  }
  box.replaceChildren(...[
    h("div", { class: "panel" },
      h("div", { class: "panel-head" }, h("h2", {}, badge(t.is_synthetic), " ", t.name || t.symbol || "unnamed token"), h("button", { class: "btn", onclick: () => { box.hidden = true; state.mint = null; } }, "Close")),
      h("dl", { class: "kv" }, h("dt", { text: "Mint" }), h("dd", { class: "mono", text: t.mint }), h("dt", { text: "Symbol" }), h("dd", {}, t.symbol || unknown()),
        h("dt", { text: "Creator" }), h("dd", { class: "mono" }, t.creator || unknown("creation transaction not read")),
        h("dt", { text: "Launch (UTC)" }), h("dd", {}, t.launch_time ? fmtTime(t.launch_time) + " — " + (t.launch_source || "") : unknown()),
        h("dt", { text: "Token program" }), h("dd", {}, t.token_program || unknown()))),
    h("div", { class: "panel" }, h("div", { class: "panel-head" }, h("h2", { text: "Price history and replay" }), readout), chart,
      slider ? h("div", { class: "replay" }, h("span", { class: "muted", text: "Replay: what was known at…" }), slider,
        h("button", { class: "btn", onclick: () => openToken(mint, null) }, "Show all")) : null,
      h("p", { class: "muted", text: "Moving the slider recomputes the risk components and the table below from observations stored up to that moment only. The price line itself is drawn in full so you can see where the cut is." })),
    h("div", { class: "panel" }, h("h2", { text: "Market observations" + (state.asOf ? " (as of replay time)" : "") }), marketTable(d)),
    riskPanel(d.risk), signalPanel(d),
    d.conflicts.length ? h("div", { class: "panel" }, h("h2", { text: "Provider disagreements" }), h("div", { class: "table-wrap" }, h("table", { class: "data" },
      h("thead", {}, h("tr", {}, ["Field", "Provider A", "Value A", "Provider B", "Value B", "Difference", "Observed (UTC)"].map((x) => h("th", { text: x })))),
      h("tbody", {}, d.conflicts.map((c) => h("tr", {}, cell(c.field), cell(c.provider_a), cell(fmtNum(c.value_a, 8), "num"), cell(c.provider_b), cell(fmtNum(c.value_b, 8), "num"), cell(fmtPct(c.rel_diff), "num"), cell(fmtTime(c.observed_at), "mono"))))))) : null].filter(Boolean));
  box.hidden = false;
  box.scrollIntoView({ behavior: "smooth", block: "start" });
}

/* ---------- paper ---------- */
const tile = (k, v, sub, cls) => h("div", { class: "tile " + (cls || "") }, h("div", { class: "k", text: k }), h("div", { class: "v" }, v == null ? unknown() : v), sub ? h("div", { class: "s", text: sub }) : null);
async function loadPaper() {
  const d = await api(`/api/paper?book=${state.book}`), m = d.metrics, body = $("#paper-body");
  showBanner(d.uses_synthetic_tokens);
  $("#demo-reset").hidden = state.book !== "demo";
  const ci = m.expectancy_ci ? `${(m.ci_confidence * 100).toFixed(1)}% interval ${fmtPct(m.expectancy_ci[0])} … ${fmtPct(m.expectancy_ci[1])}` : "interval needs at least 2 resolved positions";
  const tiles = h("div", { class: "tiles" },
    tile("Verdict", m.verdict, m.verdict_note, "verdict"),
    tile("Signals recorded", m.signals, `${m.candidates} candidates · ${m.rejected} rejected`),
    tile("Positions resolved", m.resolved, `${m.open} open · ${m.unsellable} unsellable`),
    tile("Failed attempts", m.failed_attempts, `${m.partial_fills} partial fills`),
    tile("Gross PnL", fmtSol(m.gross_pnl_sol), "price effect incl. impact, before fees"),
    tile("Fees and costs", m.fees_sol.toFixed(4) + " SOL", "venue fees, network fees, rent"),
    tile("Net PnL", fmtSol(m.net_pnl_sol), "resolved positions only"),
    tile("Expectancy per candidate", fmtPct(m.expectancy), ci),
    tile("Win rate", fmtPct(m.win_rate), m.avg_win == null ? "" : `avg win ${fmtPct(m.avg_win)} · avg loss ${fmtPct(m.avg_loss)}`),
    tile("Max drawdown", m.max_drawdown_sol.toFixed(4) + " SOL", "of cumulative net PnL"),
    tile("Exposure", m.exposure_sol_hours.toFixed(2) + " SOL·h", `peak concurrent ${m.peak_concurrent_capital_sol.toFixed(2)} SOL`),
    tile("Open positions", fmtSol(m.open_marked_to_last_sol), `at last price · ${fmtSol(m.open_marked_to_zero_sol)} at zero`));
  const reasons = Object.entries(m.rejection_reasons);
  const ledgerHead = ["Decided (UTC)", "Token", "Decision", "Reasons", "Position", "Cost SOL", "Proceeds SOL", "Net SOL", "Exit"];
  const ledger = d.ledger.slice().reverse().map((r) => h("tr", { class: "clickable", tabindex: 0, onclick: () => { switchView("tokens"); openToken(r.mint); } },
    cell(fmtTime(r.as_of), "mono"), h("td", {}, r.is_synthetic ? h("span", { class: "badge badge-synthetic", text: "SYN" }) : h("span", { class: "badge badge-live", text: "LIVE" }), " ", r.symbol || short(r.mint)),
    cell(r.decision), h("td", { text: r.reasons.map((x) => x.split(":")[0]).join(", ") || "—" }), cell(r.status || (r.decision === "candidate" ? "pending data" : "—")),
    cell(r.cost_sol == null ? "—" : r.cost_sol.toFixed(4), "num"), cell(r.proceeds_sol == null ? "—" : r.proceeds_sol.toFixed(4), "num"),
    cell(r.net_pnl_sol == null ? "—" : fmtSol(r.net_pnl_sol), "num"), cell(r.exit_reason || "—")));
  body.replaceChildren(tiles,
    h("div", { class: "grid-2" },
      h("div", { class: "panel" }, h("h3", { text: "Net return per resolved candidate" }), barChart(m.distribution, "Distribution of net return per resolved candidate"),
        h("p", { class: "muted", text: m.return_definition })),
      h("div", { class: "panel" }, h("h3", { text: "Cumulative net PnL (SOL), in order of exit" }),
        lineChart(d.equity_curve.map((p) => ({ x: p.t, y: p.cum_net_sol })), { title: "Cumulative net PnL", yLabel: "SOL", xFmt: fmtTime, yFmt: (v) => v.toFixed(3), zero: true }))),
    h("div", { class: "grid-2" },
      h("div", { class: "panel" }, h("h3", { text: "Why candidates were rejected" }), reasons.length ? h("dl", { class: "kv" }, reasons.flatMap(([k, v]) => [h("dt", { class: "mono", text: k }), h("dd", { text: v })])) : h("p", { class: "muted", text: "No rejections recorded." }),
        h("p", { class: "muted", text: "A token can be rejected for several reasons. Rejections are kept in the ledger, never dropped." })),
      h("div", { class: "panel" }, h("h3", { text: "Pre-registered evaluation plan" }), h("dl", { class: "kv" },
        h("dt", { text: "Ruleset" }), h("dd", { class: "mono", text: m.ruleset }), h("dt", { text: "Minimum sample" }), h("dd", { text: `${m.plan.min_resolved_candidates} resolved candidates over ${m.plan.min_span_days} days` }),
        h("dt", { text: "So far" }), h("dd", { text: `${m.resolved} resolved over ${m.span_days.toFixed(1)} days` }),
        h("dt", { text: "Rulesets tried" }), h("dd", { text: m.plan.rulesets_tried }), h("dt", { text: "Primary metric" }), h("dd", { text: m.plan.primary_metric }),
        h("dt", { text: "Config hash" }), h("dd", { class: "mono", text: m.config_hash })))),
    h("div", { class: "panel" }, h("h3", { text: `Complete ledger — ${d.ledger.length} signals, newest first` }),
      h("div", { class: "table-wrap" }, h("table", { class: "data" }, h("thead", {}, h("tr", {}, ledgerHead.map((x) => h("th", { text: x })))), h("tbody", {}, ledger.length ? ledger : h("tr", {}, h("td", { colspan: ledgerHead.length, class: "muted", text: "No signals yet." })))))));
}

/* ---------- claim check ---------- */
function renderClaim(r) {
  const out = $("#claim-result");
  if (r.status !== "ok") { out.replaceChildren(h("p", { class: "muted", text: r.note || "No data." })); return; }
  const usd = (v) => (v == null ? unknown() : "$" + fmtNum(v));
  const kv = h("dl", { class: "kv" },
    h("dt", { text: "Alert minute" }), h("dd", { class: "mono", text: r.alert_minute }),
    h("dt", { text: "Cap in that minute (open / high / low / close)" }), h("dd", { class: "mono", text: ["open", "high", "low", "close"].map((k) => "$" + fmtNum(r.alert_candle_cap_usd[k])).join(" / ") }),
    h("dt", { text: "Cap definition" }), h("dd", { text: r.cap_definition }),
    h("dt", { text: "Highest later one-minute high" }), h("dd", { text: `$${fmtNum(r.peak_after_alert.cap_usd)} at ${r.peak_after_alert.time} (+${Math.round(r.peak_after_alert.minutes_after_alert)} min)` }),
    h("dt", { text: "Best-case multiple from the alert minute" }), h("dd", { class: "mono", text: `${r.best_case_multiple_from_alert_open.toFixed(1)}× from open · ${r.best_case_multiple_from_alert_close.toFixed(1)}× from close` }),
    h("dt", { text: "Minutes closing at or above" }), h("dd", { class: "mono", text: Object.entries(r.minutes_closing_at_or_above).map(([k, v]) => `${k}: ${v}`).join(" · ") }),
    h("dt", { text: "Cap at the last candle read" }), h("dd", { class: "mono" }, usd(r.last_cap_usd)));
  if (r.claimed_cap_usd) kv.append(h("dt", { text: "Claimed cap" }), h("dd", { class: "mono", text: `$${fmtNum(r.claimed_cap_usd)} — observed open is ${r.observed_over_claimed_cap.toFixed(1)}× that; claimed cap ${r.claimed_cap_seen_in_alert_minute ? "WAS" : "was NOT"} inside the alert minute's range` }));
  if (r.claimed_multiple) kv.append(h("dt", { text: "Claimed multiple" }), h("dd", { class: "mono", text: `${r.claimed_multiple}× — ${r.claim_reproducible_from_alert_time ? "reachable" : "NOT reachable"} from the alert-minute open even at the best later minute` }));
  if (r.onchain_at_alert) kv.append(h("dt", { text: "On-chain pool reading" }), h("dd", { class: "mono", text: r.onchain_at_alert.price_sol ? `${fmtNum(r.onchain_at_alert.cap_sol)} SOL cap at ${r.onchain_at_alert.block_time} (slot ${r.onchain_at_alert.slot})` : JSON.stringify(r.onchain_at_alert) }));
  out.replaceChildren(kv, h("ul", { class: "muted" }, r.caveats.map((c) => h("li", { text: c }))));
}

/* ---------- health ---------- */
async function loadHealth() {
  const [st, ev] = await Promise.all([loadStatus(), api("/api/events?limit=40")]);
  showBanner(false);
  const c = st.counts;
  $("#health-body").replaceChildren(
    h("div", { class: "tiles" }, tile("Live tokens", c.tokens_live, `${c.observations_live} observations`), tile("Synthetic tokens", c.tokens_synthetic, `${c.observations_synthetic} observations`),
      tile("Provider conflicts", c.conflicts), tile("Raw snapshots stored", c.raw_snapshots, "per-provider switch in .env"),
      tile("Event log", st.event_log.ok ? "intact" : "BROKEN", `${st.event_log.count} entries, hash-chained`)),
    h("div", { class: "panel" }, h("h3", { text: "Providers" }), h("div", { class: "table-wrap" }, h("table", { class: "data" },
      h("thead", {}, h("tr", {}, ["Provider", "Last success (UTC)", "Last error (UTC)", "Last error", "OK", "Errors", "Rate-limited until"].map((x) => h("th", { text: x })))),
      h("tbody", {}, st.provider_health.length ? st.provider_health.map((p) => h("tr", {}, cell(p.provider), cell(fmtTime(p.last_ok), "mono"), cell(fmtTime(p.last_error), "mono"), cell(p.last_error_text || "—"),
        h("td", { class: "num", text: p.ok_count }), h("td", { class: "num", text: p.error_count }), cell(fmtTime(p.rate_limited_until) || "—", "mono")))
        : h("tr", {}, h("td", { colspan: 7, class: "muted", text: "No provider has been called yet (demo mode makes no network calls)." })))))),
    h("div", { class: "grid-2" },
      h("div", { class: "panel" }, h("h3", { text: "Settings in effect" }), h("dl", { class: "kv" },
        h("dt", { text: "Mode" }), h("dd", { text: st.mode }), h("dt", { text: "Solana RPC" }), h("dd", { class: "mono", text: st.settings.solana_rpc_url }),
        h("dt", { text: "Raw snapshot storage" }), h("dd", { class: "mono", text: Object.entries(st.settings.store_raw).map(([k, v]) => `${k}: ${v ? "on" : "off"}`).join(" · ") }),
        h("dt", { text: "Paper settings" }), h("dd", { class: "mono", text: Object.entries(st.settings.paper).map(([k, v]) => `${k}=${v}`).join("  ") }),
        h("dt", { text: "Decision rule" }), h("dd", { class: "mono", text: Object.entries(st.decision_rule).map(([k, v]) => `${k}=${v}`).join("  ") }),
        h("dt", { text: "Exit rule" }), h("dd", { class: "mono", text: Object.entries(st.exit_rule).map(([k, v]) => `${k}=${v}`).join("  ") }))),
      h("div", { class: "panel" }, h("h3", { text: "Recent events" }), h("div", { class: "table-wrap" }, h("table", { class: "data" },
        h("thead", {}, h("tr", {}, ["#", "Time (UTC)", "Type", "Hash"].map((x) => h("th", { text: x })))),
        h("tbody", {}, ev.events.map((e) => h("tr", { title: JSON.stringify(e.payload) }, h("td", { class: "num", text: e.id }), cell(fmtTime(e.ts), "mono"), cell(e.type), h("td", { class: "mono", text: e.hash.slice(0, 12) + "…" })))))))));
}

/* ---------- navigation and wiring ---------- */
async function switchView(view) {
  state.view = view;
  for (const tab of document.querySelectorAll(".tab")) {
    if (tab.dataset.view === view) tab.setAttribute("aria-current", "page");
    else tab.removeAttribute("aria-current");
  }
  for (const sec of document.querySelectorAll(".view")) sec.hidden = sec.id !== "view-" + view;
  try {
    if (view === "tokens") await loadTokens();
    if (view === "paper") await loadPaper();
    if (view === "health") await loadHealth();
    if (view === "claim") { showBanner(false); setMessage("#claim-message", state.status && !state.status.live_enabled ? "Live connectors are off. Restart with --live to use this check." : ""); }
  } catch (err) { setMessage("#tokens-message", err.message, true); }
}
async function busy(button, messageId, label, fn) {
  button.disabled = true;
  setMessage(messageId, label);
  try { setMessage(messageId, await fn()); } catch (err) { setMessage(messageId, err.message, true); } finally { button.disabled = false; await loadStatus().catch(() => {}); }
}
document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => switchView(tab.dataset.view)));
$("#search-form").addEventListener("submit", (e) => {
  e.preventDefault();
  loadTokens().then((data) => { if (data.query && data.tokens.length === 1) return openToken(data.tokens[0].mint); return null; })
    .catch((err) => setMessage("#tokens-message", err.message, true));
});
$("#scope-select").addEventListener("change", () => loadTokens());
$("#fetch-live").addEventListener("click", (e) => busy(e.currentTarget, "#tokens-message", "Fetching public data (read-only). GeckoTerminal allows about 10 calls a minute, so this can take a while…", async () => {
  const mint = $("#search-input").value.trim();
  const r = await api("/api/ingest", { mint });
  await loadTokens(); await openToken(mint);
  return `Stored ${r.stored.market} market, ${r.stored.launch} launch, ${r.stored.holders} holder observation(s).` + (r.errors.length ? " Unavailable: " + r.errors.map((x) => `${x.provider} (${x.kind})`).join(", ") + "." : "");
}));
$("#discover-live").addEventListener("click", (e) => busy(e.currentTarget, "#tokens-message", "Reading the provider's newest-pools list…", async () => {
  const r = await api("/api/discover", {}); await loadTokens();
  return `${r.added} new launch(es) imported. ${r.coverage_note}.`;
}));
$("#book-select").addEventListener("change", (e) => { state.book = e.target.value; loadPaper().catch((err) => setMessage("#paper-message", err.message, true)); });
$("#paper-run").addEventListener("click", (e) => busy(e.currentTarget, "#paper-message", "Recording signals and updating positions…", async () => {
  const r = await api("/api/paper/run", { book: state.book }); await loadPaper();
  return `${r.new_signals} new signal(s) recorded; positions updated: ${JSON.stringify(r.simulated)}.`;
}));
$("#demo-reset").addEventListener("click", (e) => busy(e.currentTarget, "#paper-message", "Regenerating synthetic data…", async () => {
  const seed = Math.floor(Math.random() * 1e6);
  const r = await api("/api/demo/reset", { seed }); await loadPaper();
  return `New synthetic universe: ${r.seeded.n_tokens} fake tokens, seed ${r.seeded.seed}.`;
}));
$("#claim-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const f = new FormData(e.target), btn = e.target.querySelector("button");
  busy(btn, "#claim-message", "Reading candles (rate-limited provider; up to a minute)…", async () => {
    renderClaim(await api("/api/audit", { mint: f.get("mint").trim(), alert_time: f.get("alert_time").trim(), claimed_cap_usd: f.get("claimed_cap_usd"), claimed_multiple: f.get("claimed_multiple"), onchain: f.get("onchain") === "on" }));
    return "Done.";
  });
});
loadStatus().then(() => switchView("tokens")).catch((err) => setMessage("#tokens-message", err.message, true));
