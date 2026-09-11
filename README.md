# Echoes of Azeroth: Voidstorm

`EchoesOfAzeroth_Voidstorm` is a content plugin for `EchoesOfAzeroth`.

It replaces the music of Voidstorm (Midnight) with the music of Netherstorm (The Burning Crusade), sub-area by sub-area: the two zones mirror each other almost point for point, and the plugin follows that mirror.

## Requires

- `EchoesOfAzeroth`

This plugin depends on the core addon.

## The mirror

| Voidstorm | Netherstorm |
|---|---|
| Storm Fields, the open plains | Netherstorm general music |
| The Ingress, Locus Point, The Howling Ridge (Singularity hubs) | Area 52 / Cosmowrench (the goblin towns' intro) |
| Nexus-Point Antius, Xenas, Mid'Ar (void-draining pylons) | Manaforges Ara, B'naar, Coruu, Duro (one intro each) |
| Shadowguard Point, Ethereum Refinery, Ethereum Overcroft | The Ethereum, Auchindoun / Mana-Tombs |
| Stormarion Keep, Obscurion Citadel (Devouring Host) | Forge Base: Oblivion / Gehenna (Burning Legion) |
| Stormarion Citadel (retaken by the ren'dorei) | Sunfury Hold |
| The Voidspire, The Approach | Tempest Keep |
| The Molt and the burrows | Mushroom intros |
| Den of Predaxas, the pits and caves | Celestial Ridge, Netherstone (crystal intros) |
| Slayer's Rise | Eye of the Storm |
| Grief Spire / Hate Spire | Outland Alliance / Horde bases |
| Exiles' Hovel | Ruins of Enkaat |

## Included music packs

Each pack exists as `(TBC)` and as `(TBC + Midnight)`, the latter merging the Midnight kit the game natively plays in the same places:

- `Netherstorm`
- `Area 52`
- `Manaforge`
- `Ethereum`
- `Forge Base`
- `Sunfury Hold`
- `Tempest Keep`
- `Tempest Keep Battle`
- `The Molt`
- `Celestial Ridge`
- `Eye of the Storm`
- `Honor Hold`
- `Thrallmar`
- `Ruins of Enkaat`

There is no pure Midnight pack: that is what you already hear with the addon disabled. Build one from the Midnight tracks in the core UI if you want it.

## Covered zones

- Voidstorm (open world), with its named sub-areas
- Slayer's Rise (open-world PvP area)

Dungeons, the raid and the delves are intentionally not mapped and keep their native music.

## Source approach

- FileDataIDs come from the wowdev community listfile (build 12.1.0).
- Sub-area names come from the game's AreaTable in every client locale, so they match `GetSubZoneText()` exactly.
- Track durations were measured from the audio files so pack rotation follows real track length.
- Intros mirror Netherstorm's own design: one walking set for the zone, and a one-shot intro that signs each kind of place.

## How to use it

1. Install `EchoesOfAzeroth`
2. Install this plugin
3. Open `/eoa options`
4. Enable the plugin in `Plugins`
5. Adjust mappings in `Zone Mapping` if desired

## Notes

- The plugin provides content only
- Playback, profiles, custom packs, custom zones, and import/export live in the core addon

## Community profiles

`EchoesOfAzeroth` is meant to grow as a community addon.

If you build a profile that feels especially polished, immersive, or lore-accurate, please share it. Great community profiles can help refine the addon over time, and an especially strong configuration may be adopted as an official default or recommended setup in the future.
