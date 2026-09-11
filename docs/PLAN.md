# EchoesOfAzeroth_Voidstorm — plan de conception

Rédigé le 11/09/2026 à partir des tables de jeu 12.1.0 (wago.tools : AreaTable, ZoneMusic, SoundKitEntry, ZoneIntroMusicTable, UiMap, Map) et du listfile communautaire wowdev. Toutes les localisations viennent d'AreaTable (10 locales). Les durées TBC ont été mesurées par ffprobe sur les fichiers téléchargés depuis wago.tools.

## Décisions (11/09/2026, après validation du plan)

1. Catégorie du plugin : **Eastern Kingdoms**.
2. Packs livrés : **TBC** et **TBC + Midnight** seulement. Aucun pack Midnight pur (la musique native est ce que l'on entend addon désactivé ; libre aux utilisateurs d'en composer un depuis les pistes `MN_*`). La section 3.3 ci-dessous décrit donc des kits internes à `Packs.lua`, pas des packs exposés.
3. Cartes mappées : **zone monde uniquement**, `[2405]` Voidstorm et `[2444]` Slayer's Rise. Ni donjons, ni raid, ni gouffres, ni BG instancié (les entrées d'instance de la section 3.4 sont abandonnées). La musique des donjons TBC reste utilisée pour l'extérieur (Voidspire, Voidscar Arena en plein air).
4. Ajustements à l'implémentation : intro du pack Ethereum = `OL_ScenicIntroUni01` (Foudreflèche, QG éthéré) au lieu de `OL_CrystalIntroUni01` ; `OL_CorruptIntro` ajouté à la rotation Forge Base ; Voidscar Arena (extérieur) → `TEMPEST_KEEP_BATTLE` plutôt que Forge Base ; intros Crystal 01/02 et stinger STG16 non embarqués.

État : plugin généré, validé par le harnais Lua 5.1 dans les 11 locales, copié dans le dossier AddOns pour test en jeu.

## 0. Objectif

Plugin de contenu pour le core `EchoesOfAzeroth`, sur le modèle de `_QuelThalas` et `_ZulAman` : remplacer, sous-zone par sous-zone, la musique de **Voidstorm** (Midnight, UiMapID 2405) par celle de **Netherstorm** (TBC, UiMapID 109) et de ses lieux apparentés (Donjon de la Tempête, Œil du cyclone, bases d'Outreterre). Convention des autres plugins conservée : pour chaque famille un pack **(TBC)**, un pack **(Midnight)** qui reproduit le kit natif, et un pack **(TBC + Midnight)** mixé.

Lecture rapide du rapprochement : Netherstorm est Farahlon rongée par le Néant, avec des manaforges qui drainent l'énergie, des éthérés (Consortium, Protectorat, **Ethereum**), une forteresse volante (Donjon de la Tempête) et des bases de la Légion. Voidstorm est Predacea rongée par le Vide, avec des **points-nexus** qui drainent le Vide, des éthérés de **l'Ethereum** (même nom de faction), une forteresse-siège (la Voidspire) et des forteresses de la Horde dévorante. Le parallèle est presque terme à terme.

## 1. Voidstorm — inventaire

### 1.1 Cartes (UiMap) et instances

| UiMapID | Nom | Type | Parent | Usage dans le plugin |
|---|---|---|---|---|
| 2405 | Voidstorm | zone | 2537 Quel'Thalas | entrée principale `[2405]` (monde ouvert, sous-zones par `GetSubZoneText()`) |
| 2444 | Slayer's Rise | zone | 2405 | carte propre : entrée `[2444]` avec ses sous-zones (sans entrée, le core remonte sur 2405) |
| 2556 | Nexus Point Xenas | donjon | 2405 | donjon (Map 2915, continent 2915) : `[2556]` |
| 2572 / 2573 / 2574 | Voidscar Arena | donjon, 3 étages | 2405 | donjon (Map 2923) : mapper les 3 étages (résolution stricte en instance) |
| 2529 / 2530 | The Voidspire | raid, 2 étages | 2405 | raid (Map 2912) |
| 2526 / 2527 | Lair of Predaxas | micro (gouffre) | 2405 | gouffre |
| 2581 / 2582 | Voidburrow | micro (gouffre) | 2405 | gouffre |
| 2528 / 2571 | Sunkiller Sanctum | donjon (gouffre « 12DelvesDevouringHost02 », Map 2965) | 2405 | gouffre |
| 2507 | Torment's Rise | donjon (boss de gouffre, Map 2966) | 2405 | gouffre |
| 2506 | Shadowguard Point | donjon (Map 2979, scénario ?) | 2405 | à vérifier en jeu |
| 2397 | Slayer's Rise | zone, parent 0 | — | champ de bataille épique instancié (Map 2799) : `[2397]` optionnel |
| 2479 | Voidstorm | continent (flags 131076, atlas 5350) | 0 | carte cosmique d'affichage : ignorer |

Tous les UiMapID d'instance sont à confirmer en jeu avec `/eoa now` (la mémoire du core rappelle que gouffres et lairs sont en difficultyID 208, type « scenario »).

### 1.2 Sous-zones (AreaTable, continent 2771) et musique native

Colonne « natif » = kit ZoneMusic réellement joué (lettres des fichiers `MUS_120_*`). « — » = pas de ZoneMusic propre, le jeu hérite du parent (la racine joue *Storm Fields* + *Gnawing Reach* B/D). Colonne « TBC » = pack proposé par défaut (définis en §3).

#### A. Racine et steppes

| AreaID | enUS | frFR | Natif (Midnight) | Rôle | TBC |
|---|---|---|---|---|---|
| 15458 | Voidstorm | Tempête du Vide | Storm Fields A/C/D/G/H + Gnawing Reach B/D | Racine de la zone : steppes et routes (« VoidstormSouth ») | `NETHERSTORM` |
| 15963 | Storm Fields | Champs des Tempêtes | — | Steppes (zm = 0, hérite de la racine) | `NETHERSTORM` |
| 16360 | Grasping Reach | Confins Avides | — | Bordure extérieure (« Outerborder ») | `NETHERSTORM` |
| 16341 | Gnawing Reach | Confins Dévorants | mus_mx_cov_seatoftheprimus_01 | « RaidInterstitial » / kit « Deep Sea » : placeholder Shadowlands (Seat of the Primus) | `NETHERSTORM` |
| 16581 | Abundant Voidburrow | Terrier du Vide de l’Abondance | — | Terrier abondant (entrée de gouffre Voidburrow ?) | `MOLT` |

#### B. Hubs ren'dorei (la Singularité)

| AreaID | enUS | frFR | Natif (Midnight) | Rôle | TBC |
|---|---|---|---|---|---|
| 15949 | The Ingress | Le Seuil | Locus Point A/B/C/D/E/H/F + Voidstorm B | Hub ren'dorei d'arrivée (« VoidElfCampAlpha ») | `AREA52` |
| 15950 | Locus Point | Halte du Noyau | Locus Point A/B/C/D/E/H/F + Voidstorm B | Hub principal de la Singularité (« VoidElfCampBeta ») | `AREA52` |
| 15951 | The Howling Ridge | La crête Hurlante | Howling Ridge A/B/C/D/E/H | Hub tertiaire sur une crête (« VoidElfCampCharlie ») | `AREA52` |
| 16844 | Dusk's Repose | Repos du Crépuscule | — | Auberge de la crête Hurlante (flag auberge) | `AREA52` |

#### C. Points-nexus (pylônes du Vide)

| AreaID | enUS | frFR | Natif (Midnight) | Rôle | TBC |
|---|---|---|---|---|---|
| 15952 | Nexus-Point Antius | Point-nexus Antius | Devouring Host A/B/C/F/G + Voidstorm C/D/F | Point-nexus = pylône drainant le Vide (« PylonAlpha ») | `MANAFORGE` |
| 15954 | Nexus-Point Xenas | Point-nexus Xenas | Devouring Host D/E/I + Voidstorm D | Point-nexus en ruine, entrée du donjon (« PylonCharlie ») | `MANAFORGE` |
| 15955 | Nexus-Point Mid'Ar | Point-nexus Mid’Ar | Devouring Host H/I + Shadowguard Void B/C + Storm Fields E + Voidstorm F | Point-nexus (« PylonEcho ») | `MANAFORGE` |

#### D. Éthérés de l'Ethereum

| AreaID | enUS | frFR | Natif (Midnight) | Rôle | TBC |
|---|---|---|---|---|---|
| 15953 | Shadowguard Point | Halte de l’Ombre-Garde | Shadowguard Void A/B/C/D/H | Camp des éthérés de l'Ethereum (« PylonBeta ») | `ETHEREUM` |
| 15962 | Ethereum Refinery | Raffinerie de l’Ethereum | Devouring Host E + Shadowguard Void A/D/H | Raffinerie éthérée (« EtherealEnergyRefinery ») | `ETHEREUM` |
| 15967 | Ethereum Overcroft | Manse de l’Ethereum | Shadowguard Void A/B/C/D/H | Exploitation éthérée (« EtherealEnergyFarm ») | `ETHEREUM` |

#### E. Forteresses de la Horde dévorante

| AreaID | enUS | frFR | Natif (Midnight) | Rôle | TBC |
|---|---|---|---|---|---|
| 15956 | Stormarion Keep | Donjon de Fulgarion | Devouring Host D/E/H/I | Forteresse de la Horde dévorante, cible de l'assaut Stormarion (« VoidFortressA ») | `FORGE_BASE` |
| 16485 | Stormarion Citadel | Citadelle de Fulgarion | Locus Point A/B/C/D/E + Voidstorm B | Citadelle Stormarion après l'assaut : musique native = hub ren'dorei | `SUNFURY` |
| 16486 | Stormarion Watch | Guet de Fulgarion | Devouring Host D/E/H/I | Guet Stormarion (« VoidFortressWatch ») | `FORGE_BASE` |
| 15957 | Obscurion Citadel | Citadelle d’Obscurion | Devouring Host B/C/F/G + Storm Fields B + Slayers Rise B + Voidstorm A/C/D/E/F | Seconde forteresse de la Horde dévorante (« VoidFortressB ») | `FORGE_BASE` |

#### F. La Voidspire (extérieur du raid)

| AreaID | enUS | frFR | Natif (Midnight) | Rôle | TBC |
|---|---|---|---|---|---|
| 15960 | The Voidspire | La flèche du Vide | Devouring Host A/C/H/F/G/I + Voidstorm C/D/F | Extérieur du raid, siège de Xal'atath (« RaidOutdoor ») | `TEMPEST_KEEP` |
| 15961 | The Approach | Les Abords | Devouring Host A/C/H/F/G/I + Voidstorm C/D/F | Approche de la Voidspire (« VoidSpireEntrance ») | `TEMPEST_KEEP` |

#### G. Faune de Predacea, mue et terriers

| AreaID | enUS | frFR | Natif (Midnight) | Rôle | TBC |
|---|---|---|---|---|---|
| 15964 | The Molt | La Mue | Silent_046_2 | Mue du kaiju (« KaijuCorpse ») : natif = silence, pauses 30–45 s | `MOLT` |
| 16364 | Underground Burrows | Terriers Souterrains | Silent_046_2 | Terriers sous la Mue (WMO) : natif = silence | `MOLT` |
| 15965 | The Bladeburrows | Les terriers Tranchants | — | Terriers Tranchants (zm = 0) | `MOLT` |
| 15966 | Den of Predaxas | Tanière de Prédaxas | Voidstorm A/E/H + Devouring Host J | Tanière du kaiju Predaxas (« KaijuDen ») | `WILDS` |
| 16534 | Lair of Predaxas | Repaire de Prédaxas | Voidstorm A/E/H + Devouring Host J | Repaire de Predaxas (gouffre, même kit) | `WILDS` |
| 16501 | Night Trench | Tranchée de la Nuit | Gnawing Reach A/C/H/E | Tranchée (kit « Gorging Pit ») | `WILDS` |
| 16804 | The Gorging Pit | La fosse de Gloutonnerie | Gnawing Reach A/C/H/E | Fosse du boss mondial (« WorldBossPOI ») | `WILDS` |
| 16652 | Overrun Hollow | Terrier du Vide | — | Terriers (« FidoBurrowsWMO ») | `MOLT` |
| 16863 | Quiet Cavern | Caverne Paisible | — | Grotte (« Local13CaveB ») | `WILDS` |
| 16864 | Consumptor Cave | Grotte du Gavodon | — | Grotte (« Local13CaveA ») | `WILDS` |

#### H. Exilés

| AreaID | enUS | frFR | Natif (Midnight) | Rôle | TBC |
|---|---|---|---|---|---|
| 16429 | Exiles' Hovel | Taudis de l’Exil | — | Taudis des exilés : draeneï / Brisés de Voidstorm | `ENKAAT` |

#### I. Slayer's Rise (zone PvP, carte 2444)

| AreaID | enUS | frFR | Natif (Midnight) | Rôle | TBC |
|---|---|---|---|---|---|
| 15959 | Slayer's Rise | Colline Meurtrière | Storm Fields B/E/F/I + Devouring Host I/J/K | Zone PvP monde, racine (carte UiMap 2444) | `EYE_OF_THE_STORM` |
| 16649 | Masters' Perch | Perchoir des Maîtres | Slayers Rise D/F/G/H + Voidstorm B | Hub PvP neutre, parent (duels, marchands) | `AREA52` |
| 15958 | Masters' Perch | Perchoir des Maîtres | — | Hub PvP neutre, enfant | `AREA52` |
| 15970 | Grief Spire | Flèche du Deuil | Slayers Rise A/B/C/E | Flèche Alliance (général Ziadan) | `OUTLAND_ALLIANCE` |
| 16850 | Retribution Hold | Bastion de la Vindicte | Slayers Rise A/B/C/E | Auberge Alliance | `OUTLAND_ALLIANCE` |
| 16223 | Bastion of Valor | Bastion de la Vaillance | — | Avant-poste Alliance (zm = 0) | `OUTLAND_ALLIANCE` |
| 15971 | Hate Spire | Flèche de la Haine | Voidstorm A/C/D/E | Flèche Horde (général Vidious) | `OUTLAND_HORDE` |
| 16851 | Mettle's Hold | Bastion du Courage | Voidstorm A/C/D/E | Auberge Horde | `OUTLAND_HORDE` |
| 16216 | Bastion of Might | Bastion de la Puissance | — | Avant-poste Horde (zm = 0) | `OUTLAND_HORDE` |
| 15973 | Voidscar Arena | Arène de la Cicatrice du Vide | Devouring Host D/E/H/I | Arène extérieure (kit Horde dévorante) | `FORGE_BASE` |
| 16218 | Shenzar Refinery | Raffinerie de Shenzar | Shadowguard Void A/B/C/D/H | Raffinerie éthérée dans Slayer's Rise (« PortalCavern ») | `ETHEREUM` |
| 16219 | The Husk | La Bogue | Gnawing Reach A/C/H/E | Carcasse (kit « Gorging Pit ») | `WILDS` |
| 16221 | Hanaar Outpost | Avant-poste Hanaar | — | Avant-poste éthéré ouest (zm = 0) | `ETHEREUM` |
| 16222 | Shadowridge Outpost | Avant-poste d’Ombrecrête | — | Avant-poste éthéré est (zm = 0) | `ETHEREUM` |
| 16600 | Shadow Rise | Ombrecime | — | Avant-poste éthéré est 2 (zm = 0) | `ETHEREUM` |
| 15974 | Path of Predation | Voie de la Prédation | — | Route de parade PvP (zm = 0) | `EYE_OF_THE_STORM` |
| 15975 | The Bloodplains | Les plaines Sanglantes | — | Champ central neutre (zm = 0) | `EYE_OF_THE_STORM` |
| 15976 | Stareater Pavilion | Pavillon de Dévore-Étoile | — | POI expédition (zm = 0) | `EYE_OF_THE_STORM` |
| 15977 | Shattersky Pavilion | Pavillon de Brise-Ciel | — | POI expédition (zm = 0) | `EYE_OF_THE_STORM` |
| 16213 | Claw's Edge | Bord-de-Griffe | — | Falaise est (zm = 0) | `EYE_OF_THE_STORM` |
| 16214 | The Fangfall | Crochute | — | Falaise ouest (zm = 0) | `EYE_OF_THE_STORM` |
| 16220 | Sparring Grounds | Terrain d’affrontement | — | Terrain de duel (zm = 0) | `EYE_OF_THE_STORM` |

#### J. Instances (continents propres)

| AreaID | Continent | enUS | Natif (Midnight) | TBC proposé |
|---|---|---|---|---|
| 16573 | 2915 Nexus-Point Xenas | Nexus-Point Xenas | Voidstorm C/D/E/F + Devouring Host K + The Light F/I | `TEMPEST_KEEP` |
| 16574 | 2915 | Corespark Engineway | — | `TEMPEST_KEEP` |
| 16575 | 2915 | Core Defense Nullward | — | `TEMPEST_KEEP` |
| 16576 | 2915 | The Nexus Core | — | `TEMPEST_KEEP` |
| 16425 | 2923 Voidscar Arena | Voidscar Arena | Shadowguard Void C + Voidstorm A/D/E + Devouring Host J | `TEMPEST_KEEP_BATTLE` |
| 16479 | 2923 (réplique extérieure) | Voidstorm | — | `EYE_OF_THE_STORM` |
| 16480 | 2923 | Slayer's Rise | — | `EYE_OF_THE_STORM` |
| 16481 | 2923 | Pit of Spite | — | `TEMPEST_KEEP_BATTLE` |
| 16482 | 2923 | The Husk | — | `WILDS` |
| 16483 | 2923 | Sparring Grounds | — | `EYE_OF_THE_STORM` |
| 16484 | 2923 | Grasping Reach | — | `NETHERSTORM` |
| 16340 | 2912 The Voidspire | The Voidspire | Devouring Host B/D/H + Shadowguard Void B/C + Voidstorm A/C/E | `TEMPEST_KEEP` |
| 16829 | 2912 | The Approach | Devouring Host A/B/C | `FORGE_BASE` |
| 16825 | 2912 | Devouring Stronghold | — | `FORGE_BASE` |
| 16826 | 2912 | Behemoth's Rise | Voidstorm A/D/E | `WILDS` |
| 16827 | 2912 | The Riftlabs | Shadowguard Void B/C/H | `ETHEREUM` |
| 16828 | 2912 | Crown of the Cosmos | — | `TEMPEST_KEEP` |
| 16507 | 2912 | Isle of Quel'Danas | mus_110_alleria_b + mus_110_alleria_a | `—` |
| 16639 | 2912 | Magisters' Terrace | — | `—` |
| 16423 | 2799 Slayer's Rise (BG) | Slayer's Rise | Midnight Battle D/E + Storm Fields B/E + Void Combat B + Voidstorm E + Devouring Host F/I/J/K | `EYE_OF_THE_STORM` |
| 16488 | 2799 | Grief Spire | mus_mx_cov_seatoftheprimus_01 | `OUTLAND_ALLIANCE` |
| 16492 | 2799 | Bastion of Valor | mus_mx_cov_seatoftheprimus_01 | `OUTLAND_ALLIANCE` |
| 16489 | 2799 | Hate Spire | mus_mx_cov_seatoftheprimus_01 | `OUTLAND_HORDE` |
| 16491 | 2799 | Bastion of Might | mus_mx_cov_seatoftheprimus_01 | `OUTLAND_HORDE` |
| 16496 | 2799 | Hanaar Outpost | mus_mx_cov_seatoftheprimus_01 | `OUTLAND_HORDE` |
| 16494 | 2799 | Shadowridge Outpost | Shadowguard Void A/B/C/D/H | `ETHEREUM` |
| 16495 | 2799 | Stareater Pavilion | Shadowguard Void A/B/C/D/H | `ETHEREUM` |
| 16499 | 2799 | Shenzar Refinery | Shadowguard Void A/B/C/D/H | `ETHEREUM` |
| 16498 | 2799 | The Husk | Gnawing Reach A/B/C/H/D/E | `WILDS` |
| 16855 | 2799 | Voidscar Arena | Devouring Host D/E/H/I | `FORGE_BASE` |
| 16592 | 2965 Sunkiller Sanctum | Sunkiller Sanctum | — | `FORGE_BASE` |
| 16596 | 2966 Torment's Rise | Torment's Rise | — | `FORGE_BASE` |
| 16354 | 2953 (gouffre Parhelion Plaza, aire « Voidstorm ») | Voidstorm | — | `—` |

Remarques :

- Dans le donjon Voidscar Arena, le sous-texte varie (Slayer's Rise, Pit of Spite, The Husk, Sparring Grounds, Grasping Reach) : les 3 étages `[2572..2574]` peuvent porter des sous-zones.
- Le raid The Voidspire réutilise « Isle of Quel'Danas » et « Magisters' Terrace » pour la fin du boss 6 (musique Alleria) : ne pas mapper, laisser le natif.
- Gnawing Reach (16341) joue nativement un placeholder Shadowlands (`mus_mx_cov_seatoftheprimus_01`), comme les flèches du BG instancié : Blizzard n'a pas fini ces kits, ce qui justifie encore plus un pack TBC.

### 1.3 Familles de pistes Midnight utilisées dans Voidstorm (FDID)

| Famille | Fichiers : lettre = FDID (durée s) |
|---|---|
| Voidstorm | A = 7692210 (139.8), B = 7692212 (145.1), C = 7692214 (105.5), D = 7692216 (139.9), E = 7692218 (152.5), F = 7713464 (109.9), H = 7692220 (290.6) |
| Storm Fields | A = 7690563 (151.3), B = 7690565 (124.4), C = 7690567 (145.9), D = 7690569 (145.1), E = 7690571 (124.5), F = 7690573 (133.4), G = 7690575 (146.4), H = 7690577 (293.9), I = 7690579 (145.8) |
| Devouring Host | A = 7681054 (96.6), B = 7681056 (76.4), C = 7681058 (93.3), D = 7681060 (126.0), E = 7681062 (91.7), F = 7703708 (71.3), G = 7703710 (68.0), H = 7681064 (199.6), I = 7703712 (105.0), J = 7703714 (77.5), K = 7703716 (87.0) |
| Locus Point | A = 7684188 (118.4), B = 7684190 (122.2), C = 7684192 (135.8), D = 7684194 (153.6), E = 7684196 (120.4), F = 7713420 (132.3), H = 7684198 (161.6) |
| Howling Ridge | A = 7681076 (83.8), B = 7681078 (85.2), C = 7681080 (95.8), D = 7681082 (60.0), E = 7681084 (91.1), H = 7681086 (140.1) |
| Shadowguard Void | A = 7681154 (156.8), B = 7681156 (139.4), C = 7681158 (130.5), D = 7681160 (150.7), H = 7681162 (174.6) |
| Gnawing Reach | A = 7696432 (108.6), B = 7696434 (123.4), C = 7696436 (126.5), D = 7703718 (81.5), E = 7703720 (135.4), H = 7696438 (163.5) |
| Slayers Rise | A = 7691961 (141.9), B = 7691963 (153.2), C = 7691965 (149.1), D = 7691971 (87.0), E = 7691975 (77.5), F = 7691977 (85.4), G = 7691980 (140.4), H = 7691982 (167.3) |
| Void Combat | A = 7692196 (169.6), B = 7692198 (159.7), C = 7692200 (125.2), D = 7692202 (171.1), E = 7692204 (135.6), F = 7692206 (130.5), G = 7724006 (31.1), H = 7692208 (234.4), I = 7726432 (125.7) |
| Ethereal Combat Void | A = 7713396 (130.3), B = 7713398 (71.8) |
| Xalatath Midnight | A = 7701033 (158.0), B = 7701035 (152.2), C = 7703760 (16.1), D = 7703762 (23.5), E = 7703764 (100.8), F = 7703766 (57.6), H = 7698310 (88.5) |

Durées mesurées par ffprobe le 11/09/2026 (`durations_midnight.csv`), sauf Locus Point reprises du plugin Quel'Thalas. Contrôle croisé : Voidstorm E, Storm Fields F, Slayers Rise B, Devouring Host I et G donnent les mêmes valeurs que les entrées `MN_ParhelionPlaza*` de Quel'Thalas.

> **Effet de bord découvert** : dans `EchoesOfAzeroth_QuelThalas/Tracks.lua`, les pistes `VE_VoidstormA…H` sont en réalité `MUS_120_Locus_Point_A…E,H,F` + `Voidstorm_B`, et `MN_ParhelionPlazaE…I` sont `Voidstorm_E`, `Storm_Fields_F`, `Slayers_Rise_B`, `Devouring_Host_I`, `Devouring_Host_G`. Les FDID sont bons, seuls les noms symboliques sont trompeurs. À corriger dans un commit séparé du plugin Quel'Thalas, pas ici.

## 2. Netherstorm — inventaire

### 2.1 Cartes

UiMapID 109 Netherstorm (parent 101 Outland). AreaTable racine 3523, 49 sous-zones directes (continent 530). Instances liées : Map 550 Tempest Keep (raid L'Œil), 552 Arcatraz, 553 Botanica, 554 Méchanar, 557 Auchindoun : Tombes-mana (donjon éthéré, en Terokkar), 566 / 968 Œil du cyclone (BG « NetherstormBG »).

### 2.2 Musique native

- **Zone entière** : ZoneMusic 272 « Zone-Netherstorm », kit 9284 = `NS_GeneralWalkUni01…10`, pauses de 3 à 5 min entre pistes. C'est la seule musique propre à la zone.
- **Foudreflèche + 4 écodômes** : ZoneMusic 335 « Zone-NetherstormEco-Dome » = `NA_GeneralWalkDay01/02` (Nagrand) + `OL_HistoricIntroUni01`.
- **Ruines d'Enkaat** : ZoneMusic 310 « Zone-OutlandDraeneiBase » = `OL_DraeneiBaseWalkUni01/02`.
- **Bastion des Solfurie** : ZoneMusic 337 « Zone-OutlandBloodElfHostile » = `GL_Forest3WalkNight01…03` (déjà dans le plugin Quel'Thalas).
- **Intros par sous-zone** (champ `IntroSound` d'AreaTable → ZoneIntroMusicTable, une fois par 10 ou 60 min) : c'est là que Netherstorm signe ses lieux. Les manaforges ont chacune une intro « Netherplant », les bases de la Légion une intro « Burning Legion », les zones de cristaux une intro « Crystal », les villes gobelines l'intro « Historic », les écodômes l'intro « Scenic ».
- **Œil du cyclone** (ZoneMusic 2234, kit 129972) : `NS_GeneralWalkUni01/03/08` + `tk_TempestKeep_AMB_11/13/18` + `tk_TempestKeep_BTL13`, intro `OL_HistoricIntroUni01`.
- **Donjon de la Tempête** (ZoneMusic 373 / 374) : `tk_TempestKeep_AMB_11…23` (ambiance), `BTL10/11/13` (combat), `STG14/15/16` (stingers de 12 s).
- `NS_MushroomIntroUni01…03` existent dans le dossier Netherstorm mais ne sont plus référencés par aucune aire de la zone (réutilisés en Draenor) : utilisables comme intros « organiques ».

### 2.3 Sous-zones (AreaTable, parent 3523)

| AreaID | enUS | frFR | ZoneMusic natif | Intro (ZoneIntroMusicTable) | Thème |
|---|---|---|---|---|---|
| 3523 | Netherstorm | Raz-de-Néant | Zone-Netherstorm : NS_GeneralWalkUni01…10 | — | Racine : anciennes terres de Farahlon rongées par le Néant |
| 3712 | Area 52 | Zone 52 | — | OL_Historic01 → OL_HistoricIntroUni01 (délai 10 min) | Ville gobeline neutre (fusée X-52) |
| 3721 | The Crumbling Waste | La Désagrégation | — | — | Terres qui s'effritent au bord du Néant |
| 3722 | Manaforge Ara | Manaforge Ara | — | NetherstormPlant01 → NS_NetherplantIntroUni01 (délai 60 min) | Manaforge Sunfury (Kael'thas), draine le Néant |
| 3723 | Arklon Ruins | Ruines Arklon | — | — | Ruines draeneï infestées de démons |
| 3724 | Cosmowrench | Cosmovrille | — | OL_Historic01 → OL_HistoricIntroUni01 (délai 10 min) | Base gobeline est |
| 3725 | Ruins of Enkaat | Ruines d’Enkaat | Zone-OutlandDraeneiBase : OL_DraeneiBaseWalkUni01 + OL_DraeneiBaseWalkUni02r | OL_Broken → OL_ActionWalkUni01 (délai 60 min) | Ruines draeneï hantées d'esprits |
| 3726 | Manaforge B'naar | Manaforge B’naar | — | NetherstormPlant02 → NS_NetherplantIntroUni02 (délai 60 min) | Manaforge Sunfury |
| 3727 | The Scrap Field | La Ferraille | — | OutlandBurningLegion01 → OL_BurningLegionIntroUni01 (délai 60 min) | Casse gobeline (Légion) |
| 3728 | The Vortex Fields | Les champs du vortex | — | — | Champs du vortex (Manaforge Duro) |
| 3729 | The Heap | Le Monceau | — | — | Décharge gobeline |
| 3730 | Manaforge Coruu | Manaforge Coruu | — | NetherstormPlant03 → NS_NetherplantIntroUni03 (délai 60 min) | Manaforge Sunfury |
| 3731 | The Tempest Rift | La faille des Tempêtes | — | — | Faille des Tempêtes |
| 3732 | Kirin'Var Village | Kirin’Var | — | — | Village Kirin Tor abandonné, hanté |
| 3733 | The Violet Tower | La tour Pourpre | — | — | Tour de Kirin'Var |
| 3734 | Manaforge Duro | Manaforge Duro | — | NetherstormPlant04 → NS_NetherplantIntroUni04 (délai 60 min) | Manaforge Sunfury (champs du vortex) |
| 3735 | Voidwind Plateau | Le plateau Vent-du-Vide | — | — | Plateau corrompu par le Vide |
| 3736 | Manaforge Ultris | Manaforge Ultris | — | NetherstormPlant01 → NS_NetherplantIntroUni01 (délai 60 min) | Manaforge détruite, infestée de créatures du Vide |
| 3737 | Celestial Ridge | Crête Céleste | — | OutlandCrystal03 → OL_CrystalIntroUni03 (délai 60 min) | Forêt de cristaux arcaniques, nid des drakes du Néant |
| 3738 | The Stormspire | La Foudreflèche | Zone-NetherstormEco-Dome : NA_GeneralWalkDay01/02 + OL_HistoricIntroUni01 | OutlandScenic → OL_ScenicIntroUni01 (délai 60 min) | QG des éthérés du Consortium |
| 3739 | Forge Base: Oblivion | Base de forge : Oubli | — | OutlandBurningLegion02 → OL_BurningLegionIntroUni02 (délai 60 min) | Base de la Légion ardente (saccageurs gangrenés) |
| 3740 | Forge Base: Gehenna | Base de forge : Géhenne | — | OutlandBurningLegion01 → OL_BurningLegionIntroUni01 (délai 60 min) | Base de la Légion ardente |
| 3741 | Ruins of Farahlon | Ruines de Farahlon | — | — | Ruines draeneï tenues par la Légion |
| 3742 | Socrethar's Seat | Siège de Socrethar | — | — | Forteresse du commandant de la Légion |
| 3837 | Sunfury Hold | Bastion des Solfurie | Zone-OutlandBloodElfHostile : GL_Forest3WalkNight01…03 | — | Bastion militaire elfe de sang |
| 3842 | Tempest Keep | Donjon de la Tempête | — | — | Forteresse naaru capturée par Kael'thas (raid L'Œil + 3 donjons) |
| 3850 | Netherstone | Pierre-de-Néant | — | OutlandCrystal01 → OL_CrystalIntroUni01 (délai 60 min) | Zone élite arcanique |
| 3851 | Midrealm Post | Comptoir des Terres-médianes | — | — | Comptoir du Consortium dans l'écodôme |
| 3852 | Tuluman's Landing | Point d’ancrage de Tuluman | — | — | Point d'ancrage de Tuluman |
| 3854 | Protectorate Watch Post | Poste de garde du Protectorat | — | — | Poste des éthérés du Protectorat |
| 3868 | Gyro-Plank Bridge | Pont de Gyro-passerelles | — | — | Pont gobelin vers les Tranchantes |
| 3873 | The Proving Grounds | Le terrain d’Essai | — | — | Terrain d'essai (éthérés) |
| 3874 | Eco-Dome Farfield | Écodôme Champlointain | Zone-NetherstormEco-Dome : NA_GeneralWalkDay01/02 + OL_HistoricIntroUni01 | OutlandScenic → OL_ScenicIntroUni01 (délai 60 min) | Écodôme éthéré |
| 3875 | Eco-Dome Skyperch | Écodôme Percheciel | Zone-NetherstormEco-Dome : NA_GeneralWalkDay01/02 + OL_HistoricIntroUni01 | OutlandScenic → OL_ScenicIntroUni01 (délai 60 min) | Écodôme éthéré |
| 3876 | Eco-Dome Sutheron | Écodôme Sudron | Zone-NetherstormEco-Dome : NA_GeneralWalkDay01/02 + OL_HistoricIntroUni01 | OutlandScenic → OL_ScenicIntroUni01 (délai 60 min) | Écodôme éthéré |
| 3877 | Eco-Dome Midrealm | Écodôme Terres-Médianes | Zone-NetherstormEco-Dome : NA_GeneralWalkDay01/02 + OL_HistoricIntroUni01 | OutlandScenic → OL_ScenicIntroUni01 (délai 60 min) | Écodôme éthéré |
| 3878 | Ethereum Staging Grounds | Lieu de rassemblement de l’Ethereum | — | — | Camp des éthérés de l'Ethereum (touchés par le Vide) |
| 3879 | Chapel Yard | Cour de la Chapelle | — | — | Cour de la chapelle (Kirin'Var) |
| 3880 | Access Shaft Zeon | Puits d’accès Zéon | — | — | Puits d'accès (mine) |
| 3881 | Trelleum Mine | Mine de Trelleum | — | — | Mine sous Manaforge Ara |
| 3882 | Invasion Point: Destroyer | Site d’invasion : Destructeur | — | OutlandBurningLegion02 → OL_BurningLegionIntroUni02 (délai 60 min) | Site d'invasion de la Légion |
| 3883 | Camp of Boom | Camp de Boum | — | — | Camp du Dr Boum |
| 3900 | Invasion Point: Overlord | Site d’invasion : Suzerain | — | — | Site d'invasion de la Légion |
| 3921 | Arklonis Ridge | Crête d’Arklonis | — | — | Crête des ruines Arklon |
| 3934 | Town Square | Place Centrale | — | — | Place de Kirin'Var |
| 3935 | Wizard Row | Allée des Sorciers | — | — | Allée de Kirin'Var |
| 5554 | Tempest Keep - The Mechanar Entrance | Donjon de la Tempête - Entrée du Méchanar | — | — | Entrée du Méchanar |
| 5555 | Tempest Keep - The Botanica Entrance | Donjon de la Tempête - Entrée de la Botanica | — | — | Entrée de la Botanica |
| 5556 | Tempest Keep - The Arcatraz Entrance | Donjon de la Tempête - Entrée de l’Arcatraz | — | — | Entrée de l'Arcatraz |
| 8613 | Rusty Rocket Tavern | Taverne de la Fusée rouillée | — | — | Taverne de Zone 52 |

### 2.4 Pistes TBC candidates (FDID, durée mesurée)

| FDID | Fichier | Durée (s) | Source native |
|---|---|---|---|
| 53620 | NS_GeneralWalkUni01 | 150.7 | Netherstorm général (ZoneMusic 272) |
| 53621 | NS_GeneralWalkUni02 | 175.4 | Netherstorm général (ZoneMusic 272) |
| 53622 | NS_GeneralWalkUni03 | 178.4 | Netherstorm général (ZoneMusic 272) |
| 53623 | NS_GeneralWalkUni04 | 181.3 | Netherstorm général (ZoneMusic 272) |
| 53624 | NS_GeneralWalkUni05 | 184.3 | Netherstorm général (ZoneMusic 272) |
| 53625 | NS_GeneralWalkUni06 | 192.0 | Netherstorm général (ZoneMusic 272) |
| 53626 | NS_GeneralWalkUni07 | 193.3 | Netherstorm général (ZoneMusic 272) |
| 53627 | NS_GeneralWalkUni08 | 168.9 | Netherstorm général (ZoneMusic 272) |
| 53628 | NS_GeneralWalkUni09 | 199.2 | Netherstorm général (ZoneMusic 272) |
| 53629 | NS_GeneralWalkUni10 | 223.0 | Netherstorm général (ZoneMusic 272) |
| 53630 | NS_MushroomIntroUni01 | 39.2 | intro Mushroom (orpheline) |
| 53631 | NS_MushroomIntroUni02 | 33.9 | intro Mushroom (orpheline) |
| 53632 | NS_MushroomIntroUni03 | 36.9 | intro Mushroom (orpheline) |
| 53633 | NS_NetherplantIntroUni01 | 44.7 | intro Netherplant (manaforges) |
| 53634 | NS_NetherplantIntroUni02 | 51.2 | intro Netherplant (manaforges) |
| 53635 | NS_NetherplantIntroUni03 | 47.8 | intro Netherplant (manaforges) |
| 53636 | NS_NetherplantIntroUni04 | 45.4 | intro Netherplant (manaforges) |
| 53637 | OL_ActionWalkUni01 | 80.8 | intro OL_Broken (Ruines d'Enkaat) |
| 53638 | OL_AllianceBaseWalkUni01 | 134.5 | base Alliance d'Outreterre (Bastion de l'Honneur…) |
| 53639 | OL_AllianceBaseWalkUni02 | 110.5 | base Alliance d'Outreterre |
| 53644 | OL_BurningLegionIntroUni01 | 16.5 | intro Légion 01 (Ferraille, Géhenne) |
| 53645 | OL_BurningLegionIntroUni02 | 35.2 | intro Légion 02 (Oubli, site d'invasion) |
| 53649 | OL_Corrupt01 | 60.9 | Outreterre corrompue (ZoneMusic 302/334, lieux tenus par la Légion) |
| 53650 | OL_Corrupt02 | 62.6 | Outreterre corrompue (ZoneMusic 302/334, lieux tenus par la Légion) |
| 53651 | OL_Corrupt03 | 74.4 | Outreterre corrompue (ZoneMusic 302/334, lieux tenus par la Légion) |
| 53652 | OL_Corrupt04 | 71.4 | Outreterre corrompue (ZoneMusic 302/334, lieux tenus par la Légion) |
| 53653 | OL_Corrupt05 | 72.6 | Outreterre corrompue (ZoneMusic 302/334, lieux tenus par la Légion) |
| 53654 | OL_Corrupt06 | 74.3 | Outreterre corrompue (ZoneMusic 302/334, lieux tenus par la Légion) |
| 53655 | OL_Corrupt07 | 52.3 | Outreterre corrompue (ZoneMusic 302/334, lieux tenus par la Légion) |
| 53656 | OL_CorruptIntro | 75.6 | Outreterre corrompue (ZoneMusic 302/334, lieux tenus par la Légion) |
| 53657 | OL_CrystalIntroUni01 | 26.8 | intro Crystal 01 (Pierre-de-Néant) |
| 53658 | OL_CrystalIntroUni02 | 21.9 | intro Crystal 02 |
| 53659 | OL_CrystalIntroUni03 | 21.6 | intro Crystal 03 (Crête Céleste) |
| 53661 | OL_DraeneiBaseWalkUni01 | 106.6 | base draeneï (Ruines d'Enkaat) |
| 53662 | OL_DraeneiBaseWalkUni02r | 99.9 | base draeneï (Ruines d'Enkaat) |
| 53665 | OL_HistoricIntroUni01 | 79.5 | intro Historic (Zone 52, Cosmovrille, Œil du cyclone) |
| 53668 | OL_HordeBaseWalkUni03 | 66.2 | base Horde d'Outreterre (Thrallmar…) |
| 53669 | OL_HordeBaseWalkUni04 | 68.1 | base Horde d'Outreterre |
| 53677 | OL_ScenicIntroUni01 | 31.5 | intro Scenic (Foudreflèche, écodômes) |
| 53779 | tk_TempestKeep_AMB_11 | 46.0 | Donjon de la Tempête ambiance (ZoneMusic 373) |
| 53780 | tk_TempestKeep_AMB_12 | 96.7 | Donjon de la Tempête ambiance (ZoneMusic 373) |
| 53781 | tk_TempestKeep_AMB_13 | 67.7 | Donjon de la Tempête ambiance (ZoneMusic 373) |
| 53782 | tk_TempestKeep_AMB_14 | 88.5 | Donjon de la Tempête ambiance (ZoneMusic 373) |
| 53783 | tk_TempestKeep_AMB_16 | 58.3 | Donjon de la Tempête ambiance (ZoneMusic 373) |
| 53784 | tk_TempestKeep_AMB_17 | 62.7 | Donjon de la Tempête ambiance (ZoneMusic 373) |
| 53785 | tk_TempestKeep_AMB_18 | 85.9 | Donjon de la Tempête ambiance (ZoneMusic 373) |
| 53786 | tk_TempestKeep_AMB_19 | 48.7 | Donjon de la Tempête ambiance (ZoneMusic 373) |
| 53787 | tk_TempestKeep_AMB_20 | 47.0 | Donjon de la Tempête ambiance (ZoneMusic 373) |
| 53788 | tk_TempestKeep_AMB_22 | 34.1 | Donjon de la Tempête ambiance (ZoneMusic 373) |
| 53789 | tk_TempestKeep_AMB_23 | 67.9 | Donjon de la Tempête ambiance (ZoneMusic 373) |
| 53790 | tk_TempestKeep_BTL10 | 59.7 | Donjon de la Tempête combat (ZoneMusic 374) |
| 53791 | tk_TempestKeep_BTL11 | 81.6 | Donjon de la Tempête combat (ZoneMusic 374) |
| 53792 | tk_TempestKeep_BTL13 | 36.6 | Donjon de la Tempête combat (ZoneMusic 374) |
| 53793 | tk_TempestKeep_STG14 | 11.8 | Donjon de la Tempête stinger |
| 53794 | tk_TempestKeep_STG15 | 11.6 | Donjon de la Tempête stinger |
| 53795 | tk_TempestKeep_STG16 | 11.8 | Donjon de la Tempête stinger |
| 53796 | TF_AuchindounWalkUni01 | 120.3 | Auchindoun (ZoneMusic 316, donjons éthérés/draeneï) |
| 53797 | TF_AuchindounWalkUni02 | 150.1 | Auchindoun |
| 53798 | TF_AuchindounWalkUni03 | 120.3 | Auchindoun |

Déjà présents avec durée dans le plugin Quel'Thalas (à redéclarer localement) : `GL_Forest3WalkNight01…03` = 53510 / 53511 / 53512 (51.3 / 28.1 / 44.4 s), `OL_BloodElfBaseWalkUni01/02` = 53642 / 53643 (120.0 / 121.6 s).

## 3. Rapprochements et packs proposés

### 3.1 Les parallèles

| Voidstorm | Netherstorm | Pourquoi |
|---|---|---|
| Steppes, routes, Storm Fields, Grasping Reach | Zone générale (`NS_GeneralWalkUni01…10`) | Deux terres brisées flottant dans le Néant / le Vide ; la colonne vertébrale du plugin |
| The Ingress, Locus Point, Howling Ridge, Dusk's Repose, Masters' Perch | Zone 52 / Cosmovrille (intro Historic) | Les hubs neutres où l'on souffle ; l'intro « Historic » est la signature des villes de Netherstorm |
| Points-nexus Antius / Xenas / Mid'Ar (« Pylon ») | Manaforges Ara / B'naar / Coruu / Duro (intros Netherplant 01–04) | Machines qui drainent le Vide ↔ machines qui drainent le Néant. Xenas « en train de s'effondrer » ↔ Manaforge Ultris détruite et envahie par le Vide |
| Shadowguard Point, Ethereum Refinery / Overcroft, Shenzar Refinery, avant-postes | Lieu de rassemblement de l'Ethereum, Foudreflèche, Tombes-mana | Même faction, même nom : l'Ethereum de Netherstorm sont les éthérés touchés par le Vide. Le set Auchindoun (`TF_AuchindounWalk`) est celui des donjons éthérés |
| Stormarion Keep / Watch, Obscurion Citadel, Voidscar Arena | Bases de forge Oubli / Géhenne, sites d'invasion, siège de Socrethar (intros Légion + set « corrupt ») | Forteresses de l'armée envahissante |
| Stormarion Citadel (occupée par les ren'dorei après l'assaut) | Bastion des Solfurie + bases elfes de sang d'Outreterre | Place forte elfique militaire ; les ren'dorei sont d'anciens elfes de sang |
| The Voidspire, The Approach, raid | Donjon de la Tempête (ambiances `tk_*_AMB`, stingers) | Le siège du maître de la zone : Xal'atath ↔ Kael'thas |
| Nexus-Point Xenas (donjon) | Donjon de la Tempête (Méchanar / Botanica / Arcatraz) | Installation technologique en ruine |
| Voidscar Arena (donjon) | Donjon de la Tempête combat (`tk_*_BTL`) | Arène = combat permanent |
| The Molt, Bladeburrows, Underground Burrows, Voidburrow | Intros Mushroom + général | Matière organique (mue, terriers) ↔ intros « champignon » |
| Den / Lair of Predaxas, Gorging Pit, Night Trench, Husk, grottes | Crête Céleste, Pierre-de-Néant (intros Crystal) | Repaires de la faune : drakes du Néant ↔ kaiju de Predacea |
| Slayer's Rise (zone PvP + BG) | Œil du cyclone (BG de Netherstorm) | Le champ de bataille de la zone, kit déjà mixé par Blizzard |
| Grief Spire, Retribution Hold, Bastion of Valor | Bases Alliance d'Outreterre | Camp Alliance |
| Hate Spire, Mettle's Hold, Bastion of Might | Bases Horde d'Outreterre | Camp Horde |
| Exiles' Hovel | Ruines d'Enkaat (base draeneï + intro Broken) | Voidstorm abrite des draeneï et des Brisés exilés |

### 3.2 Packs TBC

| Clé | Label | intro | Pistes | Zones par défaut |
|---|---|---|---|---|
| `NETHERSTORM` | Netherstorm (TBC) | — | any = NS_GeneralWalkUni01…10 | 2405 racine, Storm Fields, Grasping Reach, Gnawing Reach |
| `AREA52` | Area 52 (TBC) | OL_HistoricIntroUni01 | any = NS_GeneralWalkUni01…10 | The Ingress, Locus Point, The Howling Ridge, Dusk's Repose, Masters' Perch |
| `MANAFORGE` | Manaforge (TBC) | NS_NetherplantIntroUni01 | any = NS_NetherplantIntroUni02…04 + NS_GeneralWalkUni01…10 | Nexus-Point Antius / Xenas / Mid'Ar |
| `ETHEREUM` | Ethereum (TBC) | OL_CrystalIntroUni01 | any = TF_AuchindounWalkUni01…03 | Shadowguard Point, Ethereum Refinery, Ethereum Overcroft, Shenzar Refinery, Hanaar / Shadowridge Outpost, Shadow Rise |
| `FORGE_BASE` | Forge Base (TBC) | OL_BurningLegionIntroUni02 | any = OL_Corrupt01…07 + OL_BurningLegionIntroUni01 | Stormarion Keep / Watch, Obscurion Citadel, Voidscar Arena (extérieur), gouffres Sunkiller Sanctum / Torment's Rise |
| `SUNFURY` | Sunfury Hold (TBC) | — | any = GL_Forest3WalkNight01…03 + OL_BloodElfBaseWalkUni01/02 | Stormarion Citadel |
| `TEMPEST_KEEP` | Tempest Keep (TBC) | tk_TempestKeep_STG14 | any = tk_TempestKeep_AMB_11…23 | The Voidspire, The Approach, raid 2529/2530, donjon Nexus Point Xenas 2556 |
| `TEMPEST_KEEP_BATTLE` | Tempest Keep Battle (TBC) | tk_TempestKeep_STG15 | any = tk_TempestKeep_BTL10 / 11 / 13 | donjon Voidscar Arena 2572…2574 |
| `MOLT` | The Molt (TBC) | NS_MushroomIntroUni01 | any = NS_MushroomIntroUni02 / 03 + NS_GeneralWalkUni01…10 | The Molt, Underground Burrows, The Bladeburrows, Overrun Hollow, Abundant Voidburrow, gouffre Voidburrow |
| `WILDS` | Celestial Ridge (TBC) | OL_CrystalIntroUni03 | any = NS_GeneralWalkUni01…10 | Den / Lair of Predaxas, Night Trench, The Gorging Pit, The Husk, Quiet Cavern, Consumptor Cave |
| `EYE_OF_THE_STORM` | Eye of the Storm (TBC) | OL_HistoricIntroUni01 | any = NS_GeneralWalkUni01 / 03 / 08 + tk_TempestKeep_AMB_11 / 13 / 18 + tk_TempestKeep_BTL13 | 2444 Slayer's Rise racine et POI neutres, BG 2397 |
| `OUTLAND_ALLIANCE` | Honor Hold (TBC) | — | any = OL_AllianceBaseWalkUni01 / 02 | Grief Spire, Retribution Hold, Bastion of Valor |
| `OUTLAND_HORDE` | Thrallmar (TBC) | — | any = OL_HordeBaseWalkUni03 / 04 | Hate Spire, Mettle's Hold, Bastion of Might |
| `ENKAAT` | Ruins of Enkaat (TBC) | OL_ActionWalkUni01 | any = OL_DraeneiBaseWalkUni01 / 02 | Exiles' Hovel |

Points à trancher pendant l'implémentation : (a) les intros TBC sont courtes (12 à 80 s) et le core les joue une fois à l'entrée, ce qui reproduit bien le comportement TBC ; (b) `NS_GeneralWalkUni*` sont longues (2,5 à 3,7 min) : garder le `silenceGap` du core ; (c) un pack « silence » pour The Molt (natif = silence) n'est pas nécessaire, l'utilisateur peut mettre `NONE` en override.

### 3.3 Packs Midnight (reproduisent les kits natifs, regroupés)

| Clé | Label | Pistes |
|---|---|---|
| `VOIDSTORM_MIDNIGHT` | Voidstorm (Midnight) | Storm Fields A…I + Gnawing Reach B / D |
| `SINGULARITY_MIDNIGHT` | Locus Point (Midnight) | Locus Point A…F / H + Voidstorm B |
| `HOWLING_RIDGE_MIDNIGHT` | Howling Ridge (Midnight) | Howling Ridge A…E / H |
| `DEVOURING_HOST_MIDNIGHT` | Devouring Host (Midnight) | Devouring Host A…K + Voidstorm A / C / D / F |
| `SHADOWGUARD_MIDNIGHT` | Shadowguard (Midnight) | Shadowguard Void A…D / H |
| `PREDAXAS_MIDNIGHT` | Predaxas (Midnight) | Voidstorm A / E / H + Devouring Host J |
| `GORGING_PIT_MIDNIGHT` | Gorging Pit (Midnight) | Gnawing Reach A / C / E / H |
| `SLAYERS_RISE_MIDNIGHT` | Slayer's Rise (Midnight) | Slayers Rise A…H + Storm Fields B / E / F / I |

Packs mixés `*_MIXED` (TBC + Midnight) : NETHERSTORM+VOIDSTORM, AREA52+SINGULARITY, MANAFORGE+DEVOURING_HOST, ETHEREUM+SHADOWGUARD, FORGE_BASE+DEVOURING_HOST, TEMPEST_KEEP+DEVOURING_HOST, WILDS+PREDAXAS, MOLT+GORGING_PIT, EYE_OF_THE_STORM+SLAYERS_RISE. Packs utilitaires optionnels : `VOID_COMBAT` (Void Combat A…I, Ethereal Combat Void A/B), `XALATATH` (Xalatath Midnight A…F / H).

### 3.4 Esquisse de `Zones.lua`

```lua
[2405] = Dsl.zone("VOIDSTORM", "NETHERSTORM", {
    ABUNDANT_VOIDBURROW    = "MOLT",
    THE_INGRESS            = "AREA52",
    LOCUS_POINT            = "AREA52",
    THE_HOWLING_RIDGE      = "AREA52",
    DUSK_S_REPOSE          = "AREA52",
    NEXUS_POINT_ANTIUS     = "MANAFORGE",
    NEXUS_POINT_XENAS      = "MANAFORGE",
    NEXUS_POINT_MID_AR     = "MANAFORGE",
    SHADOWGUARD_POINT      = "ETHEREUM",
    ETHEREUM_REFINERY      = "ETHEREUM",
    ETHEREUM_OVERCROFT     = "ETHEREUM",
    STORMARION_KEEP        = "FORGE_BASE",
    STORMARION_CITADEL     = "SUNFURY",
    STORMARION_WATCH       = "FORGE_BASE",
    OBSCURION_CITADEL      = "FORGE_BASE",
    THE_VOIDSPIRE          = "TEMPEST_KEEP",
    THE_APPROACH           = "TEMPEST_KEEP",
    THE_MOLT               = "MOLT",
    UNDERGROUND_BURROWS    = "MOLT",
    THE_BLADEBURROWS       = "MOLT",
    DEN_OF_PREDAXAS        = "WILDS",
    LAIR_OF_PREDAXAS       = "WILDS",
    NIGHT_TRENCH           = "WILDS",
    THE_GORGING_PIT        = "WILDS",
    OVERRUN_HOLLOW         = "MOLT",
    QUIET_CAVERN           = "WILDS",
    CONSUMPTOR_CAVE        = "WILDS",
    EXILES_HOVEL           = "ENKAAT",
}),
[2444] = Dsl.zone("SLAYERS_RISE", "EYE_OF_THE_STORM", {
    MASTERS_PERCH          = "AREA52",
    GRIEF_SPIRE            = "OUTLAND_ALLIANCE",
    RETRIBUTION_HOLD       = "OUTLAND_ALLIANCE",
    BASTION_OF_VALOR       = "OUTLAND_ALLIANCE",
    HATE_SPIRE             = "OUTLAND_HORDE",
    METTLE_S_HOLD          = "OUTLAND_HORDE",
    BASTION_OF_MIGHT       = "OUTLAND_HORDE",
    VOIDSCAR_ARENA         = "FORGE_BASE",
    SHENZAR_REFINERY       = "ETHEREUM",
    THE_HUSK               = "WILDS",
    HANAAR_OUTPOST         = "ETHEREUM",
    SHADOWRIDGE_OUTPOST    = "ETHEREUM",
    SHADOW_RISE            = "ETHEREUM",
}),
[2556] = Dsl.zone("NEXUS_POINT_XENAS", "TEMPEST_KEEP"),
[2572] = Dsl.zone("VOIDSCAR_ARENA", "TEMPEST_KEEP_BATTLE"), [2573] = ..., [2574] = ...,
[2529] = Dsl.zone("THE_VOIDSPIRE", "TEMPEST_KEEP"), [2530] = ...,
[2526] = Dsl.zone("LAIR_OF_PREDAXAS", "WILDS"), [2527] = ...,
[2581] = Dsl.zone("VOIDBURROW", "MOLT"), [2582] = ...,
[2528] = Dsl.zone("SUNKILLER_SANCTUM", "FORGE_BASE"), [2571] = ...,
[2507] = Dsl.zone("TORMENTS_RISE", "FORGE_BASE"),
[2397] = Dsl.zone("SLAYERS_RISE_BG", "EYE_OF_THE_STORM"),  -- optionnel
```

Les sous-zones à ZoneMusic = 0 qui doivent garder le pack de la zone (Storm Fields, Grasping Reach, POI PvP…) n'ont pas besoin d'entrée : le core retombe sur le pack de la zone.

## 4. Structure du plugin et étapes

Dossier `~/Documents/Code/EchoesOfAzeroth_Voidstorm/`, calqué sur `_ZulAman` :

- `EchoesOfAzeroth_Voidstorm.toc` : `## Interface: 120100`, `## Title: Echoes of Azeroth: Voidstorm`, `## Dependencies: EchoesOfAzeroth`, `## X-Curse-Project-ID:` (à créer sur CurseForge), ordre de chargement `Locale.lua, Tracks.lua, Packs.lua, Zones.lua, Plugin.lua`.
- `Plugin.lua` : `id = "voidstorm"`, `title = "Voidstorm"`, `order = 30`, `category = "Eastern Kingdoms"` (même regroupement UI que Quel'Thalas, la carte 2405 est fille de 2537 Quel'Thalas ; alternative : une catégorie « Midnight »).
- `Locale.lua` : noms de zones et de sous-zones dans les 10 locales (annexe A, données AreaTable 12.1.0, donc exactes pour `GetSubZoneText()`).
- `Tracks.lua` : préfixes `NS_` (Netherstorm), `TK_` (Donjon de la Tempête), `OL_` (Outreterre général), `TF_` (Auchindoun), `GL_` (Ghostlands), `MN_` (Midnight) ; durées de §2.4 et de `durations_midnight.csv`.
- `Packs.lua` / `Zones.lua` : §3.2 à §3.4.
- `README.md`, `.pkgmeta` (ignorer `README.md`, `.github`, `.cursor`, `.gitignore`, **`docs`**), `.github/workflows/release.yml` copié de `_ZulAman` avec le nom du .toc, `icon.png` 64×64.

Étapes :

1. Valider ce plan (packs, catégorie, granularité des packs Midnight).
2. Générer `Tracks.lua` (FDID + durées) depuis les CSV du scratchpad, puis `Locale.lua` depuis les AreaTable localisées.
3. Écrire `Packs.lua`, `Zones.lua`, `Plugin.lua`, `.toc`.
4. Charger le plugin dans le harnais Lua 5.1 à stubs (comme pour le core) : chaque `nameKey` et clé de sous-zone doit exister dans `Locale.lua`, chaque pack référencé doit exister, chaque FDID doit avoir une durée.
5. Copier à la main dans `/mnt/Games/World of Warcraft/_retail_/Interface/AddOns/` et vérifier en jeu avec `/eoa now` : UiMapID de Slayer's Rise (2444), des donjons, du raid, des gouffres ; textes de sous-zone des lieux à ZoneMusic = 0 ; comportement des intros.
6. `git init`, dépôt GitHub `AnasyaDev/EchoesOfAzeroth_Voidstorm` via l'alias SSH `github-anasyadev`, projet CurseForge, variable `CF_PROJECT_ID`, ajouter l'entrée `voidstorm` dans `EchoesOfAzeroth/tools/push_addon_release.py`, release `v1.0.0` (commit une ligne, sans trailer).
7. Commit séparé côté Quel'Thalas pour renommer `VE_Voidstorm*` et `MN_ParhelionPlazaE…I`.

## Annexe A — noms localisés (AreaTable 12.1.0)

### A.1 Voidstorm

| AreaID | enUS | frFR | deDE | esES | esMX | ptBR | ruRU | itIT | koKR | zhCN | zhTW |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15458 | Voidstorm | Tempête du Vide | Leerensturm | Tormenta del Vacío | Tormenta del Vacío | Tempestade do Caos | Буря Бездны | Tempesta del Vuoto | 공허폭풍 | 虚影风暴 | 虛無風暴 |
| 15949 | The Ingress | Le Seuil | Der Ingress | El Acceso | El Acceso | A Passagem | Проход | Ingresso | 침투지 | 破境之地 | 初始地 |
| 15950 | Locus Point | Halte du Noyau | Locuspunkt | Punto de Enclave | Punto Intersticial | Ponto Lócus | Узел средоточия | Presidio del Locus | 공간 지점 | 方位点 | 暗域點 |
| 15951 | The Howling Ridge | La crête Hurlante | Heulender Grat | La Cresta Aullante | El Risco Aullador | Serra Uivante | Воющая гряда | Cresta Ululante | 울부짖는 능선 | 啸影山脊 | 咆哮峰 |
| 15952 | Nexus-Point Antius | Point-nexus Antius | Nexuspunkt Antius | Punto de Nexo: Antius | Punto del Nexo Antius | Ponto de Nexus Antius | Узел Нексуса Антий | Punta del Nexus Antius | 공결탑 안티우스 | 节点安提乌斯 | 奧核點安提厄斯 |
| 15953 | Shadowguard Point | Halte de l’Ombre-Garde | Schattenwachtspitze | Punto de la Guardia de las Sombras | Punto de la Guardia de las Sombras | Ponto da Guarda Sombria | Форпост Темной Стражи | Presidio della Guardia dell'Ombra | 어둠수호병 지점 | 影卫营 | 影衛崗哨 |
| 15954 | Nexus-Point Xenas | Point-nexus Xenas | Nexuspunkt Xenas | Punto de Nexo: Xenas | Punto del Nexo Xenas | Ponto de Nexus Xenas | Узел Нексуса Зенас | Punta del Nexus Xenas | 공결탑 제나스 | 节点希纳斯 | 奧核點瑟納斯 |
| 15955 | Nexus-Point Mid'Ar | Point-nexus Mid’Ar | Nexuspunkt Mid'ar | Punto de Nexo: Mid'Ar | Punto del Nexo Mid'Ar | Ponto de Nexus Mid'ar | Узел Нексуса Мид'ар | Punta del Nexus Mid'ar | 공결탑 미드아르 | 节点米达尔 | 奧核點米達爾 |
| 15956 | Stormarion Keep | Donjon de Fulgarion | Sturmarionfeste | Castillo de Tormentarion | Fuerte de Tormentarion | Bastilha de Tempestrião | Крепость Штормарион | Fortezza di Buferion | 스토마리온 요새 | 斯托玛兰要塞 | 風瑪利昂要塞 |
| 15957 | Obscurion Citadel | Citadelle d’Obscurion | Obskurionzitadelle | Ciudadela Obscurion | Ciudadela de Obscurion | Cidadela de Obscurião | Цитадель Обскурион | Cittadella Obscurion | 암연지 성채 | 胧影堡垒 | 朧暗堡壘 |
| 15958 | Masters' Perch | Perchoir des Maîtres | Hort der Meister | Pedestal del Maestro | Nido del Amo | Ninho do Mestre | Высота непобедимых | Trespolo dei Maestri | 지배자의 망루 | 主宰者之座 | 主宰棲所 |
| 15959 | Slayer's Rise | Colline Meurtrière | Schlächteranhöhe | Alto del Asesino | Alto del Asesino | Alto do Matador | Зубец убийцы | Altura del Carnefice | 학살자의 오름길 | 屠戮者高地 | 殺戮者高崗 |
| 15960 | The Voidspire | La flèche du Vide | Die Leerenspitze | Aguja del Vacío | La Aguja del Vacío | A Torre do Caos | Шпиль Бездны | Pinnacolo del Vuoto | 공허첨탑 | 虚影尖塔 | 虛無之尖 |
| 15961 | The Approach | Les Abords | Der Zugang | La Vereda | El Acercamiento | A Aproximação | Подступ | Soglia | 접근로 | 临影口 | 通道入口 |
| 15962 | Ethereum Refinery | Raffinerie de l’Ethereum | Astraleumraffinerie | Refinería de El Etereum | Refinería de El Etereum | Refinaria de Etéreum | Завод братства Эфириум | Raffineria degli Etereum | 에테리움 정제소 | 复仇军精炼厂 | 以太皇族精煉廠 |
| 15963 | Storm Fields | Champs des Tempêtes | Sturmfelder | Campos de la Tormenta | Campos Tormentosos | Campos Tempestuosos | Разгул Бури | Campi Tempestosi | 폭풍의 지대 | 风暴疆土 | 風暴原野 |
| 15964 | The Molt | La Mue | Tal der Transformation | La Muda | La Piel | A Exúvia | Распадок | Piana della Muta | 허물 | 蜕躯之原 | 蛻殼 |
| 15965 | The Bladeburrows | Les terriers Tranchants | Die Klingenhöhlen | Las Madrigueras Filosas | Las Madrigueras Filosas | Covas Afiadas | Кинжальные катакомбы | Cunicoli Aguzzi | 칼날굴 | 刃锋穴窟 | 劍刃地穴 |
| 15966 | Den of Predaxas | Tanière de Prédaxas | Bau von Predaxas | Cubil de Predaxas | Cubil de Predaxas | Covil de Predaxas | Логово Предаксаса | Tana di Predaxas | 프레닥사스의 소굴 | 普雷达萨斯之巢 | 普德薩斯之穴 |
| 15967 | Ethereum Overcroft | Manse de l’Ethereum | Hochplateau des Astraleums | Sobrebóveda de El Etereum | Sobrecoto de El Etereum | Sobrecâmara de Etéreum | Эфириальный Подсвод | Sovracripta degli Etereum | 에테리움 높은뜰 | 复仇军上层区 | 以太皇族高地 |
| 15970 | Grief Spire | Flèche du Deuil | Kummerspitze | Aguja del Pesar | Aguja del Pesar | Pináculo da Mágoa | Шпиль Горя | Guglia della Pena | 비탄의 첨탑 | 哀痛尖塔 | 悲慟尖塔 |
| 15971 | Hate Spire | Flèche de la Haine | Hassspitze | Aguja del Odio | Aguja del Odio | Pináculo do Ódio | Шпиль Ненависти | Guglia dell'Odio | 증오의 첨탑 | 憎恨尖塔 | 憎惡尖塔 |
| 15973 | Voidscar Arena | Arène de la Cicatrice du Vide | Die Arena der Leerennarbe | Arena Lacravacua | Arena Rajavacío | Arena da Chaga do Caos | Арена Шрама Бездны | Arena Sfregiavuoto | 공허흉터 투기장 | 虚空之痕竞技场 | 虛無之痕競技場 |
| 15974 | Path of Predation | Voie de la Prédation | Pfad der Prädation | Senda de la Depredación | Camino de Depredación | Caminho da Predação | Путь хищника | Sentiero della Predazione | 포식의 길 | 掠食之路 | 掠擊之路 |
| 15975 | The Bloodplains | Les plaines Sanglantes | Die Blutebenen | Las Llanuras Sangrientas | La Meseta Sangrienta | Planície Sangrenta | Кровавые равнины | Pianure del Sangue | 핏빛 평원 | 血痕平原 | 鮮血平原 |
| 15976 | Stareater Pavilion | Pavillon de Dévore-Étoile | Sternenfresserpavillon | Pabellón Devoraestrellas | Pabellón Astrófago | Pavilhão Fendestrela | Павильон Поедателя Звезд | Padiglione Mangiastelle | 별포식자 정자 | 噬星亭台 | 噬星者亭閣 |
| 15977 | Shattersky Pavilion | Pavillon de Brise-Ciel | Himmelsbrecherpavillon | Pabellón Rompecielos | Pabellón Rajacielos | Pavilhão Rompe-céu | Павильон Расколотого Неба | Padiglione Spezzacielo | 하늘파편 정자 | 碎穹亭台 | 碎天亭閣 |
| 16213 | Claw's Edge | Bord-de-Griffe | Klauenkamm | Filo de la Garra | Filo de la Garra | Garra Afiada | Урочище Когтя | Ciglio dell'Artiglio | 발톱 벼랑 | 利爪之缘 | 利爪之緣 |
| 16214 | The Fangfall | Crochute | Fangzahnfall | Salto del Colmillo | Caída del Colmillo | Quedapresa | Кряж Клыка | Calazanna | 송곳니 절벽 | 牙陨台 | 牙落 |
| 16216 | Bastion of Might | Bastion de la Puissance | Bastion der Macht | Bastión de Poderío | Bastión de Poder | Bastião da Força | Бастион мощи | Bastione del Vigore | 힘의 보루 | 力量堡垒 | 強力堡壘 |
| 16218 | Shenzar Refinery | Raffinerie de Shenzar | Shenzarraffinerie | Refinería Shenzar | Refinería Shenzar | Refinaria de Shenzar | Завод Шензар | Raffineria di Shenzar | 셴자르 정제소 | 申扎尔精炼厂 | 宣扎精煉廠 |
| 16219 | The Husk | La Bogue | Die Hülse | La Carcasa | La Cáscara | A Casca | Остов | Guscio Vuoto | 껍질 | 残骨空躯 | 屍殼 |
| 16220 | Sparring Grounds | Terrain d’affrontement | Übungsgelände | Liza de entrenamiento | Coto de Entrenamiento | Campo de Duelos | Учебная площадка | Campi d'Addestramento | 대련장 | 角力斗场 | 練武場 |
| 16221 | Hanaar Outpost | Avant-poste Hanaar | Außenposten Hanaar | Avanzada Hanaar | Puesto de Avanzada Hanaar | Posto Avançado Hanaar | Ханаарская застава | Avamposto di Hanaar | 하나르 전초기지 | 哈纳尔岗哨 | 哈納爾哨站 |
| 16222 | Shadowridge Outpost | Avant-poste d’Ombrecrête | Schattenkammaußenposten | Avanzada Crestasombra | Puesto de Avanzada Umbracresta | Posto Avançado da Serra Sombria | Тенескальная застава | Avamposto della Cresta d'Ombra | 어둠능선 전초기지 | 影脊岗哨 | 影脊哨站 |
| 16223 | Bastion of Valor | Bastion de la Vaillance | Bastion der Tapferkeit | Bastión del Valor | Bastión de Valor | Bastião da Bravura | Бастион доблести | Bastione del Valore | 용맹의 보루 | 英勇堡垒 | 英靈堡壘 |
| 16340 | The Voidspire | La flèche du Vide | Die Leerenspitze | Aguja del Vacío | La Aguja del Vacío | A Torre do Caos | Шпиль Бездны | Pinnacolo del Vuoto | 공허첨탑 | 虚影尖塔 | 虛無之尖 |
| 16341 | Gnawing Reach | Confins Dévorants | Die Nagende Senke | Confín Lacerante | Tramo Carcomido | Confins Devoradores | Беспредельный рубеж | Distesa Mordente | 갉아먹는 유역 | 啃噬之境 | 啃食之境 |
| 16360 | Grasping Reach | Confins Avides | Greifende Gefilde | Confín Oprimente | Tramo Atrapante | Borda Agarradora | Алчущая грань | Distesa Stritolante | 휘감는 손아귀 | 攫握之境 | 纏繞之境 |
| 16364 | Underground Burrows | Terriers Souterrains | Unterirdische Höhlen | Madrigueras Subterráneas | Madrigueras Subterráneas | Tocas Subterrâneas | Подземные лазы | Cunicoli Sotterranei | 지하 땅굴 | 地底洞窟 | 地底深穴 |
| 16423 | Slayer's Rise | Colline Meurtrière | Schlächteranhöhe | Alto del Asesino | Alto del Asesino | Alto do Matador | Зубец убийцы | Altura del Carnefice | 학살자의 오름길 | 屠戮者高地 | 殺戮者高崗 |
| 16425 | Voidscar Arena | Arène de la Cicatrice du Vide | Arena der Leerennarbe | Arena Lacravacua | Arena Rajavacío | Arena da Chaga do Caos | Арена Шрама Бездны | Arena Sfregiavuoto | 공허흉터 투기장 | 虚空之痕竞技场 | 虛痕競技場 |
| 16429 | Exiles' Hovel | Taudis de l’Exil | Hütte der Exilanten | Choza de los Exiliados | Refugio de Exiliados | Refúgio dos Exilados | Пристанище изгнанников | Spelonca degli Esiliati | 추방자의 거처 | 流亡者陋居 | 流放者小屋 |
| 16479 | Voidstorm | Tempête du Vide | Leerensturm | Tormenta del Vacío | Tormenta del Vacío | Tempestade do Caos | Буря Бездны | Tempesta del Vuoto | 공허폭풍 | 虚影风暴 | 虛無風暴 |
| 16480 | Slayer's Rise | Colline Meurtrière | Schlächteranhöhe | Alto del Asesino | Alto del Asesino | Alto do Matador | Зубец убийцы | Altura del Carnefice | 학살자의 오름길 | 屠戮者高地 | 殺戮者高崗 |
| 16481 | Pit of Spite | Fosse de la Rancune | Grube der Bosheit | Foso de Maldad | Foso del Resentimiento | Fosso do Rancor | Помост Злобы | Fossa della Perfidia | 원한의 구덩이 | 怨毒角斗场 | 怨恨坑洞 |
| 16482 | The Husk | La Bogue | Die Hülse | La Carcasa | La Cáscara | A Casca | Остов | Guscio Vuoto | 껍질 | 残骨空躯 | 屍殼 |
| 16483 | Sparring Grounds | Terrain d’affrontement | Übungsgelände | Liza de entrenamiento | Coto de Entrenamiento | Campo de Duelos | Учебная площадка | Campi d'Addestramento | 대련장 | 角力斗场 | 練武場 |
| 16484 | Grasping Reach | Confins Avides | Greifende Gefilde | Confín Oprimente | Tramo Atrapante | Borda Agarradora | Алчущая грань | Distesa Stritolante | 휘감는 손아귀 | 攫握之境 | 纏繞之境 |
| 16485 | Stormarion Citadel | Citadelle de Fulgarion | Sturmarionzitadelle | Ciudadela de Tormentarion | Ciudadela de Tormentarion | Cidadela de Tempestrião | Цитадель Штормарион | Cittadella Buferion | 스토마리온 성채 | 斯托玛兰堡垒 | 風瑪利昂堡壘 |
| 16486 | Stormarion Watch | Guet de Fulgarion | Sturmarionwacht | Atalaya de Tormentarion | Avanzada de Tormentarion | Vigília de Tempestrião | Дозор Штормарион | Presidio di Buferion | 스토마리온 감시터 | 斯托玛兰岗哨 | 風瑪利昂守望 |
| 16487 | Path of Predation | Voie de la Prédation | Pfad der Prädation | Senda de la Depredación | Camino de Depredación | Caminho da Predação | Путь хищника | Sentiero della Predazione | 포식의 길 | 掠食之路 | 掠擊之路 |
| 16488 | Grief Spire | Flèche du Deuil | Kummerspitze | Aguja del Pesar | Aguja del Pesar | Pináculo da Mágoa | Шпиль Горя | Guglia della Pena | 비탄의 첨탑 | 哀痛尖塔 | 悲慟尖塔 |
| 16489 | Hate Spire | Flèche de la Haine | Hassspitze | Aguja del Odio | Aguja del Odio | Pináculo do Ódio | Шпиль Ненависти | Guglia dell'Odio | 증오의 첨탑 | 憎恨尖塔 | 憎惡尖塔 |
| 16490 | The Bloodplains | Les plaines Sanglantes | Die Blutebenen | Las Llanuras Sangrientas | La Meseta Sangrienta | Planície Sangrenta | Кровавые равнины | Pianure del Sangue | 핏빛 평원 | 血痕平原 | 鮮血平原 |
| 16491 | Bastion of Might | Bastion de la Puissance | Bastion der Macht | Bastión de Poderío | Bastión de Poder | Bastião da Força | Бастион мощи | Bastione del Vigore | 힘의 보루 | 力量堡垒 | 強力堡壘 |
| 16492 | Bastion of Valor | Bastion de la Vaillance | Bastion der Tapferkeit | Bastión del Valor | Bastión de Valor | Bastião da Bravura | Бастион доблести | Bastione del Valore | 용맹의 보루 | 英勇堡垒 | 英靈堡壘 |
| 16493 | Claw's Edge | Bord-de-Griffe | Klauenkamm | Filo de la Garra | Filo de la Garra | Garra Afiada | Урочище Когтя | Ciglio dell'Artiglio | 발톱 벼랑 | 利爪之缘 | 利爪之緣 |
| 16494 | Shadowridge Outpost | Avant-poste d’Ombrecrête | Schattenkammaußenposten | Avanzada Crestasombra | Puesto de Avanzada Umbracresta | Posto Avançado da Serra Sombria | Тенескальная застава | Avamposto della Cresta d'Ombra | 어둠능선 전초기지 | 影脊岗哨 | 影脊哨站 |
| 16495 | Stareater Pavilion | Pavillon de Dévore-Étoile | Sternenfresserpavillon | Pabellón Devoraestrellas | Pabellón Astrófago | Pavilhão Fendestrela | Павильон Поедателя Звезд | Padiglione Mangiastelle | 별포식자 정자 | 噬星亭台 | 噬星者亭閣 |
| 16496 | Hanaar Outpost | Avant-poste Hanaar | Außenposten Hanaar | Avanzada Hanaar | Puesto de Avanzada Hanaar | Posto Avançado Hanaar | Ханаарская застава | Avamposto di Hanaar | 하나르 전초기지 | 哈纳尔岗哨 | 哈納爾哨站 |
| 16497 | The Fangfall | Crochute | Fangzahnfall | Salto del Colmillo | Caída del Colmillo | Quedapresa | Кряж Клыка | Calazanna | 송곳니 절벽 | 牙陨台 | 牙落 |
| 16498 | The Husk | La Bogue | Die Hülse | La Carcasa | La Cáscara | A Casca | Остов | Guscio Vuoto | 껍질 | 残骨空躯 | 屍殼 |
| 16499 | Shenzar Refinery | Raffinerie de Shenzar | Shenzarraffinerie | Refinería Shenzar | Refinería Shenzar | Refinaria de Shenzar | Завод Шензар | Raffineria di Shenzar | 셴자르 정제소 | 申扎尔精炼厂 | 宣扎精煉廠 |
| 16500 | Sparring Grounds | Terrain d’affrontement | Übungsgelände | Liza de entrenamiento | Coto de Entrenamiento | Campo de Duelos | Учебная площадка | Campi d'Addestramento | 대련장 | 角力斗场 | 練武場 |
| 16501 | Night Trench | Tranchée de la Nuit | Nachtgraben | Zanja Nocturna | Fosa Nocturna | Trincheira da Noite | Впадина ночи | Fossa Notturna | 밤의 도랑 | 暗夜战壕 | 黑夜海溝 |
| 16507 | Isle of Quel'Danas | Île de Quel’Danas | Insel von Quel'Danas | Isla de Quel'Danas | Isla de Quel'Danas | Ilha de Quel'Danas | Остров Кель'Данас | Isola di Quel'Danas | 쿠엘다나스 섬 | 奎尔丹纳斯岛 | 奎爾達納斯之島 |
| 16534 | Lair of Predaxas | Repaire de Prédaxas | Unterschlupf von Predaxas | Guarida de Predaxas | Guarida de Predaxas | Reduto de Predaxas | Берлога Предаксаса | Antro di Predaxas | 프레닥사스의 둥지 | 普雷达萨斯之穴 | 普德薩斯巢穴 |
| 16573 | Nexus-Point Xenas | Point-nexus Xenas | Nexuspunkt Xenas | Punto de Nexo: Xenas | Punto del Nexo Xenas | Ponto de Nexus Xenas | Узел Нексуса Зенас | Punta del Nexus Xenas | 공결탑 제나스 | 节点希纳斯 | 奧核點瑟納斯 |
| 16574 | Corespark Engineway | Moteur de noyétincelle | Der Kernfunkenmaschinenweg | Vía de Chispanúcleo | Paso del Motor Nucleochispa | Viamotor Centelha Nuclear | Механостанция сердцевинной искры | Motostrada di Scintinucleo | 핵심불꽃 동력로 | 核闪引擎道 | 核火引擎通路 |
| 16575 | Core Defense Nullward | Protection anti-Vide du noyau | Kernverteidigung Nullbereich | Resguardo nulo de defensa del núcleo | Nulirresguardo de Defensa del Núcleo | Nulaguarda da Defesa do Núcleo | Нуль-защита ядра | Nulloguardia del Nucleo di Difesa | 핵 방위용 무위의 수호물 | 护核虚无结界 | 核心防禦空無結界 |
| 16576 | The Nexus Core | Le noyau du Nexus | Der Kern des Nexus | Núcleo del Nexo | El Núcleo del Nexo | O Núcleo do Nexus | Ядро Нексуса | Nucleo del Nexus | 공결탑 핵 | 节点核心 | 奧核中心 |
| 16581 | Abundant Voidburrow | Terrier du Vide de l’Abondance | Opulenter Leerenbau | Túnel del Vacío Exuberante | Madriguera del Vacío Abundante | Toca do Caos Abundante | Изобильная нора Бездны | Concavuota dell'Abbondanza | 넘치는 공허굴 | 盎然虚空之窟 | 豐足虛無地穴 |
| 16599 | Slayer's Rise | Colline Meurtrière | Schlächteranhöhe | Alto del Asesino | Alto del Asesino | Alto do Matador | Зубец убийцы | Altura del Carnefice | 학살자의 오름길 | 屠戮者高地 | 殺戮者高崗 |
| 16600 | Shadow Rise | Ombrecime | Schattenanhöhe | Alto de la Sombra | Alto de las Sombras | Alto das Sombras | Вершина теней | Altura dell'Ombra | 어둠의 오르막 | 暗影高地 | 暗影高地 |
| 16639 | Magisters' Terrace | Terrasse des Magistères | Terrasse der Magister | Bancal del Magister | Bancal del Magister | Terraço dos Magísteres | Терраса Магистров | Terrazza dei Magisteri | 마법학자의 정원 | 魔导师平台 | 博學者殿堂 |
| 16648 | Voidstorm | Tempête du Vide | Der Leerensturm | Tormenta del Vacío | Tormenta del Vacío | Tempestade do Caos | Буря Бездны | Tempesta del Vuoto | 공허폭풍 | 虚影风暴 | 虛無風暴 |
| 16649 | Masters' Perch | Perchoir des Maîtres | Der Hort der Meister | Pedestal del Maestro | Nido del Amo | Ninho do Mestre | Высота непобедимых | Trespolo dei Maestri | 지배자의 망루 | 主宰者之座 | 主宰棲所 |
| 16652 | Overrun Hollow | Terrier du Vide | Das überwucherte Tal | Cuenca Infestada | Valle Infestado | Vazio Sobrepujado | Кишащая лощина | Rifugio Invaso | 무성한 공동 | 滥魔窟 | 暴走谷地 |
| 16804 | The Gorging Pit | La fosse de Gloutonnerie | Die Schlemmergrube | El Foso Engullidor | El Foso Voraz | O Poço Devorador | Зияющее чрево | Fossa Insaziabile | 폭식 구덩이 | 贪婪深坑 | 吞食地穴 |
| 16825 | Devouring Stronghold | Bastion de la Dévoration | Die Verschlingende Feste | Bastión de la Devoración | Fortaleza Devoradora | Baluarte Devorador | Пожирающая крепость | Fortezza Divorante | 포식의 요새 | 吞噬据点 | 吞噬城塞 |
| 16826 | Behemoth's Rise | Cime du Béhémoth | Die Anhöhe des Ungetüms | Alto del Behemoth | Alto de Behemoth | Ascensão de Beemote | Подъем Исполина | Altura del Behemoth | 거수의 단상 | 巨兽崛起 | 巨獸高地 |
| 16827 | The Riftlabs | Les laboratoires de la Faille | Die Risslabore | Laboratorios de Falla | Los Laboratorios de la Falla | Os Fissuratórios | Глубинные лаборатории | Laboratori della Fenditura | 균열 실험실 | 裂隙实验室 | 裂隙實驗區 |
| 16828 | Crown of the Cosmos | Couronne du Cosmos | Die Krone des Kosmos | Corona del Cosmos | Corona del Cosmos | Coroa do Cosmos | Корона космоса | Corona del Cosmo | 우주의 왕관 | 宇宙之冕 | 宇宙之冠 |
| 16829 | The Approach | Les Abords | Der Zugang | La Vereda | El Acercamiento | A Aproximação | Подступ | Soglia | 접근로 | 临影口 | 通道入口 |
| 16844 | Dusk's Repose | Repos du Crépuscule | Zur Abenddämmerung | Reposo del Anochecer | Reposo del Ocaso | Repouso do Crepúsculo | Покой Заката | Riposo del Vespro | 어스름의 안식처 | 黄昏憩所 | 黃昏之憩 |
| 16850 | Retribution Hold | Bastion de la Vindicte | Festung der Vergeltung | Bastión de la Reprensión | Fuerte de Reprensión | Forte da Retribuição | Форт воздаяния | Forte Castigo | 응보의 요새 | 惩戒要塞 | 懲戒要塞 |
| 16851 | Mettle's Hold | Bastion du Courage | Festung des Eifers | Bastión del Temple | Fuerte del Temple | Forte da Bravura | Форт бесстрашия | Forte Ardore | 기개의 요새 | 斗勇要塞 | 精神要塞 |
| 16855 | Voidscar Arena | Arène de la Cicatrice du Vide | Arena der Leerennarbe | Arena Lacravacua | Arena Rajavacío | Arena da Chaga do Caos | Арена Шрама Бездны | Arena Sfregiavuoto | 공허흉터 투기장 | 虚空之痕竞技场 | 虛無之痕競技場 |
| 16863 | Quiet Cavern | Caverne Paisible | Die Stille Höhle | Caverna de la Quietud | Caverna Tranquila | Caverna Silenciosa | Тихая пещера | Grotta Silenziosa | 고요한 동굴 | 宁静洞穴 | 寂靜洞穴 |
| 16864 | Consumptor Cave | Grotte du Gavodon | Die Vertilgerhöhle | Cueva del Consumidor | Cueva del Consumidor | Caverna do Empanturrador | Пещера ненасытника | Grotta dei Consumanti | 탐식충 동굴 | 吞噬虫洞穴 | 吞食蟲洞穴 |

### A.2 Netherstorm

| AreaID | enUS | frFR | deDE | esES | esMX | ptBR | ruRU | itIT | koKR | zhCN | zhTW |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3523 | Netherstorm | Raz-de-Néant | Nethersturm | Tormenta Abisal | Tormenta Abisal | Eternévoa | Пустоверть | Landa Fatua | 황천의 폭풍 | 虚空风暴 | 虛空風暴 |
| 3712 | Area 52 | Zone 52 | Area 52 | Área 52 | Área 52 | Área 52 | Зона 52 | Area 52 | 52번 구역 | 52区 | 52區 |
| 3721 | The Crumbling Waste | La Désagrégation | Die Schwindende Weite | Las Ruinas Desmoronadas | Las Ruinas Desmoronadas | Ermo Esfacelado | Гиблый пустырь | Terre Disgregate | 부서진 잔해 | 碎裂废土 | 破碎荒地 |
| 3722 | Manaforge Ara | Manaforge Ara | Manaschmiede Ara | Forja de Maná Ara | Forja de Maná Ara | Manaforja Ara | Манагорн Ара | Manaforgia Ara | 아라 마나괴철로 | 法力熔炉：艾拉 | 法力熔爐艾拉 |
| 3723 | Arklon Ruins | Ruines Arklon | Ruinen von Arklon | Ruinas Arklon | Ruinas Arklon | Ruínas Arklon | Руины Арклон | Rovine di Arklon | 알클론 폐허 | 阿尔科隆废墟 | 阿克隆廢墟 |
| 3724 | Cosmowrench | Cosmovrille | Kosmozang | Cosmotirón | Cosmotirón | Chave do Cosmos | Космоворот | Kosmika | 비틀린 우주 | 扳钳镇 | 扭曲太空 |
| 3725 | Ruins of Enkaat | Ruines d’Enkaat | Ruinen von Enkaat | Ruinas de Enkaat | Ruinas de Enkaat | Ruínas de Enkaat | Руины Энкаата | Rovine di Enkaat | 엔카트 폐허 | 恩卡特废墟 | 安卡特廢墟 |
| 3726 | Manaforge B'naar | Manaforge B’naar | Manaschmiede B'naar | Forja de Maná B'naar | Forja de Maná B'naar | Manaforja B'naar | Манагорн Б'наар | Manaforgia B'naar | 브나르 마나괴철로 | 法力熔炉：布纳尔 | 法力熔爐巴納爾 |
| 3727 | The Scrap Field | La Ferraille | Das Trümmerfeld | El Campo de Sobras | El Campo de Sobras | Campo dos Refugos | Захламленное поле | Campo dei Rottami | 고철 지대 | 废料之地 | 廢棄農場 |
| 3728 | The Vortex Fields | Les champs du vortex | Die Vortexfelder | Los Campos del Vórtice | Los Campos del Vórtice | Campos de Vórtice | Вихревые поля | Campi del Vortice | 소용돌이 지대 | 漩涡平原 | 漩渦農場 |
| 3729 | The Heap | Le Monceau | Der Hügel | La Pila | La Pila | Os Destroços | Груда | Cumulo di Rottami | 고철더미 | 机甲废场 | 聚集之地 |
| 3730 | Manaforge Coruu | Manaforge Coruu | Manaschmiede Coruu | Forja de Maná Coruu | Forja de Maná Coruu | Manaforja Coruu | Манагорн Коруу | Manaforgia Coruu | 코루 마나괴철로 | 法力熔炉：库鲁恩 | 法力熔爐寇魯 |
| 3731 | The Tempest Rift | La faille des Tempêtes | Kluft der Stürme | La Falla de la Tempestad | La Falla de la Tempestad | Fenda Tempestuosa | Пояс Бурь | Faglia delle Tempeste | 폭풍우 균열 | 风暴裂隙 | 風暴裂口 |
| 3732 | Kirin'Var Village | Kirin’Var | Kirin'Var | Poblado Kirin'Var | Poblado Kirin'Var | Vila Kirin'Var | Деревня Кирин'Вар | Kirin'Var | 키린바르 마을 | 肯瑞瓦村 | 肯瑞瓦村莊 |
| 3733 | The Violet Tower | La tour Pourpre | Der Violette Turm | Torre Violeta | Torre Violeta | Torre Violeta | Аметистовая башня | Torre Violacea | 보랏빛 탑 | 紫罗兰之塔 | 紫羅蘭之塔 |
| 3734 | Manaforge Duro | Manaforge Duro | Manaschmiede Duro | Forja de Maná Duro | Forja de Maná Duro | Manaforja Dúria | Манагорн Даро | Manaforgia Duro | 듀로 마나괴철로 | 法力熔炉：杜隆 | 法力熔爐杜羅 |
| 3735 | Voidwind Plateau | Le plateau Vent-du-Vide | Leerenwindplateau | Meseta del Viento del Vacío | Meseta del Viento del Vacío | Platô dos Ventos do Caos | Плато Пустынного Ветра | Tavolato di Ventovacuo | 공허의 바람 고원 | 虚风高原 | 裂風高原 |
| 3736 | Manaforge Ultris | Manaforge Ultris | Manaschmiede Ultris | Forja de Maná Ultris | Forja de Maná Ultris | Manaforja Ultris | Манагорн Ультрис | Manaforgia Ultris | 울트리스 마나괴철로 | 法力熔炉：乌提斯 | 法力熔爐奧崔斯 |
| 3737 | Celestial Ridge | Crête Céleste | Sternensturz | Cresta Celestial | Cresta Celestial | Pico Celestial | Небесная гряда | Cresta Celeste | 하늘 마루 | 苍穹之脊 | 天國山脈 |
| 3738 | The Stormspire | La Foudreflèche | Die Sturmsäule | Flecha de la Tormenta | La Flecha de la Tormenta | Pináculo da Tempestade | Штормовая Вершина | Guglia Tempestosa | 폭풍 첨탑 | 风暴尖塔 | 風暴之尖 |
| 3739 | Forge Base: Oblivion | Base de forge : Oubli | Konstruktionsbasis: Vergessenheit | Base Forja: Olvido | Base Forja: Olvido | Base-forja: Oblívio | База Легиона: Забвение | Fornace Oblio | 망각의 괴철로 주둔지 | 铸魔基地：湮灭 | 熔爐基地:遺忘 |
| 3740 | Forge Base: Gehenna | Base de forge : Géhenne | Konstruktionsbasis: Gehenna | Base Forja: Gehenna | Base Forja: Gehenna | Base-forja: Geena | База Легиона: Геенна | Fornace Gehenna | 지옥의 괴철로 주둔지 | 铸魔基地：炼狱 | 熔爐基地:苦難 |
| 3741 | Ruins of Farahlon | Ruines de Farahlon | Ruinen von Farahlon | Ruinas de Farahlon | Ruinas de Farahlon | Ruínas de Farahlon | Руины Фаралона | Rovine di Farahlon | 파랄론 폐허 | 法兰伦废墟 | 法拉隆廢墟 |
| 3742 | Socrethar's Seat | Siège de Socrethar | Socrethars Sitz | Trono de Socrethar | Trono de Socrethar | Trono de Socrethar | Трон Сокретара | Trono di Socrethar | 소크레타르의 옥좌 | 索克雷萨之座 | 索奎薩爾的領地 |
| 3837 | Sunfury Hold | Bastion des Solfurie | Sonnenzornposten | Bastión Furia del Sol | Bastión Furia del Sol | Acampamento Solfúria | Форт Ярости Солнца | Presidio dei Furia del Sole | 성난태양 주둔지 | 日怒堡 | 日怒要塞 |
| 3842 | Tempest Keep | Donjon de la Tempête | Festung der Stürme | El Castillo de la Tempestad | El Castillo de la Tempestad | Bastilha da Tormenta | Крепость Бурь | Forte Tempesta | 폭풍우 요새 | 风暴要塞 | 風暴要塞 |
| 3850 | Netherstone | Pierre-de-Néant | Netherstein | Piedra Abisal | Piedra Abisal | Pedra Etérea | Осколки Пустоты | Pietrafatua | 황천의 돌무지 | 虚空石 | 虛空石 |
| 3851 | Midrealm Post | Comptoir des Terres-médianes | Mittelreichposten | Puesto de la Tierra Media | Puesto de la Tierra Media | Posto Terramédia | Застава срединных земель | Accampamento di Mezzoregno | 중앙 생태지구 주둔지 | 中央圆顶哨站 | 領地崗哨 |
| 3852 | Tuluman's Landing | Point d’ancrage de Tuluman | Tulumans Landeplatz | Alto de Tuluman | Alto de Tuluman | Acampamento do Tuluman | Лагерь Тулумана | Approdo di Tuluman | 툴루만의 교역지 | 图鲁曼的营地 | 吐魯曼平臺 |
| 3854 | Protectorate Watch Post | Poste de garde du Protectorat | Wachposten des Protektorats | Avanzada del Protectorado | Avanzada del Protectorado | Posto de Guarda do Protetorado | Застава Стражей Протектората | Presidio del Protettorato | 자유연합 경비초소 | 维序派哨站 | 護國者哨站 |
| 3868 | Gyro-Plank Bridge | Pont de Gyro-passerelles | Gyroplankenbrücke | Puente Girolámina | Puente Girolámina | Ponte Giroprancha | Гиро-балочный мост | Ponte Giromatico | 자이로 교각 | 机械桥 | 環木橋 |
| 3873 | The Proving Grounds | Le terrain d’Essai | Die Versuchsgründe | El Terreno de Pruebas | El Terreno de Pruebas | Campo de Testes | Испытательный полигон | Piana del Conflitto | 수련의 장 | 实验场 | 試煉場 |
| 3874 | Eco-Dome Farfield | Écodôme Champlointain | Biokuppel Fernfeld | Ecodomo Campolejano | Ecodomo Campolejano | Eco-domo Campolonge | Заповедник "Дальнее поле" | Ecosfera Camporemoto | 외곽 생태지구 | 边缘生态圆顶 | 秘境原野 |
| 3875 | Eco-Dome Skyperch | Écodôme Percheciel | Biokuppel Himmelssitz | Ecodomo Altocielo | Ecodomo Altocielo | Eco-domo Pouso do Céu | Заповедник "Высь" | Ecosfera Sottocielo | 하늘마루 생태지구 | 高空生态圆顶 | 秘境棲木 |
| 3876 | Eco-Dome Sutheron | Écodôme Sudron | Biokuppel Sutheron | Ecodomo Sutheron | Ecodomo Sutheron | Eco-domo Sutheron | Заповедник "Сатерон" | Ecosfera Sopravento | 수데론 생태지구 | 苏瑟伦生态圆顶 | 桑什倫秘境 |
| 3877 | Eco-Dome Midrealm | Écodôme Terres-Médianes | Biokuppel Mittelreich | Ecodomo de la Tierra Media | Ecodomo de la Tierra Media | Eco-domo Terramédia | Заповедник "Срединные земли" | Ecosfera Mezzoregno | 중앙 생태지구 | 中央生态圆顶 | 秘境領地 |
| 3878 | Ethereum Staging Grounds | Lieu de rassemblement de l’Ethereum | Stützpunkt des Astraleums | Punto de Escala de El Etereum | Punto de Escala de El Etereum | Bivaques do Eteréum | Испытательный полигон Эфириума | Campo Base degli Etereum | 에테리움 작전 지역 | 复仇军前沿基地 | 以太皇族軍事要塞 |
| 3879 | Chapel Yard | Cour de la Chapelle | Kapellenhof | Patio de la Capilla | Patio de la Capilla | Pátio da Capela | Церковный двор | Chiostro della Cappella | 예배당 지구 | 礼拜堂广场 | 教堂庭院 |
| 3880 | Access Shaft Zeon | Puits d’accès Zéon | Zugangsschacht Zeon | Eje de Acceso Zeon | Eje de Acceso Zeon | Poço de Acesso Zeon | Вход в шахту Зеон | Pozzo d'Accesso Zeon | 지온 작업 갱도 | 瑟安竖井 | 礦井之路通道 |
| 3881 | Trelleum Mine | Mine de Trelleum | Trelleummine | Mina Trelleum | Mina Trelleum | Mina Trelleum | Рудник Треллеума | Miniera di Trelleum | 트렐리움 광산 | 特雷卢姆矿井 | 崔爾曼礦坑 |
| 3882 | Invasion Point: Destroyer | Site d’invasion : Destructeur | Invasionspunkt: Zerstörer | Punto de Invasión: Destructor | Punto de Invasión: Destructor | Ponto de Invasão: Destruidor | Точка вторжения: Разрушение | Portale di Invasione: Distruzione | 파괴자의 침공 거점 | 登陆场：破坏 | 侵略點：摧毀者 |
| 3883 | Camp of Boom | Camp de Boum | Lager von Dr. Bumm | Campamento de Bum | Campamento de Bum | Acampamento do Dr. Cabum | Лагерь Бума | Accampamento di Boom | 붐의 야영지 | 砰砰博士的营地 | 爆爆營地 |
| 3900 | Invasion Point: Overlord | Site d’invasion : Suzerain | Invasionspunkt: Oberanführer | Punto de Invasión: Señor Supremo | Punto de Invasión: Señor Supremo | Ponto de Invasão: Lorde supremo | Точка вторжения: Властитель | Portale di Invasione: Angoscia | 대군주의 침공 거점 | 登陆场：霸王 | 侵略點：主宰者 |
| 3921 | Arklonis Ridge | Crête d’Arklonis | Arklonisgrat | Cresta Arklonis | Cresta Arklonis | Pico Arklonis | Гряда Арклонис | Cresta di Arklonis | 아클로니스 마루 | 阿尔科隆山脉 | 阿卡隆斯山脊 |
| 3934 | Town Square | Place Centrale | Ratsplatz | Plaza de la Ciudad | Plaza de la Ciudad | Praça da Cidade | Городская площадь | Piazza Centrale | 마을 광장 | 城镇广场 | 小鎮廣場 |
| 3935 | Wizard Row | Allée des Sorciers | Zaubergasse | Pasaje del Zahorí | Pasaje del Zahorí | Estreito do Teurgo | Путь Волшебника | Rione dei Maghi | 마법사 지구 | 巫师街 | 巫師街 |
| 5554 | Tempest Keep - The Mechanar Entrance | Donjon de la Tempête - Entrée du Méchanar | Festung der Stürme - Eingang zur Mechanar | El Castillo de la Tempestad: Entrada de El Mechanar | El Castillo de la Tempestad: Entrada de El Mechanar | Entrada da Bastilha da Tormenta: Mecanar | Крепость Бурь: Механар | Ingresso a Mecanar di Forte Tempesta | 폭풍우 요새 - 메카나르 입구 | 风暴要塞 - 能源舰入口 | 風暴要塞 - 麥克納爾入口 |
| 5555 | Tempest Keep - The Botanica Entrance | Donjon de la Tempête - Entrée de la Botanica | Festung der Stürme - Eingang zur Botanika | El Castillo de la Tempestad: Entrada de El Invernáculo | El Castillo de la Tempestad: Entrada de El Invernáculo | Entrada da Bastilha da Tormenta: Jardim Botânico | Крепость Бурь: Ботаника | Ingresso a Botanica di Forte Tempesta | 폭풍우 요새 - 신록의 정원 입구 | 风暴要塞 - 生态船入口 | 風暴要塞 - 波塔尼卡入口 |
| 5556 | Tempest Keep - The Arcatraz Entrance | Donjon de la Tempête - Entrée de l’Arcatraz | Festung der Stürme - Eingang zur Arkatraz | El Castillo de la Tempestad: Entrada de El Arcatraz | El Castillo de la Tempestad: Entrada de El Arcatraz | Entrada da Bastilha da Tormenta: Arcatraz | Крепость Бурь: Аркатрац | Ingresso ad Arcatraz di Forte Tempesta | 폭풍우 요새 - 알카트라즈 입구 | 风暴要塞 - 禁魔监狱入口 | 風暴要塞 - 亞克崔茲入口 |
| 8613 | Rusty Rocket Tavern | Taverne de la Fusée rouillée | Taverne "Zur Rostigen Rakete" | Taberna El Cohete Oxidado | Taberna Cohete oxidado | Taberna do Foguete Enferrujado | Таверна "Ржавая ракета" | Taverna Vecchio Razzo | 녹슨 로켓 선술집 | 生锈火箭旅店 | 鏽蝕火箭旅店 |

## Annexe B — kits natifs de Voidstorm, fichier par fichier

- **ZoneMusic 3286** « Zone 12.0 - Voidstorm - Fields - General - Walk » (pauses 180–300 s) — 15458 Voidstorm
  - 7690563 `MUS_120_Storm_Fields_A`
  - 7690567 `MUS_120_Storm_Fields_C`
  - 7690569 `MUS_120_Storm_Fields_D`
  - 7690575 `MUS_120_Storm_Fields_G`
  - 7690577 `MUS_120_Storm_Fields_H`
  - 7696434 `MUS_120_Gnawing_Reach_B`
  - 7703718 `MUS_120_Gnawing_Reach_D`
- **ZoneMusic 3272** « Zone 12.0 - Voidstorm - Hub - Void Elf - Walk » (pauses 180–300 s) — 15949 The Ingress, 15950 Locus Point
  - 7684188 `MUS_120_Locus_Point_A`
  - 7684190 `MUS_120_Locus_Point_B`
  - 7684192 `MUS_120_Locus_Point_C`
  - 7684194 `MUS_120_Locus_Point_D`
  - 7684196 `MUS_120_Locus_Point_E`
  - 7684198 `MUS_120_Locus_Point_H`
  - 7692212 `MUS_120_Voidstorm_B`
  - 7713420 `MUS_120_Locus_Point_F`
- **ZoneMusic 3242** « Zone 12.0 - Voidstorm - Hub - Howling Ridge - Walk » (pauses 180–300 s) — 15951 The Howling Ridge
  - 7681076 `MUS_120_Howling_Ridge_A`
  - 7681078 `MUS_120_Howling_Ridge_B`
  - 7681080 `MUS_120_Howling_Ridge_C`
  - 7681082 `MUS_120_Howling_Ridge_D`
  - 7681084 `MUS_120_Howling_Ridge_E`
  - 7681086 `MUS_120_Howling_Ridge_H`
- **ZoneMusic 3507** « Zone 12.0 - Voidstorm - Antius - General - Walk » (pauses 180–300 s) — 15952 Nexus-Point Antius
  - 7681054 `MUS_120_Devouring_Host_A`
  - 7681056 `MUS_120_Devouring_Host_B`
  - 7681058 `MUS_120_Devouring_Host_C`
  - 7692214 `MUS_120_Voidstorm_C`
  - 7692216 `MUS_120_Voidstorm_D`
  - 7703708 `MUS_120_Devouring_Host_F`
  - 7703710 `MUS_120_Devouring_Host_G`
  - 7713464 `MUS_120_Voidstorm_F`
- **ZoneMusic 3241** « Zone 12.0 - Voidstorm - Shadowguard - General - Walk » (pauses 180–300 s) — 15953 Shadowguard Point, 15967 Ethereum Overcroft, 16218 Shenzar Refinery
  - 7681154 `MUS_120_Shadowguard_Void_A`
  - 7681156 `MUS_120_Shadowguard_Void_B`
  - 7681158 `MUS_120_Shadowguard_Void_C`
  - 7681160 `MUS_120_Shadowguard_Void_D`
  - 7681162 `MUS_120_Shadowguard_Void_H`
- **ZoneMusic 3388** « Zone 12.0 - Voidstorm - Xenas - General - Walk » (pauses 180–300 s) — 15954 Nexus-Point Xenas
  - 7681060 `MUS_120_Devouring_Host_D`
  - 7681062 `MUS_120_Devouring_Host_E`
  - 7692216 `MUS_120_Voidstorm_D`
  - 7703712 `MUS_120_Devouring_Host_I`
- **ZoneMusic 3509** « Zone 12.0 - Voidstorm - Mid'Ar - General - Walk » (pauses 180–300 s) — 15955 Nexus-Point Mid'Ar
  - 7681064 `MUS_120_Devouring_Host_H`
  - 7681156 `MUS_120_Shadowguard_Void_B`
  - 7681158 `MUS_120_Shadowguard_Void_C`
  - 7690571 `MUS_120_Storm_Fields_E`
  - 7703712 `MUS_120_Devouring_Host_I`
  - 7713464 `MUS_120_Voidstorm_F`
- **ZoneMusic 3240** « Zone 12.0 - Voidstorm - Devrouing Host - General - Walk » (pauses 180–300 s) — 15956 Stormarion Keep, 15973 Voidscar Arena, 16486 Stormarion Watch, 16855 Voidscar Arena
  - 7681060 `MUS_120_Devouring_Host_D`
  - 7681062 `MUS_120_Devouring_Host_E`
  - 7681064 `MUS_120_Devouring_Host_H`
  - 7703712 `MUS_120_Devouring_Host_I`
- **ZoneMusic 3385** « Zone 12.0 - Voidstorm - Obscurion Citadel - General - Walk » (pauses 180–300 s) — 15957 Obscurion Citadel
  - 7681056 `MUS_120_Devouring_Host_B`
  - 7681058 `MUS_120_Devouring_Host_C`
  - 7690565 `MUS_120_Storm_Fields_B`
  - 7691963 `MUS_120_Slayers_Rise_B`
  - 7692210 `MUS_120_Voidstorm_A`
  - 7692214 `MUS_120_Voidstorm_C`
  - 7692216 `MUS_120_Voidstorm_D`
  - 7692218 `MUS_120_Voidstorm_E`
  - 7703708 `MUS_120_Devouring_Host_F`
  - 7703710 `MUS_120_Devouring_Host_G`
  - 7713464 `MUS_120_Voidstorm_F`
- **ZoneMusic 3310** « Zone 12.0 - Voidstorm - Slayer's Rise - General - Walk » (pauses 180–300 s) — 15959 Slayer's Rise
  - 7690565 `MUS_120_Storm_Fields_B`
  - 7690571 `MUS_120_Storm_Fields_E`
  - 7690573 `MUS_120_Storm_Fields_F`
  - 7690579 `MUS_120_Storm_Fields_I`
  - 7703712 `MUS_120_Devouring_Host_I`
  - 7703714 `MUS_120_Devouring_Host_J`
  - 7703716 `MUS_120_Devouring_Host_K`
- **ZoneMusic 3291** « Zone 12.0 - Voidstorm - Voidspire - Host - Walk » (pauses 180–300 s) — 15960 The Voidspire, 15961 The Approach
  - 7681054 `MUS_120_Devouring_Host_A`
  - 7681058 `MUS_120_Devouring_Host_C`
  - 7681064 `MUS_120_Devouring_Host_H`
  - 7692214 `MUS_120_Voidstorm_C`
  - 7692216 `MUS_120_Voidstorm_D`
  - 7703708 `MUS_120_Devouring_Host_F`
  - 7703710 `MUS_120_Devouring_Host_G`
  - 7703712 `MUS_120_Devouring_Host_I`
  - 7713464 `MUS_120_Voidstorm_F`
- **ZoneMusic 3508** « Zone 12.0 - Voidstorm - Refinery - General - Walk » (pauses 180–300 s) — 15962 Ethereum Refinery
  - 7681062 `MUS_120_Devouring_Host_E`
  - 7681154 `MUS_120_Shadowguard_Void_A`
  - 7681160 `MUS_120_Shadowguard_Void_D`
  - 7681162 `MUS_120_Shadowguard_Void_H`
- **ZoneMusic 3417** « Zone 12.0 - Voidstorm - The Molt - General - Walk » (pauses 30–45 s) — 15964 The Molt, 16364 Underground Burrows
  - 7714000 `Silent_046_2`
- **ZoneMusic 3512** « Zone 12.0 - Voidstorm - Predaxas - General - Walk » (pauses 180–300 s) — 15966 Den of Predaxas, 16534 Lair of Predaxas
  - 7692210 `MUS_120_Voidstorm_A`
  - 7692218 `MUS_120_Voidstorm_E`
  - 7692220 `MUS_120_Voidstorm_H`
  - 7703714 `MUS_120_Devouring_Host_J`
- **ZoneMusic 3290** « Zone 12.0 - Voidstorm - Slayer's Rise - Grief Spire - Walk » (pauses 180–300 s) — 15970 Grief Spire, 16850 Retribution Hold
  - 7691961 `MUS_120_Slayers_Rise_A`
  - 7691963 `MUS_120_Slayers_Rise_B`
  - 7691965 `MUS_120_Slayers_Rise_C`
  - 7691975 `MUS_120_Slayers_Rise_E`
- **ZoneMusic 3309** « Zone 12.0 - Voidstorm - Slayer's Rise - Hate Spire - Walk » (pauses 180–300 s) — 15971 Hate Spire, 16851 Mettle's Hold
  - 7692210 `MUS_120_Voidstorm_A`
  - 7692214 `MUS_120_Voidstorm_C`
  - 7692216 `MUS_120_Voidstorm_D`
  - 7692218 `MUS_120_Voidstorm_E`
- **ZoneMusic 3511** « Zone 12.0 - Voidstorm - Gorging Pit - General - Walk » (pauses 180–300 s) — 16219 The Husk, 16501 Night Trench, 16804 The Gorging Pit
  - 7696432 `MUS_120_Gnawing_Reach_A`
  - 7696436 `MUS_120_Gnawing_Reach_C`
  - 7696438 `MUS_120_Gnawing_Reach_H`
  - 7703720 `MUS_120_Gnawing_Reach_E`
- **ZoneMusic 3302** « Raid 12.0 - Voidspire - General - Walk » (pauses 180–300 s) — 16340 The Voidspire
  - 7681056 `MUS_120_Devouring_Host_B`
  - 7681060 `MUS_120_Devouring_Host_D`
  - 7681064 `MUS_120_Devouring_Host_H`
  - 7681156 `MUS_120_Shadowguard_Void_B`
  - 7681158 `MUS_120_Shadowguard_Void_C`
  - 7692210 `MUS_120_Voidstorm_A`
  - 7692214 `MUS_120_Voidstorm_C`
  - 7692218 `MUS_120_Voidstorm_E`
- **ZoneMusic 3307** « Zone 12.0 - Voidstorm - Deep Sea - General - Walk » (pauses 150–270 s) — 16341 Gnawing Reach
  - 3931650 `mus_mx_cov_seatoftheprimus_01`
- **ZoneMusic 3447** « PvP 12.0 - Slayer's Rise - General - Walk » (pauses 30–60 s) — 16423 Slayer's Rise
  - 7690557 `MUS_120_Midnight_Battle_D`
  - 7690559 `MUS_120_Midnight_Battle_E`
  - 7690565 `MUS_120_Storm_Fields_B`
  - 7690571 `MUS_120_Storm_Fields_E`
  - 7692198 `MUS_120_Void_Combat_B`
  - 7692218 `MUS_120_Voidstorm_E`
  - 7703708 `MUS_120_Devouring_Host_F`
  - 7703712 `MUS_120_Devouring_Host_I`
  - 7703714 `MUS_120_Devouring_Host_J`
  - 7703716 `MUS_120_Devouring_Host_K`
- **ZoneMusic 3428** « Dungeon 12.0 - Voidscar Arena - Arena - Walk » (pauses 180–300 s) — 16425 Voidscar Arena
  - 7681158 `MUS_120_Shadowguard_Void_C`
  - 7692210 `MUS_120_Voidstorm_A`
  - 7692216 `MUS_120_Voidstorm_D`
  - 7692218 `MUS_120_Voidstorm_E`
  - 7703714 `MUS_120_Devouring_Host_J`
- **ZoneMusic 3455** « Zone 12.0 - Voidstorm - Stormarion Citadel - Walk » (pauses 180–300 s) — 16485 Stormarion Citadel
  - 7684188 `MUS_120_Locus_Point_A`
  - 7684190 `MUS_120_Locus_Point_B`
  - 7684192 `MUS_120_Locus_Point_C`
  - 7684194 `MUS_120_Locus_Point_D`
  - 7684196 `MUS_120_Locus_Point_E`
  - 7692212 `MUS_120_Voidstorm_B`
- **ZoneMusic 3445** « PvP 12.0 - Slayer's Rise - Grief Spire - Walk » (pauses 30–60 s) — 16488 Grief Spire, 16492 Bastion of Valor
  - 3931650 `mus_mx_cov_seatoftheprimus_01`
- **ZoneMusic 3446** « PvP 12.0 - Slayer's Rise - Hate Spire - Walk » (pauses 30–60 s) — 16489 Hate Spire, 16491 Bastion of Might, 16496 Hanaar Outpost
  - 3931650 `mus_mx_cov_seatoftheprimus_01`
- **ZoneMusic 3444** « PvP 12.0 - Slayer's Rise - Shadowguard - Walk » (pauses 30–60 s) — 16494 Shadowridge Outpost, 16495 Stareater Pavilion, 16499 Shenzar Refinery
  - 7681154 `MUS_120_Shadowguard_Void_A`
  - 7681156 `MUS_120_Shadowguard_Void_B`
  - 7681158 `MUS_120_Shadowguard_Void_C`
  - 7681160 `MUS_120_Shadowguard_Void_D`
  - 7681162 `MUS_120_Shadowguard_Void_H`
- **ZoneMusic 3448** « PvP 12.0 - Slayer's Rise - Husk - Walk » (pauses 30–60 s) — 16498 The Husk
  - 7696432 `MUS_120_Gnawing_Reach_A`
  - 7696434 `MUS_120_Gnawing_Reach_B`
  - 7696436 `MUS_120_Gnawing_Reach_C`
  - 7696438 `MUS_120_Gnawing_Reach_H`
  - 7703718 `MUS_120_Gnawing_Reach_D`
  - 7703720 `MUS_120_Gnawing_Reach_E`
- **ZoneMusic 3398** « Raid 12.0 - Voidspire - Boss 6 - Post-Fight » (pauses 180–300 s) — 16507 Isle of Quel'Danas
  - 6042831 `mus_110_alleria_b`
  - 6042833 `mus_110_alleria_a`
- **ZoneMusic 3389** « Dungeon 12.0 - Xenas - Entrance - Walk » (pauses 180–300 s) — 16573 Nexus-Point Xenas
  - 7692214 `MUS_120_Voidstorm_C`
  - 7692216 `MUS_120_Voidstorm_D`
  - 7692218 `MUS_120_Voidstorm_E`
  - 7703716 `MUS_120_Devouring_Host_K`
  - 7703754 `MUS_120_The_Light_F`
  - 7713452 `MUS_120_The_Light_I`
  - 7713464 `MUS_120_Voidstorm_F`
- **ZoneMusic 3289** « Zone 12.0 - Voidstorm - Hub - PvP - Walk » (pauses 180–300 s) — 16649 Masters' Perch
  - 7691971 `MUS_120_Slayers_Rise_D`
  - 7691977 `MUS_120_Slayers_Rise_F`
  - 7691980 `MUS_120_Slayers_Rise_G`
  - 7691982 `MUS_120_Slayers_Rise_H`
  - 7692212 `MUS_120_Voidstorm_B`
- **ZoneMusic 3298** « Raid 12.0 - Voidspire - Behemoth - Walk » (pauses 180–300 s) — 16826 Behemoth's Rise
  - 7692210 `MUS_120_Voidstorm_A`
  - 7692216 `MUS_120_Voidstorm_D`
  - 7692218 `MUS_120_Voidstorm_E`
- **ZoneMusic 3300** « Raid 12.0 - Voidspire - Riftlabs - Walk » (pauses 180–300 s) — 16827 The Riftlabs
  - 7681156 `MUS_120_Shadowguard_Void_B`
  - 7681158 `MUS_120_Shadowguard_Void_C`
  - 7681162 `MUS_120_Shadowguard_Void_H`
- **ZoneMusic 3293** « Raid 12.0 - Voidspire - Entrance - Walk » (pauses 180–300 s) — 16829 The Approach
  - 7681054 `MUS_120_Devouring_Host_A`
  - 7681056 `MUS_120_Devouring_Host_B`
  - 7681058 `MUS_120_Devouring_Host_C`

