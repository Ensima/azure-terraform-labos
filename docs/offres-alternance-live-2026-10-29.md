# Offres d'alternance cloud / infra en ligne : relevé du 29 octobre 2026

> Collecte automatique sur **HelloWork**, **France Travail** (qui reprend aussi les offres de La Bonne Alternance) et le **site carrière d'AXA**,
> pour l'Île-de-France. Mots-clés : cloud, DevOps, Azure, AWS, Terraform, Kubernetes, SRE, infrastructure, ingénieur système, FinOps, etc.
> **233 offres récupérées**, dont **49 en alternance dans le cloud, l'infra ou le DevOps**. Parmi elles, **42 sont publiées par des écoles**
> (offres de recrutement pour leurs propres formations, pas de vrais postes), et **6 viennent de grands employeurs**.
>
> Welcome to the Jungle et JobTeaser bloquent les robots. Les sites carrière de Thales, BNP, SG, VINCI, etc. ne sont pas encore autorisés
> dans l'environnement (voir « Pour aller plus loin »). Le script de collecte est dans `tools/veille-alternance/`.

## ⚠️ À lire avant tout

En octobre, les grands groupes recrutent pour un **démarrage immédiat**, pas pour septembre 2027.
Ces offres servent à **voir qui recrute et sous quels intitulés**, pas à postuler maintenant.
**Signal de calendrier confirmé** : l'alternance cyber d'AXA ci-dessous a été publiée le **8 avril 2026**, et l'alternance DevOps de Thales Avionics le **1er avril 2026**.
→ Le vrai créneau pour ta rentrée de septembre 2027 : **février à avril 2027**.

---

## ⭐ Offres VIP (grands employeurs), classées pour un profil « ingénieur cloud / infra »

| # | Employeur | Intitulé | Lieu | Publiée → expire | Pourquoi c'est intéressant | Lien |
|---|---|---|---|---|---|---|
| 1 | **AP-HP** (DSN, Centre de Solutions Infrastructures) | **Apprenti Ingénieur Infrastructure DevOps** | Paris | 15/10/2026 → 14/11/2026 | **Le plus proche du métier visé.** Équipe qui construit l'infrastructure : serveurs, stockage, réseau, 3 datacenters, virtualisation, **plateformes cloud**, **infrastructure en code**, **conteneurs**, conformité HDS (hébergement de données de santé), **CI/CD**. 1er employeur d'Île-de-France | [HelloWork](https://www.hellowork.com/fr-fr/emplois/79044890.html) |
| 2 | **AXA Group Operations** | **Security Monitoring Analyst APPRENTICESHIP** | **81 rue Mstislav Rostropovitch, Paris 17e** | **08/04/2026** → encore en ligne | Contrat de 24 mois, démarrage dès que possible. Cyber / SOC plutôt que cloud, mais AXA et 2 ans. **Confirme l'adresse d'AXA Group Operations** | [AXA](https://recrutement.axa.fr/emploi/paris/security-monitoring-analyst-apprenticeship/3441/46022465920) |
| 3 | **Direction générale du Trésor** (ministère) | Apprenti Ingénieur Système Réseaux et DevOps | Paris 12e | 28/10/2026 → 27/11/2026 | Exploitation de l'infra (Linux, Active Directory, réseau, pare-feu), sécurisation, automatisation. ⚠️ **Contrat d'un an exactement**, incompatible avec un MSc de 2 ans | [HelloWork](https://www.hellowork.com/fr-fr/emplois/84888269.html) |
| 4 | **Valeo** (Mobility Tech Center) | Alternant – Ingénieur Cloud & Tests Logiciels – Digital Key | Créteil (94) | 27/10/2026 → 26/11/2026 | Cloud côté qualité et tests de bout en bout (clé digitale de voiture), R&D. Plus test et développement qu'infra | [HelloWork](https://www.hellowork.com/fr-fr/emplois/84866744.html) |
| 5 | **Schneider Electric** (filiale Etap) | Alternance Développement Cloud / IA / DevOps | Colombes (92) | ≈ 07/10/2026 | Cloud et DevOps, mais orienté développement | [France Travail](https://candidat.francetravail.fr/offres/recherche/detail/214XXXM) |
| 6 | LACROIX SAVAC (transport, taille moyenne) | Ingénieur Data – DevOps en Alternance | Paris 8e | ≈ 03/10/2026 | Data + DevOps | [France Travail](https://candidat.francetravail.fr/offres/recherche/detail/7611985) |

## 👀 À surveiller (grands groupes qui recrutent en ce moment sur ces métiers, hors alternance)

- **Thales** : **9 stages DevOps / infra / réseaux publiés le 28/10/2026** à Gennevilliers (DevOps Infrastructure et Système, DevOps & Conteneurisation,
  DevOps Réseaux d'infrastructure…) et 2 stages cyber à Vélizy. La campagne de stages tourne en ce moment, les alternances arrivent au printemps.
- **AXA** : postes en CDI qui montrent où sont les équipes cloud et infra : *Responsable DevOps ALM / Platform Engineering* (Suresnes),
  *Workplace Infrastructure Architecture Expert*, *Data Center Urbanization Officer*, *Microsoft 365 Platform Expert* (Paris).
  Sites AXA vus : Paris 17e, Suresnes, Nanterre, Malakoff. ⚠️ La date « 16/10/2026 » affichée par la recherche AXA est une date de réindexation,
  pas la date de publication réelle.

## 🚫 Offres d'écoles (à ignorer)

42 offres « Administrateur Cloud & DevSecOps », « Administrateur Systèmes et Réseaux »… publiées par **Institut F2I (15), REDSUP (13), IFFP (3), ISCOD (3),
NEXA (2), Studi (2)**, etc. Ce sont des **campagnes de recrutement d'étudiants** pour leurs formations, pas des postes en entreprise.

---

## Pour aller plus loin

Pour récupérer **toutes** les offres des grands groupes, il faut autoriser leurs sites carrière dans l'environnement
(menu de l'environnement cloud → Edit → Network access → Allowed domains) :

`labonnealternance.apprentissage.beta.gouv.fr` (agrège toutes les offres d'alternance) · `careers.thalesgroup.com` · `group.bnpparibas` ·
`careers.societegenerale.com` · `jobs.vinci.com` · `www.safran-group.com` · `www.capgemini.com` · `orange.jobs` · `www.devoteam.com`

**Relancer la collecte** (de préférence chaque semaine de février à avril 2027) :

```bash
python3 -I tools/veille-alternance/collect.py <dossier_sortie>
python3 -I tools/veille-alternance/analyze.py <dossier_sortie>/offers_raw.json <dossier_sortie>/offers_classified.json
```
