/**
 * The Zellijist × Morocco Design — Atelier zellije chez Flexform
 * Service de réservation ; les inscrits vont dans le classeur « Flexform zellijist waitlist ».
 *
 * Appelé uniquement par la fonction Vercel api/atelier.js de thezellijist.com,
 * qui ajoute le secret partagé (propriété de script SECRET = ATELIER_SECRET sur Vercel).
 *
 * Une feuille par session (« Mardi 6 oct · 12h », « Mercredi 7 oct · 15h ») : chaque feuille
 * est la liste des inscrits de son créneau. La feuille du lundi n'est jamais modifiée.
 * Installation : voir atelier/README.md.
 */

// ---------- Configuration ----------
const SESSIONS = {
  'mar-06-1200': { sheet: 'Mardi 6 oct · 12h', label: 'Mardi 6 octobre · 12:00 · Flexform', capacity: 10 },
  'mer-07-1500': { sheet: 'Mercredi 7 oct · 15h', label: 'Mercredi 7 octobre · 15:00 · Flexform', capacity: 10 },
};
const MAX_SEATS_PER_BOOKING = 2;
const NOTIFY_EMAIL = '';                     // ex. 'studio@…' : reçoit un mail à chaque inscription ('' = désactivé)
const SEND_CONFIRMATION = true;              // mail de confirmation au participant

// Secret partagé et clé admin : Paramètres du projet → Propriétés du script
//   SECRET    = même valeur que ATELIER_SECRET sur Vercel
//   ADMIN_KEY = mot de passe de la page /flexform/inscrits.html
const PROPS = PropertiesService.getScriptProperties();

// Classeur « Flexform zellijist waitlist » : le script n'a pas besoin d'y être lié.
const SPREADSHEET_ID = '10A0u_yuBySkuBUPJhRee2-EZpy7Xf3KVKwuKFdfNJKY';

const HEADERS = ['Inscrit le', 'Prénom', 'Nom', 'Email', 'Téléphone', 'Places', 'Société / Studio', 'Statut'];
const COL = { email: 4, seats: 6, status: 8 }; // 1-indexées

// ---------- Endpoints ----------
function doGet(e) {
  const p = (e && e.parameter) || {};
  if (!secretOk_(p.secret)) return json_({ ok: false, error: 'secret' });
  if (p.action === 'list') {
    const admin = PROPS.getProperty('ADMIN_KEY');
    if (!admin || p.key !== admin) return json_({ ok: false, error: 'unauthorized' });
    return json_({ ok: true, sessions: availability_(), rows: allRows_() });
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
    if (!secretOk_(d.secret)) return json_({ ok: false, error: 'secret' });

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

    const rows = rows_(d.session);
    if (rows.some(r => r.email.toLowerCase() === email && r.status !== 'Annulé')) {
      return json_({ ok: false, error: 'already_registered', sessions: availability_() });
    }
    const remaining = availability_()[d.session].remaining;
    if (seats > remaining) return json_({ ok: false, error: remaining > 0 ? 'not_enough_seats' : 'full', sessions: availability_() });

    sheet_(d.session).appendRow([new Date(), firstName, lastName, email, "'" + phone, seats, company, 'Confirmé']);
    SpreadsheetApp.flush();

    notify_(session, { firstName, lastName, email, phone, seats, company });
    return json_({ ok: true, sessions: availability_() });
  } finally {
    lock.releaseLock();
  }
}

// ---------- Helpers ----------
function secretOk_(v) {
  const s = PROPS.getProperty('SECRET');
  return Boolean(s) && v === s;
}

function availability_() {
  const out = {};
  Object.keys(SESSIONS).forEach(id => {
    const booked = rows_(id).filter(r => r.status !== 'Annulé').reduce((a, r) => a + (Number(r.seats) || 0), 0);
    const cap = SESSIONS[id].capacity;
    out[id] = { label: SESSIONS[id].label, capacity: cap, booked: booked, remaining: Math.max(0, cap - booked) };
  });
  return out;
}

function rows_(id) {
  const sh = sheet_(id);
  if (sh.getLastRow() < 2) return [];
  return sh.getRange(2, 1, sh.getLastRow() - 1, HEADERS.length).getValues()
    .filter(r => r[1] || r[3])
    .map(r => ({
      date: r[0] instanceof Date ? r[0].toISOString() : String(r[0]),
      sessionId: id, session: SESSIONS[id].label,
      firstName: r[1], lastName: r[2], email: String(r[3]), phone: String(r[4]),
      seats: r[5], company: r[6], status: r[7],
    }));
}

function allRows_() {
  return Object.keys(SESSIONS).reduce((all, id) => all.concat(rows_(id)), []);
}

/** Feuille de la session ; créée avec ses en-têtes si elle n'existe pas encore. */
function sheet_(id) {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  const name = SESSIONS[id].sheet;
  let sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    sh.appendRow(HEADERS);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold').setBackground('#2D5E37').setFontColor('#E6AC03');
    sh.getRange(2, COL.status, 999, 1).setDataValidation(
      SpreadsheetApp.newDataValidation().requireValueInList(['Confirmé', 'Présent', 'Annulé'], true).build());
    sh.setColumnWidth(1, 140);
    sh.setColumnWidths(2, 3, 150);
    sh.setColumnWidth(4, 220);
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
        subject: 'Atelier zellije — réservation confirmée',
        name: 'The Zellijist',
        htmlBody:
          '<p>Bonjour ' + p.firstName + ',</p>' +
          '<p>Votre place est confirmée pour l\'atelier zellije The Zellijist × Morocco Design :</p>' +
          '<p><b>' + session.label + '</b><br>' + p.seats + ' place(s)</p>' +
          '<p>Showroom Flexform, Casablanca. Merci d\'arriver 10 minutes en avance.</p>' +
          '<p>À très vite,<br>The Zellijist</p>',
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

/** À lancer une fois depuis l'éditeur : crée les feuilles Mardi et Mercredi. */
function setup() {
  Object.keys(SESSIONS).forEach(sheet_);
}
