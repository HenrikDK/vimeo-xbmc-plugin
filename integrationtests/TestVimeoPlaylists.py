import BaseTestCase
import nose
import sys

class TestVimeoPlaylists(BaseTestCase.BaseTestCase):

    def test_plugin_should_queue_playlist_and_start_playback_if_user_selects_play_all_in_playlist(self):
        sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
        sys.modules["__main__"].settings.setSetting("perpage", "6")

        self.navigation.executeAction({"action": "play_all", "videoid": "53068487", "album": "2179483"})

        self.assert_playlist_count_greater_than_or_equals(30)
        self.assert_directory_items_should_have_thumbnails()
        self.assert_playlist_contains_only_unique_video_items()
        self.assert_playlist_videos_does_not_contain("53068482")
        self.assert_playlist_videos_contain("53153270")

    def test_plugin_should_queue_playlist_and_start_playback_if_user_selects_play_all_outside_playlist(self):
        sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
        sys.modules["__main__"].settings.setSetting("perpage", "6")

        self.navigation.executeAction({"action": "play_all", "album": "2179483"})

        self.assert_playlist_count_greater_than_or_equals(30)
        self.assert_directory_items_should_have_thumbnails()
        self.assert_playlist_contains_only_unique_video_items()

    def test_plugin_should_queue_user_watch_later_feed_if_user_selects_play_all_outside_list(self):
        sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
        sys.modules["__main__"].settings.setSetting("perpage", "6")
        self.initializeVimeoClient()
        self.initializePlugin()

        self.navigation.executeAction({"action": "play_all", "login":"true", "api": "my_watch_later"})

        self.assert_playlist_count_greater_than_or_equals(10)
        self.assert_directory_items_should_have_thumbnails()
        self.assert_playlist_contains_only_unique_video_items()

    def test_plugin_should_queue_user_new_subscriptions_feed_if_user_selects_play_all_on_external_user_outside_list(self):
        sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
        sys.modules["__main__"].settings.setSetting("perpage", "6")
        self.initializeVimeoClient()
        self.initializePlugin()

        self.navigation.executeAction({"action": "play_all", "login": "true", "api": "my_newsubscriptions"})

        self.assert_playlist_count_greater_than_or_equals(10)
        self.assert_half_of_all_directory_items_should_have_thumbnails()

    def test_plugin_should_queue_users_liked_videos_if_user_selects_play_all_outside_list(self):
        sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
        sys.modules["__main__"].settings.setSetting("perpage", "6")
        self.initializeVimeoClient()
        self.initializePlugin()

        self.navigation.executeAction({"action": "play_all", "login": "true", "api": "my_likes"})

        self.assert_playlist_count_greater_than_or_equals(10)
        self.assert_directory_items_should_have_thumbnails()
        self.assert_playlist_contains_only_unique_video_items()

    def test_plugin_should_queue_users_videos_if_user_selects_play_all_outside_list(self):
        sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
        sys.modules["__main__"].settings.setSetting("perpage", "6")
        self.initializeVimeoClient()
        self.initializePlugin()

        self.navigation.executeAction({"action": "play_all", "login": "true", "api": "my_videos"})

        self.assert_playlist_count_greater_than_or_equals(2)
        self.assert_playlist_contains_only_unique_video_items()

if __name__ == "__main__":
    nose.runmodule()
