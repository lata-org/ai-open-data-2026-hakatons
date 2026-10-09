"""Lejupielādē un ielādē VZD atvērtos datus SQLite datubāzē dati/kadastrs.db.

Paredzēts regulārai palaišanai. Katram failam tiek glabāta SHA-256 jaucējsumma;
ja avots nav mainījies, ielāde tiek izlaista. Ielāde katrai tabulai notiek vienā
transakcijā (vecais saturs tiek aizstāts tikai tad, ja jaunais ir nolasīts veiksmīgi),
tāpēc pārtraukts palaidums neatstāj datubāzi pa pusei atjauninātu.

    uv run --no-project --with httpx --with certifi atjaunot.py               # VAR aktuālie + vēsturiskie dati
    uv run --no-project --with httpx --with certifi atjaunot.py --bez-vestures  # tikai aktuālie (ātrāk)
    uv run --no-project --with httpx --with certifi atjaunot.py --dokumenti   # + dokumentu metadati
    uv run --no-project --with httpx --with certifi atjaunot.py --nivkis      # + kadastra dati (XML)
    uv run --no-project --with httpx --with certifi atjaunot.py --tikai aw_eka.csv,aw_iela.csv
    uv run --no-project --with httpx --with certifi atjaunot.py --statuss     # tikai parāda stāvokli

Avota apraksti: VAR_ATVERTIE_DATI_MODELIS.md, NIVKIS_ATVERTIE_DATI_MODELIS.md
"""

import argparse
import csv
import hashlib
import io
import pathlib
import sqlite3
import sys
import zipfile
from datetime import datetime, timezone
from xml.etree import ElementTree as ET

import httpx

# Windows konsole pēc noklusējuma lieto cp1252, kas nespēj attēlot latviešu burtus —
# print() krīt ar UnicodeEncodeError un pārtrauc atjaunināšanu pusceļā.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HERE = pathlib.Path(__file__).resolve().parent
DATI = HERE / "dati"
LEJUP = DATI / "lejupielades"
DB = DATI / "kadastrs.db"
SHEMA = HERE / "shema.sql"

VAR_BAZE = "https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource"
NIV_BAZE = "https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource"

# fails -> (resursa_id, mērķa tabula, grupa)
VAR_FAILI = {
    "aw_novads.csv":           ("c62c60bb-58d4-4f26-82c0-5b630769f9d1", "aw_novads", "aktuali"),
    "aw_pilseta.csv":          ("ee02baa4-2bc3-4f77-a6cb-5427a3e9befe", "aw_pilseta", "aktuali"),
    "aw_pagasts.csv":          ("6ba8c905-27a1-443a-b9c6-256a0777425b", "aw_pagasts", "aktuali"),
    "aw_ciems.csv":            ("0d3810f4-1ac0-4fba-8b10-0188084a361b", "aw_ciems", "aktuali"),
    "aw_iela.csv":             ("3c4ab802-76cf-433c-9c1c-89215e28d833", "aw_iela", "aktuali"),
    "aw_eka.csv":              ("a510737a-18ce-400f-ad4b-04fce5228272", "aw_eka", "aktuali"),
    "aw_dziv.csv":             ("b83be373-f444-4f50-9b98-28741845325e", "aw_dziv", "aktuali"),
    "aw_rajons.csv":           ("e7f17c92-fad4-4153-bef5-670a321c4ec1", "aw_rajons", "aktuali"),
    "aw_ppils.csv":            ("21856ec7-8592-40d6-9e65-b23117348c98", "aw_ppils", "aktuali"),
    "aw_vietu_centroidi.csv":  ("68f1152c-0f4c-4fc3-abb3-df4b8bfea992", "aw_vietu_centroidi", "aktuali"),
    "aw_pilseta_his.csv":      ("87e2c4e5-13d9-4142-9052-8a6e9f094479", "aw_vesture", "vesture"),
    "aw_novads_his.csv":       ("c5c3d570-1596-49f2-a486-53439b449641", "aw_vesture", "vesture"),
    "aw_pagasts_his.csv":      ("5950bf88-4441-470f-9e13-efcbd79bc1f0", "aw_vesture", "vesture"),
    "aw_ciems_his.csv":        ("c8f34472-8ca4-40d5-9c84-05b24dc19afe", "aw_vesture", "vesture"),
    "aw_iela_his.csv":         ("a7461a4e-4407-4506-9333-a50c4f51b328", "aw_vesture", "vesture"),
    "aw_eka_his.csv":          ("d07443d7-15a8-4db6-9e53-7a68eec3c0dd", "aw_vesture", "vesture"),
    "aw_dziv_his.csv":         ("26e63e84-c04d-40b5-9c37-0ca9d08789ad", "aw_vesture", "vesture"),
    "aw_doc_nl.csv":           ("7d98b01c-60d3-46e6-8583-320a83301174", "aw_doc", "dokumenti"),
    "aw_doc_tg.csv":           ("b1552dfe-605f-4260-9602-e5e6886bb754", "aw_doc", "dokumenti"),
    "aw_doc_vieta.csv":        ("2dbe69b1-6b14-4f35-98b8-2a64119af163", "aw_doc", "dokumenti"),
}

NIVKIS_FAILI = {
    "property.zip":     ("931e6299-61ba-477b-ba8d-f0fb30db9667", "properties"),
    "parcel.zip":       ("1618f19a-c818-4966-8183-a2e3c108597a", "parcels"),
    "parcelpart.zip":   ("58635c63-8c04-4193-a9f2-ec674c57ae93", "parcel_parts"),
    "building.zip":     ("9fe29b57-07cd-4458-b22c-b0b9f2bc8915", "buildings"),
    "premisegroup.zip": ("5d8b1cfa-1e67-4b77-a6ac-b4e37eba0d7e", "premise_groups"),
    "address.zip":      ("2aeea249-6948-4713-92c2-e01543ea0f33", "addresses"),
    "ownership.zip":    ("a0d801da-8eb0-4426-9087-50e8139bce39", "ownerships"),
    "encumbrance.zip":  ("ca8a415c-a894-427f-b14d-d1e44c582620", "encumbrances"),
    "mark.zip":         ("9417c9f2-5961-492d-8606-ca84a5b41386", "marks"),
    "valuation.zip":    ("35a2dbfa-e4b9-41d5-88d0-e1393115dcb1", "valuations"),
}

# Kolonnas, kuras CSV ielādē jāpārvērš skaitļos (pārējās paliek teksts, kā prasa modelis).
REALI = {"koord_x", "koord_y", "dd_e", "dd_n"}

# Vēsturisko failu mērķa kolonnas (visi ielādējas vienā aw_vesture tabulā).
VESTURE_KOL = ["kods", "tips_cd", "nosaukums", "vkur_cd", "vkur_tips",
               "dat_sak", "dat_mod", "dat_beig", "std", "kods_his"]


def tagad():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for gab in iter(lambda: fh.read(1 << 20), b""):
            h.update(gab)
    return h.hexdigest()


def lejupieladet(client, url, merkis):
    pagaidu = merkis.with_suffix(merkis.suffix + ".daljejs")
    with client.stream("GET", url) as r:
        r.raise_for_status()
        with open(pagaidu, "wb") as fh:
            for gab in r.iter_bytes(1 << 20):
                fh.write(gab)
    pagaidu.replace(merkis)          # atomiski — nepilnīgs fails nekad nepaliek
    return merkis


def csv_rindas(path):
    """Atgriež (galvenes, rindu ģenerators). Kodējums utf-8-sig noņem BOM."""
    fh = open(path, "r", encoding="utf-8-sig", newline="")
    lasitajs = csv.reader(fh)
    galvene = [h.strip().lower() for h in next(lasitajs)]
    return galvene, lasitajs, fh


def ieladet_csv(con, fails, tabula, path):
    """Ielādē CSV tabulā. Kolonnas kartē pēc NOSAUKUMA, ne pēc secības."""
    galvene, rindas, fh = csv_rindas(path)
    try:
        db_kol = [r[1] for r in con.execute(f"PRAGMA table_info({tabula})")]
        if tabula == "aw_vesture":
            merki = [k for k in VESTURE_KOL if k in galvene]
            papildu, papildu_vert = ["avota_fails"], [fails.replace(".csv", "")]
        elif tabula == "aw_doc":
            merki = [k for k in galvene if k in db_kol]
            papildu, papildu_vert = [], []
        else:
            merki = [k for k in galvene if k in db_kol]
            papildu, papildu_vert = [], []

        nezinami = [k for k in galvene if k not in db_kol and k not in ("kods_his",)]
        if tabula == "aw_vesture":
            nezinami = [k for k in galvene if k not in VESTURE_KOL]
        if nezinami:
            print(f"      ! avotā ir kolonnas, kuru shēmā nav: {nezinami}")

        idx = {k: galvene.index(k) for k in merki}
        kol = merki + papildu
        sql = f"INSERT INTO {tabula} ({','.join(kol)}) VALUES ({','.join('?' * len(kol))})"

        def sagatavot(r):
            vert = []
            for k in merki:
                v = r[idx[k]].strip() if idx[k] < len(r) else ""
                if v == "":
                    vert.append(None)
                elif k in REALI:
                    try:
                        vert.append(float(v))
                    except ValueError:
                        vert.append(None)
                else:
                    vert.append(v)
            return vert + papildu_vert

        con.execute("BEGIN")
        if tabula in ("aw_vesture", "aw_doc"):
            con.execute(f"DELETE FROM {tabula} WHERE avota_fails = ?"
                        if tabula == "aw_vesture" else
                        "DELETE FROM aw_doc WHERE adreses_veids = ?",
                        (fails.replace(".csv", "") if tabula == "aw_vesture"
                         else fails.replace("aw_doc_", "").replace(".csv", "").upper(),))
        else:
            con.execute(f"DELETE FROM {tabula}")
        n = 0
        partija = []
        for r in rindas:
            if not r:
                continue
            partija.append(sagatavot(r))
            n += 1
            if len(partija) >= 20000:
                con.executemany(sql, partija)
                partija.clear()
        if partija:
            con.executemany(sql, partija)
        con.execute("COMMIT")
        return n
    except Exception:
        con.execute("ROLLBACK")
        raise
    finally:
        fh.close()


# ---------------------------------------------------------------- NĪVKIS XML

def bez_nosaukumvietas(sakne):
    """NĪVKIS XML lieto noklusēto xmlns, tāpēc ElementTree tagi ir '{ns}Tag'.
    Bez šī `find('ObjectRelation')` neatrod neko un tabulas paliek tukšas."""
    for el in sakne.iter():
        if isinstance(el.tag, str) and el.tag.startswith("{"):
            el.tag = el.tag.split("}", 1)[1]
    return sakne


def teksts(el, cels):
    if el is None:
        return None
    x = el.find(cels)
    if x is None or x.text is None:
        return None
    v = x.text.strip()
    return v or None


def skaitlis(el, cels):
    v = teksts(el, cels)
    if v is None:
        return None
    try:
        return float(v.replace(",", "."))
    except ValueError:
        return None


def vesels(el, cels):
    v = skaitlis(el, cels)
    return int(v) if v is not None else None


def eksplikacija(it):
    """BuildingOrPremiseGroupExplicationData -> 13 kolonnu virkne."""
    e = it.find(".//BuildingOrPremiseGroupExplicationData")
    if e is None:
        return [None] * 13
    return [
        skaitlis(e, "TotalArea"),
        skaitlis(e, "TotalAreaDetails/ExpedientArea"),
        skaitlis(e, ".//FlatTotalArea"),
        skaitlis(e, ".//FlatArea"),
        skaitlis(e, ".//LivingArea"),
        skaitlis(e, ".//FlatAuxArea"),
        skaitlis(e, ".//FlatOuterArea"),
        skaitlis(e, ".//NonlivingTotalArea"),
        skaitlis(e, ".//NonlivingInteriorArea"),
        skaitlis(e, ".//NonlivingOuterArea"),
        skaitlis(e, ".//SharedArea"),
        skaitlis(e, ".//SharedInteriorArea"),
        skaitlis(e, ".//SharedOuterArea"),
    ]


def zemes_merki(it, saknes_kods):
    for lp in it.findall(".//LandPurposeData"):
        ex = lp.find("LandPurposeExplicationData")
        yield [saknes_kods,
               teksts(lp, "LandPurposeKind/LandPurposeKindId"),
               teksts(lp, "LandPurposeKind/LandPurposeKindName"),
               skaitlis(lp, "LandPurposeArea")] + (
            [skaitlis(ex, "AgricultTotal"), skaitlis(ex, ".//Areable"),
             skaitlis(ex, ".//Orchards"), skaitlis(ex, ".//Meadows"),
             skaitlis(ex, ".//Pastures"), skaitlis(ex, "Forest"),
             skaitlis(ex, "Bushes"), skaitlis(ex, "Swamp"),
             skaitlis(ex, "UnderWaterTotal"), skaitlis(ex, ".//UnderFishPonds"),
             skaitlis(ex, ".//Flooded"), skaitlis(ex, "UnderBuildings"),
             skaitlis(ex, "UnderRoads"), skaitlis(ex, "OtherLand"),
             skaitlis(ex, "Drained")] if ex is not None else [None] * 15)


def nivkis_ieraksti(it, veids):
    """Atgriež {tabula: [rindu saraksts]} vienam ItemData elementam."""
    r = {}
    orel = it.find("ObjectRelation")
    ock = teksts(orel, "ObjectCadastreNr") if orel is not None else None
    otyp = teksts(orel, "ObjectType") if orel is not None else None

    if veids == "property":
        kn = teksts(it, ".//ProCadastreNr")
        r["properties"] = [[kn, teksts(it, ".//PropertyKind"),
                            teksts(it, ".//ShareFlatProperty"), teksts(it, ".//PropertyName"),
                            skaitlis(it, ".//PropertyParcelTotalArea"),
                            skaitlis(it, ".//PropertyPremiseGroupTotalArea"),
                            teksts(it, ".//LandbookFolioNr"),
                            teksts(it, ".//LandbookFolioLiterNr"),
                            teksts(it, ".//LandbookOfficeName"),
                            teksts(it, ".//NotCorroboratedInLandbook")]]
        r["property_objects"] = [[kn, teksts(o, "ObjectKindData"),
                                  teksts(o, "ObjectCadastreNrData"),
                                  vesels(o, "ShareParts"), vesels(o, "NrOfShares")]
                                 for o in it.findall(".//ObjectData")]
    elif veids == "parcel":
        kn = teksts(it, ".//ParcelCadastreNr")
        r["parcels"] = [[kn, vesels(it, ".//ParcelStatusKindId"),
                         teksts(it, ".//ParcelStatusKindName"), teksts(it, ".//ParcelVARISCode"),
                         teksts(it, ".//ATVKCode"), skaitlis(it, ".//ParcelArea"),
                         vesels(it, ".//ParcelLizValue"), skaitlis(it, ".//NewForestArea")]]
        r["parcel_land_purposes"] = list(zemes_merki(it, kn))
        r["parcel_surveys"] = [[kn, teksts(s, "SurveyKind"), teksts(s, "SurveyDate")]
                               for s in it.findall(".//SurveyData")]
        r["parcel_planned"] = [[kn, teksts(p, "VARISCode"),
                                teksts(p, "PlannedParcelCadastreNr"),
                                skaitlis(p, "PlannedParcelArea")]
                               for p in it.findall(".//PlannedParcelData")]
    elif veids == "parcelpart":
        kn = teksts(it, ".//ParcelPartCadastreNr")
        r["parcel_parts"] = [[kn, ock, skaitlis(it, ".//ParcelPartArea"),
                              vesels(it, ".//ParcelPartLizValue")]]
        r["parcel_part_land_purposes"] = list(zemes_merki(it, kn))
    elif veids == "building":
        kn = teksts(it, ".//BuildingCadastreNr")
        r["buildings"] = [[kn, ock, teksts(it, ".//VARISCode"), teksts(it, ".//BuildingName"),
                           teksts(it, ".//BuildingUseKindId"), teksts(it, ".//BuildingUseKindName"),
                           skaitlis(it, ".//BuildingArea"), skaitlis(it, ".//BuildingConstrArea"),
                           vesels(it, ".//BuildingGroundFloors"),
                           vesels(it, ".//BuildingUndergroundFloors"),
                           teksts(it, ".//BuildingMaterialKind/MaterialKindId"),
                           teksts(it, ".//BuildingMaterialKind/MaterialKindName"),
                           vesels(it, ".//BuildingPregCount"),
                           teksts(it, ".//BuildingAcceptionYears"),
                           vesels(it, ".//BuildingExploitYear"),
                           teksts(it, ".//BuildingDeprecation"),
                           teksts(it, ".//BuildingDepValDate"),
                           teksts(it, ".//BuildingSurveyDate"), teksts(it, ".//NotForLandBook"),
                           teksts(it, ".//Prereg"), teksts(it, ".//NotExist"),
                           teksts(it, ".//EngineeringStructureType")] + eksplikacija(it) + [
                          teksts(it, ".//BuildingKind/BuildingKindId"),
                          teksts(it, ".//BuildingKind/BuildingKindName"),
                          teksts(it, ".//BuildingHistoricalLiter"),
                          teksts(it, ".//BuildingHistoricalName")]]
        r["building_parcels"] = [[kn, p.text.strip()] for p in
                                 it.findall(".//ParcelCadastreNrList/ObjectCadastreNrData")
                                 if p.text and p.text.strip()]
        r["building_elements"] = [[kn, teksts(b, "BuildingElementName"),
                                   teksts(b, ".//MaterialKindName"),
                                   vesels(b, "BuildingElementExploitYear")]
                                  for b in it.findall(".//BuildingElementData")]
        r["building_amounts"] = [[kn, teksts(a, ".//AmountKindName"),
                                  skaitlis(a, "BuildingAmountQuantity"),
                                  teksts(a, ".//MeasureKindName")]
                                 for a in it.findall(".//BuildingAmountData")]
    elif veids == "premisegroup":
        kn = teksts(it, ".//PremiseGroupCadastreNr")
        r["premise_groups"] = [[kn, ock, teksts(it, ".//PremiseGroupName"),
                                teksts(it, ".//PremiseGroupVARISCode"),
                                teksts(it, ".//PremiseGroupUseKindId"),
                                teksts(it, ".//PremiseGroupUseKindName"),
                                vesels(it, ".//PremiseGroupBuildingFloor"),
                                vesels(it, ".//PremiseGroupPremiseCount"),
                                skaitlis(it, ".//PremiseGroupArea"),
                                teksts(it, ".//PremiseGroupSurveyDate"),
                                teksts(it, ".//PremiseGroupAcceptionYears"),
                                teksts(it, ".//NotForLandBook")] + eksplikacija(it)]
    elif veids == "address":
        r["addresses"] = [[ock, otyp, teksts(a, "ARCode"), teksts(a, "PostIndex"),
                           teksts(a, "Town"), teksts(a, "County"), teksts(a, "Parish"),
                           teksts(a, "Village"), teksts(a, "Street"), teksts(a, "House"),
                           teksts(a, "Apartment")] for a in it.findall(".//AddressData")]
    elif veids == "ownership":
        r["ownerships"] = [[ock, otyp, teksts(o, "OwnershipStatus"), teksts(o, "PersonStatus")]
                           for o in it.findall(".//OwnershipStatusKind")]
    elif veids == "encumbrance":
        r["encumbrances"] = [[ock, otyp, teksts(e, ".//EncumbranceKindId"),
                              teksts(e, ".//EncumbranceKindName"), vesels(e, "EncumbranceNr"),
                              teksts(e, "EncumbranceEstablishDate"),
                              skaitlis(e, "EncumbranceArea"), teksts(e, "EncumbranceMeasure")]
                             for e in it.findall(".//EncumbranceRowData")]
    elif veids == "mark":
        r["marks"] = [[ock, otyp, teksts(m, "MarkType"), teksts(m, "MarkDate"),
                       teksts(m, "MarkDescription"), skaitlis(m, "MarkArea")]
                      for m in it.findall(".//MarkRecData")]
    elif veids == "valuation":
        r["valuations"] = [[ock, otyp, teksts(v, "ValueType"), skaitlis(v, "PropertyValuation"),
                            teksts(v, "PropertyValuationDate"),
                            skaitlis(v, "PropertyCadastralValue"),
                            teksts(v, "PropertyCadastralValueDate"),
                            skaitlis(v, "ObjectCadastralValue"),
                            teksts(v, "ObjectCadastralValueDate"), teksts(v, "ValDescription"),
                            skaitlis(v, "ObjectForestValue"), teksts(v, "ObjectForestValueDate")]
                           for v in it.findall(".//ValuationRowData")]
    return r


NIVKIS_KOL = {
    "properties": "cadastre_nr,property_kind,share_flat_property,property_name,parcel_total_area,"
                  "premise_group_total_area,landbook_folio_nr,landbook_folio_liter,landbook_office,"
                  "not_corroborated",
    "property_objects": "property_cadastre_nr,object_kind,object_cadastre_nr,share_parts,nr_of_shares",
    "parcels": "cadastre_nr,status_id,status_name,varis_code,atvk_code,area,liz_value,new_forest_area",
    "parcel_land_purposes": "parcel_cadastre_nr,purpose_id,purpose_name,purpose_area,agricult_total,"
                            "areable,orchards,meadows,pastures,forest,bushes,swamp,under_water_total,"
                            "under_fish_ponds,flooded,under_buildings,under_roads,other_land,drained",
    "parcel_surveys": "parcel_cadastre_nr,survey_kind,survey_date",
    "parcel_planned": "parcel_cadastre_nr,varis_code,planned_cadastre_nr,planned_area",
    "parcel_parts": "cadastre_nr,parcel_cadastre_nr,area,liz_value",
    "parcel_part_land_purposes": "parcel_part_cadastre_nr,purpose_id,purpose_name,purpose_area,"
                                 "agricult_total,areable,orchards,meadows,pastures,forest,bushes,"
                                 "swamp,under_water_total,under_fish_ponds,flooded,under_buildings,"
                                 "under_roads,other_land,drained",
    "buildings": "cadastre_nr,parcel_cadastre_nr,varis_code,name,use_kind_id,use_kind_name,area,"
                 "constr_area,ground_floors,underground_floors,material_id,material_name,preg_count,"
                 "acception_years,exploit_year,deprecation,dep_val_date,survey_date,not_for_landbook,"
                 "prereg,not_exist,engineering_type,total_area,expedient_area,flat_total_area,"
                 "flat_area,living_area,flat_aux_area,flat_outer_area,nonliving_total,"
                 "nonliving_interior,nonliving_outer,shared_area,shared_interior,shared_outer,"
                 "building_kind_id,building_kind_name,historical_liter,historical_name",
    "building_parcels": "building_cadastre_nr,parcel_cadastre_nr",
    "building_elements": "building_cadastre_nr,element_name,material_name,exploit_year",
    "building_amounts": "building_cadastre_nr,amount_kind_name,quantity,measure_kind_name",
    "premise_groups": "cadastre_nr,building_cadastre_nr,name,varis_code,use_kind_id,use_kind_name,"
                      "floor,premise_count,area,survey_date,acception_years,not_for_landbook,"
                      "total_area,expedient_area,flat_total_area,flat_area,living_area,flat_aux_area,"
                      "flat_outer_area,nonliving_total,nonliving_interior,nonliving_outer,"
                      "shared_area,shared_interior,shared_outer",
    "addresses": "object_cadastre_nr,object_type,ar_code,post_index,town,county,parish,village,"
                 "street,house,apartment",
    "ownerships": "object_cadastre_nr,object_type,ownership_status,person_status",
    "encumbrances": "object_cadastre_nr,object_type,kind_id,kind_name,encumbrance_nr,"
                    "establish_date,area,measure",
    "marks": "object_cadastre_nr,object_type,mark_type,mark_date,description,area",
    "valuations": "object_cadastre_nr,object_type,value_type,property_valuation,property_val_date,"
                  "property_cadastral_value,property_cad_val_date,object_cadastral_value,"
                  "object_cad_val_date,val_description,forest_value,forest_value_date",
}


TABULAS_PA_VEIDIEM = {
    "property": ["properties", "property_objects"],
    "parcel": ["parcels", "parcel_land_purposes", "parcel_surveys", "parcel_planned"],
    "parcelpart": ["parcel_parts", "parcel_part_land_purposes"],
    "building": ["buildings", "building_parcels", "building_elements", "building_amounts"],
    "premisegroup": ["premise_groups"],
    "address": ["addresses"],
    "ownership": ["ownerships"],
    "encumbrance": ["encumbrances"],
    "mark": ["marks"],
    "valuation": ["valuations"],
}


def ieladet_nivkis_zip(con, fails, path):
    veids = fails.replace(".zip", "")
    merki = TABULAS_PA_VEIDIEM[veids]

    def izgazt(buferi, vismaz):
        ielikts = 0
        for tab, buf in buferi.items():
            if len(buf) >= vismaz and buf:
                kol = NIVKIS_KOL[tab]
                con.executemany(f"INSERT INTO {tab} ({kol}) VALUES "
                                f"({','.join('?' * len(kol.split(',')))})", buf)
                ielikts += len(buf)
                buf.clear()
        return ielikts

    con.execute("BEGIN")
    try:
        for t in merki:
            con.execute(f"DELETE FROM {t}")
        rindas_kopa = 0
        buferi = {t: [] for t in merki}
        with zipfile.ZipFile(path) as z:
            for nosaukums in (n for n in z.namelist() if n.lower().endswith(".xml")):
                sakne = bez_nosaukumvietas(ET.parse(io.BytesIO(z.read(nosaukums))).getroot())
                for it in sakne.iter():
                    if not it.tag.endswith("ItemData"):
                        continue
                    for tab, rindas in nivkis_ieraksti(it, veids).items():
                        if rindas:
                            buferi[tab].extend(rindas)
                rindas_kopa += izgazt(buferi, 20000)
        rindas_kopa += izgazt(buferi, 1)
        con.execute("COMMIT")
        return rindas_kopa
    except Exception:
        con.execute("ROLLBACK")
        raise


# ---------------------------------------------------------------- galvenā plūsma

def apstradat(con, client, fails, resursa_id, tabula, baze, datu_kopa, piespiest):
    url = f"{baze}/{resursa_id}/download/{fails}"
    merkis = LEJUP / fails
    print(f"  {fails}")
    lejupieladet(client, url, merkis)
    h = sha256(merkis)
    baiti = merkis.stat().st_size
    iepr = con.execute("SELECT sha256, rindas FROM avota_fails WHERE fails=?", (fails,)).fetchone()
    if iepr and iepr[0] == h and not piespiest:
        print(f"      nav mainījies ({baiti/1e6:.1f} MB, {iepr[1]} rindas) — izlaists")
        con.execute("UPDATE avota_fails SET lejupieladets=? WHERE fails=?", (tagad(), fails))
        con.commit()
        return 0, False
    n = (ieladet_nivkis_zip(con, fails, merkis) if fails.endswith(".zip")
         else ieladet_csv(con, fails, tabula, merkis))
    con.execute("""INSERT INTO avota_fails
        (fails, datu_kopa, merka_tabula, resursa_id, url, lejupieladets, ieladets, sha256, baiti, rindas)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(fails) DO UPDATE SET lejupieladets=excluded.lejupieladets,
            ieladets=excluded.ieladets, sha256=excluded.sha256, baiti=excluded.baiti,
            rindas=excluded.rindas, merka_tabula=excluded.merka_tabula""",
        (fails, datu_kopa, tabula, resursa_id, url, tagad(), tagad(), h, baiti, n))
    con.commit()
    print(f"      ielādēts {n} ierakstu ({baiti/1e6:.1f} MB)")
    return n, True


def statuss(con):
    print(f"{'fails':26} {'tabula':22} {'rindas':>9} {'MB':>7}  ielādēts")
    for r in con.execute("SELECT fails, merka_tabula, rindas, baiti, ieladets "
                         "FROM avota_fails ORDER BY datu_kopa, fails"):
        print(f"{r[0]:26} {(r[1] or ''):22} {(r[2] or 0):>9} {(r[3] or 0)/1e6:>7.1f}  {r[4] or ''}")
    print()
    for t in ("aw_novads", "aw_pilseta", "aw_pagasts", "aw_ciems", "aw_iela", "aw_eka",
              "aw_dziv", "aw_ppils", "aw_vietu_centroidi", "aw_rajons", "aw_doc", "aw_vesture",
              "properties", "parcels", "buildings", "premise_groups", "addresses"):
        try:
            n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        except sqlite3.OperationalError:
            continue
        if n:
            print(f"  {t:22} {n:>9}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vesture", action="store_true",
                    help="novecojis: vēsturiskie faili tagad ielādējas pēc noklusējuma")
    ap.add_argument("--bez-vestures", action="store_true",
                    help="izlaist vēsturiskos failus (~390 MB lejupielāde)")
    ap.add_argument("--dokumenti", action="store_true", help="ielādēt arī dokumentu metadatus (~220 MB)")
    ap.add_argument("--nivkis", action="store_true", help="ielādēt arī NĪVKIS kadastra datus (~620 MB)")
    ap.add_argument("--tikai", help="komatatdalīts failu saraksts")
    ap.add_argument("--piespiest", action="store_true", help="ielādēt arī tad, ja fails nav mainījies")
    ap.add_argument("--statuss", action="store_true", help="tikai parādīt datubāzes stāvokli")
    args = ap.parse_args()

    DATI.mkdir(exist_ok=True)
    LEJUP.mkdir(exist_ok=True)
    con = sqlite3.connect(DB)
    con.executescript(SHEMA.read_text(encoding="utf-8"))

    if args.statuss:
        statuss(con)
        return 0

    darbs = []
    for f, (rid, tab, grupa) in VAR_FAILI.items():
        if grupa == "aktuali" or (grupa == "vesture" and not args.bez_vestures) \
                or (grupa == "dokumenti" and args.dokumenti):
            darbs.append((f, rid, tab, VAR_BAZE, "VAR"))
    if args.nivkis:
        darbs += [(f, rid, tab, NIV_BAZE, "NIVKIS") for f, (rid, tab) in NIVKIS_FAILI.items()]
    if args.tikai:
        atlase = {x.strip() for x in args.tikai.split(",")}
        darbs = [d for d in darbs if d[0] in atlase]
        if not darbs:
            print(f"Nekas neatbilst --tikai {args.tikai}", file=sys.stderr)
            return 1

    cur = con.execute("INSERT INTO atjauninajums (sakts, datu_kopa) VALUES (?,?)",
                      (tagad(), "NIVKIS" if args.nivkis else "VAR"))
    palaid_id = cur.lastrowid
    con.commit()

    kopa = mainiti = 0
    print(f"Atjaunoju {len(darbs)} failus -> {DB}")
    with httpx.Client(timeout=httpx.Timeout(60, read=600), follow_redirects=True,
                      headers={"User-Agent": "ogre-izglitiba/1.0 (VZD atvertie dati)"}) as client:
        for f, rid, tab, baze, dk in darbs:
            try:
                n, mainijas = apstradat(con, client, f, rid, tab, baze, dk, args.piespiest)
                kopa += n
                mainiti += 1 if mainijas else 0
            except Exception as exc:  # noqa: BLE001
                print(f"      KĻŪDA: {exc!r}", file=sys.stderr)

    con.execute("""UPDATE atjauninajums SET beidzies=?, faili_parbaditi=?, faili_mainiti=?,
                   rindas_ieladetas=? WHERE id=?""",
                (tagad(), len(darbs), mainiti, kopa, palaid_id))
    con.execute("ANALYZE")
    con.commit()
    print(f"\nPabeigts: {len(darbs)} faili pārbaudīti, {mainiti} atjaunoti, {kopa} rindas.")
    print(f"Datubāze: {DB} ({DB.stat().st_size / 1e6:.0f} MB)")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
