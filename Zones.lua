local _, ns = ...
local api = _G.EchoesOfAzeroth
local Dsl = api and api.PluginDsl
if not Dsl then
    error("EchoesOfAzeroth core must load before EchoesOfAzeroth_Voidstorm")
end

-- ============================================================
-- Zone -> music-pack mapping (Midnight UiMapIDs)
--
-- Open world only, on purpose: the Voidstorm dungeons, the raid and
-- the delves keep their native music.  Tempest Keep music is still
-- used, but for the outdoor Voidspire.
--
-- Sub-areas that have no ZoneMusic of their own in the game data
-- (Storm Fields, Grasping Reach, the PvP field POIs...) are left out
-- so they inherit the zone pack.
--
-- Discover zone / subzone info in-game:  /eoa now
-- ============================================================

local SLAYERS_RISE_SUBZONES = {
    MASTERS_PERCH       = "AREA52",
    GRIEF_SPIRE         = "OUTLAND_ALLIANCE",
    RETRIBUTION_HOLD    = "OUTLAND_ALLIANCE",
    BASTION_OF_VALOR    = "OUTLAND_ALLIANCE",
    HATE_SPIRE          = "OUTLAND_HORDE",
    METTLES_HOLD        = "OUTLAND_HORDE",
    BASTION_OF_MIGHT    = "OUTLAND_HORDE",
    VOIDSCAR_ARENA      = "TEMPEST_KEEP_BATTLE",
    SHENZAR_REFINERY    = "ETHEREUM",
    HANAAR_OUTPOST      = "ETHEREUM",
    SHADOWRIDGE_OUTPOST = "ETHEREUM",
    SHADOW_RISE         = "ETHEREUM",
    THE_HUSK            = "WILDS",
}

local VOIDSTORM_SUBZONES = {
    -- Singularity (ren'dorei) hubs
    THE_INGRESS         = "AREA52",
    LOCUS_POINT         = "AREA52",
    THE_HOWLING_RIDGE   = "AREA52",
    DUSKS_REPOSE        = "AREA52",

    -- Nexus-Points (void-draining pylons) <-> manaforges
    NEXUS_POINT_ANTIUS  = "MANAFORGE",
    NEXUS_POINT_XENAS   = "MANAFORGE",
    NEXUS_POINT_MIDAR   = "MANAFORGE",

    -- Ethereum ethereals
    SHADOWGUARD_POINT   = "ETHEREUM",
    ETHEREUM_REFINERY   = "ETHEREUM",
    ETHEREUM_OVERCROFT  = "ETHEREUM",

    -- Devouring Host fortresses <-> Legion forge bases
    STORMARION_KEEP     = "FORGE_BASE",
    STORMARION_WATCH    = "FORGE_BASE",
    OBSCURION_CITADEL   = "FORGE_BASE",
    STORMARION_CITADEL  = "SUNFURY",

    -- The Voidspire (outdoor) <-> Tempest Keep
    THE_VOIDSPIRE       = "TEMPEST_KEEP",
    THE_APPROACH        = "TEMPEST_KEEP",

    -- Predacea: the kaiju's molt and burrows
    THE_MOLT            = "MOLT",
    UNDERGROUND_BURROWS = "MOLT",
    THE_BLADEBURROWS    = "MOLT",
    ABUNDANT_VOIDBURROW = "MOLT",
    OVERRUN_HOLLOW      = "MOLT",

    -- Predacea: dens, pits and caves
    DEN_OF_PREDAXAS     = "WILDS",
    LAIR_OF_PREDAXAS    = "WILDS",
    NIGHT_TRENCH        = "WILDS",
    THE_GORGING_PIT     = "WILDS",
    QUIET_CAVERN        = "WILDS",
    CONSUMPTOR_CAVE     = "WILDS",

    -- Exiles
    EXILES_HOVEL        = "ENKAAT",

    -- Slayer's Rise fallback.  The PvP area has its own UiMap (2444,
    -- mapped below); these entries only matter if the client reports
    -- map 2405 while standing there.  Safe to delete once /eoa now
    -- confirms 2444 in-game.
    SLAYERS_RISE        = "EYE_OF_THE_STORM",
    PATH_OF_PREDATION   = "EYE_OF_THE_STORM",
    THE_BLOODPLAINS     = "EYE_OF_THE_STORM",
    STAREATER_PAVILION  = "EYE_OF_THE_STORM",
    SHATTERSKY_PAVILION = "EYE_OF_THE_STORM",
    CLAWS_EDGE          = "EYE_OF_THE_STORM",
    THE_FANGFALL        = "EYE_OF_THE_STORM",
    SPARRING_GROUNDS    = "EYE_OF_THE_STORM",
}
for key, packKey in pairs(SLAYERS_RISE_SUBZONES) do
    VOIDSTORM_SUBZONES[key] = packKey
end

ns.ZoneMusic = {
    -- Voidstorm (2405), child of Quel'Thalas (2537)
    [2405] = Dsl.zone("VOIDSTORM", "NETHERSTORM", VOIDSTORM_SUBZONES),

    -- Slayer's Rise (2444), the open-world PvP area, child of 2405
    [2444] = Dsl.zone("SLAYERS_RISE", "EYE_OF_THE_STORM", SLAYERS_RISE_SUBZONES),
}
