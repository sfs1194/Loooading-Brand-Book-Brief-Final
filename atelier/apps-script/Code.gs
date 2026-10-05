/**
 * The Zellijist × Morocco Design — Atelier zellige chez Flexform
 * Backend de réservation (Google Apps Script lié à un Google Sheet).
 *
 * L'onglet « Inscriptions » est le récap de tous les inscrits,
 * l'onglet « Récap » affiche places réservées / restantes par session.
 * Installation : voir atelier/README.md.
 */

// ---------- Configuration ----------
const SESSIONS = {
  'mar-06-1200': { label: 'Mardi 6 octobre · 12:00 · Flexform', capacity: 10 },
  'mer-07-1500': { label: 'Mercredi 7 octobre · 15:00 · Flexform', capacity: 10 },
};
const MAX_SEATS_PER_BOOKING = 2;
const ADMIN_KEY = 'CHANGER-CETTE-CLE';      // clé pour la page inscrits.html
const NOTIFY_EMAIL = '';                     // ex. 'studio@…' : reçoit un mail à chaque inscription ('' = désactivé)
const SEND_CONFIRMATION = true;              // mail de confirmation au participant

const SHEET_NAME = 'Inscriptions';
const RECAP_NAME = 'Récap';
const HEADERS = ['Date d\'inscription', 'Session ID', 'Session', 'Prénom', 'Nom', 'Email', 'Téléphone', 'Places', 'Société / Studio', 'Statut'];
// Colonnes (1-indexées)
const COL = { session: 2, email: 6, seats: 8, status: 10 };

// ---------- Endpoints ----------
function doGet(e) {
  const p = (e && e.parameter) || {};
  if (p.action === 'list') {
    if (p.key !== ADMIN_KEY) return json_({ ok: false, error: 'unauthorized' });
    return json_({ ok: true, sessions: availability_(), rows: rows_() });
  }
  return json_({ ok: true, sessions: availability_() });
}

function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(15000);
  } catch (err) {
    return json_({ ok: false, error: 'busy' });
  }
  try {
    const d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (d.website) return json_({ ok: true, sessions: availability_() }); // honeypot anti-spam

    const session = SESSIONS[d.session];
    const firstName = clean_(d.firstName, 80);
    const lastName = clean_(d.lastName, 80);
    const email = clean_(d.email, 120).toLowerCase();
    const phone = clean_(d.phone, 40);
    const company = clean_(d.company, 120);
    const seats = Math.max(1, Math.min(MAX_SEATS_PER_BOOKING, parseInt(d.seats, 10) || 1));

    if (!session) return json_({ ok: false, error: 'invalid_session' });
    if (!firstName || !lastName || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !phone) {
      return json_({ ok: false, error: 'invalid_fields' });
    }

    const sh = sheet_();
    const data = sh.getLastRow() > 1 ? sh.getRange(2, 1, sh.getLastRow() - 1, HEADERS.length).getValues() : [];
    const dup = data.some(r => r[COL.session - 1] === d.session && String(r[COL.email - 1]).toLowerCase() === email && r[COL.status - 1] !== 'Annulé');
    if (dup) return json_({ ok: false, error: 'already_registered', sessions: availability_() });

    const remaining = availability_()[d.session].remaining;
    if (seats > remaining) return json_({ ok: false, error: remaining > 0 ? 'not_enough_seats' : 'full', sessions: availability_() });

    sh.appendRow([new Date(), d.session, session.label, firstName, lastName, email, "'" + phone, seats, company, 'Confirmé']);
    SpreadsheetApp.flush();

    notify_(session, { firstName, lastName, email, phone, seats, company });
    return json_({ ok: true, sessions: availability_() });
  } finally {
    lock.releaseLock();
  }
}

// ---------- Helpers ----------
function availability_() {
  const counts = {};
  Object.keys(SESSIONS).forEach(id => (counts[id] = 0));
  rows_().forEach(r => {
    if (r.status !== 'Annulé' && counts[r.sessionId] !== undefined) counts[r.sessionId] += Number(r.seats) || 0;
  });
  const out = {};
  Object.keys(SESSIONS).forEach(id => {
    const cap = SESSIONS[id].capacity;
    out[id] = { label: SESSIONS[id].label, capacity: cap, booked: counts[id], remaining: Math.max(0, cap - counts[id]) };
  });
  return out;
}

function rows_() {
  const sh = sheet_();
  if (sh.getLastRow() < 2) return [];
  return sh.getRange(2, 1, sh.getLastRow() - 1, HEADERS.length).getValues().map(r => ({
    date: r[0] instanceof Date ? r[0].toISOString() : String(r[0]),
    sessionId: r[1], session: r[2], firstName: r[3], lastName: r[4],
    email: r[5], phone: String(r[6]), seats: r[7], company: r[8], status: r[9],
  }));
}

function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME, 0);
    sh.appendRow(HEADERS);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold').setBackground('#2D5E37').setFontColor('#D6B53F');
    sh.getRange(2, COL.status, 999, 1).setDataValidation(
      SpreadsheetApp.newDataValidation().requireValueInList(['Confirmé', 'Présent', 'Annulé'], true).build());
  }
  return sh;
}

function clean_(v, max) {
  return String(v == null ? '' : v).replace(/[\r\n\t]+/g, ' ').replace(/^[=+\-@]+/, '').trim().slice(0, max);
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function notify_(session, p) {
  try {
    if (SEND_CONFIRMATION) {
      MailApp.sendEmail({
        to: p.email,
        subject: 'Atelier zellige — réservation confirmée',
        name: 'The Zellijist',
        htmlBody:
          '<p>Bonjour ' + p.firstName + ',</p>' +
          '<p>Votre place est confirmée pour l\'atelier zellige The Zellijist × Morocco Design :</p>' +
          '<p><b>' + session.label + '</b><br>' + p.seats + ' place(s)</p>' +
          '<p>Showroom Flexform, Casablanca. Merci d\'arriver 10 minutes en avance.</p>' +
          '<p>À très vite,<br>The Zellijist · Saad Filali Studio</p>',
      });
    }
    if (NOTIFY_EMAIL) {
      MailApp.sendEmail(NOTIFY_EMAIL, 'Nouvelle inscription — ' + session.label,
        [p.firstName + ' ' + p.lastName, p.email, p.phone, p.seats + ' place(s)', p.company].join('\n'));
    }
  } catch (err) {
    console.error(err); // un mail en échec ne doit pas annuler l'inscription
  }
}

/** À lancer une fois depuis l'éditeur : crée les onglets et le récap. */
function setup() {
  sheet_();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let recap = ss.getSheetByName(RECAP_NAME);
  if (!recap) recap = ss.insertSheet(RECAP_NAME, 1);
  recap.clear();
  recap.appendRow(['Session', 'Capacité', 'Réservées', 'Restantes', 'Inscriptions']);
  const ids = Object.keys(SESSIONS);
  ids.forEach((id, i) => {
    const r = i + 2;
    const src = "'" + SHEET_NAME + "'!";
    recap.getRange(r, 1, 1, 5).setValues([[
      SESSIONS[id].label,
      SESSIONS[id].capacity,
      '=SUMIFS(' + src + 'H:H,' + src + 'B:B,"' + id + '",' + src + 'J:J,"<>Annulé")',
      '=B' + r + '-C' + r,
      '=COUNTIFS(' + src + 'B:B,"' + id + '",' + src + 'J:J,"<>Annulé")',
    ]]);
  });
  const total = ids.length + 2;
  recap.getRange(total, 1, 1, 5).setValues([['TOTAL', '=SUM(B2:B' + (total - 1) + ')', '=SUM(C2:C' + (total - 1) + ')', '=SUM(D2:D' + (total - 1) + ')', '=SUM(E2:E' + (total - 1) + ')']]);
  recap.getRange(1, 1, 1, 5).setFontWeight('bold').setBackground('#2D5E37').setFontColor('#D6B53F');
  recap.getRange(total, 1, 1, 5).setFontWeight('bold');
  recap.setFrozenRows(1);
  recap.autoResizeColumns(1, 5);
}
