# Nintec Journal · CA / ES / EN / NL

El Journal es publica com a HTML estàtic en els quatre idiomes de la web. Inclou setze articles complets, portada, arxiu i criteri editorial: 76 rutes del Journal, 108 pàgines totals i 96 URL indexables al sitemap.

- Català: `/blog/`
- Castellà: `/es/blog/`
- Anglès: `/en/blog/`
- Neerlandès: `/nl/blog/`

El selector conserva l’article o pàgina equivalent. La navegació corporativa manté l’idioma. Canonicals, hreflang CA/ES/EN/NL/x-default, metadades socials i JSON-LD s’emeten durant el build. No es depèn de traducció automàtica al navegador.

## Fonts i manteniment

- `src/journal/content/*.json`: contingut català, autoria, fonts, relacionats i dates.
- `src/journal/locales/{es,en,nl}.json`: traduccions completes de textos, articles, metadades, crèdits i interfície.
- `src/journal/images.json`: procedència i drets de les imatges; derivats optimitzats a `src/assets/journal/`.
- `journal.py` i `journal_i18n.py`: renderització estàtica, escapament i traducció estricta. Un text sense traducció atura el build.
- `src/journal.css` i `src/journal.js`: presentació i cerca localitzada. Sense JS, articles i enllaços continuen accessibles.
- `build.py`: reutilitza capçalera, footer, formulari i configuració SEO de la web.
- `scripts/vercel_config.py`: genera les rutes publicades, sense catch-all ni canvis de DNS.

Els noms propis, títols originals de fonts externes i avisos obligatoris de llicència es conserven quan correspon. El text editorial, els peus d’imatge i la resta de la interfície estan traduïts.

## Afegir un article

1. Crear un JSON amb ID i slug únics, tipus, categoria, autoria, SEO, entradeta, fonts i 2–3 articles relacionats. El cos només accepta paràgrafs i H2; no HTML arbitrari.
2. Contrastar afirmacions i registrar `verifiedAt`. Distingir anuncis de fabricants, evidència independent i anàlisi editorial. Documentar drets i procedència de qualsevol imatge.
3. Preparar totes les traduccions als tres catàlegs abans de publicar. Conservar les qualificacions, fonts i límits de l’original.
4. Durant la revisió: `status: draft`, `datePublished: null`. La preview amb `--journal-preview` inclou esborranys amb noindex. Aquesta opció és incompatible amb `--production`.
5. En publicar: establir `status: published` i el timestamp real amb zona horària. `eventDate` és la data dels fets; no substituir-la per la de publicació ni retrodatatar articles. Si hi ha una actualització substancial, afegir `dateModified` i explicar-la.
6. Regenerar `vercel.json`, executar proves i build de producció. Revisar diff i secrets, fer commit i push normal a main amb autorització. Vercel reconstrueix des de les fonts.

L’edició inicial cobreix els fets del 28/09 al 19/10/2026. Les dates de publicació són les reals, posteriors als fets. L’ampliació del 20/10/2026 afegeix vuit peces completes en quatre idiomes (IDs 9–16). L’arxiu mostra dates de referència, sense un rang fix: els estudis antics continuen identificats com a context. Les fonts sense data de publicació coneguda mostren la data de consulta, no una data inventada. La guia C2PA identifica explícitament la revisió de documentació.

## Comprovacions

```sh
node --test tests/*.test.cjs
python3 tests/journal.test.py
python3 tests/vercel.test.py
python3 tests/navigation.test.py
python3 tests/home.test.py
python3 build.py --output /tmp/nintec-seo-preview
python3 build.py --production --output /tmp/nintec-seo-production
python3 tests/seo.test.py /tmp/nintec-seo-preview /tmp/nintec-seo-production
python3 scripts/check_secrets.py
VERCEL_ENV=production python3 scripts/build_vercel.py
```

Les proves de Journal comproven integritat de traduccions, rutes equivalents, schema, dates, fonts i exclusió d’esborranys amb un fixture separat. Les proves de reserva no envien formularis reals. No s’ha afegit cap CMS ni servei extern de traducció.
