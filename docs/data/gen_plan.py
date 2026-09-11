import csv, collections, re
from pathlib import Path

OUT = Path("/home/loadren/Documents/Code/EchoesOfAzeroth_Voidstorm/docs/PLAN.md")
LOCS = ["frFR","deDE","esES","esMX","ptBR","ruRU","itIT","koKR","zhCN","zhTW"]

lf = {}
for line in open("listfile.csv", encoding="utf-8", errors="replace"):
    a,_,b = line.rstrip("\n").partition(";")
    if a.isdigit(): lf[int(a)] = b
kits = collections.defaultdict(list)
for r in csv.DictReader(open("SoundKitEntry.csv", encoding="utf-8")):
    kits[int(r["SoundKitID"])].append(int(r["FileDataID"]))
zm = {int(r["ID"]): r for r in csv.DictReader(open("ZoneMusic.csv", encoding="utf-8"))}
zim = {int(r["ID"]): r for r in csv.DictReader(open("ZoneIntroMusicTable.csv", encoding="utf-8"))}
areas = {int(r["ID"]): r for r in csv.DictReader(open("areatable.csv", encoding="utf-8"))}
loc = {l: {int(r["ID"]): r["AreaName_lang"] for r in csv.DictReader(open(f"areatable_{l}.csv", encoding="utf-8"))} for l in LOCS}
dur = {}
for f in ("durations_tbc.csv","durations_midnight.csv"):
    for r in csv.reader(open(f)):
        if r and r[0].isdigit() and not r[1].startswith("error"): dur[int(r[0])] = r[1]

def stem(fdid):
    return lf.get(fdid, "?").split("/")[-1].rsplit(".",1)[0]

def family_summary(fdids):
    fam = collections.OrderedDict()
    for f in sorted(fdids):
        s = stem(f)
        m = re.match(r"MUS_120_(.+)_([A-Z])$", s)
        if m:
            fam.setdefault(m.group(1).replace("_"," "), []).append(m.group(2))
        else:
            m2 = re.match(r"(.+?)(\d{2})$", s)
            if m2:
                fam.setdefault(m2.group(1) + "##", []).append(m2.group(2))
            else:
                fam.setdefault(s, [])
    out = []
    for k, v in fam.items():
        if k.endswith("##"):
            out.append(k[:-2] + (v[0] + "…" + v[-1] if len(v) > 2 else "/".join(v)))
        elif v:
            out.append(f"{k} {'/'.join(v)}")
        else:
            out.append(k)
    return " + ".join(out)

def native(area_id):
    a = areas[area_id]
    z = int(a["ZoneMusic"])
    if z == 0:
        return "—", ""
    r = zm[z]
    fd = set()
    for k in (int(r["Sounds_0"]), int(r["Sounds_1"])):
        fd |= set(kits.get(k, []))
    return family_summary(fd), r["SetName"]

def fr(i): return loc["frFR"].get(i, "?")
def en(i): return areas[i]["AreaName_lang"]

# ---------------- Voidstorm thematic notes & proposals ----------------
ROLE = {
 15458:"Racine de la zone : steppes et routes (« VoidstormSouth »)",
 15963:"Steppes (zm = 0, hérite de la racine)",
 16360:"Bordure extérieure (« Outerborder »)",
 15949:"Hub ren'dorei d'arrivée (« VoidElfCampAlpha »)",
 15950:"Hub principal de la Singularité (« VoidElfCampBeta »)",
 15951:"Hub tertiaire sur une crête (« VoidElfCampCharlie »)",
 16844:"Auberge de la crête Hurlante (flag auberge)",
 15952:"Point-nexus = pylône drainant le Vide (« PylonAlpha »)",
 15954:"Point-nexus en ruine, entrée du donjon (« PylonCharlie »)",
 15955:"Point-nexus (« PylonEcho »)",
 15953:"Camp des éthérés de l'Ethereum (« PylonBeta »)",
 15962:"Raffinerie éthérée (« EtherealEnergyRefinery »)",
 15967:"Exploitation éthérée (« EtherealEnergyFarm »)",
 15956:"Forteresse de la Horde dévorante, cible de l'assaut Stormarion (« VoidFortressA »)",
 16485:"Citadelle Stormarion après l'assaut : musique native = hub ren'dorei",
 16486:"Guet Stormarion (« VoidFortressWatch »)",
 15957:"Seconde forteresse de la Horde dévorante (« VoidFortressB »)",
 15960:"Extérieur du raid, siège de Xal'atath (« RaidOutdoor »)",
 15961:"Approche de la Voidspire (« VoidSpireEntrance »)",
 16341:"« RaidInterstitial » / kit « Deep Sea » : placeholder Shadowlands (Seat of the Primus)",
 16581:"Terrier abondant (entrée de gouffre Voidburrow ?)",
 15964:"Mue du kaiju (« KaijuCorpse ») : natif = silence, pauses 30–45 s",
 16364:"Terriers sous la Mue (WMO) : natif = silence",
 15965:"Terriers Tranchants (zm = 0)",
 15966:"Tanière du kaiju Predaxas (« KaijuDen »)",
 16534:"Repaire de Predaxas (gouffre, même kit)",
 16501:"Tranchée (kit « Gorging Pit »)",
 16804:"Fosse du boss mondial (« WorldBossPOI »)",
 16652:"Terriers (« FidoBurrowsWMO »)",
 16863:"Grotte (« Local13CaveB »)",
 16864:"Grotte (« Local13CaveA »)",
 16429:"Taudis des exilés : draeneï / Brisés de Voidstorm",
 15959:"Zone PvP monde, racine (carte UiMap 2444)",
 16649:"Hub PvP neutre, parent (duels, marchands)",
 15958:"Hub PvP neutre, enfant",
 15970:"Flèche Alliance (général Ziadan)",
 16850:"Auberge Alliance",
 16223:"Avant-poste Alliance (zm = 0)",
 15971:"Flèche Horde (général Vidious)",
 16851:"Auberge Horde",
 16216:"Avant-poste Horde (zm = 0)",
 15973:"Arène extérieure (kit Horde dévorante)",
 16218:"Raffinerie éthérée dans Slayer's Rise (« PortalCavern »)",
 16219:"Carcasse (kit « Gorging Pit »)",
 16221:"Avant-poste éthéré ouest (zm = 0)",
 16222:"Avant-poste éthéré est (zm = 0)",
 16600:"Avant-poste éthéré est 2 (zm = 0)",
 15974:"Route de parade PvP (zm = 0)",
 15975:"Champ central neutre (zm = 0)",
 15976:"POI expédition (zm = 0)",
 15977:"POI expédition (zm = 0)",
 16213:"Falaise est (zm = 0)",
 16214:"Falaise ouest (zm = 0)",
 16220:"Terrain de duel (zm = 0)",
}
PROP = {
 15458:"NETHERSTORM", 15963:"NETHERSTORM", 16360:"NETHERSTORM", 16341:"NETHERSTORM",
 15949:"AREA52", 15950:"AREA52", 15951:"AREA52", 16844:"AREA52",
 15952:"MANAFORGE", 15954:"MANAFORGE", 15955:"MANAFORGE",
 15953:"ETHEREUM", 15962:"ETHEREUM", 15967:"ETHEREUM", 16218:"ETHEREUM", 16221:"ETHEREUM", 16222:"ETHEREUM", 16600:"ETHEREUM",
 15956:"FORGE_BASE", 16486:"FORGE_BASE", 15957:"FORGE_BASE", 15973:"FORGE_BASE",
 16485:"SUNFURY",
 15960:"TEMPEST_KEEP", 15961:"TEMPEST_KEEP",
 15964:"MOLT", 16364:"MOLT", 15965:"MOLT", 16652:"MOLT", 16581:"MOLT",
 15966:"WILDS", 16534:"WILDS", 16501:"WILDS", 16804:"WILDS", 16219:"WILDS", 16863:"WILDS", 16864:"WILDS",
 16429:"ENKAAT",
 15959:"EYE_OF_THE_STORM", 16649:"AREA52", 15958:"AREA52",
 15970:"OUTLAND_ALLIANCE", 16850:"OUTLAND_ALLIANCE", 16223:"OUTLAND_ALLIANCE",
 15971:"OUTLAND_HORDE", 16851:"OUTLAND_HORDE", 16216:"OUTLAND_HORDE",
 15974:"EYE_OF_THE_STORM", 15975:"EYE_OF_THE_STORM", 15976:"EYE_OF_THE_STORM", 15977:"EYE_OF_THE_STORM", 16213:"EYE_OF_THE_STORM", 16214:"EYE_OF_THE_STORM", 16220:"EYE_OF_THE_STORM",
}

GROUPS = [
 ("A. Racine et steppes", [15458, 15963, 16360, 16341, 16581]),
 ("B. Hubs ren'dorei (la Singularité)", [15949, 15950, 15951, 16844]),
 ("C. Points-nexus (pylônes du Vide)", [15952, 15954, 15955]),
 ("D. Éthérés de l'Ethereum", [15953, 15962, 15967]),
 ("E. Forteresses de la Horde dévorante", [15956, 16485, 16486, 15957]),
 ("F. La Voidspire (extérieur du raid)", [15960, 15961]),
 ("G. Faune de Predacea, mue et terriers", [15964, 16364, 15965, 15966, 16534, 16501, 16804, 16652, 16863, 16864]),
 ("H. Exilés", [16429]),
 ("I. Slayer's Rise (zone PvP, carte 2444)", [15959, 16649, 15958, 15970, 16850, 16223, 15971, 16851, 16216, 15973, 16218, 16219, 16221, 16222, 16600, 15974, 15975, 15976, 15977, 16213, 16214, 16220]),
]

NS_THEME = {
 3523:"Racine : anciennes terres de Farahlon rongées par le Néant",
 3712:"Ville gobeline neutre (fusée X-52)",
 3724:"Base gobeline est",
 3721:"Terres qui s'effritent au bord du Néant",
 3722:"Manaforge Sunfury (Kael'thas), draine le Néant",
 3726:"Manaforge Sunfury",
 3730:"Manaforge Sunfury",
 3734:"Manaforge Sunfury (champs du vortex)",
 3736:"Manaforge détruite, infestée de créatures du Vide",
 3881:"Mine sous Manaforge Ara",
 3837:"Bastion militaire elfe de sang",
 3842:"Forteresse naaru capturée par Kael'thas (raid L'Œil + 3 donjons)",
 5554:"Entrée du Méchanar", 5555:"Entrée de la Botanica", 5556:"Entrée de l'Arcatraz",
 3738:"QG des éthérés du Consortium",
 3874:"Écodôme éthéré", 3875:"Écodôme éthéré", 3876:"Écodôme éthéré", 3877:"Écodôme éthéré",
 3851:"Comptoir du Consortium dans l'écodôme",
 3854:"Poste des éthérés du Protectorat",
 3878:"Camp des éthérés de l'Ethereum (touchés par le Vide)",
 3873:"Terrain d'essai (éthérés)",
 3739:"Base de la Légion ardente (saccageurs gangrenés)",
 3740:"Base de la Légion ardente",
 3882:"Site d'invasion de la Légion", 3900:"Site d'invasion de la Légion",
 3742:"Forteresse du commandant de la Légion",
 3741:"Ruines draeneï tenues par la Légion",
 3723:"Ruines draeneï infestées de démons", 3921:"Crête des ruines Arklon",
 3725:"Ruines draeneï hantées d'esprits",
 3732:"Village Kirin Tor abandonné, hanté", 3733:"Tour de Kirin'Var", 3934:"Place de Kirin'Var", 3935:"Allée de Kirin'Var", 3879:"Cour de la chapelle (Kirin'Var)",
 3737:"Forêt de cristaux arcaniques, nid des drakes du Néant",
 3850:"Zone élite arcanique",
 3735:"Plateau corrompu par le Vide",
 3728:"Champs du vortex (Manaforge Duro)",
 3731:"Faille des Tempêtes",
 3727:"Casse gobeline (Légion)", 3729:"Décharge gobeline", 3883:"Camp du Dr Boum",
 3868:"Pont gobelin vers les Tranchantes",
 3880:"Puits d'accès (mine)",
 3852:"Point d'ancrage de Tuluman",
 8613:"Taverne de Zone 52",
}

def ns_intro(a):
    i = int(a["IntroSound"])
    if not i: return "—"
    z = zim.get(i)
    if not z: return f"ZIM {i} ?"
    files = [stem(f) for f in kits.get(int(z["SoundID"]), [])]
    return f'{z["Name"]} → {", ".join(files)} (délai {z["MinDelayMinutes"]} min)'

# ---------------- write ----------------
L = []
w = L.append

w("# EchoesOfAzeroth_Voidstorm — plan de conception")
w("")
w("Rédigé le 11/09/2026 à partir des tables de jeu 12.1.0 (wago.tools : AreaTable, ZoneMusic, SoundKitEntry, ZoneIntroMusicTable, UiMap, Map) et du listfile communautaire wowdev. Toutes les localisations viennent d'AreaTable (10 locales). Les durées TBC ont été mesurées par ffprobe sur les fichiers téléchargés depuis wago.tools.")
w("")
w("## 0. Objectif")
w("")
w("Plugin de contenu pour le core `EchoesOfAzeroth`, sur le modèle de `_QuelThalas` et `_ZulAman` : remplacer, sous-zone par sous-zone, la musique de **Voidstorm** (Midnight, UiMapID 2405) par celle de **Netherstorm** (TBC, UiMapID 109) et de ses lieux apparentés (Donjon de la Tempête, Œil du cyclone, bases d'Outreterre). Convention des autres plugins conservée : pour chaque famille un pack **(TBC)**, un pack **(Midnight)** qui reproduit le kit natif, et un pack **(TBC + Midnight)** mixé.")
w("")
w("Lecture rapide du rapprochement : Netherstorm est Farahlon rongée par le Néant, avec des manaforges qui drainent l'énergie, des éthérés (Consortium, Protectorat, **Ethereum**), une forteresse volante (Donjon de la Tempête) et des bases de la Légion. Voidstorm est Predacea rongée par le Vide, avec des **points-nexus** qui drainent le Vide, des éthérés de **l'Ethereum** (même nom de faction), une forteresse-siège (la Voidspire) et des forteresses de la Horde dévorante. Le parallèle est presque terme à terme.")
w("")

# ---- 1. Voidstorm
w("## 1. Voidstorm — inventaire")
w("")
w("### 1.1 Cartes (UiMap) et instances")
w("")
w("| UiMapID | Nom | Type | Parent | Usage dans le plugin |")
w("|---|---|---|---|---|")
w("| 2405 | Voidstorm | zone | 2537 Quel'Thalas | entrée principale `[2405]` (monde ouvert, sous-zones par `GetSubZoneText()`) |")
w("| 2444 | Slayer's Rise | zone | 2405 | carte propre : entrée `[2444]` avec ses sous-zones (sans entrée, le core remonte sur 2405) |")
w("| 2556 | Nexus Point Xenas | donjon | 2405 | donjon (Map 2915, continent 2915) : `[2556]` |")
w("| 2572 / 2573 / 2574 | Voidscar Arena | donjon, 3 étages | 2405 | donjon (Map 2923) : mapper les 3 étages (résolution stricte en instance) |")
w("| 2529 / 2530 | The Voidspire | raid, 2 étages | 2405 | raid (Map 2912) |")
w("| 2526 / 2527 | Lair of Predaxas | micro (gouffre) | 2405 | gouffre |")
w("| 2581 / 2582 | Voidburrow | micro (gouffre) | 2405 | gouffre |")
w("| 2528 / 2571 | Sunkiller Sanctum | donjon (gouffre « 12DelvesDevouringHost02 », Map 2965) | 2405 | gouffre |")
w("| 2507 | Torment's Rise | donjon (boss de gouffre, Map 2966) | 2405 | gouffre |")
w("| 2506 | Shadowguard Point | donjon (Map 2979, scénario ?) | 2405 | à vérifier en jeu |")
w("| 2397 | Slayer's Rise | zone, parent 0 | — | champ de bataille épique instancié (Map 2799) : `[2397]` optionnel |")
w("| 2479 | Voidstorm | continent (flags 131076, atlas 5350) | 0 | carte cosmique d'affichage : ignorer |")
w("")
w("Tous les UiMapID d'instance sont à confirmer en jeu avec `/eoa now` (la mémoire du core rappelle que gouffres et lairs sont en difficultyID 208, type « scenario »).")
w("")
w("### 1.2 Sous-zones (AreaTable, continent 2771) et musique native")
w("")
w("Colonne « natif » = kit ZoneMusic réellement joué (lettres des fichiers `MUS_120_*`). « — » = pas de ZoneMusic propre, le jeu hérite du parent (la racine joue *Storm Fields* + *Gnawing Reach* B/D). Colonne « TBC » = pack proposé par défaut (définis en §3).")
w("")
for title, ids in GROUPS:
    w(f"#### {title}")
    w("")
    w("| AreaID | enUS | frFR | Natif (Midnight) | Rôle | TBC |")
    w("|---|---|---|---|---|---|")
    for i in ids:
        nat, _ = native(i)
        w(f"| {i} | {en(i)} | {fr(i)} | {nat} | {ROLE.get(i,'')} | `{PROP.get(i,'')}` |")
    w("")

w("#### J. Instances (continents propres)")
w("")
w("| AreaID | Continent | enUS | Natif (Midnight) | TBC proposé |")
w("|---|---|---|---|---|")
INST = [
 (16573,"2915 Nexus-Point Xenas","TEMPEST_KEEP"),(16574,"2915","TEMPEST_KEEP"),(16575,"2915","TEMPEST_KEEP"),(16576,"2915","TEMPEST_KEEP"),
 (16425,"2923 Voidscar Arena","TEMPEST_KEEP_BATTLE"),(16479,"2923 (réplique extérieure)","EYE_OF_THE_STORM"),(16480,"2923","EYE_OF_THE_STORM"),(16481,"2923","TEMPEST_KEEP_BATTLE"),(16482,"2923","WILDS"),(16483,"2923","EYE_OF_THE_STORM"),(16484,"2923","NETHERSTORM"),
 (16340,"2912 The Voidspire","TEMPEST_KEEP"),(16829,"2912","FORGE_BASE"),(16825,"2912","FORGE_BASE"),(16826,"2912","WILDS"),(16827,"2912","ETHEREUM"),(16828,"2912","TEMPEST_KEEP"),(16507,"2912","—"),(16639,"2912","—"),
 (16423,"2799 Slayer's Rise (BG)","EYE_OF_THE_STORM"),(16488,"2799","OUTLAND_ALLIANCE"),(16492,"2799","OUTLAND_ALLIANCE"),(16489,"2799","OUTLAND_HORDE"),(16491,"2799","OUTLAND_HORDE"),(16496,"2799","OUTLAND_HORDE"),(16494,"2799","ETHEREUM"),(16495,"2799","ETHEREUM"),(16499,"2799","ETHEREUM"),(16498,"2799","WILDS"),(16855,"2799","FORGE_BASE"),
 (16592,"2965 Sunkiller Sanctum","FORGE_BASE"),(16596,"2966 Torment's Rise","FORGE_BASE"),(16354,"2953 (gouffre Parhelion Plaza, aire « Voidstorm »)","—"),
]
for i, cont, p in INST:
    nat, _ = native(i)
    w(f"| {i} | {cont} | {en(i)} | {nat} | `{p}` |")
w("")
w("Remarques :")
w("")
w("- Dans le donjon Voidscar Arena, le sous-texte varie (Slayer's Rise, Pit of Spite, The Husk, Sparring Grounds, Grasping Reach) : les 3 étages `[2572..2574]` peuvent porter des sous-zones.")
w("- Le raid The Voidspire réutilise « Isle of Quel'Danas » et « Magisters' Terrace » pour la fin du boss 6 (musique Alleria) : ne pas mapper, laisser le natif.")
w("- Gnawing Reach (16341) joue nativement un placeholder Shadowlands (`mus_mx_cov_seatoftheprimus_01`), comme les flèches du BG instancié : Blizzard n'a pas fini ces kits, ce qui justifie encore plus un pack TBC.")
w("")

# ---- 1.3 Midnight tracks
w("### 1.3 Familles de pistes Midnight utilisées dans Voidstorm (FDID)")
w("")
FAMS = ["Voidstorm","Storm_Fields","Devouring_Host","Locus_Point","Howling_Ridge","Shadowguard_Void","Gnawing_Reach","Slayers_Rise","Void_Combat","Ethereal_Combat_Void","Xalatath_Midnight"]
QT_KNOWN = {7684188:"118.4",7684190:"122.2",7684192:"135.8",7684194:"153.6",7684196:"120.4",7684198:"161.6",7713420:"132.3"}
w("| Famille | Fichiers : lettre = FDID (durée s) |")
w("|---|---|")
for fam in FAMS:
    rows = sorted((stem(f)[-1], f) for f,p in lf.items() if re.search(rf"/MUS_120_{fam}_[A-Z]\.mp3$", p))
    w(f"| {fam.replace('_',' ')} | " + ", ".join(f"{l} = {f} ({dur.get(f) or QT_KNOWN.get(f,'?')})" for l,f in rows) + " |")
w("")
w("Durées mesurées par ffprobe le 11/09/2026 (`durations_midnight.csv`), sauf Locus Point reprises du plugin Quel'Thalas. Contrôle croisé : Voidstorm E, Storm Fields F, Slayers Rise B, Devouring Host I et G donnent les mêmes valeurs que les entrées `MN_ParhelionPlaza*` de Quel'Thalas.")
w("")
w("> **Effet de bord découvert** : dans `EchoesOfAzeroth_QuelThalas/Tracks.lua`, les pistes `VE_VoidstormA…H` sont en réalité `MUS_120_Locus_Point_A…E,H,F` + `Voidstorm_B`, et `MN_ParhelionPlazaE…I` sont `Voidstorm_E`, `Storm_Fields_F`, `Slayers_Rise_B`, `Devouring_Host_I`, `Devouring_Host_G`. Les FDID sont bons, seuls les noms symboliques sont trompeurs. À corriger dans un commit séparé du plugin Quel'Thalas, pas ici.")
w("")

# ---- 2. Netherstorm
w("## 2. Netherstorm — inventaire")
w("")
w("### 2.1 Cartes")
w("")
w("UiMapID 109 Netherstorm (parent 101 Outland). AreaTable racine 3523, 49 sous-zones directes (continent 530). Instances liées : Map 550 Tempest Keep (raid L'Œil), 552 Arcatraz, 553 Botanica, 554 Méchanar, 557 Auchindoun : Tombes-mana (donjon éthéré, en Terokkar), 566 / 968 Œil du cyclone (BG « NetherstormBG »).")
w("")
w("### 2.2 Musique native")
w("")
w("- **Zone entière** : ZoneMusic 272 « Zone-Netherstorm », kit 9284 = `NS_GeneralWalkUni01…10`, pauses de 3 à 5 min entre pistes. C'est la seule musique propre à la zone.")
w("- **Foudreflèche + 4 écodômes** : ZoneMusic 335 « Zone-NetherstormEco-Dome » = `NA_GeneralWalkDay01/02` (Nagrand) + `OL_HistoricIntroUni01`.")
w("- **Ruines d'Enkaat** : ZoneMusic 310 « Zone-OutlandDraeneiBase » = `OL_DraeneiBaseWalkUni01/02`.")
w("- **Bastion des Solfurie** : ZoneMusic 337 « Zone-OutlandBloodElfHostile » = `GL_Forest3WalkNight01…03` (déjà dans le plugin Quel'Thalas).")
w("- **Intros par sous-zone** (champ `IntroSound` d'AreaTable → ZoneIntroMusicTable, une fois par 10 ou 60 min) : c'est là que Netherstorm signe ses lieux. Les manaforges ont chacune une intro « Netherplant », les bases de la Légion une intro « Burning Legion », les zones de cristaux une intro « Crystal », les villes gobelines l'intro « Historic », les écodômes l'intro « Scenic ».")
w("- **Œil du cyclone** (ZoneMusic 2234, kit 129972) : `NS_GeneralWalkUni01/03/08` + `tk_TempestKeep_AMB_11/13/18` + `tk_TempestKeep_BTL13`, intro `OL_HistoricIntroUni01`.")
w("- **Donjon de la Tempête** (ZoneMusic 373 / 374) : `tk_TempestKeep_AMB_11…23` (ambiance), `BTL10/11/13` (combat), `STG14/15/16` (stingers de 12 s).")
w("- `NS_MushroomIntroUni01…03` existent dans le dossier Netherstorm mais ne sont plus référencés par aucune aire de la zone (réutilisés en Draenor) : utilisables comme intros « organiques ».")
w("")
w("### 2.3 Sous-zones (AreaTable, parent 3523)")
w("")
w("| AreaID | enUS | frFR | ZoneMusic natif | Intro (ZoneIntroMusicTable) | Thème |")
w("|---|---|---|---|---|---|")
ns_ids = [3523] + sorted(i for i,a in areas.items() if a["ParentAreaID"]=="3523")
for i in ns_ids:
    a = areas[i]
    nat, setname = native(i)
    natstr = "—" if nat == "—" else f"{setname} : {nat}"
    w(f"| {i} | {en(i)} | {fr(i)} | {natstr} | {ns_intro(a)} | {NS_THEME.get(i,'')} |")
w("")

# ---- 2.4 TBC tracks with durations
w("### 2.4 Pistes TBC candidates (FDID, durée mesurée)")
w("")
w("| FDID | Fichier | Durée (s) | Source native |")
w("|---|---|---|---|")
SRC = {
 **{f:"Netherstorm général (ZoneMusic 272)" for f in range(53620,53630)},
 **{f:"intro Mushroom (orpheline)" for f in range(53630,53633)},
 **{f:"intro Netherplant (manaforges)" for f in range(53633,53637)},
 **{f:"Donjon de la Tempête ambiance (ZoneMusic 373)" for f in range(53779,53790)},
 **{f:"Donjon de la Tempête combat (ZoneMusic 374)" for f in range(53790,53793)},
 **{f:"Donjon de la Tempête stinger" for f in range(53793,53796)},
 53665:"intro Historic (Zone 52, Cosmovrille, Œil du cyclone)",
 53657:"intro Crystal 01 (Pierre-de-Néant)",53658:"intro Crystal 02",53659:"intro Crystal 03 (Crête Céleste)",
 53644:"intro Légion 01 (Ferraille, Géhenne)",53645:"intro Légion 02 (Oubli, site d'invasion)",
 53637:"intro OL_Broken (Ruines d'Enkaat)",
 53661:"base draeneï (Ruines d'Enkaat)",53662:"base draeneï (Ruines d'Enkaat)",
 53796:"Auchindoun (ZoneMusic 316, donjons éthérés/draeneï)",53797:"Auchindoun",53798:"Auchindoun",
 **{f:"Outreterre corrompue (ZoneMusic 302/334, lieux tenus par la Légion)" for f in range(53649,53657)},
 53677:"intro Scenic (Foudreflèche, écodômes)",
 53638:"base Alliance d'Outreterre (Bastion de l'Honneur…)",53639:"base Alliance d'Outreterre",
 53668:"base Horde d'Outreterre (Thrallmar…)",53669:"base Horde d'Outreterre",
}
for f in sorted(SRC):
    w(f"| {f} | {stem(f)} | {dur.get(f,'(en cours)')} | {SRC[f]} |")
w("")
w("Déjà présents avec durée dans le plugin Quel'Thalas (à redéclarer localement) : `GL_Forest3WalkNight01…03` = 53510 / 53511 / 53512 (51.3 / 28.1 / 44.4 s), `OL_BloodElfBaseWalkUni01/02` = 53642 / 53643 (120.0 / 121.6 s).")
w("")

# ---- 3. Comparaisons
w("## 3. Rapprochements et packs proposés")
w("")
w("### 3.1 Les parallèles")
w("")
w("| Voidstorm | Netherstorm | Pourquoi |")
w("|---|---|---|")
w("| Steppes, routes, Storm Fields, Grasping Reach | Zone générale (`NS_GeneralWalkUni01…10`) | Deux terres brisées flottant dans le Néant / le Vide ; la colonne vertébrale du plugin |")
w("| The Ingress, Locus Point, Howling Ridge, Dusk's Repose, Masters' Perch | Zone 52 / Cosmovrille (intro Historic) | Les hubs neutres où l'on souffle ; l'intro « Historic » est la signature des villes de Netherstorm |")
w("| Points-nexus Antius / Xenas / Mid'Ar (« Pylon ») | Manaforges Ara / B'naar / Coruu / Duro (intros Netherplant 01–04) | Machines qui drainent le Vide ↔ machines qui drainent le Néant. Xenas « en train de s'effondrer » ↔ Manaforge Ultris détruite et envahie par le Vide |")
w("| Shadowguard Point, Ethereum Refinery / Overcroft, Shenzar Refinery, avant-postes | Lieu de rassemblement de l'Ethereum, Foudreflèche, Tombes-mana | Même faction, même nom : l'Ethereum de Netherstorm sont les éthérés touchés par le Vide. Le set Auchindoun (`TF_AuchindounWalk`) est celui des donjons éthérés |")
w("| Stormarion Keep / Watch, Obscurion Citadel, Voidscar Arena | Bases de forge Oubli / Géhenne, sites d'invasion, siège de Socrethar (intros Légion + set « corrupt ») | Forteresses de l'armée envahissante |")
w("| Stormarion Citadel (occupée par les ren'dorei après l'assaut) | Bastion des Solfurie + bases elfes de sang d'Outreterre | Place forte elfique militaire ; les ren'dorei sont d'anciens elfes de sang |")
w("| The Voidspire, The Approach, raid | Donjon de la Tempête (ambiances `tk_*_AMB`, stingers) | Le siège du maître de la zone : Xal'atath ↔ Kael'thas |")
w("| Nexus-Point Xenas (donjon) | Donjon de la Tempête (Méchanar / Botanica / Arcatraz) | Installation technologique en ruine |")
w("| Voidscar Arena (donjon) | Donjon de la Tempête combat (`tk_*_BTL`) | Arène = combat permanent |")
w("| The Molt, Bladeburrows, Underground Burrows, Voidburrow | Intros Mushroom + général | Matière organique (mue, terriers) ↔ intros « champignon » |")
w("| Den / Lair of Predaxas, Gorging Pit, Night Trench, Husk, grottes | Crête Céleste, Pierre-de-Néant (intros Crystal) | Repaires de la faune : drakes du Néant ↔ kaiju de Predacea |")
w("| Slayer's Rise (zone PvP + BG) | Œil du cyclone (BG de Netherstorm) | Le champ de bataille de la zone, kit déjà mixé par Blizzard |")
w("| Grief Spire, Retribution Hold, Bastion of Valor | Bases Alliance d'Outreterre | Camp Alliance |")
w("| Hate Spire, Mettle's Hold, Bastion of Might | Bases Horde d'Outreterre | Camp Horde |")
w("| Exiles' Hovel | Ruines d'Enkaat (base draeneï + intro Broken) | Voidstorm abrite des draeneï et des Brisés exilés |")
w("")
w("### 3.2 Packs TBC")
w("")
w("| Clé | Label | intro | Pistes | Zones par défaut |")
w("|---|---|---|---|---|")
w("| `NETHERSTORM` | Netherstorm (TBC) | — | any = NS_GeneralWalkUni01…10 | 2405 racine, Storm Fields, Grasping Reach, Gnawing Reach |")
w("| `AREA52` | Area 52 (TBC) | OL_HistoricIntroUni01 | any = NS_GeneralWalkUni01…10 | The Ingress, Locus Point, The Howling Ridge, Dusk's Repose, Masters' Perch |")
w("| `MANAFORGE` | Manaforge (TBC) | NS_NetherplantIntroUni01 | any = NS_NetherplantIntroUni02…04 + NS_GeneralWalkUni01…10 | Nexus-Point Antius / Xenas / Mid'Ar |")
w("| `ETHEREUM` | Ethereum (TBC) | OL_CrystalIntroUni01 | any = TF_AuchindounWalkUni01…03 | Shadowguard Point, Ethereum Refinery, Ethereum Overcroft, Shenzar Refinery, Hanaar / Shadowridge Outpost, Shadow Rise |")
w("| `FORGE_BASE` | Forge Base (TBC) | OL_BurningLegionIntroUni02 | any = OL_Corrupt01…07 + OL_BurningLegionIntroUni01 | Stormarion Keep / Watch, Obscurion Citadel, Voidscar Arena (extérieur), gouffres Sunkiller Sanctum / Torment's Rise |")
w("| `SUNFURY` | Sunfury Hold (TBC) | — | any = GL_Forest3WalkNight01…03 + OL_BloodElfBaseWalkUni01/02 | Stormarion Citadel |")
w("| `TEMPEST_KEEP` | Tempest Keep (TBC) | tk_TempestKeep_STG14 | any = tk_TempestKeep_AMB_11…23 | The Voidspire, The Approach, raid 2529/2530, donjon Nexus Point Xenas 2556 |")
w("| `TEMPEST_KEEP_BATTLE` | Tempest Keep Battle (TBC) | tk_TempestKeep_STG15 | any = tk_TempestKeep_BTL10 / 11 / 13 | donjon Voidscar Arena 2572…2574 |")
w("| `MOLT` | The Molt (TBC) | NS_MushroomIntroUni01 | any = NS_MushroomIntroUni02 / 03 + NS_GeneralWalkUni01…10 | The Molt, Underground Burrows, The Bladeburrows, Overrun Hollow, Abundant Voidburrow, gouffre Voidburrow |")
w("| `WILDS` | Celestial Ridge (TBC) | OL_CrystalIntroUni03 | any = NS_GeneralWalkUni01…10 | Den / Lair of Predaxas, Night Trench, The Gorging Pit, The Husk, Quiet Cavern, Consumptor Cave |")
w("| `EYE_OF_THE_STORM` | Eye of the Storm (TBC) | OL_HistoricIntroUni01 | any = NS_GeneralWalkUni01 / 03 / 08 + tk_TempestKeep_AMB_11 / 13 / 18 + tk_TempestKeep_BTL13 | 2444 Slayer's Rise racine et POI neutres, BG 2397 |")
w("| `OUTLAND_ALLIANCE` | Honor Hold (TBC) | — | any = OL_AllianceBaseWalkUni01 / 02 | Grief Spire, Retribution Hold, Bastion of Valor |")
w("| `OUTLAND_HORDE` | Thrallmar (TBC) | — | any = OL_HordeBaseWalkUni03 / 04 | Hate Spire, Mettle's Hold, Bastion of Might |")
w("| `ENKAAT` | Ruins of Enkaat (TBC) | OL_ActionWalkUni01 | any = OL_DraeneiBaseWalkUni01 / 02 | Exiles' Hovel |")
w("")
w("Points à trancher pendant l'implémentation : (a) les intros TBC sont courtes (12 à 80 s) et le core les joue une fois à l'entrée, ce qui reproduit bien le comportement TBC ; (b) `NS_GeneralWalkUni*` sont longues (2,5 à 3,7 min) : garder le `silenceGap` du core ; (c) un pack « silence » pour The Molt (natif = silence) n'est pas nécessaire, l'utilisateur peut mettre `NONE` en override.")
w("")
w("### 3.3 Packs Midnight (reproduisent les kits natifs, regroupés)")
w("")
w("| Clé | Label | Pistes |")
w("|---|---|---|")
w("| `VOIDSTORM_MIDNIGHT` | Voidstorm (Midnight) | Storm Fields A…I + Gnawing Reach B / D |")
w("| `SINGULARITY_MIDNIGHT` | Locus Point (Midnight) | Locus Point A…F / H + Voidstorm B |")
w("| `HOWLING_RIDGE_MIDNIGHT` | Howling Ridge (Midnight) | Howling Ridge A…E / H |")
w("| `DEVOURING_HOST_MIDNIGHT` | Devouring Host (Midnight) | Devouring Host A…K + Voidstorm A / C / D / F |")
w("| `SHADOWGUARD_MIDNIGHT` | Shadowguard (Midnight) | Shadowguard Void A…D / H |")
w("| `PREDAXAS_MIDNIGHT` | Predaxas (Midnight) | Voidstorm A / E / H + Devouring Host J |")
w("| `GORGING_PIT_MIDNIGHT` | Gorging Pit (Midnight) | Gnawing Reach A / C / E / H |")
w("| `SLAYERS_RISE_MIDNIGHT` | Slayer's Rise (Midnight) | Slayers Rise A…H + Storm Fields B / E / F / I |")
w("")
w("Packs mixés `*_MIXED` (TBC + Midnight) : NETHERSTORM+VOIDSTORM, AREA52+SINGULARITY, MANAFORGE+DEVOURING_HOST, ETHEREUM+SHADOWGUARD, FORGE_BASE+DEVOURING_HOST, TEMPEST_KEEP+DEVOURING_HOST, WILDS+PREDAXAS, MOLT+GORGING_PIT, EYE_OF_THE_STORM+SLAYERS_RISE. Packs utilitaires optionnels : `VOID_COMBAT` (Void Combat A…I, Ethereal Combat Void A/B), `XALATATH` (Xalatath Midnight A…F / H).")
w("")

# ---- 4. Zones.lua sketch
w("### 3.4 Esquisse de `Zones.lua`")
w("")
w("```lua")
w("[2405] = Dsl.zone(\"VOIDSTORM\", \"NETHERSTORM\", {")
sub_2405 = [i for _, ids in GROUPS[:8] for i in ids if i != 15458 and PROP.get(i) and PROP[i] != "NETHERSTORM"]
seen_keys = set()
for i in sub_2405:
    key = re.sub(r"[^A-Z0-9]+", "_", en(i).upper()).strip("_")
    if key in seen_keys: continue
    seen_keys.add(key)
    w(f"    {key:<22} = \"{PROP[i]}\",")
w("}),")
w("[2444] = Dsl.zone(\"SLAYERS_RISE\", \"EYE_OF_THE_STORM\", {")
seen_keys = set()
for i in GROUPS[8][1]:
    if i == 15959 or PROP.get(i) in (None, "EYE_OF_THE_STORM"): continue
    key = re.sub(r"[^A-Z0-9]+", "_", en(i).upper()).strip("_")
    if key in seen_keys: continue
    seen_keys.add(key)
    w(f"    {key:<22} = \"{PROP[i]}\",")
w("}),")
w("[2556] = Dsl.zone(\"NEXUS_POINT_XENAS\", \"TEMPEST_KEEP\"),")
w("[2572] = Dsl.zone(\"VOIDSCAR_ARENA\", \"TEMPEST_KEEP_BATTLE\"), [2573] = ..., [2574] = ...,")
w("[2529] = Dsl.zone(\"THE_VOIDSPIRE\", \"TEMPEST_KEEP\"), [2530] = ...,")
w("[2526] = Dsl.zone(\"LAIR_OF_PREDAXAS\", \"WILDS\"), [2527] = ...,")
w("[2581] = Dsl.zone(\"VOIDBURROW\", \"MOLT\"), [2582] = ...,")
w("[2528] = Dsl.zone(\"SUNKILLER_SANCTUM\", \"FORGE_BASE\"), [2571] = ...,")
w("[2507] = Dsl.zone(\"TORMENTS_RISE\", \"FORGE_BASE\"),")
w("[2397] = Dsl.zone(\"SLAYERS_RISE_BG\", \"EYE_OF_THE_STORM\"),  -- optionnel")
w("```")
w("")
w("Les sous-zones à ZoneMusic = 0 qui doivent garder le pack de la zone (Storm Fields, Grasping Reach, POI PvP…) n'ont pas besoin d'entrée : le core retombe sur le pack de la zone.")
w("")

# ---- 5. Steps
w("## 4. Structure du plugin et étapes")
w("")
w("Dossier `~/Documents/Code/EchoesOfAzeroth_Voidstorm/`, calqué sur `_ZulAman` :")
w("")
w("- `EchoesOfAzeroth_Voidstorm.toc` : `## Interface: 120100`, `## Title: Echoes of Azeroth: Voidstorm`, `## Dependencies: EchoesOfAzeroth`, `## X-Curse-Project-ID:` (à créer sur CurseForge), ordre de chargement `Locale.lua, Tracks.lua, Packs.lua, Zones.lua, Plugin.lua`.")
w("- `Plugin.lua` : `id = \"voidstorm\"`, `title = \"Voidstorm\"`, `order = 30`, `category = \"Eastern Kingdoms\"` (même regroupement UI que Quel'Thalas, la carte 2405 est fille de 2537 Quel'Thalas ; alternative : une catégorie « Midnight »).")
w("- `Locale.lua` : noms de zones et de sous-zones dans les 10 locales (annexe A, données AreaTable 12.1.0, donc exactes pour `GetSubZoneText()`).")
w("- `Tracks.lua` : préfixes `NS_` (Netherstorm), `TK_` (Donjon de la Tempête), `OL_` (Outreterre général), `TF_` (Auchindoun), `GL_` (Ghostlands), `MN_` (Midnight) ; durées de §2.4 et de `durations_midnight.csv`.")
w("- `Packs.lua` / `Zones.lua` : §3.2 à §3.4.")
w("- `README.md`, `.pkgmeta` (ignorer `README.md`, `.github`, `.cursor`, `.gitignore`, **`docs`**), `.github/workflows/release.yml` copié de `_ZulAman` avec le nom du .toc, `icon.png` 64×64.")
w("")
w("Étapes :")
w("")
w("1. Valider ce plan (packs, catégorie, granularité des packs Midnight).")
w("2. Générer `Tracks.lua` (FDID + durées) depuis les CSV du scratchpad, puis `Locale.lua` depuis les AreaTable localisées.")
w("3. Écrire `Packs.lua`, `Zones.lua`, `Plugin.lua`, `.toc`.")
w("4. Charger le plugin dans le harnais Lua 5.1 à stubs (comme pour le core) : chaque `nameKey` et clé de sous-zone doit exister dans `Locale.lua`, chaque pack référencé doit exister, chaque FDID doit avoir une durée.")
w("5. Copier à la main dans `/mnt/Games/World of Warcraft/_retail_/Interface/AddOns/` et vérifier en jeu avec `/eoa now` : UiMapID de Slayer's Rise (2444), des donjons, du raid, des gouffres ; textes de sous-zone des lieux à ZoneMusic = 0 ; comportement des intros.")
w("6. `git init`, dépôt GitHub `AnasyaDev/EchoesOfAzeroth_Voidstorm` via l'alias SSH `github-anasyadev`, projet CurseForge, variable `CF_PROJECT_ID`, ajouter l'entrée `voidstorm` dans `EchoesOfAzeroth/tools/push_addon_release.py`, release `v1.0.0` (commit une ligne, sans trailer).")
w("7. Commit séparé côté Quel'Thalas pour renommer `VE_Voidstorm*` et `MN_ParhelionPlazaE…I`.")
w("")

# ---- Annex A: locales
w("## Annexe A — noms localisés (AreaTable 12.1.0)")
w("")
w("### A.1 Voidstorm")
w("")
w("| AreaID | enUS | " + " | ".join(LOCS) + " |")
w("|---|---|" + "---|"*len(LOCS))
vs_ids = sorted(i for i,a in areas.items() if a["ContinentID"] in ("2771","2923","2912","2915","2799"))
for i in vs_ids:
    w(f"| {i} | {en(i)} | " + " | ".join(loc[l].get(i,"?") for l in LOCS) + " |")
w("")
w("### A.2 Netherstorm")
w("")
w("| AreaID | enUS | " + " | ".join(LOCS) + " |")
w("|---|---|" + "---|"*len(LOCS))
for i in ns_ids:
    w(f"| {i} | {en(i)} | " + " | ".join(loc[l].get(i,"?") for l in LOCS) + " |")
w("")

# ---- Annex B: raw kits
w("## Annexe B — kits natifs de Voidstorm, fichier par fichier")
w("")
seen = set()
for i in sorted(i for i,a in areas.items() if a["ContinentID"] in ("2771","2923","2912","2915","2799")):
    z = int(areas[i]["ZoneMusic"])
    if not z or z in seen: continue
    seen.add(z)
    r = zm[z]
    users = [f"{j} {en(j)}" for j,a in areas.items() if int(a["ZoneMusic"])==z and a["ContinentID"] in ("2771","2923","2912","2915","2799")]
    w(f"- **ZoneMusic {z}** « {r['SetName']} » (pauses {int(r['SilenceIntervalMin_0'])//1000}–{int(r['SilenceIntervalMax_0'])//1000} s) — {', '.join(users)}")
    fd = set()
    for k in (int(r["Sounds_0"]), int(r["Sounds_1"])):
        fd |= set(kits.get(k, []))
    for f in sorted(fd):
        w(f"  - {f} `{stem(f)}`")
w("")
OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print(OUT, len(L), "lines")
