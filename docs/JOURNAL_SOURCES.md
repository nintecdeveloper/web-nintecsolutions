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

## Ampliació del 20 d’octubre de 2026 · articles 9–16

Vuit peces noves, escrites i traduïdes íntegrament a CA/ES/EN/NL. No es presenten com a vuit notícies del dia: la portada combina anàlisi i context i cada article conserva la data del fet o estudi. Els exemples de pressupostos, reunions, robòtica i proves de permisos són hipotètics, explícitament identificats. No es documenten proves pròpies, clients nous ni mètriques de Nintec.

| ID | Tema | Base factual revisada | Límit editorial |
| --- | --- | --- | --- |
| 9 | Mistral Large 4 | Mistral, 06/10/2026, https://mistral.ai/news/mistral-large-4/ | API en preview; pesos previstos a finals de mes, no publicats segons l’anunci revisat. Anàlisi de control operatiu, sense benchmarks propis. |
| 10 | Gemini Robotics 2 | Google DeepMind, 30/07/2026, https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/ i documentació del producte | Capacitats atribuïdes al fabricant; demostració i torn de feina no són equivalents. |
| 11 | Prompt injection | Anthropic, 24/11/2025, https://www.anthropic.com/research/prompt-injection-defenses i OWASP https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | Context defensiu; no incident propi ni promesa d’immunitat. |
| 12 | Cerca i clics | Pew, 22/07/2025, https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/ i Google Search Central https://developers.google.com/search/docs/appearance/ai-features | 900 adults EUA, navegació març i recuperació abril 2025; associació observada, no experiment causal ni predicció del trànsit actual. |
| 13 | IA i feina | Anthropic Economic Index, 15/01/2026, https://www.anthropic.com/research/economic-index-primitives i ILO, 20/05/2025, https://www.ilo.org/publications/generative-ai-and-jobs-refined-global-index-occupational-exposure | Ús, exposició i ocupació són mesures diferents; sense extrapolar acomiadaments. |
| 14 | Energia | IEA, 16/04/2026, https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary | Eficiència per tasca vs consum agregat; exemple aritmètic explícitament hipotètic. |
| 15 | MCP | Arquitectura oficial https://modelcontextprotocol.io/docs/learn/architecture i Linux Foundation, 09/12/2025, https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | Protocol compartit no és certificació de cada servidor ni permisos universals. |
| 16 | C2PA | https://c2pa.org/principles/ i https://c2pa.org/faqs/, consultats 20/10/2026 | Data de revisió identificada com a tal; procedència no és garantia de veritat. No afirmem haver verificat C2PA en les imatges del Journal. |

Les fonts sense data coneguda de publicació mostren «Consulta» (localitzat) amb la data real de verificació. Les dates de consulta no es fan passar per dates de publicació de la font. Els títols originals de les fonts i els noms d’autoria es mantenen.

### Fotografies incorporades

`src/journal/images.json` conserva URL de l’original, pàgina de drets, autoria, llicència, mides, modificacions i data de verificació. Derivats WebP 480/960/1440, sense generació d’imatges. Els fitxers amb ShareAlike mantenen la mateixa llicència; el crèdit públic enllaça la llicència i declara l’adaptació/retall.

- **Mistral:** Arthur Mensch amb Narendra Modi, París, juny 2026. Prime Minister’s Office, Government of India / Press Information Bureau, GODL–India. Fotografia d’arxiu, no llançament del model. Retall horitzontal de l’original (0,650,2200,2025), redimensionament i WebP; atribució i llicència visibles.
- **Robòtica:** KUKA a Innorobo 2015, Scailyna, CC BY-SA 4.0. No és un robot ni una demostració de Gemini. Orientació EXIF normalitzada i dimensions adaptades.
- **Energia:** Charles Devaux, Power lines (Unsplash), 2016, CC0 1.0. Publicació anterior al canvi de llicència d’Unsplash del 2017, documentada a Commons. No s’atribueix a un centre de dades concret.
- **MCP:** Network switches, Jon ‘ShakataGaNai’ Davis, 2008, CC BY-SA 3.0. Metàfora de connexió identificada; MCP és programari.
- **C2PA:** Camera (Unsplash), Alexander Wang / darkleiv, 04/03/2017, CC0 1.0 anterior al canvi de llicència. No s’afirma compatibilitat C2PA del dispositiu.
- **Altres peces:** es reutilitzen les fotografies acreditades de Google (cerca), reunió a Anthropic (seguretat) i Dario Amodei (Economic Index), amb els peus d’arxiu existents.

La portada prioritza Mistral, cerca i robòtica. La graella conté els 16 articles; la selecció d’anàlisi conserva tres targetes per no ampliar innecessàriament el bloc. L’arxiu elimina el rang fix inicial i conserva els 16 elements ordenats per data de referència.
