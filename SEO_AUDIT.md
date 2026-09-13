# Auditoría SEO — Nintec Digital Solutions

Fecha: 13 de septiembre de 2026. Alcance: código del rediseño, revisión privada en Sites y comprobación HTTP del dominio público. Los PASS del paquete no significan que la web pública haya sido sustituida ni que Google la haya indexado.

## Estado inicial y prioridades, antes de implementar

| Prioridad | Hallazgo | Resolución |
|---|---|---|
| CRITICAL | El dominio público sirve Wix, no este proyecto. `/nintec360/` devuelve 404. | Paquete de producción independiente; entrega al responsable del dominio. No se cambian DNS ni hosting. |
| HIGH | `https://nintecsolutions.com/` redirige 301 a `https://www.nintecsolutions.com/`; HTTP sin www necesita dos saltos. | Origen canónico de producción con www; reglas 301 preparadas. Aplicación en proveedor pendiente. |
| HIGH | Wix muestra `WEB \| My Site 1`; su sitemap contiene 18 URLs antiguas. | Metadatos por página e inventario de redirecciones por contenido confirmado, no por nombre del slug. |
| HIGH | No había separación explícita de indexación entre revisión y producción. | Builds distintos; revisión noindex, producción indexable salvo borradores legales. |
| MEDIUM | Imágenes originales pesadas; retrato mayor de 640.938 bytes. | WebP responsive, dimensiones, lazy loading y logotipo optimizado. |
| MEDIUM | Metadatos sociales incompletos y datos estructurados limitados. | Open Graph, Twitter, imagen de marca y grafo JSON-LD. |
| MEDIUM | Intenciones de IA, llamadas y OCR poco explícitas. | Introducciones y FAQs precisas en los tres idiomas; enlaces contextuales. |
| LOW | Navegación jerárquica y recursos compartidos mejorables. | Breadcrumbs discretos; scripts según página; bootstrap de idioma pequeño inline. |

La inspección inicial quedó registrada antes de modificar el código. La web ya entregaba todo el contenido en HTML, tenía 30 páginas localizadas y no dependía de fuentes remotas ni de librerías frontend pesadas. Se conserva el generador Python, HTML/CSS/JS, reservas, formularios, diseño y círculo de cuatro segundos.

## Arquitectura e intención por página

Cada ruta existe en catalán (raíz), castellano (`/es/`) e inglés (`/en/`). Se mantienen los slugs para evitar cambios innecesarios de enlaces.

| Ruta base | Intención principal | Decisión |
|---|---|---|
| `/` | Agentes IA y automatización para empresas; marca Nintec | Presentación general y acceso al producto |
| `/nintec360/` | Agente IA para llamadas, WhatsApp, email, CRM y seguimiento comercial | Página principal del producto; FAQs de llamadas salientes y canales |
| `/casos/` | Automatización en restaurantes, inmobiliarias y retail | Tres casos sustanciales con procesos y resultados ya corroborados |
| `/equip/` | Quién es Nintec Solutions, equipo en Mataró | Confianza, personas y datos de contacto existentes |
| `/contacte/` | Auditoría de automatización para empresas | Conversión y reserva existente |
| `/finance/` | OCR de facturas y automatización administrativa con IA | Servicio financiero específico |
| `/compliance/` | Nintec Compliance | Mantiene claramente su estado próximo lanzamiento |
| `/privacitat/`, `/cookies/`, `/termes/` | Información legal | Noindex y fuera del sitemap: contienen notas de trabajo pendientes de validación |

Son 7 páginas de marketing por 3 idiomas: **21 URLs en el sitemap de producción**. Las 9 legales continúan accesibles mediante enlaces. No se crean páginas sectoriales vacías ni artículos repetidos para multiplicar keywords.

## Implementación

- Canonical propio por URL e idioma, con origen verificado `https://www.nintecsolutions.com` en producción. La revisión privada se referencia a sí misma y lleva noindex.
- Hreflang recíproco ca/es/en y x-default catalán en HTML y sitemap. HTML lang correcto y contenido traducido generado en servidor; la preferencia del usuario sigue funcionando antes del primer render.
- Títulos y descripciones específicos por página y localizados; un H1 por página y enlaces internos comprobados. Breadcrumbs visibles y estructurados en páginas interiores.
- `Organization`, `WebSite`, `WebPage`, `BreadcrumbList` y `Service` donde procede. Solo identidad/contactos del proyecto; sin reseñas, ratings, ofertas, certificaciones ni precios inventados.
- Open Graph y Twitter con imagen 1200×630 construida a partir del logotipo existente; favicon correcto.
- Robots permite rastrear páginas y recursos para leer noindex; no se utiliza robots como protección privada. La autenticación de Sites conserva el acceso exclusivo del propietario. [Google: noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing).
- 404 HTML traducida, noindex y enlaces de recuperación. El servidor final debe conservar respuesta HTTP 404 para URLs inexistentes, sin fallback 200 de SPA.
- `_redirects` y `_headers` preparados para hosting estático compatible. No son configuración ejecutada en Wix: hay que aplicarlos o traducirlos al proveedor de producción.
- Verificación opcional mediante `GOOGLE_SITE_VERIFICATION` al construir producción, solo con un token real proporcionado por Search Console. No se ha añadido ningún token inventado.
- No se añaden Analytics, GTM, píxeles ni seguimiento de visitantes.

Los enlaces hreflang ayudan a identificar variantes lingüísticas; no sustituyen el contenido traducido. [Documentación de Google](https://developers.google.com/search/docs/specialty/international/localized-versions). El sitemap facilita el descubrimiento, pero no garantiza indexación. [Google: sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview).

## Rendimiento y pruebas

Las cinco fotografías originales sumaban **843.438 bytes**. Sus variantes WebP mayores suman **89.046 bytes** (aproximadamente 89% menos peso de archivo, no una promesa de mejora equivalente de velocidad). Se conservan originales en fuente y se publican variantes responsive con tamaños intrínsecos. El logotipo de cabecera usa una variante pequeña; el original queda disponible para identidad estructurada.

La portada de producción ocupa 29.675 bytes de HTML sin comprimir. `api.js` solo se solicita en contacto y compliance; el reproductor del círculo solo en portada y producto. El resto del JavaScript se carga diferido. No se añade una dependencia de build para optimizar imágenes: los resultados WebP están versionados.

Validación realizada:

- Build privado y build de producción: 30 páginas cada uno.
- Validación de enlaces, anclas, assets, H1, títulos, canonicals, descripciones, idiomas, IDs y etiquetas de formularios en ambas salidas.
- Pruebas SEO en ambas salidas: metadata por idioma, hreflang recíproco, grafo JSON-LD, srcset, sitemap, robots, destinos de redirecciones y marcado 404.
- 14 pruebas Node de idioma, reservas y reproductor: pasan. Escrituras con transporte simulado; ninguna reserva de prueba enviada al servicio real.
- Navegador local: producto en móvil y equipo en escritorio inspeccionados visualmente; portada, casos, equipo, contacto y producto ES/EN sin desbordamiento horizontal a 375 px de contenido. Idioma persistente comprobado durante navegación. Sin imágenes cargadas rotas en estas comprobaciones.
- No hay datos de campo de este nuevo sitio en Search Console/CrUX. **Core Web Vitals: PARTIAL**. No se ha realizado una medición Lighthouse ni se inventan valores LCP, INP o CLS. Habrá que medir tras publicar en el dominio real. [Google: Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals).

## Dominio público y redirecciones

La respuesta pública comprobada el 13/09/2026 es Wix, con canonical de portada `https://www.nintecsolutions.com`. Robots y sitemap devuelven 200. El sitemap es un índice de Wix, no el generado aquí. Una URL inexistente devuelve 404. `/nintec360/` aún devuelve 404.

Mapa de URLs antiguas confirmado por títulos públicos:

| Wix | Destino preparado |
|---|---|
| `/the-card` | `/es/finance/` |
| `/privacy-policy` | `/es/nintec360/` (el contenido actual es producto, pese al slug) |
| `/accessibility-statement`, `/blank`, `/blank-1`, `/blank-2` | `/es/nintec360/#canals` |
| `/blank-3`, `/blank-4`, `/blank-6` | `/es/nintec360/` |
| `/help-center`, `/blank-5`, `/blank-7`, `/blank-8` | `/es/compliance/` |
| `/blank-9` | `/es/privacitat/` |
| `/blank-10` | `/es/cookies/` |
| `/blank-11` | `/es/termes/#titular` |

`/download-the-app` figura en el sitemap antiguo, pero la lectura HTTP falló con un error TLS transitorio; queda pendiente confirmar su contenido antes de asignarle un destino. No se redirige por intuición. Se conservan también los aliases heredados `.dc.html`, y se preparan normalizaciones index.html y barra final. Las reglas de hostname deben combinarse con normalización de ruta en el proveedor para evitar cadenas cuando concurran ambas condiciones.

## Riesgos y pendientes reales

1. **Despliegue público externo**: Sites privado no actualiza Wix. No hay acceso autenticado al proveedor/DNS para sustituir la web. El ZIP de producción contiene archivos estáticos y reglas, no un instalador de Wix. Si se requiere una migración de hosting, debe decidirla el propietario; aquí no se ha ejecutado.
2. **Search Console**: sin acceso ni verificación, envío de sitemap ni solicitudes de indexación. No hay evidencia de que Google haya indexado el rediseño.
3. **Identidad y textos legales**: se conservan los contactos aprobados del proyecto (info@nintecsolutions.com, +34 684 76 68 44). Wix muestra otros: revisar consistencia en el lanzamiento. Los borradores legales necesitan información definitiva; no se inventa NIF ni se promete cumplimiento normativo.
4. **HTTP de producción**: verificar reglas 301, cabeceras, 404 real, compresión y caché después del despliegue en el proveedor elegido. El test de archivos no acredita ejecución de reglas en dicho proveedor.
5. **Contenido futuro**: potenciales guías sobre llamadas fuera de horario, WhatsApp con CRM, reactivación, venta/pago configurable, automatización para restaurantes, inmobiliarias, retail y OCR de facturas. Publicar solo con explicación propia, evidencia y diferenciación suficiente. No afirmar compatibilidad Verifactu, certificaciones o resultados adicionales sin verificar.

## Estado de entrega

| Área | Estado |
|---|---|
| SEO técnico global | PARTIAL: implementación validada, dominio público pendiente |
| Indexabilidad | PARTIAL: paquete preparado, Wix aún activo |
| Sitemap, robots, canonicals, hreflang, structured data, metadata | PASS en paquete de producción |
| Core Web Vitals / performance | PARTIAL: optimizaciones y presupuesto de archivos; sin datos de campo |
| Mobile SEO | PASS en comprobaciones descritas |
| Build producción | PASS |

Para publicar, usar el paquete de producción; para continuar trabajando en Sites, mantener el build privado predeterminado. Consultar `GOOGLE_INDEXING_CHECKLIST.md` para los cinco pasos restantes.
