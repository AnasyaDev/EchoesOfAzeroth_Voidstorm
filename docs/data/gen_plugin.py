import csv, re
from pathlib import Path
ROOT = Path("/home/loadren/Documents/Code/EchoesOfAzeroth_Voidstorm")
LOCS = ["frFR","deDE","esES","esMX","ptBR","ruRU","itIT","koKR","zhCN","zhTW"]

lf = {}
for line in open("listfile.csv", encoding="utf-8", errors="replace"):
    a,_,b = line.rstrip("\n").partition(";")
    if a.isdigit(): lf[int(a)] = b
dur = {}
for f in ("durations_tbc.csv","durations_midnight.csv"):
    for r in csv.reader(open(f)):
        if r and r[0].isdigit() and not r[1].startswith("error"): dur[int(r[0])] = float(r[1])
# known from the Quel'Thalas plugin (same FDIDs)
dur.update({53510:51.3,53511:28.1,53512:44.4,53642:120.0,53643:121.6,
            7684188:118.4,7684190:122.2,7684192:135.8,7684194:153.6,7684196:120.4,7684198:161.6,7713420:132.3})

def fd(stem_regex):
    """fdid of the unique listfile entry whose basename matches"""
    rx = re.compile(stem_regex + r"\.mp3$", re.I)
    hits = [f for f,p in lf.items() if rx.search(p.split("/")[-1])]
    assert len(hits) == 1, (stem_regex, hits)
    return hits[0]

def mn(fam, letters):
    return [(f"MN_{fam.replace('_','')}{l}", fd(f"^MUS_120_{fam}_{l}")) for l in letters]

SECTIONS = [
 ("Netherstorm > General (ZoneMusic 272, the only zone-wide set)", [(f"NS_GeneralWalkUni{i:02d}", fd(f"^NS_GeneralWalkUni{i:02d}")) for i in range(1,11)]),
 ("Netherstorm > Mushroom intros (orphaned in current data)", [(f"NS_MushroomIntroUni{i:02d}", fd(f"^NS_MushroomIntroUni{i:02d}")) for i in range(1,4)]),
 ("Netherstorm > Netherplant intros (one per manaforge)", [(f"NS_NetherplantIntroUni{i:02d}", fd(f"^NS_NetherplantIntroUni{i:02d}")) for i in range(1,5)]),
 ("Tempest Keep > ambient (ZoneMusic 373)", [(f"TK_TempestKeepAMB{i}", fd(f"^tk_TempestKeep_AMB_{i}")) for i in (11,12,13,14,16,17,18,19,20,22,23)]),
 ("Tempest Keep > battle (ZoneMusic 374)", [(f"TK_TempestKeepBTL{i}", fd(f"^tk_TempestKeep_BTL{i}")) for i in (10,11,13)]),
 ("Tempest Keep > stingers (ZoneIntroMusicTable 535-537)", [(f"TK_TempestKeepSTG{i}", fd(f"^tk_TempestKeep_STG{i}")) for i in (14,15)]),
 ("Outland > intros (ZoneIntroMusicTable)", [
    ("OL_HistoricIntroUni01", fd("^OL_HistoricIntroUni01")),
    ("OL_ScenicIntroUni01", fd("^OL_ScenicIntroUni01")),
    ("OL_CrystalIntroUni03", fd("^OL_CrystalIntroUni03")),
    ("OL_BurningLegionIntroUni01", fd("^OL_BurningLegionIntroUni01")),
    ("OL_BurningLegionIntroUni02", fd("^OL_BurningLegionIntroUni02")),
    ("OL_ActionWalkUni01", fd("^OL_ActionWalkUni01")),
 ]),
 ("Outland > corrupt set (Legion-held ground, ZoneMusic 302/334)", [(f"OL_Corrupt{i:02d}", fd(f"^OL_Corrupt{i:02d}")) for i in range(1,8)] + [("OL_CorruptIntro", fd("^OL_CorruptIntro"))]),
 ("Outland > base themes", [
    ("OL_DraeneiBaseWalkUni01", fd("^OL_DraeneiBaseWalkUni01")),
    ("OL_DraeneiBaseWalkUni02r", fd("^OL_DraeneiBaseWalkUni02r")),
    ("OL_AllianceBaseWalkUni01", fd("^OL_AllianceBaseWalkUni01")),
    ("OL_AllianceBaseWalkUni02", fd("^OL_AllianceBaseWalkUni02")),
    ("OL_HordeBaseWalkUni03", fd("^OL_HordeBaseWalkUni03")),
    ("OL_HordeBaseWalkUni04", fd("^OL_HordeBaseWalkUni04")),
    ("OL_BloodElfBaseWalkUni01", fd("^OL_BloodElfBaseWalkUni01")),
    ("OL_BloodElfBaseWalkUni02", fd("^OL_BloodElfBaseWalkUni02")),
 ]),
 ("Terokkar > Auchindoun (ZoneMusic 316, ethereal / draenei dungeons)", [(f"TF_AuchindounWalkUni{i:02d}", fd(f"^TF_AuchindounWalkUni{i:02d}")) for i in range(1,4)]),
 ("Ghostlands > Forest 3 night (Sunfury Hold set, ZoneMusic 337)", [(f"GL_Forest3WalkNight{i:02d}", fd(f"^GL_Forest3WalkNight{i:02d}")) for i in range(1,4)]),
 ("Midnight > Voidstorm (native, used by the mixed packs only)", mn("Voidstorm","ABCDEFH")),
 ("Midnight > Storm Fields", mn("Storm_Fields","ABCDEFGHI")),
 ("Midnight > Devouring Host", mn("Devouring_Host","ABCDEFGHIJK")),
 ("Midnight > Locus Point (void elf hub)", mn("Locus_Point","ABCDEFH")),
 ("Midnight > Howling Ridge", mn("Howling_Ridge","ABCDEH")),
 ("Midnight > Shadowguard Void (Ethereum)", mn("Shadowguard_Void","ABCDH")),
 ("Midnight > Gnawing Reach (Gorging Pit kit)", mn("Gnawing_Reach","ABCDEH")),
 ("Midnight > Slayer's Rise", mn("Slayers_Rise","ABCDEFGH")),
]

L = ["local _, ns = ...", "",
"-- ============================================================",
"-- Track catalog — FileDataIDs from the wowdev community listfile",
"-- (build 12.1.0), grouped by source.  Durations were measured with",
"-- ffprobe on the files served by wago.tools (2026-09-11), except the",
"-- Ghostlands / Blood Elf Base / Locus Point rows, which reuse the",
"-- values already measured for EchoesOfAzeroth_QuelThalas.",
"--",
"-- Prefixes:",
"--   NS_ = Netherstorm zone music (TBC)",
"--   TK_ = Tempest Keep (TBC raid, dungeons, Eye of the Storm)",
"--   OL_ = Outland general (TBC intros and base themes)",
"--   TF_ = Terokkar / Auchindoun (TBC ethereal dungeons)",
"--   GL_ = Ghostlands (TBC blood elf hostile set)",
"--   MN_ = Midnight native Voidstorm music (mixed packs only)",
"-- ============================================================", "",
"ns.Tracks = {", ""]
all_rows = []
for comment, rows in SECTIONS:
    L.append(f"    -- {comment} " + "-"*max(3, 60-len(comment)))
    for sym, f in rows:
        L.append(f"    {sym:<28} = {f},")
        all_rows.append((sym, f))
    L.append("")
L.append("}")
L += ["", "-- ============================================================",
"-- Track durations (seconds), keyed by FileDataID, so the engine can",
"-- schedule the next track when the current one ends.",
"-- ============================================================", "",
"ns.TrackDurations = {"]
seen = set()
for sym, f in all_rows:
    assert f in dur, (sym, f)
    assert f not in seen, ("dup", sym, f); seen.add(f)
    L.append(f"    [{f}] = {dur[f]:6.1f},  -- {sym}")
L.append("}")
(ROOT/"Tracks.lua").write_text("\n".join(L)+"\n", encoding="utf-8")
print("Tracks.lua:", len(all_rows), "tracks")

# ---------------- Locale.lua ----------------
areas = {int(r["ID"]): r["AreaName_lang"] for r in csv.DictReader(open("areatable.csv", encoding="utf-8"))}
loc = {l: {int(r["ID"]): r["AreaName_lang"] for r in csv.DictReader(open(f"areatable_{l}.csv", encoding="utf-8"))} for l in LOCS}
NAMES = [("VOIDSTORM", 15458), ("SLAYERS_RISE", 15959)]
SUBS = [
 ("THE_INGRESS",15949),("LOCUS_POINT",15950),("THE_HOWLING_RIDGE",15951),("DUSKS_REPOSE",16844),
 ("NEXUS_POINT_ANTIUS",15952),("NEXUS_POINT_XENAS",15954),("NEXUS_POINT_MIDAR",15955),
 ("SHADOWGUARD_POINT",15953),("ETHEREUM_REFINERY",15962),("ETHEREUM_OVERCROFT",15967),
 ("STORMARION_KEEP",15956),("STORMARION_CITADEL",16485),("STORMARION_WATCH",16486),("OBSCURION_CITADEL",15957),
 ("THE_VOIDSPIRE",15960),("THE_APPROACH",15961),
 ("THE_MOLT",15964),("UNDERGROUND_BURROWS",16364),("THE_BLADEBURROWS",15965),("ABUNDANT_VOIDBURROW",16581),("OVERRUN_HOLLOW",16652),
 ("DEN_OF_PREDAXAS",15966),("LAIR_OF_PREDAXAS",16534),("NIGHT_TRENCH",16501),("THE_GORGING_PIT",16804),("QUIET_CAVERN",16863),("CONSUMPTOR_CAVE",16864),
 ("EXILES_HOVEL",16429),
 # Slayer's Rise (own UiMap 2444; also listed under 2405 as a fallback)
 ("SLAYERS_RISE",15959),("MASTERS_PERCH",16649),
 ("GRIEF_SPIRE",15970),("RETRIBUTION_HOLD",16850),("BASTION_OF_VALOR",16223),
 ("HATE_SPIRE",15971),("METTLES_HOLD",16851),("BASTION_OF_MIGHT",16216),
 ("VOIDSCAR_ARENA",15973),("SHENZAR_REFINERY",16218),("THE_HUSK",16219),
 ("HANAAR_OUTPOST",16221),("SHADOWRIDGE_OUTPOST",16222),("SHADOW_RISE",16600),
 ("PATH_OF_PREDATION",15974),("THE_BLOODPLAINS",15975),("STAREATER_PAVILION",15976),("SHATTERSKY_PAVILION",15977),
 ("CLAWS_EDGE",16213),("THE_FANGFALL",16214),("SPARRING_GROUNDS",16220),
]
def lua_str(s):
    out = []
    for ch in s:
        if ch == '"': out.append('\\"')
        elif ch == '\\': out.append('\\\\')
        elif ord(ch) < 128: out.append(ch)
        else: out.append("".join(f"\\{b}" for b in ch.encode("utf-8")))
    return '"' + "".join(out) + '"'
def line(prefix, key, text, width):
    s = f"    {prefix}.{key:<{width}} = {lua_str(text)}"
    if any(ord(c) >= 128 for c in text): s += f"  -- {text}"
    return s
W = max(len(k) for k,_ in SUBS)
O = ["local _, ns = ...", "",
"-- ============================================================",
"-- Localization",
"--",
"-- English (enUS) is the base; every other client locale overrides",
"-- below.  All strings are the AreaTable.AreaName_lang values of",
"-- build 12.1.0 (wago.tools), so they match GetSubZoneText() exactly.",
"-- Non-ASCII characters are written as UTF-8 byte escapes.",
"--",
"-- Keys are locale-independent constants used by Zones.lua.",
"-- ============================================================", "",
"local names = {"]
for k,i in NAMES: O.append(f"    {k:<{W}} = {lua_str(areas[i])},")
O += ["}", "", "local subzones = {"]
for k,i in SUBS: O.append(f"    {k:<{W}} = {lua_str(areas[i])},")
O += ["}", "", "-- ============================================================", "-- Locale overrides", "-- ============================================================", "", "local locale = GetLocale()", ""]
first = True
for l in LOCS:
    cond = f'locale == "{l}"'
    if l == "esES": cond = 'locale == "esES" or locale == "esMX"'
    if l == "esMX":
        # only emit esMX block if it differs from esES
        if all(loc["esMX"][i] == loc["esES"][i] for _,i in NAMES+SUBS): continue
        cond = 'locale == "esMX"'
    O.append(("if " if first else "elseif ") + cond + " then"); first = False
    for k,i in NAMES: O.append(line("names", k, loc[l][i], W))
    O.append("")
    for k,i in SUBS: O.append(line("subzones", k, loc[l][i], W))
    O.append("")
O += ["end", "", "-- ============================================================", "-- Expose to namespace", "-- ============================================================", "",
"ns.L = setmetatable(names, {", "    __index = function(_, key) return key end,", "})", "",
"ns.SubzoneNames = subzones", "", "ns.SubzoneKeys = {}", "for key, localizedName in pairs(subzones) do", "    ns.SubzoneKeys[localizedName] = key", "end"]
# esES vs esMX: if they differ, the esES block must not cover esMX
if not all(loc["esMX"][i] == loc["esES"][i] for _,i in NAMES+SUBS):
    O = [s.replace('locale == "esES" or locale == "esMX"', 'locale == "esES"') for s in O]
(ROOT/"Locale.lua").write_text("\n".join(O)+"\n", encoding="utf-8")
# collision check per locale
for l in ["enUS"]+LOCS:
    src = areas if l=="enUS" else loc[l]
    by_text = {}
    for k,i in SUBS:
        by_text.setdefault(src[i], set()).add(k)
    bad = {t:ks for t,ks in by_text.items() if len(ks) > 1}
    if bad: print("COLLISION", l, bad)
print("Locale.lua:", len(SUBS), "subzones, esES==esMX:", all(loc["esMX"][i] == loc["esES"][i] for _,i in NAMES+SUBS))
