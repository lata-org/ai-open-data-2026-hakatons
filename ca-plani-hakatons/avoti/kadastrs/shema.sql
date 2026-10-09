-- ================================================================
-- Kadastra un adrešu datu SQLite shēma
--
-- Avoti:  VAR_ATVERTIE_DATI_MODELIS.md  (12.1 sadaļa) — aw_* tabulas
--         NIVKIS_ATVERTIE_DATI_MODELIS.md (11.1 sadaļa) — pārējās
-- Papildus: atjaunināšanas uzskaite (avota_fails, atjauninajums)
-- ================================================================

PRAGMA journal_mode = WAL;

-- ================================================================
-- 0. Atjaunināšanas uzskaite
-- ================================================================

-- Katrs lejupielādētais avota fails ar tā jaucējsummu. Ja jaucējsumma
-- nav mainījusies, atkārtota ielāde tiek izlaista.
CREATE TABLE IF NOT EXISTS avota_fails (
    fails           TEXT PRIMARY KEY,   -- aw_eka.csv, building.zip
    datu_kopa       TEXT NOT NULL,      -- VAR | NIVKIS
    merka_tabula    TEXT,
    resursa_id      TEXT,
    url             TEXT,
    lejupieladets   TEXT,               -- ISO laikspiedols
    ieladets        TEXT,
    sha256          TEXT,
    baiti           INTEGER,
    rindas          INTEGER
);

-- Katra `atjaunot.py` palaiduma žurnāls.
CREATE TABLE IF NOT EXISTS atjauninajums (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sakts           TEXT NOT NULL,
    beidzies        TEXT,
    datu_kopa       TEXT NOT NULL,
    faili_parbaditi INTEGER DEFAULT 0,
    faili_mainiti   INTEGER DEFAULT 0,
    rindas_ieladetas INTEGER DEFAULT 0,
    piezime         TEXT
);

-- ================================================================
-- 1. VAR — Valsts adrešu reģistrs
-- ================================================================

CREATE TABLE IF NOT EXISTS aw_novads (
    kods TEXT PRIMARY KEY, tips_cd TEXT, nosaukums TEXT, vkur_cd TEXT, vkur_tips TEXT,
    apstipr TEXT, apst_pak TEXT, statuss TEXT, sort_nos TEXT,
    dat_sak TEXT, dat_mod TEXT, dat_beig TEXT,
    atrib TEXT,                                   -- ATVK kods
    std TEXT
);

CREATE TABLE IF NOT EXISTS aw_pilseta (
    kods TEXT PRIMARY KEY, tips_cd TEXT, nosaukums TEXT, vkur_cd TEXT, vkur_tips TEXT,
    apstipr TEXT, apst_pak TEXT, statuss TEXT, sort_nos TEXT,
    dat_sak TEXT, dat_mod TEXT, dat_beig TEXT, atrib TEXT, std TEXT
);

CREATE TABLE IF NOT EXISTS aw_pagasts (
    kods TEXT PRIMARY KEY, tips_cd TEXT, nosaukums TEXT, vkur_cd TEXT, vkur_tips TEXT,
    apstipr TEXT, apst_pak TEXT, statuss TEXT, sort_nos TEXT,
    dat_sak TEXT, dat_mod TEXT, dat_beig TEXT, atrib TEXT, std TEXT
);

CREATE TABLE IF NOT EXISTS aw_ciems (
    kods TEXT PRIMARY KEY, tips_cd TEXT, nosaukums TEXT,
    vkur_cd TEXT,                                 -- FK -> pagasts vai pilsēta
    vkur_tips TEXT, apstipr TEXT, apst_pak TEXT, statuss TEXT, sort_nos TEXT,
    dat_sak TEXT, dat_mod TEXT, dat_beig TEXT,
    atrib TEXT,                                   -- "1" = mazciems
    std TEXT
);

CREATE TABLE IF NOT EXISTS aw_iela (
    kods TEXT PRIMARY KEY, tips_cd TEXT, nosaukums TEXT,
    vkur_cd TEXT,                                 -- FK -> ciems vai pilsēta
    vkur_tips TEXT, apstipr TEXT, apst_pak TEXT, statuss TEXT, sort_nos TEXT,
    dat_sak TEXT, dat_mod TEXT, dat_beig TEXT, atrib TEXT, std TEXT
);

CREATE TABLE IF NOT EXISTS aw_eka (
    kods TEXT PRIMARY KEY, tips_cd TEXT, statuss TEXT, apstipr TEXT, apst_pak TEXT,
    vkur_cd TEXT,                                 -- FK -> iela vai ciems/pagasts
    vkur_tips TEXT, nosaukums TEXT, sort_nos TEXT,
    atrib TEXT,                                   -- pasta indekss LV-XXXX
    pnod_cd TEXT, dat_sak TEXT, dat_mod TEXT, dat_beig TEXT,
    for_build TEXT,                               -- Y = zemes vienība, N = ēka
    plan_adr TEXT,                                -- Y = plānotā adrese
    std TEXT,
    koord_x REAL, koord_y REAL,                   -- LKS-92
    dd_e REAL, dd_n REAL                          -- WGS84 lon/lat
);

CREATE TABLE IF NOT EXISTS aw_dziv (
    kods TEXT PRIMARY KEY, tips_cd TEXT, statuss TEXT, apstipr TEXT, apst_pak TEXT,
    vkur_cd TEXT,                                 -- FK -> aw_eka.kods
    vkur_tips TEXT, nosaukums TEXT, sort_nos TEXT, atrib TEXT,
    dat_sak TEXT, dat_mod TEXT, dat_beig TEXT, std TEXT
);

CREATE TABLE IF NOT EXISTS aw_ppils (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kods TEXT,                                    -- FK -> aw_eka.kods
    ppils TEXT, ppils_cd TEXT, dat_sak TEXT, dat_mod TEXT, dat_beig TEXT
);

-- ATKĀPE NO MODEĻA: VAR_ATVERTIE_DATI_MODELIS.md deklarē `kods TEXT PRIMARY KEY`,
-- bet reālajos datos kods NAV unikāls — 18 objektiem (pagastiem ar nesavienotām
-- teritorijas daļām, piem. Zebrenes pag., Lažas pag.) ir vairāki centroīdi.
-- Tāpēc surogātatslēga un indekss uz kods.
CREATE TABLE IF NOT EXISTS aw_vietu_centroidi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kods TEXT, tips_cd TEXT, nosaukums TEXT, vkur_cd TEXT, vkur_tips TEXT,
    std TEXT, koord_x REAL, koord_y REAL, dd_e REAL, dd_n REAL
);
CREATE INDEX IF NOT EXISTS idx_centroidi_kods ON aw_vietu_centroidi(kods);

CREATE TABLE IF NOT EXISTS aw_rajons (
    kods TEXT PRIMARY KEY, tips_cd TEXT, nosaukums TEXT, vkur_cd TEXT, vkur_tips TEXT,
    apstipr TEXT, apst_pak TEXT, statuss TEXT, sort_nos TEXT,
    dat_sak TEXT, dat_mod TEXT, dat_beig TEXT, atrib TEXT
);

CREATE TABLE IF NOT EXISTS aw_doc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adreses_kods TEXT NOT NULL,
    adreses_veids TEXT NOT NULL,                  -- NL | TG | VIETA
    autors TEXT, datums TEXT, veids TEXT, numurs TEXT, nosaukums TEXT
);

CREATE TABLE IF NOT EXISTS aw_vesture (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kods TEXT NOT NULL, tips_cd TEXT, nosaukums TEXT, vkur_cd TEXT, vkur_tips TEXT,
    dat_sak TEXT, dat_mod TEXT, dat_beig TEXT, std TEXT,
    kods_his TEXT,                                -- tikai aw_eka_his
    avota_fails TEXT
);

CREATE INDEX IF NOT EXISTS idx_novads_statuss   ON aw_novads(statuss);
CREATE INDEX IF NOT EXISTS idx_pilseta_vkur     ON aw_pilseta(vkur_cd);
CREATE INDEX IF NOT EXISTS idx_pilseta_statuss  ON aw_pilseta(statuss);
CREATE INDEX IF NOT EXISTS idx_pagasts_vkur     ON aw_pagasts(vkur_cd);
CREATE INDEX IF NOT EXISTS idx_pagasts_statuss  ON aw_pagasts(statuss);
CREATE INDEX IF NOT EXISTS idx_ciems_vkur       ON aw_ciems(vkur_cd);
CREATE INDEX IF NOT EXISTS idx_ciems_statuss    ON aw_ciems(statuss);
CREATE INDEX IF NOT EXISTS idx_iela_vkur        ON aw_iela(vkur_cd);
CREATE INDEX IF NOT EXISTS idx_iela_nosaukums   ON aw_iela(nosaukums);
CREATE INDEX IF NOT EXISTS idx_iela_statuss     ON aw_iela(statuss);
CREATE INDEX IF NOT EXISTS idx_eka_vkur         ON aw_eka(vkur_cd);
CREATE INDEX IF NOT EXISTS idx_eka_statuss      ON aw_eka(statuss);
CREATE INDEX IF NOT EXISTS idx_eka_std          ON aw_eka(std);
CREATE INDEX IF NOT EXISTS idx_eka_pnod         ON aw_eka(pnod_cd);
CREATE INDEX IF NOT EXISTS idx_eka_nosaukums    ON aw_eka(nosaukums);
CREATE INDEX IF NOT EXISTS idx_dziv_vkur        ON aw_dziv(vkur_cd);
CREATE INDEX IF NOT EXISTS idx_dziv_statuss     ON aw_dziv(statuss);
CREATE INDEX IF NOT EXISTS idx_ppils_kods       ON aw_ppils(kods);
CREATE INDEX IF NOT EXISTS idx_doc_kods         ON aw_doc(adreses_kods);
CREATE INDEX IF NOT EXISTS idx_doc_veids        ON aw_doc(adreses_veids);
CREATE INDEX IF NOT EXISTS idx_vest_kods        ON aw_vesture(kods);
CREATE INDEX IF NOT EXISTS idx_vest_avots       ON aw_vesture(avota_fails);
CREATE INDEX IF NOT EXISTS idx_vest_kodshis     ON aw_vesture(kods_his);
CREATE INDEX IF NOT EXISTS idx_vest_std         ON aw_vesture(std);
CREATE INDEX IF NOT EXISTS idx_vest_tips        ON aw_vesture(tips_cd);

-- ================================================================
-- 2. NĪVKIS — Nekustamā īpašuma valsts kadastrs
-- ================================================================

CREATE TABLE IF NOT EXISTS properties (
    cadastre_nr TEXT PRIMARY KEY,                 -- 11 cipari
    property_kind TEXT NOT NULL,
    share_flat_property TEXT,
    property_name TEXT,
    parcel_total_area REAL,
    premise_group_total_area REAL,
    landbook_folio_nr TEXT,
    landbook_folio_liter TEXT,
    landbook_office TEXT,
    not_corroborated TEXT
);

CREATE TABLE IF NOT EXISTS property_objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_cadastre_nr TEXT NOT NULL REFERENCES properties(cadastre_nr),
    object_kind TEXT NOT NULL,
    object_cadastre_nr TEXT NOT NULL,
    share_parts INTEGER,
    nr_of_shares INTEGER
);

CREATE TABLE IF NOT EXISTS parcels (
    cadastre_nr TEXT PRIMARY KEY,                 -- 11 cipari
    status_id INTEGER, status_name TEXT,
    varis_code TEXT,                              -- FK -> aw_eka.kods
    atvk_code TEXT, area REAL, liz_value INTEGER, new_forest_area REAL
);

CREATE TABLE IF NOT EXISTS parcel_land_purposes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parcel_cadastre_nr TEXT NOT NULL REFERENCES parcels(cadastre_nr),
    purpose_id TEXT, purpose_name TEXT, purpose_area REAL,
    agricult_total REAL, areable REAL, orchards REAL, meadows REAL, pastures REAL,
    forest REAL, bushes REAL, swamp REAL, under_water_total REAL, under_fish_ponds REAL,
    flooded REAL, under_buildings REAL, under_roads REAL, other_land REAL, drained REAL
);

CREATE TABLE IF NOT EXISTS parcel_surveys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parcel_cadastre_nr TEXT NOT NULL, survey_kind TEXT, survey_date TEXT
);

CREATE TABLE IF NOT EXISTS parcel_planned (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parcel_cadastre_nr TEXT NOT NULL, varis_code TEXT,
    planned_cadastre_nr TEXT, planned_area REAL
);

CREATE TABLE IF NOT EXISTS parcel_parts (
    cadastre_nr TEXT PRIMARY KEY,                 -- 15 cipari
    parcel_cadastre_nr TEXT NOT NULL, area REAL, liz_value INTEGER
);

CREATE TABLE IF NOT EXISTS parcel_part_land_purposes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parcel_part_cadastre_nr TEXT NOT NULL,
    purpose_id TEXT, purpose_name TEXT, purpose_area REAL,
    agricult_total REAL, areable REAL, orchards REAL, meadows REAL, pastures REAL,
    forest REAL, bushes REAL, swamp REAL, under_water_total REAL, under_fish_ponds REAL,
    flooded REAL, under_buildings REAL, under_roads REAL, other_land REAL, drained REAL
);

CREATE TABLE IF NOT EXISTS buildings (
    cadastre_nr TEXT PRIMARY KEY,                 -- 14 cipari
    parcel_cadastre_nr TEXT,                      -- no ObjectRelation
    varis_code TEXT,                              -- FK -> aw_eka.kods
    name TEXT, use_kind_id TEXT, use_kind_name TEXT,
    area REAL, constr_area REAL,
    ground_floors INTEGER, underground_floors INTEGER,
    material_id TEXT, material_name TEXT, preg_count INTEGER,
    acception_years TEXT, exploit_year INTEGER,
    deprecation TEXT, dep_val_date TEXT, survey_date TEXT,
    not_for_landbook TEXT, prereg TEXT, not_exist TEXT, engineering_type TEXT,
    total_area REAL, expedient_area REAL, flat_total_area REAL, flat_area REAL,
    living_area REAL, flat_aux_area REAL, flat_outer_area REAL,
    nonliving_total REAL, nonliving_interior REAL, nonliving_outer REAL,
    shared_area REAL, shared_interior REAL, shared_outer REAL,
    building_kind_id TEXT, building_kind_name TEXT,
    historical_liter TEXT, historical_name TEXT
);

CREATE TABLE IF NOT EXISTS building_parcels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_cadastre_nr TEXT NOT NULL, parcel_cadastre_nr TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS building_elements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_cadastre_nr TEXT NOT NULL,
    element_name TEXT, material_name TEXT, exploit_year INTEGER
);

CREATE TABLE IF NOT EXISTS building_amounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_cadastre_nr TEXT NOT NULL,
    amount_kind_name TEXT, quantity REAL, measure_kind_name TEXT
);

CREATE TABLE IF NOT EXISTS premise_groups (
    cadastre_nr TEXT PRIMARY KEY,                 -- 17 cipari
    building_cadastre_nr TEXT NOT NULL,
    name TEXT,
    varis_code TEXT,                              -- FK -> aw_dziv.kods
    use_kind_id TEXT, use_kind_name TEXT,
    floor INTEGER, premise_count INTEGER, area REAL,
    survey_date TEXT, acception_years TEXT, not_for_landbook TEXT,
    total_area REAL, expedient_area REAL, flat_total_area REAL, flat_area REAL,
    living_area REAL, flat_aux_area REAL, flat_outer_area REAL,
    nonliving_total REAL, nonliving_interior REAL, nonliving_outer REAL,
    shared_area REAL, shared_interior REAL, shared_outer REAL
);

CREATE TABLE IF NOT EXISTS addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_cadastre_nr TEXT NOT NULL, object_type TEXT NOT NULL,
    ar_code TEXT,                                 -- FK -> aw_eka.kods / aw_dziv.kods
    post_index TEXT, town TEXT, county TEXT, parish TEXT, village TEXT,
    street TEXT, house TEXT, apartment TEXT
);

CREATE TABLE IF NOT EXISTS ownerships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_cadastre_nr TEXT NOT NULL, object_type TEXT NOT NULL,
    ownership_status TEXT, person_status TEXT
);

CREATE TABLE IF NOT EXISTS encumbrances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_cadastre_nr TEXT NOT NULL, object_type TEXT NOT NULL,
    kind_id TEXT, kind_name TEXT, encumbrance_nr INTEGER,
    establish_date TEXT, area REAL, measure TEXT
);

CREATE TABLE IF NOT EXISTS marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_cadastre_nr TEXT NOT NULL, object_type TEXT NOT NULL,
    mark_type TEXT, mark_date TEXT, description TEXT, area REAL
);

CREATE TABLE IF NOT EXISTS valuations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_cadastre_nr TEXT NOT NULL, object_type TEXT NOT NULL,
    value_type TEXT,
    property_valuation REAL, property_val_date TEXT,
    property_cadastral_value REAL, property_cad_val_date TEXT,
    object_cadastral_value REAL, object_cad_val_date TEXT,
    val_description TEXT, forest_value REAL, forest_value_date TEXT
);

CREATE INDEX IF NOT EXISTS idx_po_property   ON property_objects(property_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_po_object     ON property_objects(object_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_parcel_varis  ON parcels(varis_code);
CREATE INDEX IF NOT EXISTS idx_parcel_atvk   ON parcels(atvk_code);
CREATE INDEX IF NOT EXISTS idx_plp_parcel    ON parcel_land_purposes(parcel_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_ps_parcel     ON parcel_surveys(parcel_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_ppl_parcel    ON parcel_planned(parcel_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_ppl_planned   ON parcel_planned(planned_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_pp_parcel     ON parcel_parts(parcel_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_pplp_part     ON parcel_part_land_purposes(parcel_part_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_bldg_parcel   ON buildings(parcel_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_bldg_varis    ON buildings(varis_code);
CREATE INDEX IF NOT EXISTS idx_bp_bldg       ON building_parcels(building_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_bp_parcel     ON building_parcels(parcel_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_be_bldg       ON building_elements(building_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_ba_bldg       ON building_amounts(building_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_pg_building   ON premise_groups(building_cadastre_nr);
CREATE INDEX IF NOT EXISTS idx_pg_varis      ON premise_groups(varis_code);
CREATE INDEX IF NOT EXISTS idx_addr_object   ON addresses(object_cadastre_nr, object_type);
CREATE INDEX IF NOT EXISTS idx_addr_ar       ON addresses(ar_code);
CREATE INDEX IF NOT EXISTS idx_own_object    ON ownerships(object_cadastre_nr, object_type);
CREATE INDEX IF NOT EXISTS idx_enc_object    ON encumbrances(object_cadastre_nr, object_type);
CREATE INDEX IF NOT EXISTS idx_mark_object   ON marks(object_cadastre_nr, object_type);
CREATE INDEX IF NOT EXISTS idx_val_object    ON valuations(object_cadastre_nr, object_type);

-- ================================================================
-- 3. Skati
-- ================================================================

-- Aktuālās ēku adreses ar koordinātēm un pilnu hierarhiju.
CREATE VIEW IF NOT EXISTS v_adrese AS
SELECT e.kods, e.std AS adrese, e.atrib AS pasta_indekss,
       e.for_build, e.dd_n AS lat, e.dd_e AS lon,
       i.nosaukums AS iela, c.nosaukums AS ciems,
       COALESCE(pag.nosaukums, pil.nosaukums) AS pagasts_vai_pilseta,
       nov.nosaukums AS novads
FROM aw_eka e
LEFT JOIN aw_iela   i   ON i.kods   = e.vkur_cd AND e.vkur_tips = '107'
LEFT JOIN aw_ciems  c   ON c.kods   = COALESCE(i.vkur_cd, CASE WHEN e.vkur_tips='106' THEN e.vkur_cd END)
LEFT JOIN aw_pagasts pag ON pag.kods = COALESCE(c.vkur_cd, CASE WHEN e.vkur_tips='105' THEN e.vkur_cd END)
LEFT JOIN aw_pilseta pil ON pil.kods = COALESCE(
       CASE WHEN i.vkur_tips='104' THEN i.vkur_cd END,
       CASE WHEN e.vkur_tips='104' THEN e.vkur_cd END)
LEFT JOIN aw_novads nov ON nov.kods = COALESCE(pag.vkur_cd, pil.vkur_cd)
WHERE e.statuss = 'EKS';

-- Pēdējais katra faila atjaunināšanas stāvoklis.
CREATE VIEW IF NOT EXISTS v_atjauninajumi AS
SELECT fails, datu_kopa, merka_tabula, rindas, baiti,
       lejupieladets, ieladets, substr(sha256, 1, 12) AS sha
FROM avota_fails ORDER BY datu_kopa, fails;

-- Vēsturiskais adreses pieraksts -> tas pats objekts šodien. Adreses kods ir
-- nemainīgs visu objekta mūžu (VAR modelis, 2.4), tāpēc katra aw_vesture rinda
-- ir tieša atslēga no vecā STD teksta uz aktuālo ierakstu attiecīgajā tabulā.
-- aktualais_std ir NULL, ja objekts aktuālajos datos vairs neeksistē.
CREATE VIEW IF NOT EXISTS v_adrese_vesture AS
SELECT v.std        AS vecais_std,
       v.nosaukums  AS vecais_nosaukums,
       v.dat_beig   AS speka_lidz,
       v.kods, v.tips_cd, v.avota_fails,
       COALESCE(e.std, d.std, i.std, c.std, pag.std, pil.std, nov.std) AS aktualais_std,
       COALESCE(e.statuss, d.statuss, i.statuss, c.statuss,
                pag.statuss, pil.statuss, nov.statuss)                 AS aktualais_statuss
FROM aw_vesture v
LEFT JOIN aw_eka     e   ON v.tips_cd = '108' AND e.kods   = v.kods
LEFT JOIN aw_dziv    d   ON v.tips_cd = '109' AND d.kods   = v.kods
LEFT JOIN aw_iela    i   ON v.tips_cd = '107' AND i.kods   = v.kods
LEFT JOIN aw_ciems   c   ON v.tips_cd = '106' AND c.kods   = v.kods
LEFT JOIN aw_pagasts pag ON v.tips_cd = '105' AND pag.kods = v.kods
LEFT JOIN aw_pilseta pil ON v.tips_cd = '104' AND pil.kods = v.kods
LEFT JOIN aw_novads  nov ON v.tips_cd = '113' AND nov.kods = v.kods;
