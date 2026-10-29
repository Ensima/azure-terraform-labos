"""Classe les offres collectées : pertinence cloud/infra, alternance, type d'employeur.

Usage : python3 -I analyze.py <offers_raw.json> <out.json>
"""
import json
import re
import sys

offers = json.load(open(sys.argv[1], encoding="utf-8"))

TECH = re.compile(
    r"(?<!saint[- ])(?<!st[- ])\bcloud|devops|devsecops|\bsre\b|site reliability|platform|azure|\baws\b|\bgcp\b|"
    r"kubernetes|k8s|terraform|infra|syst[eè]me|r[ée]seau|sysops|finops|ing[ée]nieur(e)? de production|"
    r"exploitation|cyber|s[ée]curit[ée] (informatique|des syst|si\b|op[ée]rationnelle|cloud)|datacenter|data center|"
    r"administrateur",
    re.I,
)
NOT_TECH = re.compile(r"[ée]nergie|commercial|marketing|rh\b|ressources humaines|comptab|assistant|qualit[ée] \(|"
                      r"maintenance industrielle|[ée]lectrique|fluides|radiocommunication|embarqu|b[aâ]timent|g[ée]nie climatique|electricien|électricien|cvc|plomb", re.I)
ALT = re.compile(r"alternan|apprenti|apprenticeship|work[- ]study|contrat pro", re.I)

SCHOOLS = re.compile(
    r"aurlom|groupe igf|institut f2i|ief2i|redsup|aivancity|studi|iscod|iffp|nexa|\bcfa\b|futurae|efht|ynov|sup de vinci|aston|"
    r"esgi|ipssi|openclassrooms|digital school|business school|[ée]cole|formation|campus|academy|acad[ée]mie|"
    r"pour (notre|son|ses) entreprise[s]? partenaire|nos entreprises partenaires|recherche pour (son|l'un de ses) (client|partenaire)",
    re.I,
)

BIG = {
    "AXA": r"\baxa\b", "BNP Paribas": r"bnp", "Société Générale": r"soci[ée]t[ée] g[ée]n[ée]rale", "Crédit Agricole": r"cr[ée]dit agricole|ca-gip|lcl\b",
    "BPCE / Natixis": r"bpce|natixis|caisse d'[ée]pargne|banque populaire", "Generali": r"generali", "Allianz": r"allianz",
    "Thales": r"thales", "Safran": r"safran", "Airbus": r"airbus", "Dassault": r"dassault", "Naval Group": r"naval group",
    "MBDA": r"mbda", "ArianeGroup": r"ariane", "Schneider Electric": r"schneider", "Valeo": r"valeo", "Renault": r"renault",
    "Stellantis": r"stellantis", "Michelin": r"michelin", "Saint-Gobain": r"saint-gobain", "Alstom": r"alstom",
    "Orange": r"\borange\b", "Bouygues": r"bouygues", "SFR": r"\bsfr\b", "Free / Iliad": r"\biliad\b|scaleway",
    "Capgemini": r"capgemini", "Sopra Steria": r"sopra", "Atos / Eviden": r"\batos\b|\beviden\b", "Accenture": r"accenture",
    "Devoteam": r"devoteam", "Wavestone": r"wavestone", "Inetum": r"inetum", "CGI": r"\bcgi\b", "IBM": r"\bibm\b",
    "Alten / Akkodis": r"\balten\b|akkodis", "Microsoft": r"microsoft", "Google": r"google", "Amazon / AWS": r"amazon|\baws emea",
    "OVHcloud": r"ovh", "VINCI": r"vinci", "Eiffage": r"eiffage", "Spie": r"\bspie\b", "Veolia": r"veolia", "Suez": r"\bsuez\b",
    "Saur": r"\bsaur\b", "NGE": r"\bnge\b", "Fayat": r"fayat", "Onet": r"\bonet\b", "Icade": r"icade", "EDF": r"\bedf\b|enedis",
    "Engie": r"engie|grdf", "TotalEnergies": r"total ?energies", "RTE": r"\brte\b", "Orano": r"orano", "CEA": r"\bcea\b",
    "SNCF": r"sncf", "RATP": r"ratp", "La Poste / Docaposte": r"la poste|docaposte", "Air France": r"air france",
    "Groupe ADP": r"a[ée]roports de paris|groupe adp", "Carrefour": r"carrefour", "L'Oréal": r"l'or[ée]al", "LVMH": r"lvmh",
    "Sanofi": r"sanofi", "AP-HP": r"ap-hp|aphp", "État / ministères": r"minist[èe]re|direction g[ée]n[ée]rale|tr[ée]sor|dinum",
    "Banque de France": r"banque de france", "Caisse des Dépôts": r"caisse des d[ée]p[ôo]ts", "Worldline": r"worldline",
    "Ubisoft": r"ubisoft", "Publicis": r"publicis", "ENI": r"\beni\b", "Action Logement": r"action logement",
    "Vygon": r"vygon", "ADR Alcen": r"alcen", "Disneyland Paris": r"disney",
}
TIER = {"AXA": "S", "VINCI": "S", "Generali": "S", "Thales": "A", "Société Générale": "A", "Devoteam": "A",
        "Capgemini": "A", "BNP Paribas": "A", "Schneider Electric": "B", "Safran": "B", "Orange": "B", "Bouygues": "B"}

res = []
for o in offers:
    t = o["title"]
    blob = " ".join([o.get("company", ""), t, o.get("desc", "")])
    tech = bool(TECH.search(t)) and not NOT_TECH.search(t)
    alt = o["source"] == "HelloWork" or bool(ALT.search(t + " " + o.get("desc", ""))) or any("altern" in q or "apprenti" in q for q in o["queries"])
    if o["source"] == "AXA":
        alt = bool(ALT.search(t))
    if re.search(r"\bstage\b|internship|stagiaire", t, re.I) and not ALT.search(t):
        alt = False
    big = [name for name, rx in BIG.items() if re.search(rx, blob, re.I)]
    school = bool(SCHOOLS.search(o.get("company", "") + " " + o.get("desc", "")[:300])) and not big
    o.update({"tech": tech, "alternance": alt, "big": big, "school": school,
              "tier": min((TIER.get(b, "Z") for b in big), default="")})
    res.append(o)

json.dump(res, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sel = [o for o in res if o["tech"] and o["alternance"]]
print("tech+alternance:", len(sel), "| grands groupes:", sum(1 for o in sel if o["big"]), "| écoles:", sum(1 for o in sel if o["school"]))
for o in sorted(sel, key=lambda o: (not o["big"], o["school"], o["tier"] or "Z")):
    print(f"{'+'.join(o['big']) or ('ÉCOLE' if o['school'] else '-'):25.25} | {o['title'][:70]:70} | {o['company'][:22]:22} | {o['location'][:22]:22} | {o['date'][:22]} | {o['source']}")
