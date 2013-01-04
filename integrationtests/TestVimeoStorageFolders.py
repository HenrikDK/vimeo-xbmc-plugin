import BaseTestCase
import nose


class TestVimeoStorageFolders(BaseTestCase.BaseTestCase):
    
    def test_plugin_should_list_stored_searches_folder_list_correctly(self):
        self.navigation.listMenu({"path": "/root/search/monkey", "api": "search", "search": "Tuna"})
        self.navigation.listMenu({"path": "/root/search/monkey", "api": "search", "search": "Tulip"})
        self.navigation.listMenu({"path": "/root/search/monkey", "api": "search", "search": "Monkey"})
        self.reset_xbmc_mocks()

        self.navigation.listMenu({"path": "/root/search/", "store": "searches", "folder": "true"})

        self.assert_directory_item_urls_contain_at_least_one("Tuna")
        self.assert_directory_item_urls_contain_at_least_one("Tulip")
        self.assert_directory_item_urls_contain_at_least_one("Monkey")
        self.assert_directory_item_urls_contain("api")
        self.assert_directory_count_less_than_or_equals(4)
        self.assert_directory_count_greater_than_or_equals(3)
        self.assert_directory_is_a_folder_list()

if __name__ == "__main__":
    nose.runmodule()
