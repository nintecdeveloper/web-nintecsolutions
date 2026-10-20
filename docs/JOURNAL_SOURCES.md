# Verificació editorial inicial — 19 octubre 2026

Les URL, dates i tipus de font consultats són dins de cada JSON. Les fonts corporatives s’utilitzen per atribuir anuncis; no s’hi atribueix una auditoria independent ni proves executades per Nintec.

| Peça | Comprovació / decisió |
|---|---|
| Sonnet 5.5 | Anunci d’Anthropic del 28/09. Posicionament per a feina delimitada. S’ometen percentatges i tarifes per evitar barrejar el llançament i canvis posteriors. |
| Dots | Anunci d’OpenAI del 29/09: entorn al núvol, eines i desplegament gradual. No es presenta com un accés universal. |
| SynthID Bio | Anunci del 30/09 i article real de Nature, DOI 10.1038/s41586-026-10965-y, seguit des de l’enllaç de DeepMind. David Stutz, Alexander I. Cowen-Rivers i col·laboradors. Prova de concepte amb abast delimitat. |
| GPT-6 / Haiku 5.5 | Dos anuncis del 07/10, amb productes i objectius diferents. No hi ha benchmark comparatiu propi ni guanyador declarat. |
| Cyber Mission | Anunci del 08/10. Cohort inicial d’infraestructura i via de codi obert diferenciades. No equival a un servei universal de protecció. |
| Gemini 4 Argon | Ampliació del 13/10 posterior al primer anunci. Vies de producte i subscripció diferenciades; no s’afirma disponibilitat universal per país/compte. |
| Possible OPV | L’accés directe a les URL originals de Reuters no es va poder completar. S’ha contrastat la peça del 15/10 en la sindicació de Reuters a MarketScreener, que atribueix la informació a CNBC. S’ometen les xifres i afirmacions exclusives de la peça del 14/10. La font corporativa Public Benefit Fund del 18/10 s’ha consultat per HTTP i s’ha tornat a obrir al lector web abans de publicar. Petició d’ajornament ≠ decisió d’ajornar. La peça conserva el caràcter possible de l’OPV i no afirma una data oficial. |
| Maia | Comunicat del 12/10 i galeria de Microsoft. Maia 200 en producció segons la companyia; Maia 300 és un pla per a 2027. La placa mostrada és un prototip. |

## Imatges i permisos

El manifest `src/journal/images.json` és la font de veritat dels URL d’origen i condicions, i inclou dimensions i variants.

- Sonnet: visita de Peter Kyle a Anthropic (2024), Alecsandra Dragoi / DSIT, Commons/Flickr, CC BY 2.0.
- Dots: Sam Altman a TechCrunch Disrupt (2019), TechCrunch / Steve Jennings, Commons/Flickr, CC BY 2.0.
- SynthID: figura 1 del paper de Nature. L’article indica CC BY 4.0 i inclou les figures sense crèdit d’excepció. Es manté completa amb `contain` i s’identifica com un esquema científic.
- Cyber: Summit (2018), Carlos Jones / ORNL, Commons/Flickr, CC BY 2.0. Peu d’arxiu explícit: no es presenta aquesta instal·lació com a participant del programa.
- Gemini: seu de Google (2014), Anthony Quintano, Commons/Flickr, CC BY 2.0. Alternativa fotogràfica d’arxiu; no es presenta com una captura d’Argon.
- OPV: Dario Amodei a TechCrunch Disrupt (2023), TechCrunch / Kimberly White, Commons/Flickr, CC BY 2.0.
- Maia: fotografia de la placa del prototip Maia 300, Microsoft News Center. Base d’ús: secció Press de Microsoft Copyright Permissions, per a informació/anàlisi editorial. Es reprodueix completa, amb el nom del producte, enllaç a Microsoft i la llegenda requerida «Used with permission from Microsoft.» No s’afirma haver rebut una autorització individual.

Les pàgines de Commons indiquen la revisió de la llicència de Flickr. No s’utilitzen fotografies de Reuters ni d’altres diaris. Les imatges es redimensionen i es converteixen a WebP; s’han conservat els blocs EXIF/XMP disponibles. Els retalls de miniatures s’indiquen al manifest. Les figures i la placa de Microsoft no es retallen.

## Excepció visual documentada

La peça GPT-6 / Haiku utilitza una composició tipogràfica HTML/CSS. No s’ha pogut establir el permís aplicable a les portades candidates dels anuncis. No s’han descarregat ni publicat aquestes portades, ni s’han generat fotos amb IA. La imatge social d’aquesta peça usa l’asset de marca existent.

La biblioteca de Google permet reutilitzar les imatges de la seva pàgina amb crèdit, però no s’ha estès aquest permís a la portada d’Argon. Per això s’utilitza la fotografia amb llicència oberta.
