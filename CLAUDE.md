# CLAUDE.md — Site web d'AGS (à construire à partir du modèle S-ComPlus)

Objectif : créer le **site vitrine de l'entreprise AGS** (infrastructures télécoms, Mali). Il doit être **similaire au
site du groupe S-ComPlus SARL** (https://scomplusgroup.com), réalisé précédemment dans `../SComPlus-Groupe`.
Les échanges avec l'utilisateur se font **en français**.

## Ce que fait AGS (texte fourni par l'utilisateur)

Nos services à AGS :
1. **Implantation des sites** (sites télécoms : recherche, acquisition et préparation des emplacements d'antennes)
2. **Maintenance des sites Orange** (maintenance préventive et corrective des sites de l'opérateur Orange)
3. **Génie civil** (fondations, dalles, locaux techniques, clôtures des sites)
4. **Installations clients (FTTH)** (raccordement fibre optique jusqu'au domicile ou au bureau)
5. **Montage des pylônes** (levage et assemblage de pylônes et mâts télécoms)

Les précisions entre parenthèses sont des interprétations : **les faire valider par l'utilisateur**.

## Point de départ : ce dossier

C'est une **copie statique** (HTML + CSS + JS, sans serveur ni base de données) du site public de S-ComPlus,
**sans l'espace admin**, sans la partie SC+ Talent & Sports et sans formulaire de contact (il dépendait de Django).
**Tout le contenu est encore celui de S-ComPlus** : nom, logo, textes, images, contacts. Il faut tout remplacer.

```
index.html                     accueil : bannière (2 images qui alternent), bandeau des activités, manifeste,
                               grille « Nos activités », section « Le groupe » (présentation, 4 valeurs,
                               mot du dirigeant), bloc « Un projet ? », contact (WhatsApp, appel), FAQ
activites.html                 grille de toutes les activités (→ deviendra « Nos services »)
activite-<slug>.html           une page par activité : bannière photo, présentation, « Ce que nous proposons »,
                               contact, autres activités (7 pages S-ComPlus → 5 pages de services AGS)
mentions-legales.html          mentions légales et confidentialité (à adapter : éditeur, contacts)
assets/css/style.css           styles de base : couleurs (:root), typographie, en-tête, menu, bannière, pied de page
assets/css/pages.css           cartes d'activités (.agrid/.acard), pages d'activité (.ahero/.adetail), valeurs,
                               mot du dirigeant, images d'attente (.ph), responsive
assets/js/main.js              en-tête qui se cache au défilement, menu mobile, diaporama de la bannière,
                               textes animés au défilement (data-reveal, data-blur), année du pied de page
assets/img/logo/               logo S-ComPlus (à remplacer par celui d'AGS) ; assets/img/ia/ images IA S-ComPlus
assetsAGS/                     7 photos réelles fournies par le client (voir plus bas)
```

**Important :** l'en-tête, le menu et le pied de page sont **recopiés dans chaque fichier HTML** (il n'y a plus de
gabarit commun). Toute modification de ces parties doit être faite dans **tous** les fichiers.
`main.js` est chargé en script classique (`defer`) pour que le site fonctionne aussi en ouvrant les fichiers
directement (double-clic), sans serveur.

## Photos fournies par AGS (`assetsAGS/`)

Photos de téléphone en portrait (810 × 1080) :
- 3 photos de responsables à leur bureau (un en chemise bleue avec gilet orange sur la chaise, un en polo rayé) ;
- 2 photos de l'équipe terrain (7 personnes en gilets orange) devant le siège ;
- 1 photo de la façade du siège avec l'équipe.
Utiles pour la section de présentation / l'équipe. Les convertir en WebP allégé (Pillow, ~1600 px, qualité 82)
dans `assets/img/` plutôt que d'utiliser les originaux. Ce ne sont pas des photos de chantier : pour les bannières
et les services, prévoir des images IA ou de vraies photos de sites.

## Plan d'adaptation (à faire avec l'utilisateur)

1. **Demander d'abord** : nom complet d'AGS et signification, logo (fichier), téléphone/WhatsApp, e-mail, adresse,
   ville, slogan éventuel, nom de domaine, nom et photo du dirigeant.
2. **Identité** : remplacer le logo (`assets/img/logo/`, versions claire et sombre, détourées) et les couleurs
   (`:root` de `style.css` : `--gold` = couleur d'accent ; partir des couleurs du logo AGS). Favicon.
3. **Textes** : titre de la bannière, présentation, valeurs, mot du dirigeant, FAQ, balises `<title>`/`description`,
   mentions légales. Remplacer « groupe » par « entreprise » là où c'est pertinent.
4. **Activités → services** : 5 pages (renommer en `service-<slug>.html`, mettre à jour tous les liens), textes et
   listes « Ce que nous proposons » pour chaque service. ⚠️ La grille `.agrid` de `pages.css` est réglée pour
   **7 cartes** (première carte en grand, dernière en bandeau) : l'ajuster pour **5 cartes**.
5. **Images** : bannière d'accueil (2) + 1 par service, générées par l'utilisateur avec Gemini (prompts ci-dessous),
   puis converties en WebP dans `assets/img/`.
6. **Contact** : liens WhatsApp (`https://wa.me/<numéro>`), `tel:` et `mailto:` dans tous les fichiers. Pas de formulaire
   (site statique) ; si l'utilisateur en veut un, proposer un service comme Formspree, ou une version Django
   comme pour S-ComPlus.
7. **Vérifier** sur téléphone (360 px) et ordinateur : rien ne doit dépasser, le bouton WhatsApp flottant ne doit
   rien recouvrir, le bouton « Menu » n'apparaît que sous 1100 px.
8. **Mise en ligne** : seulement quand l'utilisateur le demande. Site statique = simple dossier servi par nginx ;
   le VPS de l'utilisateur (alias SSH `dilitech-vps`) héberge déjà d'autres sites : ne toucher qu'à ce projet.

## Prompts d'images (Gemini) pour les 5 services

Même style que S-ComPlus : photo réaliste, lumière dorée, Mali. À coller tel quel, format paysage 4:3
(première carte et bannière en 16:9). Toujours terminer par : *no text, no logo, no watermark*.

- **Implantation des sites** : `Photorealistic editorial photo, landscape 4:3. Telecom engineers surveying a new mobile network site in rural Mali, measuring a fenced plot of red laterite land with a GPS device and plans, a 4x4 vehicle nearby, savanna landscape, warm golden-hour light, safety vests and helmets. High detail, documentary style. No text, no logo, no watermark.`
- **Maintenance des sites** : `Photorealistic editorial photo, landscape 4:3. Two Malian telecom technicians in orange safety vests and helmets maintaining equipment at the base of a mobile network tower: open outdoor equipment cabinets, batteries and cables, laptop and tools, warm golden-hour light. High detail, documentary style. No text, no brand logo, no watermark.`
- **Génie civil** : `Photorealistic editorial photo, landscape 4:3. Civil works for a telecom tower site in Mali: workers pouring a reinforced concrete foundation, rebar cage, concrete mixer, formwork, red laterite ground, safety helmets and vests, warm golden-hour light. High detail, documentary style. No text, no logo, no watermark.`
- **Installations clients (FTTH)** : `Photorealistic editorial photo, landscape 4:3. Malian fiber optic technician in a safety vest installing a fiber optic connection in a modern home in Bamako, splicing yellow fiber cables with a fusion splicer, a router on the wall, bright natural light. High detail, documentary style. No text, no brand logo, no watermark.`
- **Montage des pylônes** : `Photorealistic editorial photo, landscape 16:9. Climbers with full safety harnesses assembling a tall steel lattice telecom tower in Mali, a crane lifting a tower section, team on the ground in orange vests and helmets, dramatic golden-hour sky. High detail, documentary style. No text, no logo, no watermark.`
- **Bannière d'accueil** : `Photorealistic aerial photo, landscape 16:9. Tall telecom towers rising above Bamako, Mali at golden hour, the Niger River and city in the background, warm haze, sense of connectivity and progress, copy space on the left. No text, no logo, no watermark.`

## Référence

Le projet modèle `../SComPlus-Groupe` (Django) contient le code source d'origine, son `CLAUDE.md`, l'outil de
conversion d'images (`outils/images.py`) et le détourage du logo (voir son historique git) : s'en inspirer.
Dossier non versionné pour l'instant (pas de dépôt git) : proposer `git init` avant les grosses modifications.
