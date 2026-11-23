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
    "correo": None,      # [PENDIENTE] correo general del estudio
    "telefono": None,    # [PENDIENTE]
    "horario": None,     # [PENDIENTE]
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
    ("derecho-administrativo-y-regulatorio", "Administrativo y regulatorio", "Permisos, concesiones y defensa ante organismos del Estado."),
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

MISION = "Desde 2011 asesoramos a personas, familias, empresarios y empresas con una mirada integral de sus asuntos, de lo personal a lo empresarial. Construimos con cada cliente una relación cercana y de confianza, con un abogado responsable de principio a fin, que combina criterio jurídico y visión de negocios para que el cliente decida informado y a tiempo."
VISION = "Ser el estudio de cabecera de las familias y empresas que confían en nosotros: el lugar donde resuelven sus asuntos legales, personales y empresariales, en una relación que perdura en el tiempo."

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
    <a href="{r}contacto/" class="rounded-full border border-copper-500/60 px-4 py-2 text-xs font-semibold uppercase tracking-wider text-copper-300 hover:bg-copper-500 hover:text-white">Conversemos</a>
  </nav>
</header>
<main>"""


def contacto_datos(dark=True):
    E = ESTUDIO
    correo = f'<a href="mailto:{E["correo"]}" class="hover:text-copper-300">{E["correo"]}</a>' if E["correo"] else PEND.format("correo general")
    tel = E["telefono"] or PEND.format("teléfono / WhatsApp")
    hor = E["horario"] or PEND.format("horario")
    return f"""<ul class="space-y-3 text-sm">
      <li><span class="text-slate2-400">Dirección:</span> {E['calle']}, {E['comuna']}, {E['ciudad']}</li>
      <li><span class="text-slate2-400">Correo:</span> {correo}</li>
      <li><span class="text-slate2-400">Teléfono:</span> {tel}</li>
      <li><span class="text-slate2-400">Horario:</span> {hor}</li>
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
      </a>""" for s, n, d in AREAS[:6])
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

<!-- MISIÓN Y VISIÓN -->
<section class="bg-white py-24 sm:py-28">
  <div class="mx-auto grid max-w-6xl gap-12 px-6 lg:grid-cols-2 lg:gap-16 lg:px-8">
    <div class="border-l-2 border-copper-500 pl-8">
      <p class="eyebrow text-copper-600">Misión</p>
      <p class="mt-5 font-serif text-2xl leading-snug text-navy-900 sm:text-[1.7rem]">{MISION}</p>
    </div>
    <div class="border-l-2 border-copper-500 pl-8">
      <p class="eyebrow text-copper-600">Visión</p>
      <p class="mt-5 font-serif text-2xl leading-snug text-navy-900 sm:text-[1.7rem]">{VISION}</p>
    </div>
  </div>
</section>

<!-- ÁREAS -->
<section class="py-24 sm:py-28">
  <div class="mx-auto max-w-6xl px-6 lg:px-8">
    <p class="eyebrow text-copper-600">Áreas de práctica</p>
    <h2 class="mt-4 max-w-2xl font-serif text-4xl leading-tight sm:text-5xl">Cómo podemos ayudarle</h2>
    <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">{areas}
    </div>
    <p class="mt-10 text-sm leading-relaxed text-navy-800/80"><span class="font-semibold text-navy-900">También:</span> {otras}.</p>
    <a href="{r}areas/" class="mt-6 inline-block rounded-full border border-navy-900/20 px-6 py-3 text-sm font-semibold hover:border-copper-500 hover:text-copper-600">Ver todas las áreas</a>
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


def escribir(path, contenido):
    destino = os.path.join(SITE, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(contenido)


def robots():
    txt = ("# BORRADOR: sitio no publicado\nUser-agent: *\nDisallow: /\n" if BORRADOR else
           "User-agent: *\nAllow: /\n\nSitemap: " + BASE + "/sitemap.xml\n")
    with open(os.path.join(SITE, "robots.txt"), "w") as f:
        f.write(txt)


if __name__ == "__main__":
    escribir("/", portada())
    robots()
    print("Sitio generado en site/ (borrador)" if BORRADOR else "Sitio generado en site/")
