"""
Nomenclature Engine – Single File Demo
-------------------------------------
Purpose:
- Normalize raw panel purchase data
- Apply shop synonyms & main-shop logic
- Apply Perso nomenclature rules (GO71 / DBIO12)
- Enrich with CME / BSC / CMC

Audience:
- DSM / Product / Architecture review
"""

from dataclasses import dataclass
from typing import Optional, Dict
# 1. DATA MODELS
@dataclass
class RawPurchase:
    household_id: str
    product_code: str
    raw_shop_name: str
    basket_size: int
    purchase_time: str


@dataclass
class EnrichedPurchase:
    household_id: str
    product_code: str
    shop: str
    main_shop: str
    cme: str
    bsc: str
    cmc: Optional[str]

# 2. REFERENCE TABLES (shoplist / mainshop)
class ShopList:
    """Resolves raw shop names using synonym mapping"""

    def __init__(self, synonyms: Dict[str, str]):
        self.synonyms = {k.lower(): v for k, v in synonyms.items()}

    def normalize(self, raw_shop: str) -> str:
        return self.synonyms.get(raw_shop.lower(), "Unknown Shop")


class MainShop:
    """Maps shops to their main (master) shop"""

    def __init__(self, mapping: Dict[str, str]):
        self.mapping = mapping

    def get(self, shop: str) -> str:
        return self.mapping.get(shop, shop)

# 3. PERSO NOMENCLATURE (GO71 / DBIO12)
class PersoNomenclature:
    """Client / study specific grouping"""

    def __init__(self, rules: Dict[str, str], name: str):
        self.rules = rules
        self.name = name

    def apply(self, shop: str) -> str:
        return self.rules.get(shop, shop)

# 4. CME / BSC / CMC ENGINES
class CMEEngine:
    """Retail circuit classification"""

    def __init__(self, mapping: Dict[str, str]):
        self.mapping = mapping

    def classify(self, shop: str) -> str:
        return self.mapping.get(shop, "Other")


class BSCEngine:
    """Shopping mission classification"""

    def classify(self, basket_size: int) -> str:
        if basket_size >= 25:
            return "Main Stock-up"
        elif basket_size >= 5:
            return "Top-up"
        return "Convenience"


class CMCEngine:
    """Consumption moment classification"""

    def classify(self, product_code: str) -> str:
        if product_code.startswith("BRKF"):
            return "Breakfast"
        if product_code.startswith("SNK"):
            return "Snack"
        if product_code.startswith("DIN"):
            return "Meal"
        return "Other"

# 5. NOMENCLATURE ENGINE (CORE PIPELINE)
class NomenclatureEngine:
    """End-to-end enrichment engine"""

    def __init__(
        self,
        shoplist: ShopList,
        mainshop: MainShop,
        perso: PersoNomenclature,
        cme: CMEEngine,
        bsc: BSCEngine,
        cmc: CMCEngine,
    ):
        self.shoplist = shoplist
        self.mainshop = mainshop
        self.perso = perso
        self.cme = cme
        self.bsc = bsc
        self.cmc = cmc

    def process(self, raw: RawPurchase) -> EnrichedPurchase:
        normalized_shop = self.shoplist.normalize(raw.raw_shop_name)
        main_shop = self.mainshop.get(normalized_shop)
        perso_shop = self.perso.apply(main_shop)

        return EnrichedPurchase(
            household_id=raw.household_id,
            product_code=raw.product_code,
            shop=perso_shop,
            main_shop=main_shop,
            cme=self.cme.classify(perso_shop),
            bsc=self.bsc.classify(raw.basket_size),
            cmc=self.cmc.classify(raw.product_code),
        )

# 6. DEMO EXECUTION (DSM VIEW)
if __name__ == "__main__":

    # --- Reference data ---
    shop_synonyms = {
        "carrefour market": "Carrefour Market",
        "carrefour hyper": "Carrefour Hyper",
        "leclerc": "E.Leclerc",
    }

    mainshop_mapping = {
        "Carrefour Market": "Carrefour",
        "Carrefour Hyper": "Carrefour",
    }

    perso_rules_go71 = {
        "Carrefour": "Carrefour Total",
    }

    cme_mapping = {
        "Carrefour Total": "GMS",
        "E.Leclerc": "GMS",
    }

    # --- Engine setup ---
    engine = NomenclatureEngine(
        shoplist=ShopList(shop_synonyms),
        mainshop=MainShop(mainshop_mapping),
        perso=PersoNomenclature(perso_rules_go71, name="GO71"),
        cme=CMEEngine(cme_mapping),
        bsc=BSCEngine(),
        cmc=CMCEngine(),
    )

    # --- Raw panel purchase ---
    raw_purchase = RawPurchase(
        household_id="H001",
        product_code="BRKF001",
        raw_shop_name="carrefour market",
        basket_size=34,
        purchase_time="2026-01-10 10:30",
    )

    enriched = engine.process(raw_purchase)

    print("RAW PURCHASE")
    print(raw_purchase)
    print("\nENRICHED PURCHASE")
    print(enriched)
