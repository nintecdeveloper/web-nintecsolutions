# Nintec360 — redisseny

Web estàtica de deu pàgines en català. HTML semàntic generat amb Python, CSS compartit i JavaScript sense dependències. No necessita React, un servidor d’aplicació ni biblioteques de tercers al navegador.

## Desenvolupament

```sh
python3 build.py
python3 -m http.server 4173 --directory dist
```

Obre `http://localhost:4173`. Després d’un canvi, executa el build i recarrega.

## Validació

```sh
python3 tests/validate.py
node tests/api.test.cjs
node --check src/app.js
```

Les proves d’API utilitzen un transport local simulat. No creen registres al projecte real.

## Publicació i SEO

`dist/` és l’arrel pública. Conté sitemap, robots, capçaleres, pàgina 404 i redireccions 301 dels noms `.dc.html` originals. `_redirects` i `_headers` segueixen el format de Cloudflare; en un altre allotjament cal configurar-ne l’equivalent. Serveix sempre les rutes de directori amb `index.html`.

El domini de la revisió privada és el valor per defecte. Per a la web pública, genera l’artefacte amb el domini definitiu:

```sh
SITE_ORIGIN=https://nintecsolutions.com python3 build.py
```

Això actualitza canonical, OpenGraph, dades estructurades i sitemap. No s’ha canviat el domini ni la web pública existent.

## Connexions preservades

La font funcional és el fitxer `contacte.dc.html` de l’arrel del ZIP, no la versió antiga de `design_handoff_reserva_auditoria/`.

- Supabase RPC `get_franges_ocupades`, amb `_desde` i `_fins`.
- Inserció a `reserves_auditoria` amb els mateixos nou camps: `nom`, `cognoms`, `empresa`, `email`, `telefon`, `missatge`, `data`, `hora`, `suggeriment_horari`.
- Propostes alternatives amb `data` i `hora` a `null`.
- Compliance: inserció de `{ email }` a `leads_compliance`.
- La clau de `src/api.js` és la clau PUBLICABLE del frontend original; no és una credencial de servei ni proporciona accés administratiu.

Les hores només es mostren després d’una resposta vàlida de la RPC. Es torna a consultar abans d’una reserva i es gestionen conflictes HTTP 409. La protecció atòmica contra dues reserves simultànies depèn de la restricció/transacció del backend existent; el ZIP no inclou el seu esquema i no s’ha modificat.

Els dotze dies laborables, les franges de 30 minuts i l’antelació mínima d’una hora conserven el comportament original. El càlcul ara usa `Europe/Madrid` independentment de la zona del visitant. No s’ha inventat un sistema de festius: l’operativa del backend ha de bloquejar-los si correspon.

Les caselles informen/recullen l’acceptació de privacitat a la interfície; no s’ha afegit un camp de consentiment a les taules, perquè no figura al contracte original. La conservació de proves de consentiment requereix definir-la amb el backend.

## Pendents abans de la publicació pública

- Validar les pàgines legals heretades: regió de dades, proveïdors, DPA, dates i textos definitius.
- Confirmar vigència, període i metodologia dels resultats de casos (≈2.000 €/mes i +25%).
- Validar les garanties de concurrència i les polítiques del backend amb el seu responsable.
- Fer una reserva real de validació amb dades autoritzades i comprovar-ne la recepció. No s’han creat reserves ni subscripcions de prova en producció.
- Decidir traduccions reals abans d’incorporar ES/EN. La versió lliurada és CA.

No hi ha testimonis inventats, certificacions, preus, números de clients ni garanties de resultats. Les demostracions estan identificades com a il·lustratives.
