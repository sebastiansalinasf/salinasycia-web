# www.salinasycia.cl

Sitio de Salinas & Cía. Abogados (Salinas y Compañía Abogados Limitada). **En borrador**: no publicado.

- `site/` — sitio generado (lo que se publica).
- `tools/build.py` — genera todas las páginas desde los datos del estudio. `BORRADOR = True` agrega noindex y bloquea robots.txt.
- `tools/publicar.sh` — reconstruye HTML y CSS.
- Textos fuente: documento de la etapa 2 en Claude.

## Reglas de contenido
- No inventar datos; todo hecho respaldado por documentos o fuentes públicas.
- Sin RUT, domicilios particulares ni datos de clientes. Sin promesas de resultados ni comparaciones (Código de Ética, Colegio de Abogados).
- El sitio no menciona ni enlaza a REGIS.
- Abogados asociados sin redes personales; contacto siempre al estudio.

## Idiomas y visibilidad (buscadores e IA)
- Cada página existe en español (`/`) y en inglés (`/en/`), generadas desde la misma fuente: `tools/contenido.py` (ES) y `tools/contenido_en.py` (EN). **Todo cambio de contenido se hace en ambos archivos.** Textos fijos de la interfaz en inglés: lista `UI_EN` en `build.py`.
- Cada página lleva: título y descripción únicos, canonical, hreflang (es-CL, en, x-default), Open Graph, JSON-LD (LegalService, Service, FAQPage, Person, BlogPosting, BreadcrumbList).
- Se generan `sitemap.xml` (con hreflang), `llms.txt` (resumen ES/EN para IA), `robots.txt` (en borrador bloquea todo; al lanzar permite GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.) y `favicon.svg`.
- Vista previa: `python3 tools/build.py --vista-previa <carpeta>`.
