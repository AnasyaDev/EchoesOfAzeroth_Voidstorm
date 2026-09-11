local _, ns = ...

-- ============================================================
-- Track catalog — FileDataIDs from the wowdev community listfile
-- (build 12.1.0), grouped by source.  Durations were measured with
-- ffprobe on the files served by wago.tools (2026-09-11), except the
-- Ghostlands / Blood Elf Base / Locus Point rows, which reuse the
-- values already measured for EchoesOfAzeroth_QuelThalas.
--
-- Prefixes:
--   NS_ = Netherstorm zone music (TBC)
--   TK_ = Tempest Keep (TBC raid, dungeons, Eye of the Storm)
--   OL_ = Outland general (TBC intros and base themes)
--   TF_ = Terokkar / Auchindoun (TBC ethereal dungeons)
--   GL_ = Ghostlands (TBC blood elf hostile set)
--   MN_ = Midnight native Voidstorm music (mixed packs only)
-- ============================================================

ns.Tracks = {

    -- Netherstorm > General (ZoneMusic 272, the only zone-wide set) ---
    NS_GeneralWalkUni01          = 53620,
    NS_GeneralWalkUni02          = 53621,
    NS_GeneralWalkUni03          = 53622,
    NS_GeneralWalkUni04          = 53623,
    NS_GeneralWalkUni05          = 53624,
    NS_GeneralWalkUni06          = 53625,
    NS_GeneralWalkUni07          = 53626,
    NS_GeneralWalkUni08          = 53627,
    NS_GeneralWalkUni09          = 53628,
    NS_GeneralWalkUni10          = 53629,

    -- Netherstorm > Mushroom intros (orphaned in current data) ----
    NS_MushroomIntroUni01        = 53630,
    NS_MushroomIntroUni02        = 53631,
    NS_MushroomIntroUni03        = 53632,

    -- Netherstorm > Netherplant intros (one per manaforge) --------
    NS_NetherplantIntroUni01     = 53633,
    NS_NetherplantIntroUni02     = 53634,
    NS_NetherplantIntroUni03     = 53635,
    NS_NetherplantIntroUni04     = 53636,

    -- Tempest Keep > ambient (ZoneMusic 373) ----------------------
    TK_TempestKeepAMB11          = 53779,
    TK_TempestKeepAMB12          = 53780,
    TK_TempestKeepAMB13          = 53781,
    TK_TempestKeepAMB14          = 53782,
    TK_TempestKeepAMB16          = 53783,
    TK_TempestKeepAMB17          = 53784,
    TK_TempestKeepAMB18          = 53785,
    TK_TempestKeepAMB19          = 53786,
    TK_TempestKeepAMB20          = 53787,
    TK_TempestKeepAMB22          = 53788,
    TK_TempestKeepAMB23          = 53789,

    -- Tempest Keep > battle (ZoneMusic 374) -----------------------
    TK_TempestKeepBTL10          = 53790,
    TK_TempestKeepBTL11          = 53791,
    TK_TempestKeepBTL13          = 53792,

    -- Tempest Keep > stingers (ZoneIntroMusicTable 535-537) -------
    TK_TempestKeepSTG14          = 53793,
    TK_TempestKeepSTG15          = 53794,

    -- Outland > intros (ZoneIntroMusicTable) ----------------------
    OL_HistoricIntroUni01        = 53665,
    OL_ScenicIntroUni01          = 53677,
    OL_CrystalIntroUni03         = 53659,
    OL_BurningLegionIntroUni01   = 53644,
    OL_BurningLegionIntroUni02   = 53645,
    OL_ActionWalkUni01           = 53637,

    -- Outland > corrupt set (Legion-held ground, ZoneMusic 302/334) ---
    OL_Corrupt01                 = 53649,
    OL_Corrupt02                 = 53650,
    OL_Corrupt03                 = 53651,
    OL_Corrupt04                 = 53652,
    OL_Corrupt05                 = 53653,
    OL_Corrupt06                 = 53654,
    OL_Corrupt07                 = 53655,
    OL_CorruptIntro              = 53656,

    -- Outland > base themes ---------------------------------------
    OL_DraeneiBaseWalkUni01      = 53661,
    OL_DraeneiBaseWalkUni02r     = 53662,
    OL_AllianceBaseWalkUni01     = 53638,
    OL_AllianceBaseWalkUni02     = 53639,
    OL_HordeBaseWalkUni03        = 53668,
    OL_HordeBaseWalkUni04        = 53669,
    OL_BloodElfBaseWalkUni01     = 53642,
    OL_BloodElfBaseWalkUni02     = 53643,

    -- Terokkar > Auchindoun (ZoneMusic 316, ethereal / draenei dungeons) ---
    TF_AuchindounWalkUni01       = 53796,
    TF_AuchindounWalkUni02       = 53797,
    TF_AuchindounWalkUni03       = 53798,

    -- Ghostlands > Forest 3 night (Sunfury Hold set, ZoneMusic 337) ---
    GL_Forest3WalkNight01        = 53510,
    GL_Forest3WalkNight02        = 53511,
    GL_Forest3WalkNight03        = 53512,

    -- Midnight > Voidstorm (native, used by the mixed packs only) ---
    MN_VoidstormA                = 7692210,
    MN_VoidstormB                = 7692212,
    MN_VoidstormC                = 7692214,
    MN_VoidstormD                = 7692216,
    MN_VoidstormE                = 7692218,
    MN_VoidstormF                = 7713464,
    MN_VoidstormH                = 7692220,

    -- Midnight > Storm Fields -------------------------------------
    MN_StormFieldsA              = 7690563,
    MN_StormFieldsB              = 7690565,
    MN_StormFieldsC              = 7690567,
    MN_StormFieldsD              = 7690569,
    MN_StormFieldsE              = 7690571,
    MN_StormFieldsF              = 7690573,
    MN_StormFieldsG              = 7690575,
    MN_StormFieldsH              = 7690577,
    MN_StormFieldsI              = 7690579,

    -- Midnight > Devouring Host -----------------------------------
    MN_DevouringHostA            = 7681054,
    MN_DevouringHostB            = 7681056,
    MN_DevouringHostC            = 7681058,
    MN_DevouringHostD            = 7681060,
    MN_DevouringHostE            = 7681062,
    MN_DevouringHostF            = 7703708,
    MN_DevouringHostG            = 7703710,
    MN_DevouringHostH            = 7681064,
    MN_DevouringHostI            = 7703712,
    MN_DevouringHostJ            = 7703714,
    MN_DevouringHostK            = 7703716,

    -- Midnight > Locus Point (void elf hub) -----------------------
    MN_LocusPointA               = 7684188,
    MN_LocusPointB               = 7684190,
    MN_LocusPointC               = 7684192,
    MN_LocusPointD               = 7684194,
    MN_LocusPointE               = 7684196,
    MN_LocusPointF               = 7713420,
    MN_LocusPointH               = 7684198,

    -- Midnight > Howling Ridge ------------------------------------
    MN_HowlingRidgeA             = 7681076,
    MN_HowlingRidgeB             = 7681078,
    MN_HowlingRidgeC             = 7681080,
    MN_HowlingRidgeD             = 7681082,
    MN_HowlingRidgeE             = 7681084,
    MN_HowlingRidgeH             = 7681086,

    -- Midnight > Shadowguard Void (Ethereum) ----------------------
    MN_ShadowguardVoidA          = 7681154,
    MN_ShadowguardVoidB          = 7681156,
    MN_ShadowguardVoidC          = 7681158,
    MN_ShadowguardVoidD          = 7681160,
    MN_ShadowguardVoidH          = 7681162,

    -- Midnight > Gnawing Reach (Gorging Pit kit) ------------------
    MN_GnawingReachA             = 7696432,
    MN_GnawingReachB             = 7696434,
    MN_GnawingReachC             = 7696436,
    MN_GnawingReachD             = 7703718,
    MN_GnawingReachE             = 7703720,
    MN_GnawingReachH             = 7696438,

    -- Midnight > Slayer's Rise ------------------------------------
    MN_SlayersRiseA              = 7691961,
    MN_SlayersRiseB              = 7691963,
    MN_SlayersRiseC              = 7691965,
    MN_SlayersRiseD              = 7691971,
    MN_SlayersRiseE              = 7691975,
    MN_SlayersRiseF              = 7691977,
    MN_SlayersRiseG              = 7691980,
    MN_SlayersRiseH              = 7691982,

}

-- ============================================================
-- Track durations (seconds), keyed by FileDataID, so the engine can
-- schedule the next track when the current one ends.
-- ============================================================

ns.TrackDurations = {
    [53620] =  150.7,  -- NS_GeneralWalkUni01
    [53621] =  175.4,  -- NS_GeneralWalkUni02
    [53622] =  178.4,  -- NS_GeneralWalkUni03
    [53623] =  181.3,  -- NS_GeneralWalkUni04
    [53624] =  184.3,  -- NS_GeneralWalkUni05
    [53625] =  192.0,  -- NS_GeneralWalkUni06
    [53626] =  193.3,  -- NS_GeneralWalkUni07
    [53627] =  168.9,  -- NS_GeneralWalkUni08
    [53628] =  199.2,  -- NS_GeneralWalkUni09
    [53629] =  223.0,  -- NS_GeneralWalkUni10
    [53630] =   39.2,  -- NS_MushroomIntroUni01
    [53631] =   33.9,  -- NS_MushroomIntroUni02
    [53632] =   36.9,  -- NS_MushroomIntroUni03
    [53633] =   44.7,  -- NS_NetherplantIntroUni01
    [53634] =   51.2,  -- NS_NetherplantIntroUni02
    [53635] =   47.8,  -- NS_NetherplantIntroUni03
    [53636] =   45.4,  -- NS_NetherplantIntroUni04
    [53779] =   46.0,  -- TK_TempestKeepAMB11
    [53780] =   96.7,  -- TK_TempestKeepAMB12
    [53781] =   67.7,  -- TK_TempestKeepAMB13
    [53782] =   88.5,  -- TK_TempestKeepAMB14
    [53783] =   58.3,  -- TK_TempestKeepAMB16
    [53784] =   62.7,  -- TK_TempestKeepAMB17
    [53785] =   85.9,  -- TK_TempestKeepAMB18
    [53786] =   48.7,  -- TK_TempestKeepAMB19
    [53787] =   47.0,  -- TK_TempestKeepAMB20
    [53788] =   34.1,  -- TK_TempestKeepAMB22
    [53789] =   67.9,  -- TK_TempestKeepAMB23
    [53790] =   59.7,  -- TK_TempestKeepBTL10
    [53791] =   81.6,  -- TK_TempestKeepBTL11
    [53792] =   36.6,  -- TK_TempestKeepBTL13
    [53793] =   11.8,  -- TK_TempestKeepSTG14
    [53794] =   11.6,  -- TK_TempestKeepSTG15
    [53665] =   79.5,  -- OL_HistoricIntroUni01
    [53677] =   31.5,  -- OL_ScenicIntroUni01
    [53659] =   21.6,  -- OL_CrystalIntroUni03
    [53644] =   16.5,  -- OL_BurningLegionIntroUni01
    [53645] =   35.2,  -- OL_BurningLegionIntroUni02
    [53637] =   80.8,  -- OL_ActionWalkUni01
    [53649] =   60.9,  -- OL_Corrupt01
    [53650] =   62.6,  -- OL_Corrupt02
    [53651] =   74.4,  -- OL_Corrupt03
    [53652] =   71.4,  -- OL_Corrupt04
    [53653] =   72.6,  -- OL_Corrupt05
    [53654] =   74.3,  -- OL_Corrupt06
    [53655] =   52.3,  -- OL_Corrupt07
    [53656] =   75.6,  -- OL_CorruptIntro
    [53661] =  106.6,  -- OL_DraeneiBaseWalkUni01
    [53662] =   99.9,  -- OL_DraeneiBaseWalkUni02r
    [53638] =  134.5,  -- OL_AllianceBaseWalkUni01
    [53639] =  110.5,  -- OL_AllianceBaseWalkUni02
    [53668] =   66.2,  -- OL_HordeBaseWalkUni03
    [53669] =   68.1,  -- OL_HordeBaseWalkUni04
    [53642] =  120.0,  -- OL_BloodElfBaseWalkUni01
    [53643] =  121.6,  -- OL_BloodElfBaseWalkUni02
    [53796] =  120.3,  -- TF_AuchindounWalkUni01
    [53797] =  150.1,  -- TF_AuchindounWalkUni02
    [53798] =  120.3,  -- TF_AuchindounWalkUni03
    [53510] =   51.3,  -- GL_Forest3WalkNight01
    [53511] =   28.1,  -- GL_Forest3WalkNight02
    [53512] =   44.4,  -- GL_Forest3WalkNight03
    [7692210] =  139.8,  -- MN_VoidstormA
    [7692212] =  145.1,  -- MN_VoidstormB
    [7692214] =  105.5,  -- MN_VoidstormC
    [7692216] =  139.9,  -- MN_VoidstormD
    [7692218] =  152.5,  -- MN_VoidstormE
    [7713464] =  109.9,  -- MN_VoidstormF
    [7692220] =  290.6,  -- MN_VoidstormH
    [7690563] =  151.3,  -- MN_StormFieldsA
    [7690565] =  124.4,  -- MN_StormFieldsB
    [7690567] =  145.9,  -- MN_StormFieldsC
    [7690569] =  145.1,  -- MN_StormFieldsD
    [7690571] =  124.5,  -- MN_StormFieldsE
    [7690573] =  133.4,  -- MN_StormFieldsF
    [7690575] =  146.4,  -- MN_StormFieldsG
    [7690577] =  293.9,  -- MN_StormFieldsH
    [7690579] =  145.8,  -- MN_StormFieldsI
    [7681054] =   96.6,  -- MN_DevouringHostA
    [7681056] =   76.4,  -- MN_DevouringHostB
    [7681058] =   93.3,  -- MN_DevouringHostC
    [7681060] =  126.0,  -- MN_DevouringHostD
    [7681062] =   91.7,  -- MN_DevouringHostE
    [7703708] =   71.3,  -- MN_DevouringHostF
    [7703710] =   68.0,  -- MN_DevouringHostG
    [7681064] =  199.6,  -- MN_DevouringHostH
    [7703712] =  105.0,  -- MN_DevouringHostI
    [7703714] =   77.5,  -- MN_DevouringHostJ
    [7703716] =   87.0,  -- MN_DevouringHostK
    [7684188] =  118.4,  -- MN_LocusPointA
    [7684190] =  122.2,  -- MN_LocusPointB
    [7684192] =  135.8,  -- MN_LocusPointC
    [7684194] =  153.6,  -- MN_LocusPointD
    [7684196] =  120.4,  -- MN_LocusPointE
    [7713420] =  132.3,  -- MN_LocusPointF
    [7684198] =  161.6,  -- MN_LocusPointH
    [7681076] =   83.8,  -- MN_HowlingRidgeA
    [7681078] =   85.2,  -- MN_HowlingRidgeB
    [7681080] =   95.8,  -- MN_HowlingRidgeC
    [7681082] =   60.0,  -- MN_HowlingRidgeD
    [7681084] =   91.1,  -- MN_HowlingRidgeE
    [7681086] =  140.1,  -- MN_HowlingRidgeH
    [7681154] =  156.8,  -- MN_ShadowguardVoidA
    [7681156] =  139.4,  -- MN_ShadowguardVoidB
    [7681158] =  130.5,  -- MN_ShadowguardVoidC
    [7681160] =  150.7,  -- MN_ShadowguardVoidD
    [7681162] =  174.6,  -- MN_ShadowguardVoidH
    [7696432] =  108.6,  -- MN_GnawingReachA
    [7696434] =  123.4,  -- MN_GnawingReachB
    [7696436] =  126.5,  -- MN_GnawingReachC
    [7703718] =   81.5,  -- MN_GnawingReachD
    [7703720] =  135.4,  -- MN_GnawingReachE
    [7696438] =  163.5,  -- MN_GnawingReachH
    [7691961] =  141.9,  -- MN_SlayersRiseA
    [7691963] =  153.2,  -- MN_SlayersRiseB
    [7691965] =  149.1,  -- MN_SlayersRiseC
    [7691971] =   87.0,  -- MN_SlayersRiseD
    [7691975] =   77.5,  -- MN_SlayersRiseE
    [7691977] =   85.4,  -- MN_SlayersRiseF
    [7691980] =  140.4,  -- MN_SlayersRiseG
    [7691982] =  167.3,  -- MN_SlayersRiseH
}
