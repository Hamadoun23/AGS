"""Génère toutes les pages HTML du site AGS à partir des données ci-dessous.

Usage, depuis la racine du projet :   python outils/generer.py

L'en-tête, le menu et le pied de page sont communs : les modifier ici, puis relancer.
Site en page unique (index.html) + mentions légales.
Les images de services sont prises dans assets/img/ia/service-<slug>.webp si elles existent
(sinon une image d'attente s'affiche) : voir outils/images.py.
"""
import sys
from pathlib import Path
from urllib.parse import quote

RACINE = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Identité et coordonnées  (⚠ À COMPLÉTER avec les vraies informations d'AGS)
# ---------------------------------------------------------------------------
NOM = 'AGS'                      # nom affiché partout (ex. « AGS SARL »)
VILLE = 'Bamako, Mali'
TEL_AFFICHE = '+223 00 00 00 00'  # À COMPLÉTER
TEL_LIEN = '+22300000000'         # À COMPLÉTER (format tel:)
WHATSAPP = '22300000000'          # À COMPLÉTER (format wa.me, sans +)
EMAIL = 'contact@ags.ml'          # À COMPLÉTER
MESSAGE_WA = f'Bonjour {NOM}, je vous contacte depuis votre site.'

# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
SERVICES = [
    dict(
        slug='implantation-des-sites', titre='Implantation des sites', court='Implantation des sites',
        accroche='Trouver, sécuriser et préparer le bon emplacement pour chaque antenne.',
        texte=[
            'Avant qu’une antenne puisse émettre, il faut lui trouver sa place. Nos équipes recherchent les '
            'terrains qui répondent aux exigences de couverture de l’opérateur, rencontrent les propriétaires '
            'et constituent les dossiers nécessaires à l’acquisition du site.',
            'Une fois l’emplacement validé, nous préparons le terrain pour que les travaux de génie civil et '
            'le montage du pylône démarrent sans attendre.',
        ],
        offre=['Recherche et prospection de sites', 'Négociation avec les propriétaires et acquisition',
               'Relevés GPS, visites techniques et rapports de site', 'Démarches administratives et autorisations',
               'Préparation et aménagement du terrain'],
    ),
    dict(
        slug='maintenance-des-sites', titre='Maintenance des sites Orange', court='Maintenance des sites Orange',
        accroche='Garder le réseau en service, de jour comme de nuit.',
        texte=[
            'Nous assurons la maintenance de sites télécoms du réseau Orange. Nos techniciens réalisent les '
            'visites préventives programmées et interviennent rapidement en cas de panne pour limiter les '
            'coupures de service.',
            'Énergie, climatisation, équipements, abords du site : chaque intervention est suivie d’un rapport '
            'pour garder un historique fiable de l’état des sites.',
        ],
        offre=['Maintenance préventive programmée', 'Interventions correctives et dépannages',
               'Entretien des groupes électrogènes, batteries et systèmes solaires',
               'Contrôle de la climatisation et des équipements', 'Rapports d’intervention et suivi des sites'],
    ),
    dict(
        slug='genie-civil', titre='Génie civil', court='Génie civil',
        accroche='Des fondations solides pour des infrastructures durables.',
        texte=[
            'Un site télécom repose d’abord sur des ouvrages bien construits. Nous réalisons les fondations des '
            'pylônes, les dalles et les locaux techniques qui accueillent les équipements, ainsi que les '
            'clôtures qui protègent le site.',
            'Nos chantiers sont menés dans le respect des plans, des normes de construction et des règles de '
            'sécurité, du terrassement jusqu’à la réception.',
        ],
        offre=['Fondations et massifs en béton armé pour pylônes', 'Dalles et plateformes pour équipements',
               'Construction de locaux techniques', 'Clôtures, portails et sécurisation des sites',
               'Terrassement et voies d’accès'],
    ),
    dict(
        slug='installations-ftth', titre='Installations clients (FTTH)', court='Installations FTTH',
        accroche='La fibre optique jusqu’au domicile et au bureau.',
        texte=[
            'Le FTTH (« fibre jusqu’à l’abonné ») apporte l’internet très haut débit directement chez le client. '
            'Nos techniciens réalisent le raccordement depuis le réseau jusqu’à la prise optique, au domicile '
            'comme en entreprise.',
            'Chaque installation est soignée, testée et mise en service avant notre départ, pour que le client '
            'profite tout de suite de sa connexion.',
        ],
        offre=['Raccordement fibre des particuliers et des entreprises', 'Tirage de câble aérien ou souterrain',
               'Soudure et pose de la prise optique', 'Installation et mise en service du modem',
               'Tests et mesures de la liaison'],
    ),
    dict(
        slug='montage-des-pylones', titre='Montage des pylônes', court='Montage des pylônes',
        accroche='Monter haut, en toute sécurité.',
        texte=[
            'Nos équipes de monteurs assemblent et lèvent les pylônes et les mâts qui portent les antennes du '
            'réseau mobile. Chaque montage suit les plans du constructeur et les règles strictes du travail en '
            'hauteur.',
            'Harnais, lignes de vie, contrôle du matériel : la sécurité de nos monteurs passe avant tout, à '
            'chaque étape du chantier.',
        ],
        offre=['Assemblage et levage de pylônes autoportants et haubanés', 'Montage de mâts et supports d’antennes',
               'Pose d’antennes et de faisceaux hertziens', 'Travaux en hauteur par des équipes formées et équipées',
               'Renforcement et démontage de pylônes'],
    ),
]

# ---------------------------------------------------------------------------
# Gabarits communs
# ---------------------------------------------------------------------------
ICO_WA = ('<svg class="ico-wa" viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3C9 3 3.3 8.6 3.3 15.6c0 2.2.6 4.4 1.7 6.3L3.2 28.8l7.1-1.8c1.8 1 3.8 1.5 5.8 1.5 7 0 12.7-5.7 12.7-12.6S23 3 16 3zm0 23.2c-1.9 0-3.8-.5-5.4-1.5l-.4-.2-4.2 1.1 1.1-4.1-.3-.4a10.4 10.4 0 0 1-1.6-5.5C5.2 9.8 10 5.1 16 5.1s10.7 4.7 10.7 10.5S21.9 26.2 16 26.2zm5.9-7.8c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7.1a8.6 8.6 0 0 1-4.3-3.7c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.6 5.8 5 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5 0-.1-.2-.2-.5-.4z"/></svg>\n')
WA = f'https://wa.me/{WHATSAPP}?text={quote(MESSAGE_WA)}'
SLOGAN = 'Bâtir le réseau, connecter le Mali.'


def logo():
    # Logo provisoire en texte, à remplacer par <img class="marque" ...> quand le logo AGS sera fourni
    return f'<span class="marque marque--texte" aria-hidden="true">{NOM}<i></i></span>'


def image(fichier, alt='', nom_attente='Image à venir', lazy=True, style=''):
    if (RACINE / fichier).exists():
        charge = ' loading="lazy"' if lazy else ' fetchpriority="high"'
        st = f' style="{style}"' if style else ''
        return f'<img src="{fichier}" alt="{alt}"{charge}{st}>'
    return f'<span class="ph" role="presentation"><span class="ph__nom">{nom_attente}</span></span>'


def img_service(s):
    return image(f'assets/img/ia/service-{s["slug"]}.webp', nom_attente=f'Image à venir : {s["court"]}')


def tete(titre, description):
    return f'''<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titre}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#1E1E1E">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{titre}">
  <meta property="og:description" content="{SLOGAN} Infrastructures télécoms au Mali.">
  <meta property="og:locale" content="fr_FR">
  <link rel="icon" type="image/png" href="assets/img/favicon.png">
  <link rel="apple-touch-icon" href="assets/img/logo/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,300..800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="assets/css/pages.css">
  <script>document.documentElement.classList.add('js')</script>
  <script src="assets/js/main.js" defer></script>
</head>
<body>
  <a class="skip" href="#contenu">Aller au contenu</a>
  <div class="grid-lines" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
'''


def entete(page):
    def lien(href, texte, cle):
        cur = ' aria-current="page"' if cle == page else ''
        return f'<a href="{href}"{cur}>{texte}</a>'
    menu_services = ''.join(f'<a href="index.html#services">{s["court"]}</a>' for s in SERVICES)
    return f'''
  <header class="header" data-header>
    <a class="brand" href="index.html" aria-label="{NOM} — accueil">{logo()}</a>
    <nav class="nav-court" aria-label="Pages">
      {lien('index.html', 'Accueil', 'accueil')}
      <a href="index.html#entreprise">L’entreprise</a>
      <a href="index.html#services">Services</a>
      <a href="#contact">Contact</a>
    </nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu"><span data-menu-label>Menu</span></button>
  </header>

  <div class="menu" id="menu" hidden>
    <div class="menu__cols">
      <nav class="menu__links" aria-label="Menu principal">
        <a href="index.html">Accueil</a>
        <a href="index.html#entreprise">L’entreprise</a>
        <a href="index.html#services">Services</a>
        <a href="#contact">Contact</a>
      </nav>
      <nav class="menu__activites" aria-label="Nos services">
        {menu_services}
      </nav>
    </div>
    <div class="menu__foot">
      <span>{NOM}</span>
      <span>{VILLE}</span>
    </div>
  </div>

  <main id="contenu">
'''


CONTACT = f'''
<!-- ===== CONTACT ===== -->
<section class="contact" id="contact">
  <div class="wrap">
    <h2 class="display contact__title" data-blur>Parlons de votre projet</h2>
    <div class="contact__direct">
      <p>Le plus simple : écrivez-nous ou appelez-nous directement.</p>
      <div class="contact__boutons">
        <a class="btn-wa" href="{WA}" target="_blank" rel="noopener">{ICO_WA}Écrire sur WhatsApp</a>
        <a class="btn btn--line contact__tel" href="tel:{TEL_LIEN}">Appeler le {TEL_AFFICHE}</a>
      </div>
    </div>
  </div>
</section>
'''

PIED = f'''</main>

  <footer class="footer">
    <div class="wrap footer__cta">
      <p class="display footer__accroche">Un projet&nbsp;?<br>Parlons-en.</p>
      <div class="footer__actions">
        <a class="btn-wa" href="{WA}" target="_blank" rel="noopener">{ICO_WA}WhatsApp</a>
        <a class="footer__tel" href="tel:{TEL_LIEN}">{TEL_AFFICHE}</a>
        <a class="footer__tel" href="mailto:{EMAIL}">{EMAIL}</a>
      </div>
    </div>
    <div class="wrap footer__bas">
      <a class="footer__logo brand" href="index.html" aria-label="{NOM} — accueil">{logo()}</a>
      <nav class="footer__liens" aria-label="Plan du site">
        <a href="index.html#entreprise">L’entreprise</a>
        <a href="index.html#services">Services</a>
      </nav>
      <p class="footer__copy">© <span id="annee">2026</span> {NOM} · {VILLE} · <a href="mentions-legales.html">Mentions légales</a></p>
    </div>
    <div class="stripe" aria-hidden="true"></div>
  </footer>

  <!-- Bouton WhatsApp toujours accessible -->
  <a class="wa-flottant" href="{WA}" target="_blank" rel="noopener" aria-label="Nous écrire sur WhatsApp">{ICO_WA}</a>
</body>
</html>
'''


def carte(s):
    n = SERVICES.index(s) + 1
    return f'''<div class="acard">
  <span class="acard__img">{img_service(s)}</span>
  <span class="acard__body">
    <span class="acard__num">{n:02d}</span>
    <b>{s["titre"]}</b>
    <span>{s["accroche"]}</span>
  </span>
</div>'''


def grille(services, petit=False):
    cls = 'agrid agrid--petit' if petit else 'agrid'
    return f'<div class="{cls}">' + '\n'.join(carte(s) for s in services) + '</div>'


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_accueil():
    bandeau = ''.join(f'<span><i class="puce" aria-hidden="true"></i>{s["court"]}</span>' for s in SERVICES)
    bandeau_bis = ''.join(f'<span aria-hidden="true"><i class="puce"></i>{s["court"]}</span>' for s in SERVICES)
    banniere1 = 'assets/img/ia/accueil-banniere.webp'
    banniere2 = 'assets/img/ia/accueil-banniere-alt.webp'
    if not (RACINE / banniere1).exists():  # en attendant les images IA : photos de l'équipe
        banniere1, banniere2 = 'assets/img/ags/equipe-terrain.webp', 'assets/img/ags/siege-facade.webp'
    corps = f'''
<!-- ===== BANNIÈRE ===== -->
<section class="hero" id="accueil" aria-label="Présentation">
  <div class="hero__slides" aria-hidden="true">
    <div class="hero__slide is-active"><img src="{banniere1}" alt="" fetchpriority="high"></div>
    <div class="hero__slide" data-lazy><img data-src="{banniere2}" alt=""></div>
  </div>
  <div class="hero__shade"></div>
  <div class="wrap hero__content">
    <h1 class="display hero__title">
      <span class="line"><span style="--i:0">Bâtir</span> <span style="--i:1">le réseau,</span></span>
      <span class="line"><span style="--i:2">connecter</span> <span style="--i:3">le Mali.</span></span>
    </h1>
    <div class="hero__side hero__in">
      <p class="small">Implantation, génie civil, montage de pylônes, maintenance et fibre optique : {NOM} réalise les infrastructures télécoms, du terrain nu jusqu’au client raccordé.</p>
      <a class="btn btn--light" href="#services">Découvrir nos services</a>
    </div>
  </div>
</section>

<!-- ===== BANDEAU : services ===== -->
<div class="marquee" aria-label="Nos services">
  <div class="marquee__track">
    {bandeau}
    {bandeau_bis}
  </div>
</div>

<!-- ===== MANIFESTE ===== -->
<section class="statement" id="manifeste">
  <img class="statement__bg" src="assets/img/ags/siege-facade.webp" alt="" loading="lazy" style="object-position: 50% 55%">
  <div class="wrap statement__inner">
    <p class="display statement__text" data-reveal>
      Du terrain nu à l’antenne qui émet&nbsp;: une seule équipe, sur le terrain, à chaque étape de vos sites télécoms.
    </p>
    <a class="btn btn--light reveal" href="#entreprise">Découvrir l’entreprise</a>
  </div>
</section>

<!-- ===== NOS SERVICES ===== -->
<section class="sec" id="services">
  <div class="wrap">
    <div class="sec__head">
      <h2 class="display sec__title" data-blur>Nos services</h2>
      <p class="small">Cinq métiers complémentaires pour construire, raccorder et entretenir les réseaux de télécommunication.</p>
    </div>
    {grille(SERVICES)}
  </div>
</section>

<!-- ===== L'ENTREPRISE ===== -->
<section class="services light" id="entreprise">
  <div class="wrap">
    <h2 class="display services__title" data-blur>Une entreprise malienne au cœur des réseaux.</h2>
    <div class="groupe__texte"><p>{NOM} accompagne les opérateurs et les entreprises du secteur des télécommunications sur toute la vie d’un site&nbsp;: nous trouvons l’emplacement, construisons les ouvrages, montons les pylônes, entretenons les équipements et raccordons les clients à la fibre optique. Nos équipes, formées et équipées, interviennent depuis Bamako sur le terrain, avec un seul objectif&nbsp;: un réseau qui fonctionne.</p></div>
    <ul class="valeurs">
      <li><span>01</span><h3>Sécurité</h3><p>Équipements de protection, travail en hauteur encadré : chaque membre de l’équipe rentre chez lui en bonne santé.</p></li><li><span>02</span><h3>Réactivité</h3><p>Une panne coupe des milliers d’abonnés : nous intervenons vite, de jour comme de nuit.</p></li><li><span>03</span><h3>Qualité</h3><p>Des travaux conformes aux plans et aux normes des opérateurs, contrôlés et documentés.</p></li><li><span>04</span><h3>Proximité</h3><p>Des équipes maliennes, sur le terrain, qui connaissent les réalités du pays.</p></li>
    </ul>
  </div>
</section>

<!-- ===== MOT DU DIRIGEANT ===== -->
<section class="sec">
  <div class="wrap mot">
    <div class="mot__photo">{image('assets/img/ags/dirigeant.webp', nom_attente='Photo du dirigeant à venir')}</div>
    <div class="mot__texte">
      <h2 class="cv__h2">Le mot du dirigeant</h2>
      <blockquote class="display mot__citation">«&nbsp;Un réseau fiable commence sur le terrain.&nbsp;»</blockquote>
      <p>Derrière chaque appel passé et chaque connexion internet, il y a un pylône monté, une fondation coulée, un technicien qui intervient. Notre ambition est de faire ce travail avec sérieux et dans les règles, pour que les Maliens restent connectés, et de former une nouvelle génération de techniciens télécoms dans notre pays.</p>
      <p class="mot__signature">La Direction générale</p>
    </div>
  </div>
</section>

<!-- ===== PROJET ===== -->
<section class="ready">
  <div class="ready__img"><img src="assets/img/ags/equipe-terrain-2.webp" alt="L’équipe terrain d’{NOM} en gilets orange devant le siège" loading="lazy" style="object-position: 50% 50%"></div>
  <div class="ready__panel">
    <h2 class="display ready__title" data-blur>Un chantier en vue&nbsp;?</h2>
    <a class="btn btn--dark" href="#contact">Démarrer la conversation</a>
  </div>
</section>
{CONTACT}
<!-- ===== FAQ ===== -->
<section class="faq light" id="faq">
  <div class="wrap faq__inner">
    <h2 class="display faq__title">FAQ</h2>
    <div class="faq__list">
      <details><summary>Quels services proposez-vous&nbsp;?</summary><p>Implantation des sites, maintenance des sites Orange, génie civil, installations clients en fibre optique (FTTH) et montage des pylônes. Chaque service a sa page sur ce site.</p></details>
      <details><summary>Où intervenez-vous&nbsp;?</summary><p>Depuis Bamako, partout où nos clients ont besoin de nous au Mali.</p></details>
      <details><summary>Qu’est-ce que le FTTH&nbsp;?</summary><p>« Fiber To The Home » : la fibre optique tirée jusqu’au domicile ou au bureau de l’abonné. Elle offre un internet beaucoup plus rapide et plus stable que les connexions classiques.</p></details>
      <details><summary>Comment demander un devis&nbsp;?</summary><p>Écrivez-nous sur WhatsApp ou appelez-nous en précisant le service souhaité et la localisation du site. Nous revenons vers vous rapidement.</p></details>
      <details><summary>Recrutez-vous&nbsp;?</summary><p>Oui, selon les chantiers : techniciens, monteurs de pylônes, ouvriers de génie civil, techniciens fibre. Envoyez-nous un message sur WhatsApp.</p></details>
    </div>
  </div>
</section>
'''
    return (tete(f'{NOM} — Infrastructures télécoms au Mali',
                 f'{NOM}, entreprise malienne d’infrastructures télécoms : implantation des sites, maintenance '
                 f'des sites Orange, génie civil, installations fibre optique (FTTH) et montage des pylônes.')
            + entete('accueil') + corps + PIED)


def page_mentions():
    corps = f'''<section class="sec sec--top">
  <div class="wrap texte-legal">
    <h1 class="display sec__title sec__title--m">Mentions légales et confidentialité</h1>

    <h2 class="cv__h2">Éditeur du site</h2>
    <p>Ce site est édité par {NOM}, {VILLE}.<br>
      Téléphone : {TEL_AFFICHE} · E-mail : {EMAIL}.</p>

    <h2 class="cv__h2">Hébergement</h2>
    <p>Le site est hébergé sur un serveur privé, administré pour le compte de l’entreprise.</p>

    <h2 class="cv__h2">Données personnelles</h2>
    <p>Le site ne contient pas de formulaire et ne collecte aucune donnée personnelle. Les informations que vous
      nous transmettez sur WhatsApp, par téléphone ou par e-mail servent uniquement à vous répondre. Elles ne sont
      ni vendues ni transmises à des tiers.</p>
    <p>Vous pouvez demander à consulter, corriger ou supprimer les informations qui vous concernent en nous écrivant.</p>

    <h2 class="cv__h2">Cookies</h2>
    <p>Le site n’utilise ni publicité, ni outil de suivi, ni cookie.</p>

    <h2 class="cv__h2">Photos et textes</h2>
    <p>Les photos et textes de ce site appartiennent à {NOM} ou à ses partenaires.
      Ils ne peuvent pas être réutilisés sans autorisation.</p>
  </div>
</section>
{CONTACT}'''
    return tete(f'Mentions légales — {NOM}', f'Mentions légales et confidentialité du site {NOM}.') + entete('') + corps + PIED


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    pages = {'index.html': page_accueil(), 'mentions-legales.html': page_mentions()}
    for nom, html in pages.items():
        (RACINE / nom).write_text(html, encoding='utf-8', newline='\n')
        print('écrit', nom)


if __name__ == '__main__':
    main()
