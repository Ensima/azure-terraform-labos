# Veille alternance cloud / infra (Île-de-France)

Deux scripts Python sans dépendance externe (ils utilisent `curl`).

| Script | Rôle |
|---|---|
| `collect.py` | Collecte les offres sur HelloWork (alternance, Île-de-France), France Travail (recherche « alternance … », Île-de-France) et le site carrière d'AXA |
| `analyze.py` | Classe chaque offre : métier cloud / infra / DevOps, alternance ou non, grand employeur, école de formation, tier de l'entreprise |

```bash
mkdir -p /tmp/veille
python3 -I tools/veille-alternance/collect.py /tmp/veille
python3 -I tools/veille-alternance/analyze.py /tmp/veille/offers_raw.json /tmp/veille/offers_classified.json
```

Les mots-clés sont dans `HW_KEYWORDS`, `FT_KEYWORDS` et `AXA_KEYWORDS` (`collect.py`). La liste des grands employeurs et leur tier sont dans
`BIG` et `TIER` (`analyze.py`).
