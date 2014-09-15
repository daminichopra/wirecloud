# -*- coding: utf-8 -*-

# Copyright (c) 2012-2014 CoNWeT Lab., Universidad Politécnica de Madrid

# This file is part of Wirecloud.

# Wirecloud is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Wirecloud is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Wirecloud.  If not, see <http://www.gnu.org/licenses/>.

import os

from selenium.webdriver.support.ui import WebDriverWait

from wirecloud.platform.models import Market
from wirecloud.commons.utils.testcases import DynamicWebServer, LocalFileSystemServer, WirecloudSeleniumTestCase


__test__ = False


class MarketManagementSeleniumTestCase(WirecloudSeleniumTestCase):

    servers = {
        'http': {
            'wcatalogue.example.com': DynamicWebServer(fallback=LocalFileSystemServer(os.path.join(os.path.dirname(__file__), 'test-data', 'responses', 'wcatalogue'))),
        },
    }
    tags = ('wirecloud-selenium', 'markets')

    def check_resource_buttons(self, marketplace, resources, button_text=None):
        for resource_name in resources:
            resource = marketplace.search_in_results(resource_name)
            self.assertIsNotNone(resource)
            button = resource.element.find_element_by_css_selector('.mainbutton')
            self.assertEqual(button.text, button_text)

    def test_no_marketplaces(self):

        Market.objects.all().delete()

        self.login('normuser')
        with self.marketplace_view as marketplace:
            alert = self.wait_element_visible_by_css_selector('.marketplace-error-view .alert')
            self.assertIsNotNone(alert)
            self.assertTrue(alert.is_displayed())

    def test_default_marketplace(self):

        self.login('normuser')
        with self.marketplace_view as marketplace:
            self.assertEqual(marketplace.get_current_marketplace_name(), 'origin')

    def test_add_marketplace(self):

        self.login()
        with self.marketplace_view as marketplace:
            marketplace.add('remote', 'http://wcatalogue.example.com', 'wirecloud')
            self.check_resource_buttons(marketplace, ('New Widget', 'New Operator', 'New Mashup'), 'Install')
            self.check_resource_buttons(marketplace, ('Test', 'TestOperator', 'Test Mashup'), 'Uninstall')

        self.login('normuser', 'admin')
        with self.marketplace_view as marketplace:
            popup_menu = marketplace.open_menu()
            popup_menu.check(must_be_absent=('remote',))

    def test_add_public_marketplace(self):

        self.login()
        with self.marketplace_view as marketplace:
            marketplace.add('remote', 'http://wcatalogue.example.com', 'wirecloud', public=True)
            self.check_resource_buttons(marketplace, ('New Widget', 'New Operator', 'New Mashup'), 'Install')
            self.check_resource_buttons(marketplace, ('Test', 'TestOperator', 'Test Mashup'), 'Uninstall')

        self.login('normuser', 'admin')
        with self.marketplace_view as marketplace:
            marketplace.switch_to('remote')
            self.check_resource_buttons(marketplace, ('New Widget', 'New Operator', 'New Mashup'), 'Install')
            self.check_resource_buttons(marketplace, ('Test', 'TestOperator', 'Test Mashup'), 'Uninstall')

    def test_add_duplicated_marketplace(self):

        self.login('user_with_markets', 'admin')
        with self.marketplace_view as marketplace:
            marketplace.add('deleteme', 'http://localhost:8080', 'wirecloud', expect_error=True)

    def test_delete_marketplace(self):

        self.login('user_with_markets', 'admin')

        with self.marketplace_view as marketplace:
            marketplace.switch_to('deleteme')
            marketplace.delete()

    def test_global_marketplace_are_deletable_by_superusers(self):

        self.login('normuser', 'admin')

        with self.marketplace_view as marketplace:
            marketplace.switch_to('origin')
            marketplace.open_menu().check((), (), ('Delete marketplace',))

        self.login('admin', 'admin')

        with self.marketplace_view as marketplace:
            marketplace.switch_to('origin')
            marketplace.delete()

    def test_publish_option_not_available_if_not_targets(self):

        Market.objects.all().delete()
        self.login(username='normuser')

        with self.myresources_view as myresources:
            catalogue_base_element = myresources.wait_catalogue_ready()

            with myresources.search_in_results('Test') as resource:

                resource.advanced_operation('Publish')
                window_menu = self.wait_element_visible_by_css_selector('.window_menu.message')
                self.driver.find_element_by_xpath("//*[contains(@class, 'window_menu')]//*[text()='Accept']").click()
