# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Recording External Revenue Account",
    "tag": "1.0.1",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Recording",
    "summary": "Generate journal entries for external revenue of recording.",
    "depends": [
        "account_recording_dimensions",
        "recording_external_revenue",
        "recording_status",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "data/queue_job_function.xml",
        "views/recording_external_revenue.xml",
        "views/recording_journal_mapping.xml",
        "views/menu.xml",
    ],
    "installable": True,
}
