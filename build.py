#!/usr/bin/env python3
"""Genera il sito statico "Di sana e robusta Costituzione" in ../site/.
Tutti i dati da completare stanno nel blocco CONFIG qui sotto."""
import json, os, shutil, html, datetime
from urllib.parse import quote
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "site")

# ---------------------------------------------------------------- CONFIG
DOMAIN = "https://www.DOMINIO-DA-INSERIRE.it"       # dominio definitivo, senza slash finale
EMAIL = "ferdinandodeblasio.it@gmail.com"            # unico canale di contatto
ISBN = None                                          # es. "978-88-...": se None, non compare
EDITORE = None                                       # es. "Nome editore": se None, non compare
BOOK_YEAR = None                                     # es. "2025": se None, la timeline dice "Oggi"
SHOP_URL = None                                      # link di acquisto del libro: se None, solo contatto email
# ----------------------------------------------------------------------

TITLE = "Di sana e robusta Costituzione"
AUTHOR1 = "Ferdinando de Blasio di Palizzi"
AUTHOR2 = "Michele D'Andrea"
ILLUSTRATOR = "Maurizio Dondi"
SUB = "L'educazione civica che non ti aspetti"
e = html.escape

ORGANI = [
    ("scheletro", "Scheletro", "La Costituzione", "scheletro.webp",
     "Busto con scheletro in trasparenza e il simbolo della Repubblica al posto del cuore",
     "Fa stare in piedi lo Stato, gli dà forma e protegge gli organi delicati. Ha 139 ossa, una per ogni articolo. L'ultimo, l'articolo 139, è la gabbia toracica che protegge il cuore dello Stato."),
    ("cuore", "Cuore", "Il Parlamento", "cuore.webp",
     "Cuore anatomico con le aule di Camera e Senato all'interno e fogli di legge al posto del sangue",
     "Due Camere che pompano democrazia. Una legge passa dall'una all'altra come il sangue nel cuore, finché esce senza modifiche. E come ogni cuore, nessuno può impedirgli di battere."),
    ("cervello", "Cervello", "Il Governo", "cervello.webp",
     "Cervello con una manifestazione del Primo Maggio, una bandiera e dei papaveri",
     "Raccoglie i segnali che arrivano dal resto del corpo, li interpreta e decide un piano d'azione. Coordina i movimenti volontari dello Stato."),
    ("arti", "Arti", "La pubblica amministrazione", "arti.webp",
     "Una gamba e un braccio muscolosi con biblioteche e aule scolastiche nei muscoli",
     "Braccia e gambe fanno un milione di cose, ma vanno tenute allenate e messe in condizione di lavorare. Quando si fermano, si ferma lo Stato."),
    ("sangue", "Sistema immunitario", "La Magistratura", "sangue.webp",
     "Globuli rossi e globuli bianchi che scorrono in un vaso sanguigno, con un martelletto da giudice",
     "Come i globuli bianchi, il sistema giudiziario difende il corpo dello Stato da ciò che lo minaccia."),
    ("psiche", "Psiche", "Il Presidente della Repubblica", "psiche.webp",
     "Due profili umani a ingranaggi, verde e rosso, con al centro una figura bianca: il tricolore",
     "La coscienza dello Stato. Ne rappresenta l'unità, firma le leggi ed è il custode della Costituzione. È la vocina che ti dice: guarda che poi te ne penti."),
    ("intestino", "Intestino", "Il popolo", "intestino.webp",
     "Stomaco e intestino con scene di manifestazioni e persone in piazza",
     "Siamo tutti noi. Quando l'intestino sta male, l'umore dell'intero corpo ne risente."),
    ("europa", "Europa", "L'Unione europea", "europa-gravidanza.webp",
     "Pancia di una donna incinta con le stelle della bandiera europea",
     "Mamma Europa e tutti i suoi figli. L'Italia è uno di loro."),
]

NAV = [("spettacolo.html", "Spettacolo"), ("libro.html", "Libro"), ("il-progetto.html", "Il progetto")]


def person(name):
    return {"@type": "Person", "name": name}


def jsonld_graph():
    authors = [person(AUTHOR1), person(AUTHOR2)]
    book = {"@type": "Book", "@id": DOMAIN + "/libro.html#libro", "name": TITLE, "alternativeName": SUB,
            "author": authors, "illustrator": person(ILLUSTRATOR), "inLanguage": "it",
            "url": DOMAIN + "/libro.html", "image": DOMAIN + "/img/og.jpg",
            "audience": {"@type": "EducationalAudience", "educationalRole": "student"}}
    if ISBN: book["isbn"] = ISBN
    if EDITORE: book["publisher"] = {"@type": "Organization", "name": EDITORE}
    if BOOK_YEAR: book["datePublished"] = BOOK_YEAR
    play = {"@type": "Play", "@id": DOMAIN + "/spettacolo.html#spettacolo", "name": TITLE,
            "description": "Lezione-spettacolo di circa un'ora sulla Costituzione italiana per le scuole medie e superiori. Un medico internista fa il check-up allo Stato.",
            "author": authors, "dateCreated": "2018", "inLanguage": "it", "url": DOMAIN + "/spettacolo.html",
            "audience": {"@type": "EducationalAudience", "educationalRole": "student"}}
    site = {"@type": "WebSite", "@id": DOMAIN + "/#sito", "name": TITLE, "url": DOMAIN + "/", "inLanguage": "it",
            "author": authors}
    return {"@context": "https://schema.org", "@graph": [site, play, book] + authors}


def head(title, desc, path, jsonld=False):
    url = DOMAIN + "/" + path if path != "index.html" else DOMAIN + "/"
    ld = ""
    if jsonld:
        ld = '\n<script type="application/ld+json">' + json.dumps(jsonld_graph(), ensure_ascii=False) + "</script>"
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="{TITLE}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#8F3D49">
<link rel="preload" href="fonts/antonio-latin-300-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">{ld}
</head>
<body>
<a class="skip" href="#contenuto">Vai al contenuto</a>
"""


def header(active):
    AC = ' aria-current="page"'
    links = "".join(
        '<a href="%s"%s>%s</a>' % (h, AC if h == active else "", t) for h, t in NAV)
    cur = ' aria-current="page"' if active == "contatti.html" else ""
    return f"""<header class="site-header"><div class="wrap">
<a class="brand" href="index.html">{TITLE}</a>
<nav class="nav" aria-label="Principale">{links}<a class="btn" href="contatti.html"{cur}>Scrivici</a></nav>
</div></header>
<main id="contenuto">
"""


def footer():
    return f"""</main>
<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><span class="brand">{TITLE}</span>
<p>{SUB}. Lezione-spettacolo e libro illustrato sulla Costituzione italiana, per le scuole medie e superiori.</p></div>
<nav aria-label="Link del sito"><h2>Il sito</h2><ul>
<li><a href="spettacolo.html">Spettacolo</a></li><li><a href="libro.html">Libro</a></li>
<li><a href="il-progetto.html">Il progetto</a></li><li><a href="contatti.html">Contatti</a></li>
<li><a href="privacy.html">Privacy</a></li></ul></nav>
<div><h2>Contatti</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>Autorizzazioni, richieste di utilizzo del titolo e segnalazioni vanno scritte a questo indirizzo.</p></div>
</div>
<p class="rights">{TITLE} è un'opera di {AUTHOR1} e {AUTHOR2}, in scena dal 2018. Illustrazioni del libro di {ILLUSTRATOR}. Testi, format, immagini e titolo non possono essere riprodotti o utilizzati senza autorizzazione degli autori. Tutti i diritti riservati.</p>
</div></footer>
<script src="main.js" defer></script>
</body>
</html>
"""


def cta_band(title="Porta il check-up nella tua scuola"):
    return f"""<section class="cta-band"><div class="wrap">
<div><h2>{title}</h2><p>Scrivici la data che hai in mente e di cosa dispone la scuola. Ti rispondiamo con disponibilità e requisiti tecnici.</p></div>
<div class="btn-row"><a class="btn" href="contatti.html#spettacolo">Richiedi lo spettacolo</a><a class="btn ghost" href="contatti.html#libro">Ordina copie del libro</a></div>
</div></section>
"""


# ------------------------------------------------------------------ pagine
def page_home():
    items = []
    for i, (k, nome, ist, img, alt, txt) in enumerate(ORGANI):
        items.append(f"""<li>
<button type="button" aria-expanded="false" aria-controls="p-{k}"><span class="organo">{nome}</span><span class="istituzione">{ist}</span></button>
<div class="panel" id="p-{k}" role="region" aria-label="{nome}: {ist}" hidden>
<div class="art"><img src="img/{img}" alt="{e(alt)}" loading="lazy" width="600" height="400"></div>
<h3>{ist}</h3><p>{txt}</p></div>
</li>""")
    referto = "\n".join(items)
    s = head(f"{TITLE} | Spettacolo e libro sulla Costituzione per le scuole",
             "Un medico internista fa il check-up allo Stato italiano. Lezione-spettacolo e libro illustrato sulla Costituzione per scuole medie e superiori, di Ferdinando de Blasio di Palizzi e Michele D'Andrea.",
             "index.html", jsonld=True)
    s += header("index.html")
    s += f"""<section class="hero"><div class="wrap">
<div>
<h1><span>Di sana</span><span>e robusta</span><span>Costituzione</span></h1>
<p class="tag">{SUB}</p>
<p class="lede">Un medico internista fa il check-up allo Stato italiano. Lo spettacolo e il libro portano la Costituzione nelle scuole medie e superiori, con il corpo umano come mappa.</p>
<div class="btn-row"><a class="btn" href="contatti.html#spettacolo">Prenota lo spettacolo</a><a class="btn ghost" href="libro.html">Scopri il libro</a></div>
<ul class="facts" style="margin-top:2rem"><li>In scena dal 2018</li><li>Decine di repliche in Piemonte, Marche, Umbria e Toscana</li><li>Circa un'ora</li></ul>
</div>
<div class="hero-art"><img src="img/corpo-intero.webp" alt="Corpo umano con gli organi che rappresentano le istituzioni: cervello, cuore, scheletro, arti, intestino, psiche e sistema immunitario" width="720" height="1025"></div>
</div></section>

<section><div class="wrap intro">
<h2>Una Costituzione che si tocca con mano</h2>
<div>
<p>Ai ragazzi la Costituzione di solito arriva come un elenco di articoli. Qui arriva come un corpo: lo scheletro che tiene in piedi lo Stato, il cuore che pompa democrazia, il cervello che decide, il sistema immunitario che lo difende.</p>
<p>Chi ha capito come funziona un corpo può capire come funziona una Repubblica. Con un linguaggio da ragazzi, qualche risata e nessuna lezione frontale.</p>
</div></div></section>

<section class="tint" aria-labelledby="t-referto"><div class="wrap">
<h2 id="t-referto">Il check-up, organo per organo</h2>
<p class="lede">Ogni organo del corpo ha il suo corrispettivo nelle istituzioni. Scegli un organo e leggi il referto.</p>
<ul class="referto-list">
{referto}
</ul>
</div></section>

<section><div class="wrap">
<h2>Sul palco e sulla pagina</h2>
<div class="paths">
<article class="path blue"><img src="img/pesci.webp" alt="Un pesce giallo e due pesci più piccoli in un acquario di onde blu" width="700" height="450" loading="lazy">
<h3>Lo spettacolo</h3>
<p>Circa un'ora di lezione-spettacolo con filmati, immagini, suoni e ragazzi chiamati sul palco. In scena un solo interprete, nei panni del medico internista.</p>
<a class="more" href="spettacolo.html">Tutto sullo spettacolo</a></article>
<article class="path warm"><img src="img/bandiera.webp" alt="Bandiera italiana con ritratti storici nelle tre fasce" width="500" height="450" loading="lazy">
<h3>Il libro</h3>
<p>Illustrato da {ILLUSTRATOR} e composto con un carattere ad alta leggibilità. Racconta gli organi dello Stato e contiene il testo integrale della Costituzione, dall'articolo 1 al 139.</p>
<a class="more" href="libro.html">Tutto sul libro</a></article>
</div></div></section>

<section class="quote"><div class="wrap">
<div><blockquote><p>La Costituzione raccontata ai ragazzi con un linguaggio ironico e leggero, ma mai banale.</p></blockquote>
<cite>La Stampa, edizione di Asti, 20 novembre 2019</cite>
<p style="margin-top:1rem">Al Teatro Alfieri lo spettacolo ha accompagnato il battesimo civico di 132 neo diciottenni. <a href="il-progetto.html#stampa">Leggi la storia del progetto</a></p></div>
<a class="clip" href="il-progetto.html#stampa" aria-label="Apri l'articolo de La Stampa"><img src="img/rassegna-la-stampa-2019-11-20.jpg" alt="Pagina de La Stampa di Asti del 20 novembre 2019 con l'articolo All'Alfieri la Costituzione diventa lezione di anatomia" width="500" height="560" loading="lazy"></a>
</div></section>
"""
    s += cta_band() + footer()
    return s


def page_spettacolo():
    s = head(f"Lo spettacolo | {TITLE}",
             "Lezione-spettacolo di circa un'ora sulla Costituzione per scuole medie e superiori: un medico internista, filmati, suoni e ragazzi sul palco. Requisiti tecnici e condizioni.",
             "spettacolo.html")
    s += header("spettacolo.html")
    s += f"""<div class="wrap page-head"><h1>Lo spettacolo</h1>
<p class="lede">Una lezione di anatomia sulla Repubblica, tenuta da un medico internista con molto da dire e poca voglia di annoiare.</p></div>

<section style="padding-top:1rem"><div class="wrap split">
<div>
<h2>Come funziona</h2>
<p>Un medico internista dalla didattica singolare accompagna la platea in una lezione di anatomia che ha per oggetto la Repubblica e i suoi organi: le dinamiche parlamentari, i ruoli e gli attori della vita istituzionale, l'Unione europea.</p>
<p>Il ritmo è quello di una chiacchierata briosa, il linguaggio quello dei ragazzi. Filmati, immagini e suoni accompagnano il racconto, e il pubblico lavora con l'attore: si batte il tempo del cuore con mani e piedi, si sale sul palco, si scopre quanto pesa tenere in allenamento i muscoli della pubblica amministrazione.</p>
<p>Alla fine ragazzi e ragazze hanno un'idea più chiara di come funziona la macchina dello Stato e di perché vale la pena prendersene cura.</p>
<dl class="spec">
<dt>Durata</dt><dd>Circa un'ora</dd>
<dt>Per chi</dt><dd>Scuole medie e superiori</dd>
<dt>In scena</dt><dd>{AUTHOR1}, unico interprete</dd>
<dt>Testo</dt><dd>{AUTHOR1} e {AUTHOR2}</dd>
<dt>Dal</dt><dd>2018, con decine di repliche in Piemonte, Marche, Umbria e Toscana</dd>
</dl>
</div>
<div class="figure blue"><img src="img/pesci.webp" alt="Un pesce giallo e due pesci più piccoli in un acquario di onde blu" width="700" height="450"></div>
</div></section>

<section class="tint"><div class="wrap split rev">
<div class="figure" style="background:var(--paper)"><img src="img/uomo-organi.webp" alt="Sagoma di uomo con cervello, cuore, stomaco e intestino in evidenza" width="500" height="900" loading="lazy"></div>
<div>
<h2>Cosa serve</h2>
<p>Lo spettacolo viaggia leggero. La scuola o il teatro mettono a disposizione:</p>
<ul class="checklist">
<li>impianto di amplificazione</li>
<li>microfono ad archetto</li>
<li>proiettore digitale con schermo adeguato</li>
<li>cavi video e audio (HDMI)</li>
</ul>
<div class="btn-row"><a class="btn" href="contatti.html#spettacolo">Richiedi lo spettacolo</a></div>
</div></div></section>

<section><div class="wrap split">
<div>
<h2>Dopo lo spettacolo, il libro</h2>
<p>Spettacolo e libro seguono lo stesso viaggio nel corpo umano. In classe i docenti possono riprendere gli organi uno per uno e arrivare al testo della Costituzione con lo stesso linguaggio.</p>
<p>Le scuole possono ordinare copie del libro insieme alla data dello spettacolo, oppure in un secondo momento.</p>
<div class="btn-row"><a class="btn ghost" href="libro.html">Vai al libro</a></div>
</div>
<div>
<h2>Domande frequenti</h2>
<details class="faq"><summary>Quanto dura lo spettacolo?</summary><p>Circa un'ora. Se la scuola ha vincoli di orario, indicali nella email di richiesta.</p></details>
<details class="faq"><summary>A quali classi è rivolto?</summary><p>Alle scuole medie e superiori. Il linguaggio e gli esempi sono pensati per ragazzi e ragazze di quelle età.</p></details>
<details class="faq"><summary>Serve un teatro?</summary><p>Serve uno spazio in cui la platea veda e senta bene e dove si possano usare amplificazione e proiettore. Nell'elenco dei requisiti trovi tutto il necessario.</p></details>
<details class="faq"><summary>Possiamo ordinare il libro per la classe?</summary><p>Sì. Scrivi indicando il numero di copie e l'indirizzo di consegna.</p></details>
</div>
</div></section>
"""
    s += cta_band() + footer()
    return s


def book_spec():
    rows = [("Titolo", f"{TITLE}"), ("Sottotitolo", SUB), ("Autori", f"{AUTHOR2}, {AUTHOR1}"),
            ("Illustrazioni", ILLUSTRATOR), ("Carattere", "EasyReading, ad alta leggibilità")]
    if EDITORE: rows.append(("Editore", EDITORE))
    if BOOK_YEAR: rows.append(("Anno", BOOK_YEAR))
    if ISBN: rows.append(("ISBN", ISBN))
    return '<dl class="spec">' + "".join(f"<dt>{k}</dt><dd>{e(v)}</dd>" for k, v in rows) + "</dl>"


def page_libro():
    shop = ""
    if SHOP_URL:
        shop = f'<a class="btn" href="{SHOP_URL}" rel="noopener">Acquista il libro</a>'
    s = head(f"Il libro | {TITLE}",
             f"{TITLE}. {SUB}. Libro illustrato da {ILLUSTRATOR} sulla Costituzione italiana, con il testo integrale e un carattere ad alta leggibilità. Per scuole, docenti e famiglie.",
             "libro.html")
    s += header("libro.html")
    s += f"""<div class="wrap page-head"><h1>Il libro</h1>
<p class="lede">{SUB}. Lo stesso viaggio nel corpo umano dello spettacolo, da sfogliare in classe e a casa.</p></div>

<section style="padding-top:1rem"><div class="wrap split rev">
<div class="figure"><img src="img/cuore.webp" alt="Cuore anatomico con le aule di Camera e Senato all'interno e fogli di legge che escono dai vasi" width="800" height="560"></div>
<div>
<h2>Un libro che si apre volentieri</h2>
<p>Gli alunni di solito ricevono la Costituzione come un muto repertorio di articoli. Questo libro la accompagna con un racconto illustrato: ogni organo del corpo diventa un'istituzione, ogni illustrazione un modo per ricordarla.</p>
<p>Il testo è composto con il carattere EasyReading, pensato per l'alta leggibilità, e si può leggere da soli o in classe con l'insegnante.</p>
{book_spec()}
<div class="btn-row">{shop}<a class="btn{' ghost' if SHOP_URL else ''}" href="contatti.html#libro">Ordina copie per la scuola</a></div>
</div></div></section>

<section class="tint"><div class="wrap">
<h2>Come è fatto</h2>
<ol class="parts" style="list-style:none;padding:0">
<li><div class="t"><small>Parte I</small>Ci vuole un fisico bestiale</div><p>Il corpo dello Stato, organo per organo: lo scheletro, il cuore, il cervello, gli arti, il sistema immunitario, la psiche, l'intestino. Ogni capitolo indica gli articoli della Costituzione da leggere.</p></li>
<li><div class="t"><small>Parte II</small>Noi e gli altri</div><p>I segni particolari che rendono riconoscibile uno Stato, dalla bandiera all'inno, e il posto dell'Italia in Europa.</p></li>
<li><div class="t"><small>Parte III</small>Da 1 a 139</div><p>Il testo integrale della Costituzione, a portata di mano durante la lettura.</p></li>
</ol></div></section>

<section><div class="wrap split">
<div>
<h2>Per i docenti</h2>
<p>Il libro riprende i temi dello spettacolo e dà agli insegnanti gli strumenti per affrontarli in classe, con lo stesso linguaggio e le stesse immagini. Chi ha visto lo spettacolo ritrova gli organi e le metafore, chi non l'ha visto può usare il libro da solo.</p>
<p>Le scuole possono ordinare più copie e abbinarle a una data dello spettacolo.</p>
</div>
<div class="figure blue"><img src="img/sangue.webp" alt="Globuli rossi e bianchi che scorrono in un vaso sanguigno" width="700" height="500" loading="lazy"></div>
</div></section>
"""
    s += cta_band("Porta il libro in classe") + footer()
    return s


def page_progetto():
    year = BOOK_YEAR or "Oggi"
    faq = [
        ("Chi ha ideato e scritto Di sana e robusta Costituzione?",
         f"{AUTHOR1} e {AUTHOR2}, nel 2018. Il titolo identifica la lezione-spettacolo con {AUTHOR1} in scena nei panni del medico internista e il libro illustrato da {ILLUSTRATOR}."),
        ("Ho visto altre iniziative con lo stesso titolo o con un titolo simile. Sono la stessa cosa?",
         "Questo sito presenta solo lo spettacolo e il libro degli autori indicati sopra. Se hai dubbi su un'altra iniziativa con un nome uguale o simile, scrivici prima di prenotare: ti diciamo se fa parte del progetto."),
        ("Posso usare testi, immagini o il titolo?",
         "Serve l'autorizzazione degli autori. Scrivi a " + EMAIL + " spiegando come e dove vuoi usarli."),
        ("Come cito il progetto?",
         f"{TITLE}, di {AUTHOR2} e {AUTHOR1}, illustrazioni di {ILLUSTRATOR}."),
    ]
    faq_html = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    s = head(f"Il progetto e gli autori | {TITLE}",
             f"La storia di {TITLE}: nata nel 2018 da {AUTHOR1} e {AUTHOR2}, con decine di repliche nelle scuole. Autori, rassegna stampa e come riconoscere l'opera originale.",
             "il-progetto.html", jsonld=True)
    s += header("il-progetto.html")
    s += f"""<div class="wrap page-head"><h1>Il progetto</h1>
<p class="lede">Dal 2018 nelle scuole italiane, con uno spettacolo e un libro che hanno lo stesso titolo, gli stessi autori e la stessa idea.</p></div>

<section style="padding-top:1rem"><div class="wrap split">
<div>
<h2>Come è nato</h2>
<ol class="timeline">
<li><span class="year">2018</span><p>Nasce la lezione-spettacolo. {AUTHOR1} e {AUTHOR2} scrivono il testo. In scena c'è un solo interprete, nei panni di un medico internista che fa il check-up allo Stato.</p></li>
<li><span class="year">2019</span><p>A novembre lo spettacolo va in scena al Teatro Alfieri di Asti per il battesimo civico di 132 neo diciottenni, con le classi quarte e quinte di quattro istituti della città. La Stampa dedica all'evento un articolo intitolato «All'Alfieri la Costituzione diventa lezione di anatomia».</p></li>
<li><span class="year">Negli anni</span><p>Decine di repliche in tutta Italia, dal Piemonte alle Marche, dall'Umbria alla Toscana.</p></li>
<li><span class="year">{year}</span><p>Il libro illustrato da {ILLUSTRATOR} porta in classe gli stessi temi, con il testo integrale della Costituzione.</p></li>
</ol>
</div>
<div class="note-box"><h3>L'opera originale</h3>
<p>{TITLE} è un'opera di {AUTHOR1} e {AUTHOR2}. Esiste come lezione-spettacolo dal 2018 e come libro illustrato da {ILLUSTRATOR}.</p>
<p>Questo sito è il riferimento per prenotare lo spettacolo e acquistare il libro.</p></div>
</div></section>

<section class="tint"><div class="wrap">
<h2>Gli autori</h2>
<div class="authors">
<div><h3>{AUTHOR1}</h3><p>Medico mancato e giurista pentito. Autore e unico interprete dello spettacolo: sul palco è il medico internista che visita lo Stato.</p></div>
<div><h3>{AUTHOR2}</h3><p>Professore, esperto di comunicazione istituzionale e divulgatore storico. Coautore del testo dello spettacolo e del libro.</p></div>
</div>
<p style="margin-top:1.5rem"><strong>Illustrazioni del libro:</strong> {ILLUSTRATOR}.</p>
</div></section>

<section id="stampa"><div class="wrap split rev">
<figure class="press" style="margin:0"><a href="img/rassegna-la-stampa-2019-11-20.jpg"><img src="img/rassegna-la-stampa-2019-11-20.jpg" alt="Pagina de La Stampa di Asti del 20 novembre 2019 con l'articolo All'Alfieri la Costituzione diventa lezione di anatomia, con tre fotografie della platea al Teatro Alfieri" width="900" height="1010" loading="lazy"></a>
<figcaption>La Stampa, edizione di Asti, 20 novembre 2019. Articolo di Valentina Fassio.</figcaption></figure>
<div>
<h2>Rassegna stampa</h2>
<p>«La Costituzione raccontata ai ragazzi con un linguaggio ironico e leggero, ma mai banale». Così La Stampa racconta la mattinata al Teatro Alfieri di Asti, dove lo spettacolo ha accompagnato la consegna della Costituzione a 132 neo diciottenni.</p>
<p>L'articolo riporta anche l'idea all'origine del progetto: trovare un metodo per spiegare la Costituzione con parole semplici, immaginando lo Stato come un corpo con i suoi organi.</p>
<h3 style="margin-top:1.75rem">Altre testimonianze</h3>
<ul class="checklist">
<li><a href="https://www.lanuovaprovincia.it/gallery/attualita/327510/festeggiati-al-teatro-alfieri-i-20-anni-del-servizio-civile-photogallery.html" rel="noopener">La Nuova Provincia</a>: Teatro Alfieri di Asti, i 20 anni del Servizio Civile</li>
<li><a href="https://www.comune.macerata.it/novita/il-2-giugno-a-macerata-la-festa-della-repubblica-itinerante/" rel="noopener">Comune di Macerata</a>: il 2 giugno, la Festa della Repubblica itinerante</li>
<li><a href="https://www.mcnet.tv/macerata-le-celebrazioni-per-la-festa-della-repubblica/" rel="noopener">MCNET</a>: Macerata, le celebrazioni per la Festa della Repubblica</li>
<li><a href="https://www.quinewspisa.it/cascina-una-mattinata-per-celebrare-la-repubblica.htm" rel="noopener">QuiNews Pisa</a>: 400 studenti celebrano la Repubblica, a Cascina</li>
<li><a href="https://www.quinewspisa.it/pisa-studenti-a-lezione-di-anatomia-costituzionale.htm" rel="noopener">QuiNews Pisa</a>: Studenti a lezione di anatomia costituzionale</li>
<li><a href="https://icborsellino.edu.it/pagine/di-sana-e-robusta-costituzione" rel="noopener">Istituto Comprensivo Borsellino</a>: scheda didattica del progetto</li>
</ul>
</div></div></section>

<section class="tint"><div class="wrap split">
<div><h2>Come riconoscere l'originale</h2>
<p>Domande che ci arrivano da scuole, docenti e organizzatori.</p></div>
<div>{faq_html}</div>
</div></section>
"""
    s += cta_band("Scrivici") + footer()
    return s


def mailto(subject, body_lines):
    return "mailto:%s?subject=%s&body=%s" % (EMAIL, quote(subject), quote("\n".join(body_lines)))


def page_contatti():
    m_show = mailto(f"Richiesta spettacolo - {TITLE}", [
        "Scuola o istituto:", "Città e provincia:", "Ordine e grado (media/superiore):", "Numero indicativo di studenti:",
        "Data o periodo desiderati:", "Luogo (aula magna, teatro, palestra):",
        "Amplificazione, microfono ad archetto, proiettore con schermo e cavi HDMI disponibili (sì/no):",
        "Referente e telefono:", "Note:"])
    m_book = mailto(f"Ordine libro - {TITLE}", [
        "Scuola o ente:", "Numero di copie:", "Indirizzo di consegna:",
        "Dati per la fattura elettronica (codice destinatario o PEC):", "Referente e telefono:", "Note:"])
    m_other = mailto(f"Autorizzazione o segnalazione - {TITLE}", ["Di cosa si tratta:", "Dove e come verrebbero usati titolo, testi o immagini (o link all'iniziativa da segnalare):"])
    s = head(f"Contatti: prenota lo spettacolo o ordina il libro | {TITLE}",
             "Per prenotare lo spettacolo, ordinare il libro o chiedere un'autorizzazione basta una email. Qui trovi le informazioni da indicare.",
             "contatti.html")
    s += header("contatti.html")
    s += f"""<div class="wrap page-head"><h1>Contatti</h1>
<p class="lede">Si prenota e si ordina per email, all'indirizzo <a href="mailto:{EMAIL}">{EMAIL}</a>. Le informazioni qui sotto ci permettono di risponderti in un solo messaggio.</p></div>

<section style="padding-top:1rem"><div class="wrap">
<div class="form-card" id="spettacolo">
<h2>Richiedi lo spettacolo</h2>
<p>Nella email indica:</p>
<ul class="checklist">
<li>scuola o istituto, città e provincia</li>
<li>ordine e grado (scuola media o superiore) e numero indicativo di studenti</li>
<li>data o periodo desiderati</li>
<li>luogo dello spettacolo: aula magna, teatro, palestra</li>
<li>se sono disponibili amplificazione, microfono ad archetto, proiettore con schermo e cavi HDMI</li>
<li>nome del referente e un telefono</li>
</ul>
<p>I requisiti tecnici sono nella <a href="spettacolo.html">pagina dello spettacolo</a>.</p>
<div class="btn-row"><a class="btn" href="{m_show}">Scrivi per lo spettacolo</a></div>
</div>

<div class="form-card" id="libro">
<h2>Ordina il libro per la scuola</h2>
<p>Nella email indica:</p>
<ul class="checklist">
<li>scuola o ente e numero di copie</li>
<li>indirizzo di consegna</li>
<li>codice destinatario o PEC per la fattura elettronica</li>
<li>nome del referente e un telefono</li>
</ul>
<p>Ti rispondiamo con prezzo, tempi e modalità di pagamento.</p>
<div class="btn-row"><a class="btn" href="{m_book}">Scrivi per il libro</a></div>
</div>

<div class="form-card" id="altro">
<h2>Autorizzazioni e segnalazioni</h2>
<p>Per usare titolo, testi o immagini del progetto, o per segnalare un'iniziativa con un nome uguale o simile, scrivi spiegando di cosa si tratta e allegando, se esiste, il link.</p>
<div class="btn-row"><a class="btn ghost" href="{m_other}">Scrivi per un'autorizzazione</a></div>
</div>
<p class="form-note">Se il pulsante non apre il tuo programma di posta, copia l'indirizzo <strong>{EMAIL}</strong> e scrivi da dove preferisci.</p>
</div></section>
"""
    s += footer()
    return s


def page_privacy():
    s = head(f"Informativa sulla privacy | {TITLE}", "Come vengono trattati i dati inviati per email a chi gestisce il sito.", "privacy.html")
    s += header("privacy.html")
    s += f"""<div class="wrap page-head"><h1>Privacy</h1></div>
<section style="padding-top:1rem"><div class="wrap">
<h2>Informativa sul trattamento dei dati</h2>
<p><strong>Titolare del trattamento:</strong> {AUTHOR1}. Contatto: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h3>Quali dati e perché</h3>
<p>I dati che invii per email (nome del referente, scuola, recapiti, indirizzo di consegna, dati per la fatturazione e il contenuto della richiesta) servono a rispondere alla tua richiesta di spettacolo o di libro e a gestire l'eventuale accordo che ne segue. La base giuridica è l'esecuzione di misure precontrattuali richieste da te e, dopo l'accordo, l'esecuzione del contratto e gli obblighi di legge.</p>
<h3>Nessun modulo</h3>
<p>Il sito non ha moduli: le richieste arrivano solo per email. I dati restano nella casella di posta del titolare e nella tua.</p>
<h3>Conservazione e destinatari</h3>
<p>Conserviamo i dati per il tempo necessario a gestire la richiesta e gli obblighi contabili e fiscali. I dati non sono diffusi né ceduti a terzi, salvo i fornitori necessari alla consegna del libro o alla fatturazione.</p>
<h3>Cookie e strumenti di terze parti</h3>
<p>Il sito non usa cookie di profilazione né strumenti di analisi di terze parti. I caratteri tipografici sono ospitati sul sito stesso. Il fornitore di hosting può registrare dati tecnici di accesso, come l'indirizzo IP, per sicurezza e funzionamento del servizio.</p>
<h3>I tuoi diritti</h3>
<p>Puoi chiedere accesso, rettifica, cancellazione, limitazione e opposizione al trattamento scrivendo a {EMAIL}. Hai diritto di presentare reclamo al Garante per la protezione dei dati personali.</p>
</div></section>
"""
    s += footer()
    return s


def page_404():
    s = head(f"Pagina non trovata | {TITLE}", "La pagina cercata non esiste.", "404.html")
    s += header("")
    s += """<div class="wrap page-head"><h1>Pagina non trovata</h1>
<p class="lede">L'indirizzo che hai aperto non esiste più o non è mai esistito. Riparti dalla home.</p>
<div class="btn-row"><a class="btn" href="index.html">Torna alla home</a></div></div>
"""
    s += footer()
    return s


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in ("styles.css", "main.js"):
        shutil.copy(os.path.join(HERE, f), os.path.join(OUT, f))
    pages = {"index.html": page_home(), "spettacolo.html": page_spettacolo(), "libro.html": page_libro(),
             "il-progetto.html": page_progetto(), "contatti.html": page_contatti(), "privacy.html": page_privacy(),
             "404.html": page_404()}
    for n, c in pages.items():
        write(n, c)
    today = datetime.date.today().isoformat()
    urls = "".join(f"<url><loc>{DOMAIN}/{'' if n=='index.html' else n}</loc><lastmod>{today}</lastmod></url>"
                   for n in pages if n != "404.html")
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#F8E4D5"/><path d="M32 52S10 38 10 23c0-7 5-12 11-12 5 0 9 3 11 7 2-4 6-7 11-7 6 0 11 5 11 12 0 15-22 29-22 29z" fill="#8F3D49"/></svg>')
    # immagine per le anteprime social
    og = Image.new("RGB", (1200, 630), (248, 228, 213))
    body = Image.open(os.path.join(OUT, "img", "corpo-intero.webp")).convert("RGBA")
    body.thumbnail((900, 580))
    og.paste(body, ((1200 - body.width) // 2, (630 - body.height) // 2), body)
    og.save(os.path.join(OUT, "img", "og.jpg"), quality=88)
    print("ok", len(pages), "pagine")


if __name__ == "__main__":
    main()
