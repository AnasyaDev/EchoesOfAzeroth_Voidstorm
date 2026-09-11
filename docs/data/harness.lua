-- Lua 5.1 stub harness: loads the core PluginDsl + a content plugin and validates the catalog.
-- usage: lua5.1 harness.lua <pluginDir> <tocName> [locale]
local pluginDir, tocName, locale = arg[1], arg[2], arg[3] or "enUS"
_G.GetLocale = function() return locale end
local registered
_G.EchoesOfAzeroth = { RegisterPlugin = function(def) registered = def; return def end }

local function run(path, name, ns)
    local f, err = loadfile(path)
    assert(f, err)
    return f(name, ns)
end
run("/home/loadren/Documents/Code/EchoesOfAzeroth/PluginDsl.lua", "EchoesOfAzeroth", {})

local ns = {}
for line in io.lines(pluginDir .. "/" .. tocName) do
    local file = line:match("^%s*([%w_]+%.lua)%s*$")
    if file then run(pluginDir .. "/" .. file, tocName:gsub("%.toc$", ""), ns) end
end
assert(registered, "plugin did not register")

local errors, warnings = {}, {}
local function err(s) errors[#errors + 1] = s end
local function warn(s) warnings[#warnings + 1] = s end

-- tracks / durations
local fdidToSymbol, symbolCount = {}, 0
for sym, fdid in pairs(ns.Tracks) do
    symbolCount = symbolCount + 1
    if type(fdid) ~= "number" then err("track " .. sym .. " is not a number") end
    if fdidToSymbol[fdid] then warn("duplicate FDID " .. fdid .. ": " .. sym .. " / " .. fdidToSymbol[fdid]) end
    fdidToSymbol[fdid] = sym
    if not ns.TrackDurations[fdid] then err("missing duration for " .. sym .. " (" .. fdid .. ")") end
end
for fdid in pairs(ns.TrackDurations) do
    if not fdidToSymbol[fdid] then warn("stale duration row " .. fdid) end
end

-- packs
local used = {}
local packCount = 0
for key, pack in pairs(ns.MusicPacks) do
    packCount = packCount + 1
    if type(pack.label) ~= "string" then err("pack " .. key .. " has no label") end
    local n = 0
    for _, list in ipairs({ pack.day or {}, pack.night or {}, pack.any or {} }) do
        for _, fdid in ipairs(list) do
            n = n + 1
            if not fdidToSymbol[fdid] then err("pack " .. key .. " references unknown FDID " .. tostring(fdid)) end
            used[fdid] = true
        end
    end
    if pack.intro then
        if not fdidToSymbol[pack.intro] then err("pack " .. key .. " intro unknown FDID " .. tostring(pack.intro)) end
        used[pack.intro] = true
    end
    if n == 0 then err("pack " .. key .. " has no rotating track") end
end
for fdid, sym in pairs(fdidToSymbol) do
    if not used[fdid] then warn("track " .. sym .. " is not used by any pack") end
end

-- locale
local rawNames = {}
for k, v in pairs(ns.L) do rawNames[k] = v end
local textToKeys = {}
for key, text in pairs(ns.SubzoneNames) do
    if type(text) ~= "string" or text == "" then err("subzone " .. key .. " has empty text") end
    textToKeys[text] = textToKeys[text] or {}
    table.insert(textToKeys[text], key)
end
for text, keys in pairs(textToKeys) do
    if #keys > 1 then err("subzone text '" .. text .. "' maps to several keys: " .. table.concat(keys, ", ")) end
end
for text, key in pairs(ns.SubzoneKeys) do
    if ns.SubzoneNames[key] ~= text then err("SubzoneKeys inconsistent for " .. key) end
end

-- zones
local usedSubzoneKeys, usedPacks = {}, {}
local zoneCount = 0
for mapId, zone in pairs(ns.ZoneMusic) do
    zoneCount = zoneCount + 1
    if type(mapId) ~= "number" then err("zone key " .. tostring(mapId) .. " is not a number") end
    if not rawNames[zone.nameKey] then err("zone " .. mapId .. " nameKey " .. tostring(zone.nameKey) .. " missing in Locale") end
    if zone.pack and not ns.MusicPacks[zone.pack] then err("zone " .. mapId .. " pack " .. zone.pack .. " missing") end
    usedPacks[zone.pack or ""] = true
    for subKey, packKey in pairs(zone.subzones or {}) do
        usedSubzoneKeys[subKey] = true
        usedPacks[packKey] = true
        if not ns.SubzoneNames[subKey] then err("zone " .. mapId .. " subzone " .. subKey .. " missing in Locale") end
        if not ns.MusicPacks[packKey] then err("zone " .. mapId .. " subzone " .. subKey .. " -> unknown pack " .. packKey) end
    end
end
for key in pairs(ns.SubzoneNames) do
    if not usedSubzoneKeys[key] then warn("subzone " .. key .. " defined in Locale but unused in Zones") end
end

print(string.format("[%s] plugin=%s tracks=%d packs=%d zones=%d subzones=%d errors=%d warnings=%d",
    locale, registered.id, symbolCount, packCount, zoneCount, (function() local n = 0 for _ in pairs(ns.SubzoneNames) do n = n + 1 end return n end)(), #errors, #warnings))
for _, e in ipairs(errors) do print("  ERROR " .. e) end
for _, w in ipairs(warnings) do print("  warn  " .. w) end
os.exit(#errors == 0 and 0 or 1)
