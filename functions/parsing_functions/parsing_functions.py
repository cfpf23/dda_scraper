import json
import re
from typing import Callable
from urllib.parse import urljoin


def find_json_key_value(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in find_json_key_value(i, kv):
                yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in find_json_key_value(j, kv):
                yield x


def parse_mediaworld_reviews(x):
    return list(find_json_key_value(x, "rankingNumber"))[0]


def parse_mediaworld_rating(x):
    return list(find_json_key_value(x, "rankingAlaTest"))[0]


def parse_mediaworld_sku(x):
    return list(find_json_key_value(x, "partNumber"))[0]


def kruidvat_nl_clean_price(x):

    x = x.replace("\n", "").replace(" ", "").strip()
    if x != "":
        return x
    return ""


def kruidvat_nl_clean_description(x):
    return x.replace("\n", "").strip()


def kruidvat_nl_clean_title(x):
    return x.replace("\n", "").strip()


def kruidvat_nl_clean_description_pdp(x):
    return x.replace("\n", "").replace("\t", "").strip()

def kruidvat_nl_clean_categories_pdp(x):
    return x.replace("\n", "").strip()

# def kruidvat_nl_clean_price_pdp(x):
#     return "".join(char.strip() for char in x)

def bipa_at_listing_data_gtmdata_parse(x, key):
    gtmdata_dict = json.loads(x)
    return gtmdata_dict.get(key)


def bol_com_rating_parse(x):
    try:
        klantbeoordeling, rating, *_ = x.split(" ")
        return float(rating.replace(",", "."))
    except Exception:
        return x


def create_kruidvat_nl_link(x):
    return urljoin("https://www.kruidvat.nl/", x)


def elkjop_no_review_parse(x):
    try:
        return x.replace("(", "").replace(")", "")
    except Exception:
        return x


def create_product_url(x, hostname=""):
    # https://www.kruidvat.nl/
    return urljoin(hostname, x)


def parse_len(x):
    return len(x)


def parse_join(x, deli=""):
    return deli.join(x)

def parse_replace(x, instrucion):
    if isinstance(x, str):
        return x.replace(instrucion.get("char"), instrucion.get("newchar"))

def parse_strip(x, char=" "):
    try:
        return x.strip(char)
    except Exception:
        return x


def parse_bool(x):
    return bool(x)


def clean_brand(x):
    try:
        if ":" in x:
            return x.split(maxsplit=1)[1].strip(":").replace(" Store", "")
        return x.split(maxsplit=2)[2].replace(" Store", "")
    except Exception:
        return x


def clean_delivery_price(x):
    try:
        junk, price, another_junk = x.split(" ")
        price = price.strip("£").strip("\n")
        return price
    except Exception:
        return x


def clean_tech_details(x):
    try:
        x = x.strip().strip("\n")
        return x.replace("\u200e", "")
    except Exception:
        return x


def connect_tech_details(x):
    try:
        return dict(zip(x[::2], x[1::2]))
    except Exception:
        return x


def clean_rating(x):
    try:
        rating = x.split(" ")[0]
        return float(rating)
    except Exception:
        return 0


def clean_reviews(x):
    try:
        reviews = x.split(" ")[0]
        return int(reviews)
    except Exception:
        return 0


def clean_price(x):
    try:
        return float(x.strip("£"))
    except Exception:
        return x


def get_no_img(x):
    try:
        js = x[0].replace("'", '"').strip(",")
        image = json.loads(js)
        return len(image["initial"])
    except Exception:
        return None


def get_level_variations(x):
    try:
        var = json.loads(x[0])
        return var
    except Exception:
        return None


def get_variation_number(x):
    try:
        var = json.loads(x[0])
        return len(var)
    except Exception:
        return 0

def take_first(x):
    for value in x:
        if value is not None and value != '':
            return value


def mapping(key: str) -> Callable:
    mapping = {
        "strip": parse_strip,
        "bool": parse_bool,
        "join": parse_join,
        "len": parse_len,
        "replace": parse_replace,
        "take_first": take_first,
        "clean_brand": clean_brand,
        "clean_price": clean_price,
        "clean_rating": clean_rating,
        "clean_reviews": clean_reviews,
        "connect_tech_details": connect_tech_details,
        "clean_tech_details": clean_tech_details,
        "clean_delivery_price": clean_delivery_price,
        "get_no_img": get_no_img,
        "get_level_variations": get_level_variations,
        "get_variation_number": get_variation_number,
        "kruidvat_nl_clean_price": kruidvat_nl_clean_price,
        "kruidvat_nl_clean_title": kruidvat_nl_clean_title,
        "kruidvat_nl_clean_description": kruidvat_nl_clean_description,
        "create_kruidvat_nl_link": create_kruidvat_nl_link,
        "bol_com_rating_parse": bol_com_rating_parse,
        "elkjop_no_review_parse": elkjop_no_review_parse,
        "create_product_url": create_product_url,
        "kruidvat_nl_clean_description_pdp": kruidvat_nl_clean_description_pdp,
        "kruidvat_nl_clean_categories_pdp": kruidvat_nl_clean_categories_pdp,
        "bipa_at_listing_data_gtmdata_parse": bipa_at_listing_data_gtmdata_parse
    }
    return mapping.get(key)
