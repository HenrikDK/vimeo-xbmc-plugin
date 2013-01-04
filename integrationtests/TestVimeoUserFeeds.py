import BaseTestCase
import nose
import sys

class TestVimeoUserFeeds(BaseTestCase.BaseTestCase):

    def setUp(self):
        BaseTestCase.BaseTestCase.setUp(self)
        sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
        sys.modules["__main__"].settings.setSetting("perpage", "0")

        self.initializeVimeoClient()
        self.initializePlugin()

    def test_plugin__should_list_my_liked_video_list_correctly(self):

        self.navigation.listMenu({"path": "/root/my_likes", "api": "my_likes", "login":"true"})

        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_count_greater_than_or_equals(3)
        self.assert_directory_is_a_video_list()
        self.assert_directory_items_should_have_external_thumbnails()
        self.assert_directory_should_have_next_folder()

    def test_plugin__should_list_my_liked_video_list_page_2_correctly(self):

        self.navigation.listMenu({"path": "/root/my_likes", "api": "my_likes", "login":"true", "page":"1"})

        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_count_greater_than_or_equals(8)
        self.assert_directory_is_a_video_list()
        self.assert_directory_items_should_have_external_thumbnails()
        self.assert_directory_should_have_next_folder()

    def test_plugin__should_list_my_contacts_folder_list(self):

        self.navigation.listMenu({'path': '/root/my_contacts', 'login': 'true', 'api': 'my_contacts', "folder":"contact"})

        self.assert_directory_count_greater_than_or_equals(1)
        self.assert_directory_count_less_than_or_equals(5)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_item_urls_contain("contact")

    def test_plugin__should_list_my_albums_folder_list_correctly(self):

        self.navigation.listMenu({'path': '/root/my_contacts', 'login': 'true', 'api': 'my_albums', "folder":"album"})

        self.assert_directory_count_greater_than_or_equals(3)
        self.assert_directory_count_less_than_or_equals(10)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_item_urls_contain("album")
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin__should_list_my_watch_later_video_listing_correctly(self):

        self.navigation.listMenu({'path': '/root/my_contacts', 'login': 'true', 'api': 'my_watch_later'})

        self.assert_directory_count_greater_than_or_equals(5)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin__should_list_my_watch_later_video_list_page_2_correctly(self):

        self.navigation.listMenu({'path': '/root/my_contacts', 'login': 'true', "page":"1",'api': 'my_watch_later'})

        self.assert_directory_count_greater_than_or_equals(5)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin__should_list_my_groups_folder_list_correctly(self):

        self.navigation.listMenu({'path': '/root/my_contacts', 'login': 'true', 'api': 'my_groups', "folder":"group"})

        self.assert_directory_count_greater_than_or_equals(8)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_item_urls_contain("group")
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin__should_list_my_channels_folder_list_correctly(self):

        self.navigation.listMenu({'path': '/root/my_channel', 'login': 'true', 'api': 'my_channels', "folder":"channel"})

        self.assert_directory_count_greater_than_or_equals(5)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_item_urls_contain("channel")
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin__should_list_my_channels_page_2_folder_list_correctly(self):

        self.navigation.listMenu({'path': '/root/my_channel', 'login': 'true', 'api': 'my_channels',"page":"1", "folder":"channel"})

        self.assert_directory_count_greater_than_or_equals(5)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_item_urls_contain("channel")
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin__should_list_new_subscription_videos_video_list_correctly(self):

        self.navigation.listMenu({'path': '/root/subscriptions/new', 'login': 'true', 'api': 'my_newsubscriptions'})

        self.assert_directory_count_greater_than_or_equals(8)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin__should_list_new_subscription_videos_video_list_page_2_correctly(self):

        self.navigation.listMenu({'path': '/root/subscriptions/new', 'login': 'true', 'api': 'my_newsubscriptions',"page":"1"})

        self.assert_directory_count_greater_than_or_equals(8)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin__should_list_my_videos_video_list_correctly(self):

        self.navigation.listMenu({'path': '/root/my_videos', 'login': 'true', 'api': 'my_videos'})

        self.assert_directory_count_greater_than_or_equals(3)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_video_list()
        self.assert_directory_contains_almost_only_unique_video_items()
        self.assert_directory_items_should_have_external_thumbnails()

    def test_plugin_should_list_contact_options_folder_list_correctly(self):
        sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")

        self.navigation.listMenu({'login': 'true', "path": "/root/contacts/smokey", "store":"contact_options", "contact":"smokey" , "folder": "true"})

        self.assert_directory_count_greater_than_or_equals(2)
        self.assert_directory_count_less_than_or_equals(51)
        self.assert_directory_is_a_folder_list()
        self.assert_directory_item_urls_contain("contact")

if __name__ == "__main__":
    nose.runmodule()
