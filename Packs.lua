local _, ns = ...
local T = ns.Tracks
local api = _G.EchoesOfAzeroth
local Dsl = api and api.PluginDsl
if not Dsl then
    error("EchoesOfAzeroth core must load before EchoesOfAzeroth_Voidstorm")
end

local Pack = Dsl.pack
local MixedPack = Dsl.mixedPack
local Merge = Dsl.mergeUnique

-- ============================================================
-- Music Packs
--
-- Every pack exists in two flavours:
--   (TBC)             Netherstorm / Outland music only
--   (TBC + Midnight)  the TBC pack merged with the Midnight kit the
--                     game natively plays in the matching Voidstorm
--                     sub-areas
--
-- No pure Midnight packs are shipped on purpose: the native music is
-- what the player already hears with the addon disabled.  Users who
-- want a native-only pack can build one from the Midnight tracks in
-- the core UI.
--
-- The TBC "intro" tracks mirror Netherstorm's own design: the zone
-- has a single walking set and signs each sub-area with a one-shot
-- intro (manaforges, Legion bases, crystal fields, goblin towns).
-- ============================================================

-- ------------------------------------------------------------
-- TBC track groups
-- ------------------------------------------------------------

local NS_GENERAL = {
    T.NS_GeneralWalkUni01,
    T.NS_GeneralWalkUni02,
    T.NS_GeneralWalkUni03,
    T.NS_GeneralWalkUni04,
    T.NS_GeneralWalkUni05,
    T.NS_GeneralWalkUni06,
    T.NS_GeneralWalkUni07,
    T.NS_GeneralWalkUni08,
    T.NS_GeneralWalkUni09,
    T.NS_GeneralWalkUni10,
}

local TK_AMBIENT = {
    T.TK_TempestKeepAMB11,
    T.TK_TempestKeepAMB12,
    T.TK_TempestKeepAMB13,
    T.TK_TempestKeepAMB14,
    T.TK_TempestKeepAMB16,
    T.TK_TempestKeepAMB17,
    T.TK_TempestKeepAMB18,
    T.TK_TempestKeepAMB19,
    T.TK_TempestKeepAMB20,
    T.TK_TempestKeepAMB22,
    T.TK_TempestKeepAMB23,
}

local TK_BATTLE = {
    T.TK_TempestKeepBTL10,
    T.TK_TempestKeepBTL11,
    T.TK_TempestKeepBTL13,
}

local OL_CORRUPT = {
    T.OL_Corrupt01,
    T.OL_Corrupt02,
    T.OL_Corrupt03,
    T.OL_Corrupt04,
    T.OL_Corrupt05,
    T.OL_Corrupt06,
    T.OL_Corrupt07,
}

-- ------------------------------------------------------------
-- Midnight native kits (mixed packs only, never exposed alone)
-- ------------------------------------------------------------

local MN_FIELDS = {          -- zone root, Storm Fields (ZoneMusic 3286)
    T.MN_StormFieldsA, T.MN_StormFieldsB, T.MN_StormFieldsC,
    T.MN_StormFieldsD, T.MN_StormFieldsE, T.MN_StormFieldsF,
    T.MN_StormFieldsG, T.MN_StormFieldsH, T.MN_StormFieldsI,
    T.MN_GnawingReachB, T.MN_GnawingReachD,
}

local MN_SINGULARITY = {     -- The Ingress, Locus Point (3272) + Howling Ridge (3242)
    T.MN_LocusPointA, T.MN_LocusPointB, T.MN_LocusPointC, T.MN_LocusPointD,
    T.MN_LocusPointE, T.MN_LocusPointF, T.MN_LocusPointH, T.MN_VoidstormB,
    T.MN_HowlingRidgeA, T.MN_HowlingRidgeB, T.MN_HowlingRidgeC,
    T.MN_HowlingRidgeD, T.MN_HowlingRidgeE, T.MN_HowlingRidgeH,
}

local MN_NEXUS = {           -- Nexus-Points Antius / Xenas / Mid'Ar (3507, 3388, 3509)
    T.MN_DevouringHostA, T.MN_DevouringHostB, T.MN_DevouringHostC,
    T.MN_DevouringHostD, T.MN_DevouringHostE, T.MN_DevouringHostF,
    T.MN_DevouringHostG, T.MN_DevouringHostH, T.MN_DevouringHostI,
    T.MN_VoidstormC, T.MN_VoidstormD, T.MN_VoidstormF,
}

local MN_SHADOWGUARD = {     -- Shadowguard Point, Ethereum Refinery / Overcroft, Shenzar Refinery (3241, 3508)
    T.MN_ShadowguardVoidA, T.MN_ShadowguardVoidB, T.MN_ShadowguardVoidC,
    T.MN_ShadowguardVoidD, T.MN_ShadowguardVoidH,
}

local MN_HOST = {            -- Stormarion Keep / Watch (3240) + Obscurion Citadel (3385)
    T.MN_DevouringHostD, T.MN_DevouringHostE, T.MN_DevouringHostH, T.MN_DevouringHostI,
    T.MN_VoidstormA, T.MN_VoidstormC, T.MN_VoidstormD, T.MN_VoidstormE,
}

local MN_STORMARION_CITADEL = { -- Stormarion Citadel after the assault (3455)
    T.MN_LocusPointA, T.MN_LocusPointB, T.MN_LocusPointC,
    T.MN_LocusPointD, T.MN_LocusPointE, T.MN_VoidstormB,
}

local MN_VOIDSPIRE = {       -- The Voidspire, The Approach (3291)
    T.MN_DevouringHostA, T.MN_DevouringHostC, T.MN_DevouringHostF,
    T.MN_DevouringHostG, T.MN_DevouringHostH, T.MN_DevouringHostI,
    T.MN_VoidstormC, T.MN_VoidstormD, T.MN_VoidstormF,
}

local MN_ARENA = {           -- Voidscar Arena dungeon kit (3428)
    T.MN_ShadowguardVoidC, T.MN_VoidstormA, T.MN_VoidstormD,
    T.MN_VoidstormE, T.MN_DevouringHostJ,
}

local MN_GORGING_PIT = {     -- Night Trench, The Gorging Pit, The Husk (3511)
    T.MN_GnawingReachA, T.MN_GnawingReachC, T.MN_GnawingReachE, T.MN_GnawingReachH,
}

local MN_PREDAXAS = {        -- Den / Lair of Predaxas (3512)
    T.MN_VoidstormA, T.MN_VoidstormE, T.MN_VoidstormH, T.MN_DevouringHostJ,
}

local MN_SLAYERS_RISE = {    -- Slayer's Rise root (3310) + Masters' Perch (3289)
    T.MN_StormFieldsB, T.MN_StormFieldsE, T.MN_StormFieldsF, T.MN_StormFieldsI,
    T.MN_DevouringHostI, T.MN_DevouringHostJ, T.MN_DevouringHostK,
    T.MN_SlayersRiseD, T.MN_SlayersRiseF, T.MN_SlayersRiseG, T.MN_SlayersRiseH,
    T.MN_VoidstormB,
}

local MN_GRIEF_SPIRE = {     -- Grief Spire, Retribution Hold (3290)
    T.MN_SlayersRiseA, T.MN_SlayersRiseB, T.MN_SlayersRiseC, T.MN_SlayersRiseE,
}

local MN_HATE_SPIRE = {      -- Hate Spire, Mettle's Hold (3309)
    T.MN_VoidstormA, T.MN_VoidstormC, T.MN_VoidstormD, T.MN_VoidstormE,
}

-- ------------------------------------------------------------
-- TBC packs
-- ------------------------------------------------------------

-- Zone backbone: the ten Netherstorm walking pieces.
local NETHERSTORM = Pack {
    label = "Netherstorm (TBC)",
    any = NS_GENERAL,
}

-- Neutral hubs (Area 52 / Cosmowrench signature intro).
local AREA52 = Pack {
    label = "Area 52 (TBC)",
    intro = T.OL_HistoricIntroUni01,
    any = NS_GENERAL,
}

-- Nexus-Points <-> manaforges: the Netherplant intros are the
-- manaforges' own signatures in TBC.
local MANAFORGE = Pack {
    label = "Manaforge (TBC)",
    intro = T.NS_NetherplantIntroUni01,
    any = Merge({
        T.NS_NetherplantIntroUni02,
        T.NS_NetherplantIntroUni03,
        T.NS_NetherplantIntroUni04,
    }, NS_GENERAL),
}

-- Ethereum ethereals <-> Auchindoun / Mana-Tombs set, with the intro
-- of the Stormspire (the ethereal headquarters of Netherstorm).
local ETHEREUM = Pack {
    label = "Ethereum (TBC)",
    intro = T.OL_ScenicIntroUni01,
    any = {
        T.TF_AuchindounWalkUni01,
        T.TF_AuchindounWalkUni02,
        T.TF_AuchindounWalkUni03,
    },
}

-- Devouring Host fortresses <-> Burning Legion forge bases.
local FORGE_BASE = Pack {
    label = "Forge Base (TBC)",
    intro = T.OL_BurningLegionIntroUni02,
    any = Merge(OL_CORRUPT, { T.OL_CorruptIntro, T.OL_BurningLegionIntroUni01 }),
}

-- Elven military hold (Stormarion Citadel once the ren'dorei take it).
local SUNFURY = Pack {
    label = "Sunfury Hold (TBC)",
    any = {
        T.GL_Forest3WalkNight01,
        T.GL_Forest3WalkNight02,
        T.GL_Forest3WalkNight03,
        T.OL_BloodElfBaseWalkUni01,
        T.OL_BloodElfBaseWalkUni02,
    },
}

-- Seat of the zone's master: Voidspire <-> Tempest Keep.
local TEMPEST_KEEP = Pack {
    label = "Tempest Keep (TBC)",
    intro = T.TK_TempestKeepSTG14,
    any = TK_AMBIENT,
}

local TEMPEST_KEEP_BATTLE = Pack {
    label = "Tempest Keep Battle (TBC)",
    intro = T.TK_TempestKeepSTG15,
    any = TK_BATTLE,
}

-- Organic ground (the kaiju's shed skin, burrows) <-> mushroom intros.
local MOLT = Pack {
    label = "The Molt (TBC)",
    intro = T.NS_MushroomIntroUni01,
    any = Merge({
        T.NS_MushroomIntroUni02,
        T.NS_MushroomIntroUni03,
    }, NS_GENERAL),
}

-- Predacea's fauna dens <-> Celestial Ridge crystal fields.
local WILDS = Pack {
    label = "Celestial Ridge (TBC)",
    intro = T.OL_CrystalIntroUni03,
    any = NS_GENERAL,
}

-- Slayer's Rise <-> Eye of the Storm, the battleground of Netherstorm
-- (this is Blizzard's own kit for the BG: ZoneMusic 2234).
local EYE_OF_THE_STORM = Pack {
    label = "Eye of the Storm (TBC)",
    intro = T.OL_HistoricIntroUni01,
    any = {
        T.NS_GeneralWalkUni01,
        T.NS_GeneralWalkUni03,
        T.NS_GeneralWalkUni08,
        T.TK_TempestKeepAMB11,
        T.TK_TempestKeepAMB13,
        T.TK_TempestKeepAMB18,
        T.TK_TempestKeepBTL13,
    },
}

local OUTLAND_ALLIANCE = Pack {
    label = "Honor Hold (TBC)",
    any = {
        T.OL_AllianceBaseWalkUni01,
        T.OL_AllianceBaseWalkUni02,
    },
}

local OUTLAND_HORDE = Pack {
    label = "Thrallmar (TBC)",
    any = {
        T.OL_HordeBaseWalkUni03,
        T.OL_HordeBaseWalkUni04,
    },
}

-- Exiles' Hovel (draenei and Broken exiles) <-> Ruins of Enkaat.
local ENKAAT = Pack {
    label = "Ruins of Enkaat (TBC)",
    intro = T.OL_ActionWalkUni01,
    any = {
        T.OL_DraeneiBaseWalkUni01,
        T.OL_DraeneiBaseWalkUni02r,
    },
}

-- ------------------------------------------------------------
-- Mixed packs (TBC + the Midnight kit native to the same places)
-- ------------------------------------------------------------

local function Midnight(label, tracks)
    return Pack { label = label, any = tracks }
end

local NETHERSTORM_MIXED = MixedPack("Netherstorm (TBC + Midnight)", NETHERSTORM, Midnight("Voidstorm (Midnight)", MN_FIELDS))
local AREA52_MIXED = MixedPack("Area 52 (TBC + Midnight)", AREA52, Midnight("Locus Point (Midnight)", MN_SINGULARITY))
local MANAFORGE_MIXED = MixedPack("Manaforge (TBC + Midnight)", MANAFORGE, Midnight("Nexus-Point (Midnight)", MN_NEXUS))
local ETHEREUM_MIXED = MixedPack("Ethereum (TBC + Midnight)", ETHEREUM, Midnight("Shadowguard (Midnight)", MN_SHADOWGUARD))
local FORGE_BASE_MIXED = MixedPack("Forge Base (TBC + Midnight)", FORGE_BASE, Midnight("Devouring Host (Midnight)", MN_HOST))
local SUNFURY_MIXED = MixedPack("Sunfury Hold (TBC + Midnight)", SUNFURY, Midnight("Stormarion Citadel (Midnight)", MN_STORMARION_CITADEL))
local TEMPEST_KEEP_MIXED = MixedPack("Tempest Keep (TBC + Midnight)", TEMPEST_KEEP, Midnight("Voidspire (Midnight)", MN_VOIDSPIRE))
local TEMPEST_KEEP_BATTLE_MIXED = MixedPack("Tempest Keep Battle (TBC + Midnight)", TEMPEST_KEEP_BATTLE, Midnight("Voidscar Arena (Midnight)", MN_ARENA))
local MOLT_MIXED = MixedPack("The Molt (TBC + Midnight)", MOLT, Midnight("Gorging Pit (Midnight)", MN_GORGING_PIT))
local WILDS_MIXED = MixedPack("Celestial Ridge (TBC + Midnight)", WILDS, Midnight("Predaxas (Midnight)", Merge(MN_PREDAXAS, MN_GORGING_PIT)))
local EYE_OF_THE_STORM_MIXED = MixedPack("Eye of the Storm (TBC + Midnight)", EYE_OF_THE_STORM, Midnight("Slayer's Rise (Midnight)", MN_SLAYERS_RISE))
local OUTLAND_ALLIANCE_MIXED = MixedPack("Honor Hold (TBC + Midnight)", OUTLAND_ALLIANCE, Midnight("Grief Spire (Midnight)", MN_GRIEF_SPIRE))
local OUTLAND_HORDE_MIXED = MixedPack("Thrallmar (TBC + Midnight)", OUTLAND_HORDE, Midnight("Hate Spire (Midnight)", MN_HATE_SPIRE))
local ENKAAT_MIXED = MixedPack("Ruins of Enkaat (TBC + Midnight)", ENKAAT, Midnight("Voidstorm (Midnight)", MN_FIELDS))

ns.MusicPacks = {
    NETHERSTORM = NETHERSTORM,
    NETHERSTORM_MIXED = NETHERSTORM_MIXED,
    AREA52 = AREA52,
    AREA52_MIXED = AREA52_MIXED,
    MANAFORGE = MANAFORGE,
    MANAFORGE_MIXED = MANAFORGE_MIXED,
    ETHEREUM = ETHEREUM,
    ETHEREUM_MIXED = ETHEREUM_MIXED,
    FORGE_BASE = FORGE_BASE,
    FORGE_BASE_MIXED = FORGE_BASE_MIXED,
    SUNFURY = SUNFURY,
    SUNFURY_MIXED = SUNFURY_MIXED,
    TEMPEST_KEEP = TEMPEST_KEEP,
    TEMPEST_KEEP_MIXED = TEMPEST_KEEP_MIXED,
    TEMPEST_KEEP_BATTLE = TEMPEST_KEEP_BATTLE,
    TEMPEST_KEEP_BATTLE_MIXED = TEMPEST_KEEP_BATTLE_MIXED,
    MOLT = MOLT,
    MOLT_MIXED = MOLT_MIXED,
    WILDS = WILDS,
    WILDS_MIXED = WILDS_MIXED,
    EYE_OF_THE_STORM = EYE_OF_THE_STORM,
    EYE_OF_THE_STORM_MIXED = EYE_OF_THE_STORM_MIXED,
    OUTLAND_ALLIANCE = OUTLAND_ALLIANCE,
    OUTLAND_ALLIANCE_MIXED = OUTLAND_ALLIANCE_MIXED,
    OUTLAND_HORDE = OUTLAND_HORDE,
    OUTLAND_HORDE_MIXED = OUTLAND_HORDE_MIXED,
    ENKAAT = ENKAAT,
    ENKAAT_MIXED = ENKAAT_MIXED,
}
