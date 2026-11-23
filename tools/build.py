# -*- coding: utf-8 -*-
"""Genera el sitio estático de www.salinasycia.cl en site/.

Mientras BORRADOR = True, todas las páginas llevan noindex y robots.txt bloquea el sitio.
Al lanzar: BORRADOR = False, reconstruir y publicar.
"""
import json, os, html

BORRADOR = True
BASE = "https://www.salinasycia.cl"
ROOT = os.path.join(os.path.dirname(__file__), "..")
SITE = os.path.join(ROOT, "site")
PEND = '<mark class="rounded bg-copper-300/30 px-1 text-inherit">[PENDIENTE: {}]</mark>'

ESTUDIO = {
    "nombre": "Salinas & Cía. Abogados",
    "razon_social": "Salinas y Compañía Abogados Limitada",
    "fundacion": "2011",
    "calle": "Av. Presidente Kennedy 5600, oficina 305",
    "comuna": "Vitacura",
    "ciudad": "Santiago",
    "instagram": "https://www.instagram.com/salinasyciaabogados/",
    "correo": "contacto@salinasycia.cl",
    "telefono": None,    # [PENDIENTE]
}

# Áreas de práctica: slug, nombre, línea breve. Las 6 primeras se destacan en portada.
AREAS = [
    ("derecho-corporativo-y-societario", "Corporativo y societario", "Constitución, modificación y orden de sociedades; pactos de accionistas."),
    ("gobierno-corporativo-y-empresas-familiares", "Empresas familiares y gobierno corporativo", "Protocolos familiares, directorios y sucesión en la empresa."),
    ("derecho-inmobiliario", "Derecho inmobiliario", "Estudios de títulos, compraventas, arriendos, embargos y remates."),
    ("herencias-y-sucesiones", "Herencias y planificación sucesoria", "Posesión efectiva, partición de bienes y testamentos."),
    ("derecho-de-familia", "Derecho de familia", "Divorcios, alimentos y cuidado personal, con reserva y criterio."),
    ("derecho-del-consumidor-y-policia-local", "Consumidor y Policía Local", "Reclamos de consumo, accidentes de tránsito y sanciones municipales."),
    ("contratos-y-negociacion", "Contratos y negociación", "Redacción, revisión y negociación de contratos; riesgos legales."),
    ("litigacion-civil", "Litigación civil", "Juicios civiles con una estrategia definida desde el inicio."),
    ("recursos-constitucionales", "Recursos constitucionales", "Recursos de protección y de amparo ante las Cortes."),
    ("derecho-laboral", "Derecho laboral", "Trabajadores y empresas: despidos, finiquitos y juicios del trabajo."),
    ("derecho-administrativo-y-regulatorio", "Administrativo, regulatorio y ambiental", "Permisos, concesiones, derecho ambiental y defensa ante organismos del Estado."),
    ("asesoria-legal-permanente", "Asesoría legal permanente", "Planes mensuales de asesoría para empresas y familias."),
]

EQUIPO = [
    {"slug": "sebastian-salinas", "nombre": "Sebastián Salinas Fuenzalida", "cargo": "Socio fundador",
     "materias": "Empresa, gobierno corporativo, inmobiliario y litigación", "foto": "assets/sebastian-salinas-fuenzalida.jpg"},
    {"slug": "felipe-lanchares", "nombre": "Felipe Lanchares Pérez", "cargo": "Abogado asociado",
     "materias": "Administrativo, regulatorio y ambiental", "foto": None},
    {"slug": "luis-salinas-correa", "nombre": "Luis Guillermo Salinas Correa", "cargo": "Abogado asociado",
     "materias": "Familia y protección de niños, niñas y adolescentes", "foto": None},
]


MISION = ("Desde 2011 asesoramos a personas, familias, empresarios y empresas con una mirada integral de sus asuntos, "
          "de lo personal a lo empresarial. Construimos con cada cliente una relación cercana y de confianza, con un abogado "
          "responsable de principio a fin, que combina criterio jurídico y visión de negocios para que el cliente decida informado y a tiempo.")
VISION = ("Ser el estudio de cabecera de las familias y empresas que confían en nosotros: el lugar donde resuelven sus asuntos "
          "legales, personales y empresariales, en una relación que perdura en el tiempo.")

NAV = [("/areas/", "Áreas"), ("/equipo/", "Equipo"), ("/estudio/", "El Estudio"), ("/blog/", "Blog"), ("/contacto/", "Contacto")]


def e(t):
    return html.escape(t, quote=True)


def head(title, desc, path, jsonld=None):
    robots = "noindex, nofollow" if BORRADOR else "index, follow, max-image-preview:large"
    ld = ""
    if jsonld:
        ld = '<script type="application/ld+json">\n' + json.dumps(jsonld, ensure_ascii=False, indent=1) + "\n</script>"
    return f"""<!DOCTYPE html>
<html lang="es-CL">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}" />
  <meta name="robots" content="{robots}" />
  <link rel="canonical" href="{BASE}{path}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(desc)}" />
  <meta property="og:url" content="{BASE}{path}" />
  <meta property="og:locale" content="es_CL" />
  <meta property="og:image" content="{BASE}/assets/og-salinasycia.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="theme-color" content="#06132A" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{rel(path)}assets/styles.css" />
  {ld}
</head>"""


def rel(path):
    """Prefijo relativo para que el sitio funcione en vista previa y en producción."""
    depth = path.strip("/").count("/") + 1 if path.strip("/") else 0
    return "../" * depth


def header(path):
    r = rel(path)
    items = "".join(f'<li><a class="hover:text-white" href="{r}{h.strip("/")}/">{t}</a></li>' for h, t in NAV)
    items_movil = "".join(f'<li><a class="block rounded-lg px-3 py-2 hover:bg-white/5 hover:text-white" href="{r}{h.strip("/")}/">{t}</a></li>' for h, t in NAV)
    return f"""
<body class="bg-paper font-sans text-navy-900 antialiased">
{'<div class="bg-copper-500 py-1.5 text-center text-xs font-semibold tracking-wider text-white">BORRADOR · Vista previa privada, no publicada</div>' if BORRADOR else ''}
<header class="sticky top-0 z-50 border-b border-white/10 bg-navy-950/95 backdrop-blur">
  <nav class="mx-auto flex max-w-6xl items-center justify-between px-6 py-4 lg:px-8" aria-label="Principal">
    <a href="{r or './'}" class="leading-none text-white">
      <span class="font-serif text-2xl">Salinas <span class="text-copper-400">&amp;</span> Cía.</span>
      <span class="mt-1 block text-[0.62rem] font-semibold uppercase tracking-[0.35em] text-slate2-400">Abogados</span>
    </a>
    <ul class="hidden gap-8 text-sm text-slate2-300 md:flex">{items}</ul>
    <a href="{r}contacto/" class="hidden rounded-full border border-copper-500/60 px-4 py-2 text-xs font-semibold uppercase tracking-wider text-copper-300 hover:bg-copper-500 hover:text-white md:inline-block">Conversemos</a>
    <details class="relative md:hidden">
      <summary class="cursor-pointer list-none rounded-full border border-copper-500/60 px-4 py-2 text-xs font-semibold uppercase tracking-wider text-copper-300">Menú</summary>
      <ul class="absolute right-0 mt-3 w-56 space-y-1 rounded-2xl bg-navy-900 p-4 text-sm text-slate2-300 shadow-xl ring-1 ring-white/10">{items_movil}</ul>
    </details>
  </nav>
</header>
<main>"""


def contacto_datos(dark=True):
    E = ESTUDIO
    correo = f'<a href="mailto:{E["correo"]}" class="hover:text-copper-300">{E["correo"]}</a>' if E["correo"] else PEND.format("correo general")
    tel = E["telefono"] or PEND.format("teléfono / WhatsApp")
    return f"""<ul class="space-y-3 text-sm">
      <li><span class="text-slate2-400">Dirección:</span> {E['calle']}, {E['comuna']}, {E['ciudad']}</li>
      <li><span class="text-slate2-400">Correo:</span> {correo}</li>
      <li><span class="text-slate2-400">Teléfono:</span> {tel}</li>
    </ul>"""


def footer(path):
    r = rel(path)
    E = ESTUDIO
    return f"""
</main>
<footer class="bg-navy-950 text-slate2-300">
  <div class="mx-auto grid max-w-6xl gap-10 px-6 py-14 sm:grid-cols-3 lg:px-8">
    <div>
      <p class="font-serif text-2xl text-white">Salinas <span class="text-copper-400">&amp;</span> Cía. Abogados</p>
      <p class="mt-3 text-sm text-slate2-400">{E['razon_social']}<br />Desde {E['fundacion']}</p>
    </div>
    <div>{contacto_datos()}</div>
    <div class="text-sm">
      <ul class="space-y-2">
        <li><a class="hover:text-copper-300" href="{E['instagram']}" target="_blank" rel="noopener">Instagram @salinasyciaabogados ↗</a></li>
        <li><a class="hover:text-copper-300" href="https://www.sebastiansalinas.cl/" target="_blank" rel="noopener">sebastiansalinas.cl ↗</a></li>
        <li><a class="hover:text-copper-300" href="https://dunora.ai/" target="_blank" rel="noopener">Dunora ↗</a></li>
        <li><a class="hover:text-copper-300" href="{r}privacidad/">Política de privacidad</a></li>
      </ul>
    </div>
  </div>
  <p class="border-t border-white/10 py-6 text-center text-xs text-slate2-500">© 2026 {E['razon_social']} · {E['ciudad']}, Chile</p>
</footer>
</body>
</html>
"""


def jsonld_estudio():
    E = ESTUDIO
    return {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "@id": BASE + "/#estudio",
        "name": E["nombre"],
        "legalName": E["razon_social"],
        "url": BASE + "/",
        "foundingDate": E["fundacion"],
        "founder": {"@id": "https://www.sebastiansalinas.cl/#person"},
        "address": {"@type": "PostalAddress", "streetAddress": E["calle"], "addressLocality": E["comuna"],
                    "addressRegion": "Región Metropolitana", "addressCountry": "CL"},
        "areaServed": "Chile",
        "knowsAbout": [a[1] for a in AREAS],
        "sameAs": [E["instagram"]],
        "email": E["correo"],
        "image": BASE + "/assets/og-salinasycia.jpg",
    }


def iniciales(nombre):
    p = nombre.split()
    return (p[0][0] + p[1][0]).upper()


def portada():
    path = "/"
    r = rel(path)
    areas = "".join(f"""
      <a href="{r}areas/{s}/" class="group rounded-2xl border border-slate2-100 bg-white p-7 transition hover:border-copper-400 hover:shadow-lg">
        <h3 class="font-serif text-2xl leading-snug text-navy-900">{n}</h3>
        <p class="mt-3 text-sm leading-relaxed text-navy-800/80">{d}</p>
        <span class="mt-5 inline-block text-xs font-semibold uppercase tracking-wider text-copper-600 group-hover:text-copper-500">Ver área →</span>
      </a>""" for s, n, d in AREAS)
    otras = " · ".join(f'<a class="hover:text-copper-600" href="{r}areas/{s}/">{n}</a>' for s, n, d in AREAS[6:])

    def tarjeta(m):
        foto = (f'<img src="{m["foto"]}" alt="{e(m["nombre"])}, {m["cargo"].lower()} de Salinas &amp; Cía. Abogados" width="976" height="1300" loading="lazy" class="aspect-[4/5] w-full rounded-xl object-cover object-top" />'
                if m["foto"] else
                f'<div class="relative flex aspect-[4/5] w-full items-center justify-center rounded-xl bg-navy-900 font-serif text-5xl text-copper-300" aria-hidden="true">{iniciales(m["nombre"])}<span class="absolute bottom-4 font-sans text-xs text-slate2-400">Foto pendiente</span></div>')
        return f"""
      <a href="{r}equipo/{m['slug']}/" class="group block">
        {foto}
        <p class="eyebrow mt-5 text-copper-600">{m['cargo']}</p>
        <h3 class="mt-1 font-serif text-2xl group-hover:text-copper-600">{m['nombre']}</h3>
        <p class="mt-1 text-sm text-navy-800/70">{m['materias']}</p>
      </a>"""
    equipo = "".join(tarjeta(m) for m in EQUIPO)

    body = f"""
<!-- HERO -->
<section class="relative overflow-hidden bg-navy-950 pb-24 pt-20 text-white sm:pb-28 sm:pt-28">
  <div aria-hidden="true" class="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,rgba(184,115,51,.18),transparent_55%)]"></div>
  <div class="relative mx-auto grid max-w-6xl items-center gap-14 px-6 lg:grid-cols-12 lg:px-8">
    <div class="lg:col-span-7">
      <p class="eyebrow flex items-center gap-3 text-copper-400"><span class="h-px w-10 bg-copper-500"></span>Estudio jurídico · Santiago · Desde 2011</p>
      <h1 class="mt-6 font-serif text-5xl leading-[1.05] sm:text-6xl">Asesoría jurídica integral para empresas, familias y personas</h1>
      <p class="mt-6 max-w-xl text-lg leading-relaxed text-slate2-300">Desde 2011 acompañamos a empresarios, empresas familiares y personas en sus decisiones legales: sociedades, contratos, patrimonio inmobiliario, conflictos y relación con el Estado. Un mismo equipo, con abogados especialistas cuando el asunto lo requiere.</p>
      <div class="mt-10 flex flex-wrap gap-4">
        <a href="{r}contacto/" class="rounded-full bg-copper-500 px-6 py-3 text-sm font-semibold text-white hover:bg-copper-600">Conversemos</a>
        <a href="{r}areas/" class="rounded-full border border-white/20 px-6 py-3 text-sm font-semibold text-white hover:border-copper-400">Ver áreas de práctica</a>
      </div>
    </div>
    <div class="lg:col-span-5">
      <div class="relative mx-auto max-w-sm">
        <div aria-hidden="true" class="absolute -inset-3 rounded-[2rem] border border-copper-500/30"></div>
        <img src="assets/edificio-kennedy-5600-vertical.webp" alt="Edificio de oficinas en Av. Presidente Kennedy 5600, Vitacura, donde se ubica Salinas &amp; Cía. Abogados" width="900" height="1200" fetchpriority="high" class="relative aspect-[4/5] w-full rounded-[1.6rem] object-cover ring-1 ring-white/10" />
      </div>
    </div>
  </div>
  <dl class="relative mx-auto mt-20 grid max-w-6xl grid-cols-1 gap-px overflow-hidden rounded-2xl bg-white/10 sm:grid-cols-3">
    <div class="bg-navy-950 p-6"><dt class="text-xs uppercase tracking-wider text-slate2-400">Fundado en</dt><dd class="mt-2 font-serif text-4xl text-copper-300">2011</dd></div>
    <div class="bg-navy-950 p-6"><dt class="text-xs uppercase tracking-wider text-slate2-400">Áreas de práctica</dt><dd class="mt-2 font-serif text-4xl text-copper-300">12</dd></div>
    <div class="bg-navy-950 p-6"><dt class="text-xs uppercase tracking-wider text-slate2-400">Oficina</dt><dd class="mt-2 font-serif text-4xl text-copper-300">Vitacura</dd></div>
  </dl>
</section>

<!-- ÁREAS -->
<section class="py-24 sm:py-28">
  <div class="mx-auto max-w-6xl px-6 lg:px-8">
    <p class="eyebrow text-copper-600">Áreas de práctica</p>
    <h2 class="mt-4 max-w-2xl font-serif text-4xl leading-tight sm:text-5xl">Cómo podemos ayudarle</h2>
    <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">{areas}
    </div>
    <a href="{r}areas/" class="mt-10 inline-block rounded-full border border-navy-900/20 px-6 py-3 text-sm font-semibold hover:border-copper-500 hover:text-copper-600">Ver todas las áreas</a>
  </div>
</section>

<!-- ENFOQUE -->
<section class="bg-white py-24 sm:py-28">
  <div class="mx-auto grid max-w-6xl gap-14 px-6 lg:grid-cols-12 lg:px-8">
    <div class="lg:col-span-5">
      <p class="eyebrow text-copper-600">Cómo trabajamos</p>
      <h2 class="mt-4 font-serif text-4xl leading-tight">Entender antes de decidir</h2>
      <img src="assets/edificio-kennedy-5600-detalle.webp" alt="Fachada del edificio en Av. Presidente Kennedy 5600, Vitacura" width="900" height="887" loading="lazy" class="mt-10 hidden w-full rounded-2xl object-cover lg:block" />
    </div>
    <div class="space-y-8 lg:col-span-7">
      <p class="text-lg leading-relaxed text-navy-800">Trabajamos con una idea simple: el cliente debe entender su situación legal y sus opciones antes de decidir.</p>
      <dl class="grid gap-8 sm:grid-cols-2">
        <div class="border-t-2 border-copper-500 pt-5"><dt class="font-serif text-2xl">Un abogado responsable</dt><dd class="mt-2 text-sm leading-relaxed text-navy-800/80">Cada asunto tiene un abogado a cargo, de principio a fin, que es su interlocutor directo.</dd></div>
        <div class="border-t-2 border-copper-500 pt-5"><dt class="font-serif text-2xl">Propuesta por escrito</dt><dd class="mt-2 text-sm leading-relaxed text-navy-800/80">Antes de empezar, un diagnóstico claro y una propuesta de trabajo y honorarios por escrito.</dd></div>
        <div class="border-t-2 border-copper-500 pt-5"><dt class="font-serif text-2xl">Especialistas asociados</dt><dd class="mt-2 text-sm leading-relaxed text-navy-800/80">Cuando la materia lo exige, sumamos abogados asociados con experiencia específica, coordinados por el estudio.</dd></div>
        <div class="border-t-2 border-copper-500 pt-5"><dt class="font-serif text-2xl">Reserva profesional</dt><dd class="mt-2 text-sm leading-relaxed text-navy-800/80">Toda la información que nos entrega está protegida por el secreto profesional.</dd></div>
      </dl>
    </div>
  </div>
</section>

<!-- MISIÓN Y VISIÓN -->
<section class="relative overflow-hidden bg-navy-900 py-24 text-white sm:py-28">
  <div aria-hidden="true" class="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,rgba(184,115,51,.15),transparent_60%)]"></div>
  <div class="relative mx-auto grid max-w-6xl gap-14 px-6 lg:grid-cols-2 lg:px-8">
    <div>
      <p class="eyebrow flex items-center gap-3 text-copper-400"><span class="h-px w-10 bg-copper-500"></span>Misión</p>
      <p class="mt-6 font-serif text-2xl leading-relaxed sm:text-3xl">{MISION}</p>
    </div>
    <div>
      <p class="eyebrow flex items-center gap-3 text-copper-400"><span class="h-px w-10 bg-copper-500"></span>Visión</p>
      <p class="mt-6 font-serif text-2xl leading-relaxed sm:text-3xl">{VISION}</p>
    </div>
  </div>
</section>

<!-- EQUIPO -->
<section class="py-24 sm:py-28">
  <div class="mx-auto max-w-6xl px-6 lg:px-8">
    <p class="eyebrow text-copper-600">Equipo</p>
    <h2 class="mt-4 font-serif text-4xl leading-tight sm:text-5xl">Abogados del estudio</h2>
    <div class="mt-12 grid gap-10 sm:grid-cols-2 lg:grid-cols-3">{equipo}
    </div>
  </div>
</section>

<!-- CONTACTO -->
<section class="bg-navy-950 py-24 text-white sm:py-28">
  <div class="mx-auto grid max-w-6xl gap-14 px-6 lg:grid-cols-12 lg:px-8">
    <div class="lg:col-span-5">
      <p class="eyebrow text-copper-400">Contacto</p>
      <h2 class="mt-4 font-serif text-4xl leading-tight sm:text-5xl">Conversemos</h2>
      <p class="mt-6 leading-relaxed text-slate2-300">Cuéntenos brevemente su consulta y le responderemos a la brevedad para coordinar una reunión.</p>
      <div class="mt-8 text-slate2-300">{contacto_datos()}</div>
    </div>
    <div class="lg:col-span-7">
      <img src="{r}assets/edificio-kennedy-5600-horizontal.webp" alt="Edificio en Av. Presidente Kennedy 5600, Vitacura" width="1600" height="900" loading="lazy" class="w-full rounded-2xl object-cover ring-1 ring-white/10" />
      <a href="{r}contacto/" class="mt-8 inline-block rounded-full bg-copper-500 px-8 py-4 text-sm font-semibold text-white hover:bg-copper-600">Escribir al estudio</a>
    </div>
  </div>
</section>"""
    desc = "Asesoría jurídica integral desde 2011 para empresas, familias y personas: societario, empresas familiares, inmobiliario, litigación y administrativo."
    return head("Salinas & Cía. Abogados | Estudio jurídico en Santiago", desc, path, jsonld_estudio()) + header(path) + body + footer(path)



from contenido import AREAS_DETALLE, PERFILES, POSTS
import re

NOMBRE_AREA = {a[0]: a[1] for a in AREAS}
MIEMBRO = {m["slug"]: m for m in EQUIPO}


def pend(t):
    """Convierte [PENDIENTE: x] / [CONFIRMAR: x] en marcas visibles."""
    return re.sub(r"\[(PENDIENTE|CONFIRMAR)([^\]]*)\]", lambda m: f'<mark class="rounded bg-copper-300/30 px-1 text-inherit">[{m.group(1)}{m.group(2)}]</mark>', t)


def pagina(path, titulo, desc, cuerpo, jsonld=None):
    return head(titulo, desc, path, jsonld) + header(path) + cuerpo + footer(path)


def migas(r, items):
    """items: lista de (texto, ruta relativa o None)."""
    partes = [f'<a class="hover:text-copper-300" href="{r or "./"}">Inicio</a>']
    for t, h in items:
        partes.append(f'<a class="hover:text-copper-300" href="{r}{h}">{t}</a>' if h else f'<span class="text-white">{t}</span>')
    return '<nav aria-label="Migas de pan" class="text-xs text-slate2-400">' + ' <span aria-hidden="true">/</span> '.join(partes) + '</nav>'


def ld_migas(items):
    lst = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"}]
    for i, (t, h) in enumerate(items, start=2):
        lst.append({"@type": "ListItem", "position": i, "name": t, "item": BASE + "/" + h})
    return {"@type": "BreadcrumbList", "itemListElement": lst}


def cabecera(r, eyebrow, h1, bajada, miga_items):
    return f"""
<section class="relative overflow-hidden bg-navy-950 pb-16 pt-14 text-white sm:pb-20 sm:pt-20">
  <div aria-hidden="true" class="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,rgba(184,115,51,.16),transparent_55%)]"></div>
  <div class="relative mx-auto max-w-6xl px-6 lg:px-8">
    {migas(r, miga_items)}
    <p class="eyebrow mt-8 flex items-center gap-3 text-copper-400"><span class="h-px w-10 bg-copper-500"></span>{eyebrow}</p>
    <h1 class="mt-5 max-w-4xl font-serif text-4xl leading-[1.08] sm:text-6xl">{h1}</h1>
    {f'<p class="mt-6 max-w-2xl text-lg leading-relaxed text-slate2-300">{bajada}</p>' if bajada else ''}
  </div>
</section>"""


def cta(r):
    return f"""
<section class="bg-navy-950 py-20 text-white">
  <div class="mx-auto flex max-w-6xl flex-col items-start justify-between gap-8 px-6 sm:flex-row sm:items-center lg:px-8">
    <div><h2 class="font-serif text-3xl sm:text-4xl">¿Necesita orientación sobre su caso?</h2>
    <p class="mt-3 text-slate2-300">Cuéntenos brevemente su consulta y le responderemos a la brevedad.</p></div>
    <a href="{r}contacto/" class="shrink-0 rounded-full bg-copper-500 px-8 py-4 text-sm font-semibold text-white hover:bg-copper-600">Escribir al estudio</a>
  </div>
</section>"""


def pagina_area(slug):
    a = AREAS_DETALLE[slug]
    path = f"/areas/{slug}/"
    r = rel(path)
    servicios = "".join(f'<li class="flex gap-3"><span class="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-copper-500"></span><span>{x}</span></li>' for x in a["servicios"])
    faq = "".join(f"""
      <details class="group border-b border-slate2-100 py-5">
        <summary class="flex cursor-pointer list-none items-start justify-between gap-6 font-serif text-xl text-navy-900">{q}<span class="mt-1 text-copper-500 transition group-open:rotate-45">+</span></summary>
        <p class="mt-3 leading-relaxed text-navy-800/85">{ans}</p>
      </details>""" for q, ans in a["faq"])
    vinc = ""
    if a.get("vinculado"):
        m = MIEMBRO[a["vinculado"]]
        vinc = f"""<div class="mt-10 rounded-2xl border border-slate2-100 bg-white p-6"><p class="eyebrow text-copper-600">Abogado asociado vinculado a esta materia</p>
        <a href="{r}equipo/{m['slug']}/" class="mt-2 block font-serif text-2xl hover:text-copper-600">{m['nombre']} →</a></div>"""
    posts = [p for p in POSTS if p["area"] == slug]
    art = f'<div class="mt-10 rounded-2xl border border-dashed border-slate2-300 p-6"><p class="eyebrow text-copper-600">Artículos relacionados</p><p class="mt-2 text-navy-800/80">Próximamente publicaremos artículos sobre esta materia. <a class="font-semibold text-copper-600 hover:text-copper-500" href="{r}blog/">Ir al blog →</a></p></div>'
    if posts:
        art = '<div class="mt-10"><p class="eyebrow text-copper-600">Artículos relacionados</p><ul class="mt-3 space-y-2">' + "".join(
            f'<li><a class="font-serif text-xl hover:text-copper-600" href="{r}blog/{p["slug"]}/">{p["titulo"]} →</a></li>' for p in posts) + "</ul></div>"
    otras = "".join(f'<li><a class="hover:text-copper-600" href="{r}areas/{s}/">{n}</a></li>' for s, n, d in AREAS if s != slug)
    cuerpo = cabecera(r, "Área de práctica", a["h1"], None, [("Áreas", "areas/"), (NOMBRE_AREA[slug], None)]) + f"""
<section class="py-20 sm:py-24">
  <div class="mx-auto grid max-w-6xl gap-14 px-6 lg:grid-cols-12 lg:px-8">
    <div class="lg:col-span-8">
      <p class="text-xl leading-relaxed text-navy-800">{a['intro']}</p>
      <h2 class="mt-14 font-serif text-3xl">Servicios</h2>
      <ul class="mt-6 space-y-3 text-navy-800">{servicios}</ul>
      <h2 class="mt-16 font-serif text-3xl">Preguntas frecuentes</h2>
      <div class="mt-4">{faq}</div>
      {vinc}{art}
    </div>
    <aside class="lg:col-span-4">
      <div class="sticky top-28 rounded-2xl bg-white p-7 ring-1 ring-slate2-100">
        <p class="eyebrow text-copper-600">Otras áreas</p>
        <ul class="mt-4 space-y-2 text-sm text-navy-800">{otras}</ul>
        <a href="{r}contacto/" class="mt-8 block rounded-full bg-copper-500 px-6 py-3 text-center text-sm font-semibold text-white hover:bg-copper-600">Consultar sobre esta materia</a>
      </div>
    </aside>
  </div>
</section>""" + cta(r)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": a["h1"], "serviceType": a["h1"], "description": a["intro"],
         "provider": {"@id": BASE + "/#estudio"}, "areaServed": "Chile", "url": BASE + path},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a["faq"]]},
        ld_migas([("Áreas de práctica", "areas/"), (NOMBRE_AREA[slug], f"areas/{slug}/")])]}
    return pagina(path, a["titulo_seo"], a["desc"], cuerpo, ld)


def pagina_areas():
    path = "/areas/"
    r = rel(path)
    tarjetas = "".join(f"""
      <a href="{r}areas/{s}/" class="group rounded-2xl border border-slate2-100 bg-white p-7 transition hover:border-copper-400 hover:shadow-lg">
        <h2 class="font-serif text-2xl leading-snug">{n}</h2>
        <p class="mt-3 text-sm leading-relaxed text-navy-800/80">{d}</p>
        <span class="mt-5 inline-block text-xs font-semibold uppercase tracking-wider text-copper-600">Ver área →</span>
      </a>""" for s, n, d in AREAS)
    cuerpo = cabecera(r, "Áreas de práctica", "Áreas de práctica", "Doce áreas para acompañar a empresas, familias y personas, de lo personal a lo empresarial.", [("Áreas", None)]) + f"""
<section class="py-20 sm:py-24"><div class="mx-auto grid max-w-6xl gap-6 px-6 sm:grid-cols-2 lg:grid-cols-3 lg:px-8">{tarjetas}</div></section>""" + cta(r)
    ld = {"@context": "https://schema.org", "@graph": [ld_migas([("Áreas de práctica", "areas/")])]}
    return pagina(path, "Áreas de práctica | Salinas & Cía. Abogados",
                  "Doce áreas de práctica para empresas, familias y personas: societario, inmobiliario, herencias, familia, laboral, consumidor, administrativo y más.", cuerpo, ld)


def foto_o_iniciales(r, m, clase="aspect-[4/5] w-full rounded-xl"):
    if m["foto"]:
        return f'<img src="{r}{m["foto"]}" alt="{e(m["nombre"])}, {m["cargo"].lower()} de Salinas &amp; Cía. Abogados" width="976" height="1300" loading="lazy" class="{clase} object-cover object-top" />'
    return f'<div class="relative flex {clase} items-center justify-center bg-navy-900 font-serif text-5xl text-copper-300" aria-hidden="true">{iniciales(m["nombre"])}<span class="absolute bottom-4 font-sans text-xs text-slate2-400">Foto pendiente</span></div>'


def pagina_equipo():
    path = "/equipo/"
    r = rel(path)
    socio = EQUIPO[0]
    asoc = "".join(f"""
      <a href="{r}equipo/{m['slug']}/" class="group grid gap-6 rounded-2xl bg-white p-6 ring-1 ring-slate2-100 sm:grid-cols-3">
        <div>{foto_o_iniciales(r, m)}</div>
        <div class="sm:col-span-2"><p class="eyebrow text-copper-600">{m['cargo']}</p><h3 class="mt-1 font-serif text-2xl group-hover:text-copper-600">{m['nombre']}</h3>
        <p class="mt-2 text-sm text-navy-800/80"><span class="font-semibold">Materias:</span> {m['materias']}</p><span class="mt-4 inline-block text-xs font-semibold uppercase tracking-wider text-copper-600">Ver perfil →</span></div>
      </a>""" for m in EQUIPO[1:])
    cuerpo = cabecera(r, "Equipo", "Equipo", "Un equipo de abogados con experiencia en la empresa, el sector inmobiliario y el sector público.", [("Equipo", None)]) + f"""
<section class="py-20 sm:py-24"><div class="mx-auto max-w-6xl px-6 lg:px-8">
  <p class="eyebrow text-copper-600">Socio fundador</p>
  <a href="{r}equipo/{socio['slug']}/" class="group mt-6 grid gap-10 sm:grid-cols-3">
    <div>{foto_o_iniciales(r, socio)}</div>
    <div class="sm:col-span-2"><h2 class="font-serif text-4xl group-hover:text-copper-600">{socio['nombre']}</h2>
      <p class="mt-4 text-lg leading-relaxed text-navy-800">{PERFILES[socio['slug']]['bio'][0]}</p><span class="mt-6 inline-block text-xs font-semibold uppercase tracking-wider text-copper-600">Ver perfil →</span></div>
  </a>
  <h2 class="mt-24 font-serif text-4xl">Abogados asociados</h2>
  <p class="mt-4 max-w-2xl leading-relaxed text-navy-800/85">Para materias que requieren experiencia específica, el estudio trabaja con abogados asociados. El cliente mantiene siempre un único punto de contacto con el estudio.</p>
  <div class="mt-10 grid gap-6 lg:grid-cols-2">{asoc}</div>
</div></section>""" + cta(r)
    ld = {"@context": "https://schema.org", "@graph": [ld_migas([("Equipo", "equipo/")])]}
    return pagina(path, "Equipo | Salinas & Cía. Abogados", "Conozca a los abogados de Salinas & Cía.: experiencia en empresas, sector inmobiliario y sector público.", cuerpo, ld)


def pagina_perfil(slug):
    m = MIEMBRO[slug]; pf = PERFILES[slug]
    path = f"/equipo/{slug}/"
    r = rel(path)
    bio = "".join(f'<p>{pend(x)}</p>' for x in pf["bio"])
    form = "".join(f'<li class="border-b border-slate2-100 py-3">{pend(x)}</li>' for x in pf["formacion"])
    areas = "".join(f'<li><a class="hover:text-copper-600" href="{r}areas/{s}/">{NOMBRE_AREA[s]}</a></li>' for s in pf["areas"])
    contacto = (f'<a class="hover:text-copper-600" href="mailto:{pf["correo"]}">{pf["correo"]}</a>' if pf["correo"]
                else f'<a class="hover:text-copper-600" href="mailto:{ESTUDIO["correo"]}">{ESTUDIO["correo"]}</a> · <a class="hover:text-copper-600" href="{r}contacto/">formulario</a>')
    enlaces = "".join(f'<li><a class="hover:text-copper-600" href="{u}" target="_blank" rel="noopener">{t} ↗</a></li>' for t, u in pf["enlaces"])
    cuerpo = cabecera(r, m["cargo"], m["nombre"], None, [("Equipo", "equipo/"), (m["nombre"], None)]) + f"""
<section class="py-20 sm:py-24"><div class="mx-auto grid max-w-6xl gap-14 px-6 lg:grid-cols-12 lg:px-8">
  <div class="lg:col-span-4">{foto_o_iniciales(r, m, "aspect-[4/5] w-full rounded-2xl")}
    <div class="mt-8 space-y-6 text-sm">
      <div><p class="eyebrow text-copper-600">Materias</p><ul class="mt-3 space-y-1.5">{areas}</ul></div>
      <div><p class="eyebrow text-copper-600">Contacto</p><p class="mt-3">{contacto}</p>{f'<ul class="mt-3 space-y-1.5">{enlaces}</ul>' if enlaces else ''}</div>
    </div>
  </div>
  <div class="lg:col-span-8">
    <div class="space-y-5 text-lg leading-relaxed text-navy-800">{bio}</div>
    <h2 class="mt-14 font-serif text-3xl">Formación</h2>
    <ul class="mt-4 text-navy-800">{form}</ul>
  </div>
</div></section>""" + cta(r)
    person = {"@type": "Person", "name": m["nombre"], "jobTitle": m["cargo"], "worksFor": {"@id": BASE + "/#estudio"}, "url": BASE + path}
    if slug == "sebastian-salinas":
        person["@id"] = "https://www.sebastiansalinas.cl/#person"
        person["sameAs"] = ["https://www.sebastiansalinas.cl/", "https://www.linkedin.com/in/sebastian-salinas-fuenzalida"]
        person["email"] = pf["correo"]
    else:
        person["@id"] = BASE + path + "#person"
    person["alumniOf"] = [x.split(", ")[-1].split(" (")[0] for x in pf["formacion"] if "Universi" in x]
    ld = {"@context": "https://schema.org", "@graph": [person, ld_migas([("Equipo", "equipo/"), (m["nombre"], f"equipo/{slug}/")])]}
    return pagina(path, pf["titulo_seo"], pf["desc"], cuerpo, ld)


def pagina_estudio():
    path = "/estudio/"
    r = rel(path)
    cuerpo = cabecera(r, "El Estudio", "El Estudio", "Salinas &amp; Cía. Abogados fue fundado en 2011 por Sebastián Salinas Fuenzalida para ofrecer una asesoría jurídica eficiente e integral a empresas, empresarios, familias empresarias y personas.", [("El Estudio", None)]) + f"""
<section class="py-20 sm:py-24"><div class="mx-auto grid max-w-6xl gap-12 px-6 lg:grid-cols-2 lg:px-8">
  <div class="border-l-2 border-copper-500 pl-8"><p class="eyebrow text-copper-600">Misión</p><p class="mt-5 font-serif text-2xl leading-snug">{MISION}</p></div>
  <div class="border-l-2 border-copper-500 pl-8"><p class="eyebrow text-copper-600">Visión</p><p class="mt-5 font-serif text-2xl leading-snug">{VISION}</p></div>
</div></section>
<section class="bg-white py-20 sm:py-24"><div class="mx-auto grid max-w-6xl gap-14 px-6 lg:grid-cols-12 lg:px-8">
  <div class="lg:col-span-5"><h2 class="font-serif text-4xl">Cómo trabajamos</h2>
    <img src="{r}assets/edificio-kennedy-5600-horizontal.webp" alt="Edificio en Av. Presidente Kennedy 5600, Vitacura, sede de Salinas &amp; Cía. Abogados" width="1600" height="900" loading="lazy" class="mt-8 w-full rounded-2xl object-cover" /></div>
  <div class="space-y-5 text-lg leading-relaxed text-navy-800 lg:col-span-7">
    <p>Creemos que una buena asesoría legal se nota en las decisiones del cliente: entender sus riesgos, conocer sus opciones y actuar a tiempo. Por eso trabajamos con:</p>
    <ul class="space-y-3">
      <li><strong>Un abogado responsable</strong> de cada asunto, de principio a fin.</li>
      <li><strong>Propuestas por escrito</strong>, con alcance y honorarios claros antes de empezar.</li>
      <li><strong>Especialistas asociados</strong> cuando la materia lo exige, coordinados por el estudio.</li>
      <li><strong>Reserva profesional</strong> sobre toda la información que nos entrega.</li>
    </ul>
    <p class="text-base text-navy-800/80">Razón social: {ESTUDIO['razon_social']}. Oficina: {ESTUDIO['calle']}, {ESTUDIO['comuna']}, {ESTUDIO['ciudad']}.</p>
  </div>
</div></section>
<section class="py-20 sm:py-24"><div class="mx-auto max-w-6xl px-6 lg:px-8">
  <h2 class="font-serif text-4xl">Ecosistema</h2>
  <div class="mt-8 grid gap-6 sm:grid-cols-2">
    <a href="https://dunora.ai/" target="_blank" rel="noopener" class="rounded-2xl bg-white p-7 ring-1 ring-slate2-100 hover:ring-copper-400"><h3 class="font-serif text-2xl">Dunora ↗</h3><p class="mt-2 text-sm text-navy-800/80">Plataforma con IA jurídica para abogados y estudios en Chile, producto de LEXINNOVA SpA, de la que Sebastián Salinas es cofundador y CEO.</p></a>
    <a href="https://www.sebastiansalinas.cl/" target="_blank" rel="noopener" class="rounded-2xl bg-white p-7 ring-1 ring-slate2-100 hover:ring-copper-400"><h3 class="font-serif text-2xl">sebastiansalinas.cl ↗</h3><p class="mt-2 text-sm text-navy-800/80">Sitio personal del socio fundador, con su trayectoria, publicaciones y blog.</p></a>
  </div>
</div></section>""" + cta(r)
    ld = {"@context": "https://schema.org", "@graph": [jsonld_estudio(), ld_migas([("El Estudio", "estudio/")])]}
    ld["@graph"][0].pop("@context", None)
    return pagina(path, "El Estudio | Salinas & Cía. Abogados, desde 2011",
                  "Historia, misión, forma de trabajo y ecosistema de Salinas & Cía. Abogados, estudio jurídico fundado en 2011 en Santiago.", cuerpo, ld)


def pagina_publicaciones():
    path = "/publicaciones/"
    r = rel(path)
    cuerpo = cabecera(r, "Publicaciones", "Publicaciones y casos", "Casos, artículos y publicaciones de los abogados del estudio.", [("Publicaciones", None)]) + f"""
<section class="py-20 sm:py-24"><div class="mx-auto max-w-4xl space-y-8 px-6 lg:px-8">
  <article class="rounded-2xl bg-white p-8 ring-1 ring-slate2-100"><p class="eyebrow text-copper-600">Caso · 2023</p>
    <h2 class="mt-2 font-serif text-2xl">Reclamo contra el Conservador de Bienes Raíces de Pozo Almonte</h2>
    <p class="mt-3 leading-relaxed text-navy-800/85">El tribunal acogió el reclamo y ordenó inscribir una compraventa, porque la medida precautoria que afectaba al inmueble se decretó después de solicitada la inscripción. Causa patrocinada por Sebastián Salinas Fuenzalida. {pend('[PENDIENTE: rol de la causa y autorización para publicarla]')}</p>
    <a class="mt-4 inline-block text-sm font-semibold text-copper-600 hover:text-copper-500" href="https://www.diarioconstitucional.cl/2023/02/14/conservador-debe-inscribir-escritura-de-compraventa-si-la-medida-precautoria-que-afecta-al-bien-objeto-del-contrato-fue-decretada-despues-de-que-se-solicitara-la-inscripcion/" target="_blank" rel="noopener">Comentario del fallo en Diario Constitucional (14/02/2023) ↗</a></article>
  <article class="rounded-2xl bg-white p-8 ring-1 ring-slate2-100"><p class="eyebrow text-copper-600">Artículo · 2007</p>
    <h2 class="mt-2 font-serif text-2xl">Enriquecimiento sin causa en los cuasicontratos. El concubinato: evolución y tendencias jurisprudenciales</h2>
    <p class="mt-3 leading-relaxed text-navy-800/85">Revista Temas de Derecho. Sebastián Salinas Fuenzalida.</p>
    <a class="mt-4 inline-block text-sm font-semibold text-copper-600 hover:text-copper-500" href="https://www.sebastiansalinas.cl/#publicaciones" target="_blank" rel="noopener">Ver referencias ↗</a></article>
  <article class="rounded-2xl bg-white p-8 ring-1 ring-slate2-100"><p class="eyebrow text-copper-600">Guía · 2021</p>
    <h2 class="mt-2 font-serif text-2xl">Guía para la constitución de personas jurídicas sin fines de lucro</h2>
    <p class="mt-3 leading-relaxed text-navy-800/85">Elaborada para el Colegio de Kinesiólogos de Chile. Sebastián Salinas Fuenzalida.</p>
    <a class="mt-4 inline-block text-sm font-semibold text-copper-600 hover:text-copper-500" href="https://www.ckch.cl/wp-content/uploads/2021/08/CKCH-Sociedades-Cientificas-Guia-para-obtencion-personalidad-juridica.pdf" target="_blank" rel="noopener">Ver la guía (PDF) ↗</a></article>
</div></section>""" + cta(r)
    return pagina(path, "Publicaciones y casos | Salinas & Cía. Abogados", "Casos, artículos y publicaciones de los abogados de Salinas & Cía. Abogados.", cuerpo,
                  {"@context": "https://schema.org", "@graph": [ld_migas([("Publicaciones", "publicaciones/")])]})


def formulario(r):
    opciones = "".join(f'<option>{n}</option>' for s, n, d in AREAS) + "<option>Otra</option>"
    c = "mt-2 w-full rounded-lg border border-slate2-300 bg-white px-4 py-3 text-navy-900 focus:border-copper-500 focus:outline-none"
    return f"""
<form name="contacto" method="POST" action="{r}contacto/gracias/" data-netlify="true" netlify-honeypot="sitio-web" class="space-y-5">
  <input type="hidden" name="form-name" value="contacto" />
  <p class="hidden"><label>No completar: <input name="sitio-web" /></label></p>
  <div class="grid gap-5 sm:grid-cols-2">
    <label class="block text-sm font-semibold">Nombre<input required name="nombre" autocomplete="name" class="{c}" /></label>
    <label class="block text-sm font-semibold">Correo electrónico<input required type="email" name="correo" autocomplete="email" class="{c}" /></label>
  </div>
  <div class="grid gap-5 sm:grid-cols-2">
    <label class="block text-sm font-semibold">Teléfono (opcional)<input type="tel" name="telefono" autocomplete="tel" class="{c}" /></label>
    <label class="block text-sm font-semibold">Área de su consulta<select required name="area" class="{c}"><option value="">Seleccione…</option>{opciones}</select></label>
  </div>
  <label class="block text-sm font-semibold">Mensaje<textarea required name="mensaje" rows="5" class="{c}"></textarea></label>
  <p class="text-xs text-navy-800/70">Por favor, no incluya datos sensibles ni detalles reservados de su caso en este primer contacto.</p>
  <label class="flex items-start gap-3 text-sm"><input required type="checkbox" name="privacidad" value="acepto" class="mt-1 h-4 w-4 accent-copper-500" /><span>He leído y acepto la <a class="underline hover:text-copper-600" href="{r}privacidad/">Política de privacidad</a>.</span></label>
  <button type="submit" class="rounded-full bg-copper-500 px-8 py-4 text-sm font-semibold text-white hover:bg-copper-600">Enviar consulta</button>
</form>"""


def pagina_contacto():
    path = "/contacto/"
    r = rel(path)
    cuerpo = cabecera(r, "Contacto", "Conversemos", "Cuéntenos brevemente su consulta y le responderemos a la brevedad para coordinar una reunión.", [("Contacto", None)]) + f"""
<section class="py-20 sm:py-24"><div class="mx-auto grid max-w-6xl gap-14 px-6 lg:grid-cols-12 lg:px-8">
  <div class="lg:col-span-7 rounded-2xl bg-white p-8 ring-1 ring-slate2-100">{formulario(r)}</div>
  <div class="lg:col-span-5">
    <h2 class="font-serif text-3xl">Oficina</h2>
    <div class="mt-5 text-navy-800">{contacto_datos()}</div>
    <img src="{r}assets/edificio-kennedy-5600-vertical.webp" alt="Edificio en Av. Presidente Kennedy 5600, Vitacura, donde se ubica Salinas &amp; Cía. Abogados" width="900" height="1200" loading="lazy" class="mt-8 aspect-[4/3] w-full rounded-2xl object-cover" />
    <a class="mt-4 inline-block text-sm font-semibold text-copper-600 hover:text-copper-500" href="https://www.google.com/maps/search/?api=1&amp;query=Av.+Presidente+Kennedy+5600,+Vitacura" target="_blank" rel="noopener">Ver en Google Maps ↗</a>
  </div>
</div></section>"""
    return pagina(path, "Contacto | Salinas & Cía. Abogados, Santiago",
                  "Escríbanos para coordinar una reunión. Formulario de contacto, correo y teléfono de Salinas & Cía. Abogados en Santiago.", cuerpo,
                  {"@context": "https://schema.org", "@graph": [ld_migas([("Contacto", "contacto/")])]})


def pagina_gracias():
    path = "/contacto/gracias/"
    r = rel(path)
    cuerpo = cabecera(r, "Contacto", "Gracias por escribirnos", "Recibimos su consulta y le responderemos a la brevedad.", [("Contacto", "contacto/"), ("Gracias", None)]) + f"""
<section class="py-20"><div class="mx-auto max-w-6xl px-6 lg:px-8"><a href="{r or './'}" class="rounded-full border border-navy-900/20 px-6 py-3 text-sm font-semibold hover:border-copper-500">Volver al inicio</a></div></section>"""
    h = pagina(path, "Gracias | Salinas & Cía. Abogados", "Recibimos su consulta.", cuerpo)
    return h.replace('content="index, follow, max-image-preview:large"', 'content="noindex"')


def pagina_privacidad():
    path = "/privacidad/"
    r = rel(path)
    cuerpo = cabecera(r, "Privacidad", "Política de privacidad", None, [("Privacidad", None)]) + f"""
<section class="py-20"><div class="mx-auto max-w-3xl space-y-5 px-6 leading-relaxed text-navy-800 lg:px-8">
  <p>{pend('[PENDIENTE: revisión del texto por el estudio antes de publicar]')}</p>
  <p><strong>Responsable.</strong> {ESTUDIO['razon_social']}, con domicilio en {ESTUDIO['calle']}, {ESTUDIO['comuna']}, {ESTUDIO['ciudad']}.</p>
  <p><strong>Datos que recogemos.</strong> Los que usted nos entrega en el formulario de contacto: nombre, correo electrónico, teléfono (opcional), área de su consulta y mensaje.</p>
  <p><strong>Para qué los usamos.</strong> Solo para responder su consulta y, si usted lo decide, coordinar una reunión o una propuesta de servicios. No los usamos para publicidad ni los compartimos con terceros, salvo el proveedor que aloja el sitio y procesa el formulario.</p>
  <p><strong>Base legal.</strong> Su consentimiento, conforme a la Ley 19.628 sobre protección de la vida privada y a la Ley 21.719 que la modifica.</p>
  <p><strong>Conservación.</strong> Conservamos los datos mientras sean necesarios para atender su consulta y luego los eliminamos, salvo que se inicie una relación profesional.</p>
  <p><strong>Sus derechos.</strong> Puede pedir acceso, rectificación, eliminación u oposición al tratamiento de sus datos escribiendo a {ESTUDIO['correo'] or pend('[PENDIENTE: correo general]')}.</p>
  <p><strong>Secreto profesional.</strong> La información que nos entregue sobre su caso está protegida por el secreto profesional.</p>
</div></section>"""
    return pagina(path, "Política de privacidad | Salinas & Cía. Abogados",
                  "Cómo tratamos los datos personales que nos entrega a través de este sitio, conforme a las leyes 19.628 y 21.719.", cuerpo)


def fecha_larga(f):
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    a, m, d = f.split("-")
    return f"{int(d)} de {meses[int(m)-1]} de {a}"


def pagina_blog():
    path = "/blog/"
    r = rel(path)
    items = "".join(f"""
    <a href="{r}blog/{p['slug']}/" class="group block rounded-2xl bg-white p-8 ring-1 ring-slate2-100 hover:ring-copper-400">
      <p class="eyebrow text-copper-600">{NOMBRE_AREA[p['area']]} · {fecha_larga(p['fecha'])}</p>
      <h2 class="mt-3 font-serif text-3xl leading-snug group-hover:text-copper-600">{p['titulo']}</h2>
      <p class="mt-3 text-navy-800/80">{p['desc']}</p>
      <p class="mt-4 text-sm text-navy-800/70">Por Sebastián Salinas Fuenzalida</p>
    </a>""" for p in sorted(POSTS, key=lambda x: x["fecha"], reverse=True))
    cuerpo = cabecera(r, "Blog", "Blog", "Artículos sobre temas jurídicos de interés para empresas, familias y personas.", [("Blog", None)]) + f"""
<section class="py-20 sm:py-24"><div class="mx-auto max-w-4xl space-y-6 px-6 lg:px-8">{items}</div></section>""" + cta(r)
    return pagina(path, "Blog | Salinas & Cía. Abogados", "Artículos sobre temas jurídicos de interés para empresas, familias y personas, escritos por los abogados de Salinas & Cía.", cuerpo,
                  {"@context": "https://schema.org", "@graph": [ld_migas([("Blog", "blog/")])]})


def pagina_post(p):
    path = f"/blog/{p['slug']}/"
    r = rel(path)
    fuentes = "".join((f'<li><a class="underline hover:text-copper-600" href="{u}" target="_blank" rel="noopener">{t}</a></li>' if u else f"<li>{pend(t)}</li>") for t, u in p["fuentes"])
    cuerpo = cabecera(r, f"{NOMBRE_AREA[p['area']]} · {fecha_larga(p['fecha'])}", p["titulo"], None, [("Blog", "blog/"), (p["titulo"], None)]) + f"""
<section class="py-20"><div class="mx-auto max-w-3xl px-6 lg:px-8">
  <div class="flex items-center gap-4 border-b border-slate2-100 pb-6">
    <img src="{r}assets/sebastian-salinas-fuenzalida.jpg" alt="Sebastián Salinas Fuenzalida" width="976" height="1300" class="h-14 w-14 rounded-full object-cover object-top" />
    <p class="text-sm"><a class="font-semibold hover:text-copper-600" href="{r}equipo/sebastian-salinas/">Sebastián Salinas Fuenzalida</a><br /><span class="text-navy-800/70">Socio fundador de Salinas &amp; Cía. Abogados</span></p>
  </div>
  <div class="articulo mt-8 space-y-5 text-lg leading-relaxed text-navy-800">{p['html']}</div>
  <p class="mt-10 border-t border-slate2-100 pt-6 text-sm italic text-navy-800/70">Sebastián Salinas Fuenzalida es abogado y socio fundador de Salinas &amp; Cía. Abogados. Este artículo es informativo y no reemplaza la asesoría legal para un caso concreto.</p>
  <div class="mt-6 text-sm"><p class="font-semibold">Fuentes</p><ul class="mt-2 space-y-1">{fuentes}</ul></div>
  <p class="mt-8 text-sm">Área relacionada: <a class="font-semibold text-copper-600 hover:text-copper-500" href="{r}areas/{p['area']}/">{NOMBRE_AREA[p['area']]} →</a></p>
</div></section>""" + cta(r)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": p["titulo"], "description": p["desc"], "datePublished": p["fecha"], "inLanguage": "es-CL",
         "author": {"@id": "https://www.sebastiansalinas.cl/#person", "@type": "Person", "name": "Sebastián Salinas Fuenzalida"},
         "publisher": {"@id": BASE + "/#estudio"}, "mainEntityOfPage": BASE + path, "image": BASE + "/assets/og-salinasycia.jpg"},
        ld_migas([("Blog", "blog/"), (p["titulo"], f"blog/{p['slug']}/")])]}
    return pagina(path, p["titulo_seo"], p["desc"], cuerpo, ld)


def escribir(destino_raiz, path, contenido, vista_previa=False):
    if vista_previa:
        # En la vista previa (artefacto de Claude) los enlaces a carpetas deben apuntar a index.html.
        contenido = re.sub(r'href="((?:\.\./)*[a-z0-9\-/]*/)"', r'href="\1index.html"', contenido)
        contenido = contenido.replace('href="./"', 'href="index.html"')
    destino = os.path.join(destino_raiz, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(contenido)


def todas():
    yield "/", portada()
    yield "/areas/", pagina_areas()
    for s in AREAS_DETALLE:
        yield f"/areas/{s}/", pagina_area(s)
    yield "/equipo/", pagina_equipo()
    for s in PERFILES:
        yield f"/equipo/{s}/", pagina_perfil(s)
    yield "/estudio/", pagina_estudio()
    yield "/publicaciones/", pagina_publicaciones()
    yield "/contacto/", pagina_contacto()
    yield "/contacto/gracias/", pagina_gracias()
    yield "/privacidad/", pagina_privacidad()
    yield "/blog/", pagina_blog()
    for p in POSTS:
        yield f"/blog/{p['slug']}/", pagina_post(p)


def robots():
    txt = ("# BORRADOR: sitio no publicado\nUser-agent: *\nDisallow: /\n" if BORRADOR else
           "User-agent: *\nAllow: /\n\nSitemap: " + BASE + "/sitemap.xml\n")
    with open(os.path.join(SITE, "robots.txt"), "w") as f:
        f.write(txt)


if __name__ == "__main__":
    import sys
    paginas = list(todas())
    for path, h in paginas:
        escribir(SITE, path, h)
    robots()
    if "--vista-previa" in sys.argv:
        dest = sys.argv[sys.argv.index("--vista-previa") + 1]
        for path, h in paginas:
            escribir(dest, path, h, vista_previa=True)
    print(f"{len(paginas)} páginas generadas en site/" + (" (borrador)" if BORRADOR else ""))
