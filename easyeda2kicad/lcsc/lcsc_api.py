import logging
import requests
import json
from bs4 import BeautifulSoup


from .lcsc_component import LcscComponent

API_ENDPOINT = "https://easyeda.com/api/products/{lcsc_id}/components?version=6.4.19.5"


class LcscApi:
    def __init__(self) -> None:
        self.headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cache-Control": "no-cahce",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537",
        }

    def get_component_details(self, lcsc_url: str) -> LcscComponent:
        resp = requests.get(url=lcsc_url, headers=self.headers)
        if resp.status_code != requests.codes.ok:
            logging.error(f"Failed to get component details from LCSC url: {lcsc_url}")
            return None

        soup = BeautifulSoup(resp.content, "html.parser")

        el = soup.find(lambda tag: tag.name == "script" and '"@type":"Product"' in tag.text)
        component_data = json.loads(el.text)

        manufacturer = component_data.get("brand", "")
        manufacturer_pn = component_data.get("mpn", "")
        lcsc_pn = component_data.get("sku", "")
        package = self.get_prop_by_name(soup, "Package")
        key_attributes = self.get_prop_by_name(soup, "Key\xa0Attributes")  # Note: weird space char
        description = component_data.get("description", "")
        datasheet_url = self.get_datasheet_url(soup)
        catagory = component_data.get("category", "")
        image_url = component_data.get("image", "")

        return LcscComponent(
            name=f"{manufacturer} {manufacturer_pn}",
            manufacturer=manufacturer,
            manufacturer_pn=manufacturer_pn,
            lcsc_pn=lcsc_pn,
            package=package,
            key_attributes=key_attributes,
            description=description,
            datasheet_url=datasheet_url,
            image_url=image_url,
            category=catagory,
        )

    def get_prop_by_name(
        self,
        soup: BeautifulSoup,
        prop_name: str,
    ) -> str:
        try:
            el = soup.find(lambda tag: tag.name == "td" and prop_name in tag.text)
            sibling_td_el = el.find_next("td")
            child_div_el = sibling_td_el.findChild("div")

            # Check in <span>
            text_el = child_div_el.findChild("span")
            if not text_el:
                # Check in <a>
                text_el = child_div_el.findChild("a")

            value = text_el.text.strip()

            return value if value else ""

        except Exception as e:
            logging.error(f"Failed to get prop {prop_name}: {e}")

    def get_datasheet_url(self, soup: BeautifulSoup) -> str:
        el = soup.find(lambda tag: tag.name == "td" and "Datasheet" in tag.text)
        sibling_td_el = el.find_next("td")
        a_el = sibling_td_el.findChild("a")
        href = a_el.get("href", None)
        return href if href else ""
