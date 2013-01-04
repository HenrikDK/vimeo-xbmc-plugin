import BaseTestCase
import nose
import sys
from mock import Mock


class TestVimeoStandardFeeds(BaseTestCase.BaseTestCase):

    def test_plugin_should_list_categories_folder_listing_correctly(self):
        self.navigation.listMenu({'path': '/root/explore/categories', 'login': 'false', 'api': 'categories', 'folder':'category'})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_items_should_have_thumbnails()
        self.assert_directory_item_urls_contain("category")

    def test_plugin_should_list_group_category_listing_correctly(self):
        self.navigation.listMenu({'path': '/root/explore/groups', 'login': 'false', 'api': 'groups', 'folder':'category'})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_items_should_have_thumbnails()
        self.assert_directory_item_urls_contain("category")

    def test_plugin_should_list_channels_category_listing_correctly(self):
        self.navigation.listMenu({'path': '/root/explore/channels', 'login': 'false', 'api': 'channels', 'folder':'category'})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_items_should_have_thumbnails()
        self.assert_directory_item_urls_contain("category")

    def test_plugin_should_list_categories_category_video_list_correctly(self):
        self.navigation.listMenu({'path': '/root/explore/categories', 'login': 'false', 'api': 'categories', 'category':'art'})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_half_of_all_directory_items_should_have_thumbnails()

    def test_plugin_should_list_categories_category_video_list_page_2_correctly(self):
        self.navigation.listMenu({'path': '/root/explore/categories', 'login': 'false', 'api': 'categories', 'category':'art', 'page':"1"})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_items_should_have_thumbnails()

    def test_plugin_should_list_channels_category_listing_correctly_art(self):
        self.navigation.listMenu({'path': '/root/explore/channels', 'login': 'false', 'api': 'channels', 'category':'art', 'folder':'channel'})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_items_should_have_thumbnails()
        self.assert_directory_item_urls_contain("channel")

    def test_plugin_should_list_channels_category_listing_page_2_correctly(self):
        self.navigation.listMenu({'path': '/root/explore/channels', 'login': 'false', 'api': 'channels', 'category':'art', 'folder':'channel', 'page':"1"})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_items_should_have_thumbnails()
        self.assert_directory_item_urls_contain("channel")

    def test_plugin_should_list_groups_category_listing_correctly(self):
        self.navigation.listMenu({'path': '/root/explore/groups', 'login': 'false', 'api': 'groups', 'category':'art', 'folder':'group'})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_items_should_have_thumbnails()
        self.assert_directory_item_urls_contain("group")

    def test_plugin_should_list_groups_category_listing_page_2_correctly(self):
        self.navigation.listMenu({'path': '/root/explore/groups', 'login': 'false', 'api': 'groups', 'category':'art', 'folder':'group', 'page':'1'})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_items_should_have_thumbnails()
        self.assert_directory_item_urls_contain("group")

    def test_plugin_should_list_search_video_list_correctly(self):
        sys.modules["__main__"].common.getUserInput = Mock()
        sys.modules["__main__"].common.getUserInput.return_value = "monkey"

        self.navigation.listMenu({"path": "/root/search/monkey", "api": "search", "search": "Monkey"})

        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_count_greater_than_or_equals(30)
        self.assert_directory_is_a_video_list()
        self.assert_directory_items_should_have_external_thumbnails()
        self.assert_directory_should_have_next_folder()

    def test_plugin_should_list_search_video_list_page_2_correctly(self):
        sys.modules["__main__"].common.getUserInput = Mock()
        sys.modules["__main__"].common.getUserInput.return_value = "monkey"

        self.navigation.listMenu({"path": "/root/search/monkey", "api": "search", "search": "Monkey", "page": 1})

        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_count_greater_than_or_equals(30)
        self.assert_directory_is_a_video_list()
        self.assert_directory_items_should_have_external_thumbnails()
        self.assert_directory_should_have_next_folder()

    def test_plugin_should_list_unicode_search_list_correctly(self):
        sys.modules["__main__"].common.getUserInput = Mock()
        sys.modules["__main__"].common.getUserInput.return_value = "monkey"

        self.navigation.listMenu({"path": "/root/search/redev", "api": "search", "search": "*redev"})

        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_count_greater_than_or_equals(30)
        self.assert_directory_is_a_video_list()
        self.assert_directory_items_should_have_external_thumbnails()
        self.assert_directory_should_have_next_folder()

    def test_plugin_should_list_hd_video_channel_correctly(self):
        self.navigation.listMenu({'path': '/root/explore/hd', 'login': 'false', 'channel': 'hd'})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin_should_list_staffpicks_video_channel_correctly(self):
        self.navigation.listMenu({'path': '/root/explore/staffpicks', 'login': 'false', 'channel': 'staffpicks'})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin_should_list_group_video_listing_correctly(self):
        self.navigation.listMenu({'path': '/root/explore/cloud', 'group': '22289'})

        self.assert_directory_count_greater_than_or_equals(10)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

if __name__ == "__main__":
    nose.runmodule()
