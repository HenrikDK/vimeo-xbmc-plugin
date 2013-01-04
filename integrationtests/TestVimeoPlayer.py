import BaseTestCase
import nose, sys


class TestVimeoPlayer(BaseTestCase.BaseTestCase):

    def test_plugin_should_resolve_video_url_correctly_on_video_playback(self):
        sys.modules["__main__"].xbmcvfs.exists.return_value = False

        self.navigation.executeAction({'action': 'play_video', 'path': '/root/search', 'videoid': '14441514'})

        self.assert_plugin_reported_that_url_was_resolved_correctly()
        self.assert_xbmc_recived_video_url()
        self.assert_video_url_contains(".mp4")
        self.assert_video_url_contains("token=")

    def test_plugin_should_playback_should_work_for_videos_with_utf8_titles(self):
        sys.modules["__main__"].xbmcvfs.exists.return_value = False

        self.navigation.executeAction({'action': 'play_video', 'path': '/root/search', 'videoid': '31538917'})

        self.assert_plugin_reported_that_url_was_resolved_correctly()
        self.assert_xbmc_recived_video_url()
        self.assert_video_url_contains(".mp4")
        self.assert_video_url_contains("token=")

    def test_plugin_should_playback_hd_videos(self):
        sys.modules["__main__"].xbmcvfs.exists.return_value = False

        self.navigation.executeAction({'action': 'play_video', 'path': '/root/search', 'videoid': '35396305'})

        self.assert_plugin_reported_that_url_was_resolved_correctly()
        self.assert_xbmc_recived_video_url()
        self.assert_video_url_contains(".mp4")
        self.assert_video_url_contains("token=")

    def test_plugin_should_playback_sd_only_videos(self):
        sys.modules["__main__"].xbmcvfs.exists.return_value = False

        self.navigation.executeAction({'action': 'play_video', 'path': '/root/search', 'videoid': '22804972'})

        self.assert_plugin_reported_that_url_was_resolved_correctly()
        self.assert_xbmc_recived_video_url()
        self.assert_video_url_contains(".mp4")
        self.assert_video_url_contains("token=")

    def test_plugin_should_playback_videos_from_local_disk_if_they_exist(self):

        self.navigation.executeAction({'action': 'play_video', 'path': '/root/search', 'videoid': '22804972'})

        self.assert_plugin_reported_that_url_was_resolved_correctly()
        self.assert_xbmc_recived_video_url()
        self.assert_video_url_contains(".mp4")
        self.assert_video_url_contains("./tmp/")



if __name__ == "__main__":
    nose.runmodule()
