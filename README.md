# Nintec360 — redisseny

Web estàtica de deu pàgines en català, castellà i anglès (30 rutes). HTML semàntic generat amb Python, CSS compartit i JavaScript sense dependències. No necessita React, un servidor d’aplicació ni biblioteques de tercers al navegador.

## Narrativa del cercle

La home i la pàgina de Nintec360 comparteixen sis etapes amb el CRM al centre. `src/cycle.json` conté el relat problema → acció → benefici de cada etapa; `cycle.py` genera el diagrama i els panells accessibles durant el build. Els continguts es renderitzen en HTML, amb selecció per clic, tacte o teclat. Les campanyes disposen de peces específiques que expliquen la gestió de cada resposta.

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
- Les mètriques dels casos han estat corroborades pel client: restauració ≈2.000 €/mes; immobiliària 100% de consultes ateses i +20% de vendes; retail +40% de ressenyes positives i +25% d’ingressos. No impliquen una previsió per a altres empreses.
- Validar les garanties de concurrència i les polítiques del backend amb el seu responsable.
- Fer una reserva real de validació amb dades autoritzades i comprovar-ne la recepció. No s’han creat reserves ni subscripcions de prova en producció.

No hi ha testimonis inventats, certificacions, preus, números de clients ni garanties de resultats. Les demostracions estan identificades com a il·lustratives.

## Casos reals: mecanisme i resultat

Cada cas mostra problema, procés assumit per Nintec360, canvi operatiu i resultat. Restauració representa la comanda, la bifurcació entre els dos locals i la derivació humana amb context; immobiliària, la qualificació i la fitxa que rep el comercial; retail, la continuïtat després de la venda i el retorn a una nova oportunitat. Els esquemes són HTML accessible amb passos ordenats i disposició vertical en mòbil; el contingut principal no depèn de clics ni de JavaScript. S’han revisat en escriptori i mòbil, i s’han validat les deu pàgines i els seus enllaços.

## Adaptació al negoci

L’antiga secció tècnica d’integracions ara explica com Nintec360 encaixa amb les eines i els processos existents. Un esquema mostra les eines actuals, les gestions que assumeix Nintec360 i la informació que torna al sistema de l’equip. Les integracions es mantenen en una franja secundària. S’ha eliminat l’entrada «Integracions» de la navegació compartida; la portada enllaça a `#adaptacio` i l’antic `#integracions` es conserva com a destí compatible. Validats els enllaços de les deu pàgines i revisada la secció en escriptori i mòbil.

## Venda dins del context del client

El bloc «El context, sempre a mà» incorpora l’exemple fictici d’Anna G.: consulta per WhatsApp, necessitat, producte seleccionat, pagament confirmat i comanda registrada. El següent pas és preparar la comanda. El recorregut queda visible, amb disposició vertical en mòbil. No s’ha afegit cap funcionalitat de compra ni s’ha modificat el backend. La referència al CSS inclou una empremta del contingut perquè les actualitzacions visuals arribin també als visitants que ja havien obert la web.

## Compra i pagament en el relat general

La tercera etapa compartida del cercle és «Venda i reserva»: explica compra, pagament, agenda i derivació segons el procés. Restauració mostra el pagament amb Stripe quan aplica; retail mostra la compra digital amb Shopify i la continuïtat posterior. Cada marca apareix una vegada al seu cas i una vegada a les eines compatibles. La demo del CRM manté la compra completada i la següent acció. Les mètriques dels casos es preserven. Aquest canvi és narratiu i no incorpora cap connexió de pagament nova a la web.

## Cercle viu i pauses de lectura

`src/cycle-player.js` controla el cercle compartit sense dependències: 4 segons per etapa, 18 segons després de seleccionar amb clic/toc, i 1,5 segons d’espera en abandonar el hover o el focus de teclat. La pausa conserva el temps restant. La seqüència automàtica recorre només les sis etapes; el CRM continua sent context central consultable manualment. El connector indica el progrés i el text canvia amb un fade discret. Es reserva l’alçada màxima del panell per evitar salts de pàgina.

Hi ha un control explícit per pausar/reprendre. `prefers-reduced-motion` desactiva l’autoplay i el moviment; la selecció manual es manté. La visibilitat de la finestra i del cercle atura el temporitzador. S’alliberen temporitzadors, animacions, listeners i observadors quan s’elimina el component o es deixa la pàgina, i es recupera el funcionament en tornar amb la memòria cau de navegació.

Validació addicional: `node --test tests/cycle-player.test.cjs` comprova temporitzacions, pauses superposades, lectura de 18 segons, visibilitat, reducció de moviment i neteja. Provat al navegador el retorn 06 → 01, la sincronització, hover, teclat, pausa explícita i disposició mòbil. Els fitxers JavaScript modificats inclouen una empremta del contingut a la URL perquè es carregui la versió actualitzada.

## Idiomes CA / ES / EN

El català és la font compartida de les plantilles. `src/locales/es.json` i `en.json` contenen traduccions revisades per text de la font, inclosos atributs accessibles i metadades. `i18n.py` genera HTML complet per a cada idioma; no substitueix textos al DOM ni depèn d’un servei de traducció. Una cadena nova sense traducció fa fallar el build. Les marques, els noms de persones i les dades de contacte es conserven explícitament al catàleg.

Rutes: català a `/`, castellà a `/es/`, anglès a `/en/`. Cada idioma conserva la mateixa estructura de pàgines i ancoratges. Els enllaços interns, canonical, Open Graph, `lang`, `hreflang` i sitemap es generen per idioma. Els identificadors tècnics dels ancoratges i els camps de l’API es mantenen estables.

El selector nadiu funciona també sense JavaScript. Amb JavaScript, desa només `nintec-language` a localStorage. Una ruta amb prefix explícit ES/EN té prioritat; en entrar a una ruta sense prefix, es respecta l’idioma desat. La selecció explícita `?lang=ca` permet tornar a català; el paràmetre es retira de la URL. Sense preferència, català. Si el navegador bloqueja l’emmagatzematge, les rutes traduïdes i el selector continuen funcionant.

`src/locales/runtime.json` declara els missatges que necessita el navegador. `src/i18n.js` resol idioma, preferència i validació dels formularis. El calendari formata els noms dels dies i mesos amb Intl, mantenint dates ISO, zona Europe/Madrid i contracte de reserva. Les confirmacions, conflictes, errors de connexió, càrrega i avisos de Compliance utilitzen els mateixos catàlegs.

Per afegir contingut: modifica la plantilla catalana i afegeix les dues traduccions; per a un missatge dinàmic, afegeix també la clau a `runtime.json` i utilitza `t()`. Executa `python3 build.py`, `python3 tests/validate.py` i `node --test tests/i18n.test.cjs tests/cycle-player.test.cjs tests/api.test.cjs`. La validació cobreix les 30 pàgines. Les proves de formularis fan servir transport local simulat, sense escriure registres reals.

## SEO y producción

El build predeterminado `python3 build.py` genera `dist` para revisión privada en Sites, con noindex. El dominio público verificado es `https://www.nintecsolutions.com`; actualmente sigue en Wix.

Generar el paquete público sin alterar la revisión: `python3 build.py --production --output ../nintec360-production`.

Comprobar ambas salidas: `python3 tests/validate.py`, `python3 tests/validate.py ../nintec360-production` y `python3 tests/seo.test.py dist ../nintec360-production`. Pruebas de interacción: `node --test tests/i18n.test.cjs tests/cycle-player.test.cjs tests/api.test.cjs`.

Los WebP están versionados. Para regenerarlos desde originales, `scripts/optimize_images.py` necesita Pillow y Arial instalado. Esto no es necesario para construir la web.

Un token HTML real de Search Console puede suministrarse mediante `GOOGLE_SITE_VERIFICATION` al construir producción. No hay token predeterminado. `_redirects` y `_headers` necesitan soporte/configuración equivalente en el proveedor público. Consultar `SEO_AUDIT.md` y `GOOGLE_INDEXING_CHECKLIST.md`; no confundir el build público con un despliegue efectivo en Wix.

## Vercel

La preparación actual para **GitHub → Vercel → Preview** se describe en `VERCEL_SETUP.md`. Vercel usa `vercel.json` y `scripts/build_vercel.py`; no interpreta `_redirects` ni `_headers`. Se conserva el flujo original de Sites por separado. No se ha cambiado el dominio ni Wix.

Deployment Vercel configurat.
