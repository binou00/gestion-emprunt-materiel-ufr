// Build the user manual as a polished .docx
// Uses globally installed `docx` module.

const fs = require('fs');
const path = require('path');

const docxPath = '/usr/local/lib/node_modules_global/lib/node_modules/docx';
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
  VerticalAlign, PageNumber,
} = require(docxPath);

// ----- Page geometry (A4) -----
const PAGE_WIDTH_DXA = 11906;
const PAGE_HEIGHT_DXA = 16838;
const MARGIN_DXA = 1440;
const CONTENT_WIDTH = PAGE_WIDTH_DXA - 2 * MARGIN_DXA;

const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const borders = { top: border, bottom: border, left: border, right: border };

function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120, line: 300 },
    ...opts,
    children: [new TextRun({ text, ...(opts.run || {}) })],
  });
}

function richP(runs, opts = {}) {
  return new Paragraph({
    spacing: { after: 120, line: 300 },
    ...opts,
    children: runs,
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    pageBreakBefore: true,
    children: [new TextRun(text)],
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun(text)],
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    children: [new TextRun(text)],
  });
}

function bullet(text, runs) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80, line: 280 },
    children: runs || [new TextRun(text)],
  });
}

function num(text, runs) {
  return new Paragraph({
    numbering: { reference: "numbers", level: 0 },
    spacing: { after: 80, line: 280 },
    children: runs || [new TextRun(text)],
  });
}

function inline(text) {
  const parts = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let last = 0;
  let m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) parts.push(new TextRun({ text: text.slice(last, m.index) }));
    const tok = m[0];
    if (tok.startsWith('**')) {
      parts.push(new TextRun({ text: tok.slice(2, -2), bold: true }));
    } else if (tok.startsWith('`')) {
      parts.push(new TextRun({ text: tok.slice(1, -1), font: "Consolas" }));
    }
    last = re.lastIndex;
  }
  if (last < text.length) parts.push(new TextRun({ text: text.slice(last) }));
  return parts;
}

function makeTable(headers, rows, columnWidthsRel) {
  const totalRel = columnWidthsRel.reduce((a, b) => a + b, 0);
  const columnWidths = columnWidthsRel.map(w =>
    Math.floor((w / totalRel) * CONTENT_WIDTH)
  );
  const diff = CONTENT_WIDTH - columnWidths.reduce((a, b) => a + b, 0);
  columnWidths[columnWidths.length - 1] += diff;

  const headerRow = new TableRow({
    tableHeader: true,
    children: headers.map((h, i) => new TableCell({
      borders,
      width: { size: columnWidths[i], type: WidthType.DXA },
      shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
      margins: { top: 100, bottom: 100, left: 120, right: 120 },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({
        spacing: { before: 0, after: 0 },
        children: [new TextRun({ text: h, bold: true })],
      })],
    })),
  });

  const dataRows = rows.map(row => new TableRow({
    children: row.map((cell, i) => new TableCell({
      borders,
      width: { size: columnWidths[i], type: WidthType.DXA },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({
        spacing: { before: 0, after: 0 },
        children: inline(cell),
      })],
    })),
  }));

  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths,
    rows: [headerRow, ...dataRows],
  });
}

function spacer() {
  return new Paragraph({ spacing: { after: 120 }, children: [new TextRun("")] });
}

function coverPage() {
  const out = [];
  for (let i = 0; i < 6; i++) out.push(spacer());

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 240 },
    children: [new TextRun({
      text: "Manuel utilisateur",
      bold: true, size: 56, font: "Arial",
    })],
  }));
  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 480 },
    children: [new TextRun({
      text: "Plateforme de gestion d'emprunt du materiel UFR SI",
      bold: true, size: 36, font: "Arial",
    })],
  }));

  out.push(new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: "2E75B6", space: 1 } },
    spacing: { after: 360 },
    children: [new TextRun("")],
  }));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 160 },
    children: [new TextRun({ text: "Universite Iba Der Thiam de Thies", size: 28, bold: true })],
  }));
  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 480 },
    children: [new TextRun({ text: "UFR Sciences de l'Ingenieur", size: 26 })],
  }));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [new TextRun({ text: "Auteures", bold: true, size: 24 })],
  }));
  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [new TextRun({ text: "Bineta Elimane Hanne", size: 24 })],
  }));
  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 360 },
    children: [new TextRun({ text: "Aminata Kounta", size: 24 })],
  }));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [new TextRun({ text: "Licence 2 Geomatique", size: 22, italics: true })],
  }));
  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [new TextRun({ text: "Projet de Programmation Orientee Objet", size: 22, italics: true })],
  }));

  for (let i = 0; i < 6; i++) out.push(spacer());

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 0 },
    children: [new TextRun({ text: "Version 1.0 - avril 2026", size: 22, bold: true })],
  }));

  return out;
}

function tocPage() {
  return [
    new Paragraph({
      pageBreakBefore: true,
      heading: HeadingLevel.HEADING_1,
      children: [new TextRun("Table des matieres")],
    }),
    new TableOfContents("Table des matieres", {
      hyperlink: true,
      headingStyleRange: "1-3",
    }),
  ];
}

const sections = [];

sections.push(h1("1. Bienvenue"));
sections.push(richP(inline("Cette plateforme permet aux etudiants, enseignants et techniciens de l'UFR Sciences de l'Ingenieur de gerer en ligne l'emprunt du materiel topographique et geodesique : stations totales, recepteurs GNSS, niveaux, accessoires, equipements informatiques mobiles.")));
sections.push(p("Vous y trouverez :"));
sections.push(bullet("Un catalogue interactif du materiel disponible"));
sections.push(bullet("Un formulaire de demande avec geolocalisation sur carte"));
sections.push(bullet("Un suivi en temps reel du statut de vos demandes"));
sections.push(bullet("Un assistant IA pour repondre a vos questions techniques"));
sections.push(richP(inline("L'objectif est de remplacer la gestion papier par un systeme tracable, transparent et accessible 24 h / 24.")));

sections.push(h1("2. Premier acces"));
sections.push(h2("2.1 Creer un compte"));
sections.push(num("", inline("Ouvrez votre navigateur et allez sur l'adresse de la plateforme (par defaut : `http://127.0.0.1:8000`).")));
sections.push(num("", inline("Cliquez sur le bouton **S'inscrire** en haut a droite.")));
sections.push(num("Remplissez le formulaire d'inscription avec :"));
sections.push(bullet("", inline("Votre **prenom** et votre **nom** (tels qu'ils apparaissent sur votre carte d'etudiant)")));
sections.push(bullet("", inline("Votre **e-mail UFR** (utilise pour les notifications)")));
sections.push(bullet("", inline("Votre **filiere** (par exemple Geomatique L2)")));
sections.push(bullet("", inline("Votre **niveau** (L2, L3, M1, M2)")));
sections.push(bullet("", inline("Votre **telephone** (optionnel, utile pour les urgences terrain)")));
sections.push(bullet("", inline("Un **nom d'utilisateur** unique")));
sections.push(bullet("", inline("Un **mot de passe robuste** (au moins 8 caracteres, avec majuscules, chiffres et caracteres speciaux)")));
sections.push(num("", inline("Cliquez sur **Creer mon compte**.")));
sections.push(richP(inline("Votre compte est cree immediatement avec le role **Etudiant**. Vous etes connecte automatiquement.")));

sections.push(h2("2.2 Se connecter"));
sections.push(num("", inline("Cliquez sur **Connexion** en haut a droite.")));
sections.push(num("Entrez votre nom d'utilisateur et votre mot de passe."));
sections.push(num("", inline("Cliquez sur **Se connecter**.")));
sections.push(p("Vous arrivez sur la page d'accueil avec acces complet aux fonctionnalites."));

sections.push(h2("2.3 Se deconnecter"));
sections.push(richP(inline("Cliquez sur votre prenom en haut a droite, puis sur **Se deconnecter**.")));

sections.push(h1("3. Catalogue du materiel"));
sections.push(h2("3.1 Consulter le catalogue"));
sections.push(richP(inline("Cliquez sur **Catalogue** dans la barre de navigation. Vous voyez une grille de toutes les references disponibles a l'UFR.")));
sections.push(p("Pour chaque materiel, vous trouvez :"));
sections.push(bullet("", inline("**Nom** et **modele**")));
sections.push(bullet("", inline("**Categorie** (Station totale, GNSS, Niveau, Accessoire, etc.)")));
sections.push(bullet("", inline("**Etat** (Disponible, Emprunte, Maintenance, Hors service)")));
sections.push(bullet("", inline("**Stock** (quantite disponible / quantite totale)")));

sections.push(h2("3.2 Filtrer par categorie"));
sections.push(richP(inline("Au-dessus de la grille, des boutons de filtre permettent d'afficher seulement les materiels d'une categorie. Cliquez sur **Toutes** pour revenir a la vue complete.")));

sections.push(h2("3.3 Comprendre les etats"));
sections.push(makeTable(
  ["Pastille", "Signification"],
  [
    ["Vert Disponible", "Au moins une unite libre, vous pouvez l'emprunter"],
    ["Jaune Emprunte", "Toutes les unites sont actuellement sorties"],
    ["Bleu Maintenance", "En reparation, indisponible temporairement"],
    ["Gris Hors service", "Definitivement indisponible"],
  ],
  [3, 7]
));

sections.push(h1("4. Faire une demande d'emprunt"));
sections.push(h2("4.1 Acceder au formulaire"));
sections.push(richP(inline("Cliquez sur **Nouvelle demande** dans la barre de navigation, ou sur le gros bouton vert depuis la page **Catalogue**.")));

sections.push(h2("4.2 Remplir les informations de periode"));
sections.push(p("Dans la premiere carte Periode d'emprunt :"));
sections.push(num("", inline("Choisissez la **date de debut** : jour ou vous recupererez le materiel.")));
sections.push(num("", inline("Choisissez la **date de fin** : jour ou vous le rendrez. La date de fin est automatiquement contrainte a etre superieure ou egale a la date de debut.")));
sections.push(num("", inline("Saisissez le **motif** de la sortie : par exemple TP de leve topographique encadre par M. Diallo, Memoire de fin d'etudes - site de Mboro, etc. **Soyez precis** : un motif vague risque de faire refuser votre demande.")));

sections.push(h2("4.3 Localiser votre zone de travail"));
sections.push(p("Dans la carte Localisation :"));
sections.push(num("La carte est centree sur Thies par defaut."));
sections.push(num("", inline("**Cliquez** a l'endroit exact ou vous comptez utiliser le materiel. Un marqueur rouge apparait.")));
sections.push(num("", inline("Vous pouvez **glisser-deposer** ce marqueur pour ajuster sa position.")));
sections.push(num("", inline("Les champs **Latitude** et **Longitude** se remplissent automatiquement.")));
sections.push(num("", inline("Saisissez optionnellement un **nom de lieu** (ex : Campus UFR SI, Carriere de Pout).")));
sections.push(p("Cette geolocalisation aide les enseignants a comprendre votre besoin et permet a l'UFR de cartographier l'usage du materiel."));

sections.push(h2("4.4 Selectionner le materiel"));
sections.push(p("Dans la carte de droite Materiel a emprunter :"));
sections.push(num("Faites defiler la liste des equipements disponibles."));
sections.push(num("", inline("**Cochez** la case devant chaque materiel souhaite.")));
sections.push(num("Le champ quantite s'active automatiquement. Saisissez la quantite voulue (limitee au stock disponible affiche)."));
sections.push(num("Le compteur en haut a droite indique combien d'articles vous avez selectionnes."));

sections.push(h2("4.5 Soumettre"));
sections.push(richP(inline("Cliquez sur le bouton vert **Soumettre ma demande**. Vous etes redirige vers **Mes demandes** ou votre nouvelle demande apparait avec le statut **En attente**.")));

sections.push(h2("4.6 Delais et bonnes pratiques"));
sections.push(bullet("", inline("Soumettez votre demande **au moins 48 heures** a l'avance.")));
sections.push(bullet("", inline("Pour un TP encadre ou un projet important : **une semaine** d'avance.")));
sections.push(bullet("En periode d'examens, les ressources sont tres sollicitees : prevoyez large."));

sections.push(h1("5. Suivre mes demandes"));
sections.push(h2("5.1 Vue d'ensemble"));
sections.push(richP(inline("Cliquez sur **Mes emprunts** dans la barre de navigation. Vous voyez un tableau recapitulant toutes vos demandes, de la plus recente a la plus ancienne.")));

sections.push(h2("5.2 Comprendre les statuts"));
sections.push(makeTable(
  ["Statut", "Signification", "Action attendue de votre part"],
  [
    ["En attente", "Soumise, attente de validation", "Patientez (48 h ouvrees max)"],
    ["Approuvee", "Validee, prete a retirer", "Rendez-vous au laboratoire pour retirer"],
    ["Refusee", "Refusee par le validateur", "Lisez le motif, refaites une demande corrigee"],
    ["En cours", "Materiel retire, sortie en cours", "Rendez le materiel a la date prevue"],
    ["Restituee", "Materiel rendu, dossier clos", "Rien a faire"],
    ["Annulee", "Annulee par vous-meme", "Rien a faire"],
  ],
  [3, 5, 6]
));

sections.push(h2("5.3 Voir les details d'une demande"));
sections.push(richP(inline("Cliquez sur le bouton **Details** au bout de chaque ligne. Une zone se deplie en dessous avec :")));
sections.push(bullet("Le motif complet"));
sections.push(bullet("La liste des articles avec quantites"));
sections.push(bullet("Le lieu et les coordonnees GPS"));

sections.push(h2("5.4 Annuler une demande"));
sections.push(richP(inline("Tant qu'une demande est en statut **En attente**, vous pouvez l'annuler. Une fois approuvee, vous devez contacter directement l'enseignant ou le technicien.")));

sections.push(h1("6. Restitution"));
sections.push(h2("6.1 Avant de venir rendre le materiel"));
sections.push(p("Verifiez que :"));
sections.push(bullet("", inline("Les **batteries** sont rechargees (utilisez les chargeurs fournis)")));
sections.push(bullet("", inline("Le materiel est **propre** : essuyez la poussiere, verifiez les optiques")));
sections.push(bullet("", inline("Les **trepieds** sont plies, sangles serrees")));
sections.push(bullet("", inline("Les **prismes** sont ranges dans leur etui")));
sections.push(bullet("", inline("**Tous** les accessoires empruntes sont presents (cordons, telecommandes, mires, etc.)")));

sections.push(h2("6.2 A la restitution"));
sections.push(p("Le technicien verifie chaque article. Trois cas possibles pour chaque piece :"));
sections.push(bullet("", inline("**Bon etat** : le materiel revient en stock, rien a signaler.")));
sections.push(bullet("", inline("**Endommage** : une fiche de maintenance est ouverte. Selon la nature et la cause du dommage, vous pouvez etre amene a participer aux frais.")));
sections.push(bullet("", inline("**Perdu** : vous devez rembourser le materiel au prix de remplacement, apres verification (declaration de perte, recherche).")));

sections.push(h2("6.3 En cas de retard"));
sections.push(richP(inline("Un rappel automatique vous est envoye. Sans justificatif valable, vous pouvez etre suspendu temporairement de la plateforme et perdre la priorite sur vos prochaines demandes. **Prevenez toujours** le technicien des que vous savez que vous serez en retard.")));

sections.push(h1("7. Assistant IA"));
sections.push(h2("7.1 Acceder a l'assistant"));
sections.push(richP(inline("Cliquez sur **Assistant IA** dans la barre de navigation. Une fenetre de discussion s'ouvre.")));

sections.push(h2("7.2 Poser une question"));
sections.push(num("Tapez votre question dans le champ en bas (par exemple : Quelle est la precision de la station Leica TS06 ?)."));
sections.push(num("", inline("Cliquez sur **Envoyer** ou pressez Entree.")));
sections.push(num("L'assistant repond en quelques secondes."));

sections.push(h2("7.3 Que peut-il faire ?"));
sections.push(p("L'assistant est entraine sur :"));
sections.push(bullet("", inline("Les **fiches techniques** du materiel UFR (Leica TS06, Topcon CTS-112 R4, CHC i50/i73, Garmin, niveaux, etc.)")));
sections.push(bullet("", inline("Les **procedures** d'emprunt et de restitution")));
sections.push(bullet("", inline("Les **notions de topographie et geodesie** (angles, distances, nivellement, GNSS, projections UTM Senegal)")));
sections.push(bullet("", inline("Les **questions frequentes** des etudiants")));

sections.push(h2("7.4 Que ne peut-il pas faire ?"));
sections.push(bullet("Faire vos calculs de TP a votre place"));
sections.push(bullet("Repondre a des questions hors-perimetre (autres cours, vie universitaire en general)"));
sections.push(bullet("Remplacer un enseignant pour des questions de fond complexes"));
sections.push(bullet("Modifier vos demandes ou reserver du materiel pour vous"));

sections.push(h2("7.5 Conversations passees"));
sections.push(richP(inline("La barre laterale gauche liste vos conversations passees. Cliquez sur l'une d'elles pour reprendre la discussion. Cliquez sur **Nouvelle** pour demarrer une discussion vierge.")));

sections.push(h1("8. Profils et roles"));
sections.push(p("La plateforme distingue quatre roles, avec des permissions differentes."));

sections.push(makeTable(
  ["Role", "Permissions"],
  [
    ["Etudiant", "Consulter le catalogue ; soumettre des demandes ; suivre ses propres demandes ; discuter avec l'assistant IA. (Role par defaut a l'inscription.)"],
    ["Enseignant", "Herite des droits de l'etudiant. Ajoute : valider ou refuser les demandes des etudiants ; voir toutes les demandes de sa filiere."],
    ["Technicien", "Herite des droits etudiant. Ajoute : marquer les sorties et restitutions ; ouvrir des fiches de maintenance ; mettre a jour le stock."],
    ["Administrateur", "Tous les droits. Gere les utilisateurs, le catalogue, et accede au tableau de bord complet via /admin/."],
  ],
  [3, 9]
));

sections.push(h2("8.1 Etudiant"));
sections.push(p("C'est le role par defaut a l'inscription. Permet :"));
sections.push(bullet("Consulter le catalogue"));
sections.push(bullet("Soumettre des demandes"));
sections.push(bullet("Suivre ses propres demandes"));
sections.push(bullet("Discuter avec l'assistant IA"));

sections.push(h2("8.2 Enseignant"));
sections.push(p("Attribue par un administrateur. Herite des droits de l'etudiant et ajoute :"));
sections.push(bullet("Valider ou refuser les demandes des etudiants"));
sections.push(bullet("Voir toutes les demandes de sa filiere"));

sections.push(h2("8.3 Technicien"));
sections.push(p("Herite des droits etudiant. Ajoute :"));
sections.push(bullet("Marquer les sorties et restitutions"));
sections.push(bullet("Ouvrir des fiches de maintenance"));
sections.push(bullet("Mettre a jour le stock"));

sections.push(h2("8.4 Administrateur"));
sections.push(richP(inline("Tous les droits. Gere les utilisateurs, le catalogue, et accede au tableau de bord complet via `/admin/`.")));

sections.push(h1("9. Foire aux questions"));

const faqs = [
  ["J'ai oublie mon mot de passe.",
   "Contactez le technicien ou l'administrateur de l'UFR. Ils peuvent reinitialiser votre mot de passe manuellement. Une fonction mot de passe oublie par e-mail sera ajoutee prochainement."],
  ["Combien de materiels puis-je emprunter en meme temps ?",
   "Pas de limite stricte, mais votre demande doit etre justifiee. Le validateur peut refuser ou ajuster une demande qui mobilise trop de materiel."],
  ["Puis-je faire une demande pour mon binome et moi ?",
   "Oui. Une seule demande, faite par le chef de binome, avec les deux noms dans le motif."],
  ["Que se passe-t-il si du materiel tombe en panne pendant ma sortie ?",
   "Si vous prouvez une utilisation conforme, vous n'etes pas responsable. Signalez la panne au technicien a la restitution. Une fiche de maintenance est ouverte automatiquement."],
  ["J'ai perdu un prisme, dois-je rembourser ?",
   "Oui, sauf cas de force majeure prouve (vol avec depot de plainte). Le prix de remplacement vous sera communique par le technicien."],
  ["Le chatbot peut-il faire mes calculs de polygonale ?",
   "Il peut expliquer la methode et les formules. Pour le calcul lui-meme, utilisez Excel ou un logiciel dedie comme Covadis."],
  ["Mes donnees sont-elles confidentielles ?",
   "Oui. Seuls vous, l'enseignant validateur et le technicien voient vos demandes. Aucune donnee n'est partagee avec des tiers."],
];

for (const [q, r] of faqs) {
  sections.push(new Paragraph({
    spacing: { before: 160, after: 60 },
    children: [
      new TextRun({ text: "Q : ", bold: true }),
      new TextRun({ text: q, bold: true }),
    ],
  }));
  sections.push(new Paragraph({
    spacing: { after: 120, line: 300 },
    children: [
      new TextRun({ text: "R : ", bold: true }),
      new TextRun({ text: r }),
    ],
  }));
}

sections.push(h1("10. Contact et support"));
sections.push(p("Pour signaler un bug, suggerer une amelioration, ou demander de l'aide :"));
sections.push(bullet("", inline("**Auteures du projet** : Bineta Elimane Hanne, Aminata Kounta")));
sections.push(bullet("", inline("**Depot GitHub** : ouvrir une issue sur le depot du projet")));
sections.push(bullet("", inline("**Sur place** : laboratoire de topographie de l'UFR SI")));
sections.push(p("Bonne utilisation !"));
sections.push(spacer());
sections.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 360 },
  children: [new TextRun({
    text: "Manuel utilisateur - version 1.0 - avril 2026.",
    italics: true,
  })],
}));

const doc = new Document({
  creator: "Bineta Elimane Hanne & Aminata Kounta",
  title: "Manuel utilisateur - Plateforme UFR SI",
  description: "Manuel utilisateur de la plateforme de gestion d'emprunt du materiel UFR SI",
  styles: {
    default: {
      document: { run: { font: "Arial", size: 22 } },
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: "1F4E79" },
        paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "2E75B6" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: "404040" },
        paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }] },
      { reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }] },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: PAGE_WIDTH_DXA, height: PAGE_HEIGHT_DXA },
          margin: { top: MARGIN_DXA, right: MARGIN_DXA, bottom: MARGIN_DXA, left: MARGIN_DXA },
        },
        titlePage: true,
      },
      headers: {
        first: new Header({ children: [new Paragraph({ children: [new TextRun("")] })] }),
      },
      footers: {
        first: new Footer({ children: [new Paragraph({ children: [new TextRun("")] })] }),
      },
      children: coverPage(),
    },
    {
      properties: {
        page: {
          size: { width: PAGE_WIDTH_DXA, height: PAGE_HEIGHT_DXA },
          margin: { top: MARGIN_DXA, right: MARGIN_DXA, bottom: MARGIN_DXA, left: MARGIN_DXA },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "BFBFBF", space: 4 } },
            children: [new TextRun({
              text: "Manuel utilisateur - UFR SI",
              size: 18, italics: true, color: "595959",
            })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Page ", size: 18, color: "595959" }),
              new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "595959" }),
            ],
          })],
        }),
      },
      children: [...tocPage(), ...sections],
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(__dirname, "manuel_utilisateur.docx");
  fs.writeFileSync(out, buf);
  console.log("Wrote", out, buf.length, "bytes");
});
