# GitHub → Vercel → Preview

Repositorio fuente preparado; no se han modificado DNS, Wix ni la publicación privada de Sites. El remoto Git existente sigue siendo Sites: no se ha creado ni enlazado un repositorio de GitHub.

## Importación

Subir este directorio de proyecto como raíz de un repositorio de GitHub (no el ZIP estático ni la carpeta padre con adjuntos). Importarlo en Vercel. Framework: Other; build: `python3 scripts/build_vercel.py`; output: `dist`; install: vacío. `vercel.json` contiene estos valores. No requiere dependencias Python externas: las imágenes optimizadas ya están versionadas. No añadir dominios ni modificar DNS todavía.

Para que esta revisión sea Preview, usar una rama distinta de la rama de producción configurada en Vercel. Vercel establece `VERCEL_ENV`; el script deja noindex en Preview y mantiene los canonicals/hreflang/sitemap con `https://www.nintecsolutions.com`. También se añade X-Robots-Tag fuera del hostname final. No se necesitan tokens de GitHub/Vercel en el código ni variables privadas para generar la web.

## Rutas

Las 30 URLs CA/ES/EN se resuelven a sus propios index.html, sin fallback SPA. Los archivos robots.txt y sitemap.xml se sirven directamente. El 404.html raíz utiliza el comportamiento nativo de Vercel para rutas inexistentes, con HTTP 404. Las versiones traducidas siguen disponibles como archivos; el fallback global es catalán.

Los aliases de Wix y .dc.html proceden de `seo.py`, con status 301. Incluyen las barras finales y normalización de index.html. Las reglas específicas del dominio sin www preceden al redirect general para evitar un salto adicional en las rutas antiguas. HTTPS lo proporciona Vercel; el hostname sin www redirige permanentemente a www una vez ambos dominios estén conectados. No existe redirección global del hostname Preview al dominio que todavía sirve Wix.

Se conservan nosniff, Referrer-Policy, Permissions-Policy, caché de assets y noindex legal. `_headers` y `_redirects` se eliminan únicamente de la salida del adaptador Vercel; sus reglas viven en vercel.json. El build original de Sites permanece intacto.

Fuentes oficiales: [configuración Vercel](https://vercel.com/docs/project-configuration/vercel-json), [404 estático](https://vercel.com/kb/guide/custom-404-page). Las reglas, salidas y destinos se prueban localmente; la respuesta HTTP de la plataforma se debe verificar en el primer Preview, todavía no creado.

## Comprobaciones

- `python3 scripts/check_secrets.py`: archivos versionados, nuevos no ignorados y blobs históricos alcanzables. No imprime valores sensibles. La configuración Supabase publishable es deliberadamente pública y no equivale a service_role; las pruebas funcionales usan transporte simulado. El escaneo por patrones no acredita permisos/RLS del servicio remoto.
- `python3 scripts/vercel_config.py --check`: evita divergencias con la política SEO existente. Regenerar sin --check si cambia esa política.
- `python3 tests/vercel.test.py`: builds Preview y Production, URLs, sitemap, robots, aliases, canonical, noindex e ignore rules.
- `python3 build.py`, `python3 build.py --production --output ../nintec360-production`, `python3 tests/validate.py`, `python3 tests/validate.py ../nintec360-production`, `python3 tests/seo.test.py dist ../nintec360-production`.
- `node --test tests/*.cjs`: todas las pruebas existentes.

`.gitignore` excluye .env y variantes, claves privadas, credenciales, carpetas privadas, configuración local de Vercel y archivos generados. Nunca subir la carpeta padre del proyecto ni adjuntos personales.
