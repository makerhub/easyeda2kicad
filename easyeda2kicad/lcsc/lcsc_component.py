class LcscComponent:
    name: str = ""  # name
    manufacturer: str = ""  # brand
    manufacturer_pn: str = ""  # mpn
    lcsc_pn: str = ""  # sku
    package: str = ""
    key_attributes: str = ""
    description: str = ""  # description
    datasheet_url: str = ""
    image_url: str = ""  # image
    category: str = ""  # category

    def __init__(
        self, name: str = "", manufacturer: str = "", manufacturer_pn: str = "", lcsc_pn: str = "", package: str = "", key_attributes: str = "", description: str = "", datasheet_url: str = "", image_url: str = "", category: str = ""
    ) -> None:
        self.name = name
        self.manufacturer = manufacturer
        self.manufacturer_pn = manufacturer_pn
        self.lcsc_pn = lcsc_pn
        self.package = package
        self.key_attributes = key_attributes
        self.description = description
        self.datasheet_url = datasheet_url
        self.image_url = image_url
        self.category = category
