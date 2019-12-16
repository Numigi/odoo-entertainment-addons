# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data, unpack
from odoo.tests.common import SavepointCase


@ddt
class TestProductTemplate(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env['product.template'].create({
            'name': 'tname'
        })

    def test_whenMusicalRelationIsRecording_thenRecordTypeIsRecord(self):
        assert False

    def test_whenMusicalRelationIsGroup_thenRecordTypeIsGroup(self):
        assert False
