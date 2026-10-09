-- ============================================================================
-- Ceļu kartes SQLite shēma (celi.db) — NAP valsts ceļu slāņi un notikumi
-- ============================================================================
-- Avoti: transportdata.gov.lv (NAP, LVC) — statiskie GeoJSON/CSV slāņi un
-- reāllaika DATEX II notikumi. Apraksts: PUBLISKO_DATU_IESPEJAS.md; plūsma,
-- API atslēgas pārvaldība un ritmi: PLUSMA.md.
--
-- Dizaina lēmumi:
--  1. Tīrs SQLite (kā visos blokos): līniju/punktu ģeometrijas WKB BLOB +
--     bbox kolonnas; telpiskā apstrāde ielādē/analītikā (shapely, ATTACH ar
--     teritorijas.db robežām). OSM/VZD ģeometrijas šeit NEglabājas (tās paliek
--     failu cauruļvados) — db tur tikai NAP slāņus, kuriem nav cita mājokļa.
--  2. Katalogs (nap_katalogs) pildās BEZ API atslēgas — monitorings strādā
--     uzreiz; slāņu/notikumu tabulas pildās tikai ar atslēgu.
--  3. cela_notikums vēsture TIKAI AUG (katrs pull pievieno jaunas versijas ar
--     ieladets laiku) — ziemas analīzēm vajag hroniku, ne tikai šodienu.
--  4. Viens notikumu tips nāk no vairākiem avotiem (SIC/uzturētāji/
--     meteostacijas) — kopas marķējums katrā rindā, nekad nesapludināt.
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------- ievāksmes

CREATE TABLE ievaks (
    ievaks_id       INTEGER PRIMARY KEY,
    avots           TEXT NOT NULL,          -- 'katalogs' | 'kopa:<dataset_id>'
    savakts         TEXT NOT NULL,
    satura_hash     TEXT,
    ierakstu_skaits INTEGER,
    piezimes        TEXT                    -- NEKAD neierakstīt API atslēgu
) STRICT;

-- ---------------------------------------------------------------- katalogs

-- Visu NAP kopu metadati (no publiskā DCAT — bez atslēgas).
CREATE TABLE nap_katalogs (
    dataset_id     TEXT PRIMARY KEY,        -- NAP kopas identifikators (nid/uuid)
    nosaukums      TEXT NOT NULL,
    nosaukums_lv   TEXT,
    apraksts       TEXT,
    temas          TEXT,                    -- mobilityTheme saraksts (ar ';')
    formats        TEXT,                    -- 'DATEX II V3 XML' | 'GeoJSON' | 'CSV'
    atjaunosana    TEXT,                    -- 'CONT' | 'BIANNUAL' | ...
    izdevejs       TEXT,
    modificets     TEXT,
    abonets        INTEGER NOT NULL DEFAULT 0,   -- vai mūsu atslēga to sedz
    noderiba       TEXT CHECK (noderiba IN ('augsta','videja','zema') OR noderiba IS NULL),
    pedejais_hash  TEXT                     -- pēdējās lejupielādes saturs
) STRICT;

-- ---------------------------------------------------------------- statiskie slāņi

-- Valsts ceļu posmi (tīkls + fiziskie atribūti + klasifikācija + prioritāte).
CREATE TABLE celu_posms (
    posms_id    INTEGER PRIMARY KEY,
    kopa        TEXT NOT NULL,              -- avota dataset_id (izsekojamībai)
    cela_nr     TEXT,                       -- 'A6', 'P80', 'V966'
    klase       TEXT CHECK (klase IN ('A','P','V') OR klase IS NULL),
    nosaukums   TEXT,
    prioritars  INTEGER NOT NULL DEFAULT 0, -- MK 188 prioritārais (ziemā tīra pirmo)
    platums_m   REAL,
    joslas      INTEGER,
    garums_m    REAL,
    atribūti    TEXT,                       -- pārējie avota atribūti JSON formā
    wkb         BLOB NOT NULL,              -- LKS-92 vai WGS84 — kā avotā; norādīts srid
    srid        INTEGER NOT NULL DEFAULT 4326,
    minx REAL NOT NULL, miny REAL NOT NULL, maxx REAL NOT NULL, maxy REAL NOT NULL
) STRICT;
CREATE INDEX idx_posms_nr ON celu_posms(cela_nr);
CREATE INDEX idx_posms_bbox ON celu_posms(minx, maxx, miny, maxy);

-- Punktveida slāņi: ceļa zīmes (ātruma, brīdinājuma), melnie punkti, meteostacijas.
-- Melnie punkti: NAP CSV koordinātu NEDOD; ielādētājs tos bagātina no
-- lvceli.lv pilnā 2020.-2022. XLSX (avota_id=Nr(MP), cela_nr=pamatceļš,
-- atribūti: km + CSNg statistika) un ATVASINĀTĀM koordinātām no
-- dati/slani/melnie_punkti_lv.geojson (km interpolācija ar per-ceļa
-- kalibrāciju + verificēta orientieru ģeokodēšana — atribūtos ticamiba/metode).
-- lat/lon NULL = atvasinājums nav pieejams.
CREATE TABLE cela_punkts (
    punkts_id  INTEGER PRIMARY KEY,
    kopa       TEXT NOT NULL,
    tips       TEXT NOT NULL CHECK (tips IN
               ('atruma_zime','bridinajuma_zime','melnais_punkts','meteostacija')),
    avota_id   TEXT,                        -- avota objekta id (meteostacijai — DATEX id)
    cela_nr    TEXT,
    vertiba    TEXT,                        -- zīmes nr/ātrums/apraksts
    apraksts   TEXT,
    lat REAL, lon REAL,                     -- WGS84; NULL = avotā nav koordinātu
    atribūti   TEXT
) STRICT;
CREATE INDEX idx_punkts_tips ON cela_punkts(tips);
CREATE INDEX idx_punkts_koord ON cela_punkts(lat, lon);

-- Līnijveida papildslāņi: gājēju ceļi, masas/gabarītu ierobežojumu posmi.
CREATE TABLE cela_papildslanis (
    rinda_id   INTEGER PRIMARY KEY,
    kopa       TEXT NOT NULL,
    tips       TEXT NOT NULL CHECK (tips IN ('gajeju_cels','masas_ierobezojums','cits')),
    avota_id   TEXT,                        -- avota objekta id (OBJECTID / mongo id)
    cela_nr    TEXT,
    vertiba    TEXT,                        -- piem. tonnāžas limits
    atribūti   TEXT,                        -- masas: parent_id grupē viena tilta rindas
    wkb        BLOB,
    srid       INTEGER NOT NULL DEFAULT 4326,
    minx REAL, miny REAL, maxx REAL, maxy REAL
) STRICT;

-- ---------------------------------------------------------------- notikumi

-- Reāllaika DATEX II notikumi — vēsture tikai aug.
-- meteo_merijums rindām: datex_id = stacijas id (koordinātas caur cela_punkts
-- tips='meteostacija'), versija = mērījuma laiks, atributi = mērvērtību JSON.
CREATE TABLE cela_notikums (
    notikums_id   INTEGER PRIMARY KEY,
    kopa          TEXT NOT NULL,            -- avota dataset_id (slidens-SIC ≠ slidens-uzturētāji!)
    -- 'laikapstakli' un 'nosprostojums' rezervēti vēl neabonētām kopām
    -- (ārkārtēji laikapstākļi; šķēršļi uz ceļa) — datubaze.py tos šobrīd nepilda.
    tips          TEXT NOT NULL CHECK (tips IN
                  ('slegums','joslas_slegums','remonts','slidens','slikti_apstakli',
                   'laikapstakli','negadijums','nosprostojums','meteo_merijums','cits')),
    datex_id      TEXT,                     -- avota situationRecord id (dedup atslēga)
    versija       TEXT,                     -- avota versija/laiks
    sakums        TEXT,                     -- derīguma sākums (ISO)
    beigas        TEXT,                     -- derīguma beigas (NULL = atvērts)
    cela_nr       TEXT,
    lat REAL, lon REAL,                     -- pirmais/vienīgais punkts (WGS84)
    wkb           BLOB,                     -- pilna līnija, ja notikums ir posms (WGS84)
    apraksts      TEXT,                     -- publiskais komentārs (brīvteksts)
    atributi      TEXT,                     -- papildlauki JSON (xsi tips, mērvērtības...)
    redzets       TEXT,                     -- kad pēdējoreiz redzēts plūsmā (arī bez izmaiņām)
    ieladets      TEXT NOT NULL,            -- kad mēs to novilkām (ISO)
    ievaks_id     INTEGER REFERENCES ievaks(ievaks_id),
    UNIQUE (kopa, datex_id, versija)        -- viens ieraksts uz avota versiju
) STRICT;
CREATE INDEX idx_notikums_tips ON cela_notikums(tips, sakums);
CREATE INDEX idx_notikums_aktivs ON cela_notikums(beigas);

-- ---------------------------------------------------------------- skati

-- Aktīvie notikumi — kartes brīdinājumu slānis. Trīs filtri:
--  1. jaunākā versija katram notikumam;
--  2. derīguma logs (datetime() normalizē ISO ar 'T' un joslu nobīdi uz UTC);
--  3. redzēts pēdējā kopas ievākumā — notikumi ar beigas NULL, kas pazuduši
--     no plūsmas, citādi paliktu "aktīvi" mūžīgi (vēsture tikai aug!).
-- meteo_merijums izslēgts: mērījumi nav notikumi (tiem savs skats).
CREATE VIEW v_aktivie_notikumi AS
SELECT n.tips, n.kopa, n.cela_nr, n.lat, n.lon, n.apraksts,
       n.sakums, n.beigas, n.ieladets
FROM cela_notikums n
WHERE n.tips <> 'meteo_merijums'
  AND (n.beigas IS NULL OR datetime(n.beigas) >= datetime('now'))
  AND n.versija = (SELECT MAX(versija) FROM cela_notikums x
                   WHERE x.kopa = n.kopa AND x.datex_id = n.datex_id)
  AND n.redzets >= (SELECT MAX(i.savakts) FROM ievaks i
                    WHERE i.avots = 'kopa:' || n.kopa);

-- Jaunākie meteostaciju mērījumi (pa stacijām, ar koordinātām no cela_punkts).
CREATE VIEW v_meteo_jaunakie AS
SELECT n.datex_id AS stacija_id, p.vertiba AS stacija, p.lat, p.lon,
       n.versija AS merits, n.atributi
FROM cela_notikums n
LEFT JOIN cela_punkts p ON p.tips = 'meteostacija' AND p.avota_id = n.datex_id
WHERE n.tips = 'meteo_merijums'
  AND n.versija = (SELECT MAX(versija) FROM cela_notikums x
                   WHERE x.kopa = n.kopa AND x.datex_id = n.datex_id);

-- Prioritārie ceļi (ziemas drošāko maršrutu slānis). Tikai tīkla kopa —
-- celu_posms tur 3 pārklājošas tīkla reprezentācijas (tikls/klasifikacija/
-- prioritarie), bez kopa filtra viens ceļš zīmētos 3 reizes!
CREATE VIEW v_prioritarie_celi AS
SELECT cela_nr, klase, nosaukums, garums_m, wkb, srid, minx, miny, maxx, maxy
FROM celu_posms WHERE prioritars = 1 AND kopa = 'valsts_celu_tikls';

-- Drošības punkti kartei (melnie punkti + brīdinājuma zīmes).
CREATE VIEW v_drosibas_punkti AS
SELECT tips, cela_nr, vertiba, apraksts, lat, lon
FROM cela_punkts WHERE tips IN ('melnais_punkts', 'bridinajuma_zime');

-- ============================================================================
-- PARAUGA APRĒĶINI, ko shēma atbalsta (ATTACH ar citiem blokiem):
--
-- 1) Melnie punkti 500 m rādiusā ap pieturām, ko lieto skolēnu maršruti:
--    ATTACH '../sabiedriskais-transports/dati/transports.db' AS tr;
--    SELECT p.vertiba, p.lat, p.lon, pk.nosaukums pietura
--    FROM cela_punkts p
--    JOIN tr.pieturu_klasteris pk
--      ON ABS(pk.lat - p.lat) < 0.006 AND ABS(pk.lon - p.lon) < 0.010
--    WHERE p.tips='melnais_punkts'
--      AND 111190*SQRT((pk.lat-p.lat)*(pk.lat-p.lat)
--            + ((pk.lon-p.lon)*0.545)*((pk.lon-p.lon)*0.545)) <= 500;
--
-- 2) Cik bieži ziemā slidens katrā ceļā (sezonas hronika):
--    SELECT cela_nr, COUNT(DISTINCT date(sakums)) dienas
--    FROM cela_notikums WHERE tips='slidens'
--      AND sakums BETWEEN '2026-11-01' AND '2027-03-31'
--    GROUP BY cela_nr ORDER BY dienas DESC;
--
-- 3) Slidenā ceļa notikumi pa pagastiem (ATTACH teritorijas.db robežas +
--    shapely point-in-polygon Python pusē pēc bbox priekšatlases).
-- ============================================================================
