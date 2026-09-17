/* Smash House — real opening state for Boca Raton.
   Sun-Thu 11:00-23:00 | Friday CLOSED | Saturday opens one hour after Shabbat ends, until 00:00.
   Sunset is computed here so the page is correct offline. PRODUCTION MUST USE HEBCAL:
   holiday closures move every year and the tzeit opinion is the owner's to choose. */
(function (SH) {
  'use strict';
  var LAT = 26.3683, LON = -80.1289, TZ = 'America/New_York';
  var TZEIT_MIN = 42;   /* tzeit hakochavim, common 42-minute opinion [TO CONFIRM with the owner] */
  var OPEN_AFTER_SHABBAT_MIN = 60;

  function parts(date) {
    var f = new Intl.DateTimeFormat('en-US', {
      timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, weekday: 'short'
    }).formatToParts(date).reduce(function (o, p) { o[p.type] = p.value; return o; }, {});
    var days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    return {
      y: +f.year, m: +f.month, d: +f.day,
      hh: +f.hour % 24, mm: +f.minute, dow: days[f.weekday],
      minutes: (+f.hour % 24) * 60 + (+f.minute)
    };
  }

  /* Sunrise equation. Returns local minutes after midnight in TZ, or null above the polar circle. */
  function sunsetMinutes(y, m, d) {
    var a = Math.floor((14 - m) / 12), yy = y + 4800 - a, mm = m + 12 * a - 3;
    var jdn = d + Math.floor((153 * mm + 2) / 5) + 365 * yy + Math.floor(yy / 4)
            - Math.floor(yy / 100) + Math.floor(yy / 400) - 32045;
    var n = jdn - 2451545 + 0.0008;
    var Jstar = n - LON / 360;
    var M = (357.5291 + 0.98560028 * Jstar) % 360;
    var Mr = M * Math.PI / 180;
    var C = 1.9148 * Math.sin(Mr) + 0.02 * Math.sin(2 * Mr) + 0.0003 * Math.sin(3 * Mr);
    var lam = (M + C + 180 + 102.9372) % 360, lr = lam * Math.PI / 180;
    var Jtransit = 2451545.0 + Jstar + 0.0053 * Math.sin(Mr) - 0.0069 * Math.sin(2 * lr);
    var sinDec = Math.sin(lr) * Math.sin(23.44 * Math.PI / 180);
    var cosDec = Math.sqrt(1 - sinDec * sinDec);
    var phi = LAT * Math.PI / 180;
    var cosW = (Math.sin(-0.833 * Math.PI / 180) - Math.sin(phi) * sinDec) / (Math.cos(phi) * cosDec);
    if (cosW < -1 || cosW > 1) return null;
    var w = Math.acos(cosW) * 180 / Math.PI;
    var Jset = Jtransit + w / 360;
    var utcMs = (Jset - 2440587.5) * 86400000;
    var p = parts(new Date(utcMs));
    return p.minutes;
  }

  function shabbatEndMinutes(y, m, d) {
    var s = sunsetMinutes(y, m, d);
    return s === null ? null : s + TZEIT_MIN;
  }

  function fmt(min) {
    if (min === null || min === undefined) return '—';
    var wrapped = ((min % 1440) + 1440) % 1440;
    var h = Math.floor(wrapped / 60), mi = Math.round(wrapped % 60);
    var ap = h >= 12 ? 'PM' : 'AM', h12 = h % 12 === 0 ? 12 : h % 12;
    return h12 + ':' + (mi < 10 ? '0' : '') + mi + ' ' + ap;
  }

  function state(now) {
    now = now || new Date();
    var p = parts(now);
    var out = { dow: p.dow, nowMin: p.minutes, isShabbat: false, open: false,
                opensAt: null, closesAt: null, note: '', key: 'closed' };

    if (p.dow === 5) {                                   /* Friday: closed all day */
      out.isShabbat = true; out.key = 'shabbat';
      var satEnd = shabbatEndMinutes(p.y, p.m, p.d + 1);
      out.opensAt = satEnd === null ? null : satEnd + OPEN_AFTER_SHABBAT_MIN;
      out.note = 'Closed for Shabbat. The grill fires up tomorrow night.';
      out.opensLabel = 'Saturday ' + fmt(out.opensAt);
    } else if (p.dow === 6) {                            /* Saturday: opens after Shabbat */
      var end = shabbatEndMinutes(p.y, p.m, p.d);
      var opens = end === null ? null : end + OPEN_AFTER_SHABBAT_MIN;
      out.opensAt = opens; out.closesAt = 1440;
      if (opens !== null && p.minutes >= opens) {
        out.open = true; out.key = 'open';
        out.note = 'Shavua tov. Open until midnight.';
      } else {
        out.isShabbat = true; out.key = 'shabbat';
        out.note = 'Shabbat Shalom. The grill fires up tonight.';
        out.opensLabel = 'tonight at ' + fmt(opens);
      }
    } else {                                             /* Sunday to Thursday */
      out.opensAt = 11 * 60; out.closesAt = 23 * 60;
      if (p.minutes >= out.opensAt && p.minutes < out.closesAt) { out.open = true; out.key = 'open'; }
      else if (p.minutes < out.opensAt) { out.opensLabel = 'today at 11:00 AM'; }
      else { out.opensLabel = 'tomorrow at 11:00 AM'; }
    }
    return out;
  }

  function week(now) {
    now = now || new Date();
    var p = parts(now);
    var names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    var rows = [];
    for (var i = 0; i < 7; i++) {
      var row = { name: names[i], today: i === p.dow, closed: false, value: '11:00 AM – 11:00 PM' };
      if (i === 5) { row.value = 'Closed'; row.closed = true; }
      if (i === 6) {
        var delta = (6 - p.dow + 7) % 7;
        var end = shabbatEndMinutes(p.y, p.m, p.d + delta);
        row.value = (end === null ? '—' : fmt(end + OPEN_AFTER_SHABBAT_MIN)) + ' – 12:00 AM';
      }
      rows.push(row);
    }
    return rows;
  }

  SH.hours = { state: state, week: week, fmt: fmt, sunsetMinutes: sunsetMinutes,
               shabbatEndMinutes: shabbatEndMinutes, parts: parts };
})(SH);
