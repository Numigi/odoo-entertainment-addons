# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Recording External Revenue",
    "tag": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Recording",
    "summary": "Manage external revenue of recording.",
    "depends": [
        "account",
        "musical_catalog",
        "product_musical_relation",
        "recording",
        "recording_platform",
    ],
    "data": [
        "views/recording_country_mapping.xml",
        "views/recording_country_state_mapping.xml",
        "views/recording_currency_mapping.xml",
        "views/recording_external_catalog_mapping.xml",
        "views/recording_external_revenue.xml",
        "views/recording_external_revenue_raw.xml",
        "views/recording_partner_mapping.xml",
        "views/recording_platform_mapping.xml",
        "views/recording_revenue_type_mapping.xml",
        "views/recording_subplatform_mapping.xml",
        "views/recording_tax_mapping.xml",
        "views/menu.xml",
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
    ],
    "demo": [
        "demo/product_product.xml",
        "demo/res_partner.xml",
        "demo/mapping.xml",
    ],
    "installable": True,
}
