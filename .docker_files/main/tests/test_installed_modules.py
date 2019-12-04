
from odoo.tests import TransactionCase


class TestModules(TransactionCase):
    """Test that main profile is installed.

    This prevents the test suite from failling because no tests are found.
    """

    def test_main_is_installed(self):
        module = self.env['ir.module.module'].search([('name', '=', 'main')])
        assert module.state == 'installed'
