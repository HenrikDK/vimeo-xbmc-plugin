# -*- coding: utf-8 -*-
import BaseTestCase
import nose
import sys
import os
from mock import Mock


class TestVimeoDownloader(BaseTestCase.BaseTestCase):

    def test_plugin_should_download_standard_videos(self):
        sys.modules["__main__"].xbmcvfs.rename.side_effect = os.rename
        sys.modules["__main__"].downloader._getNextItemFromQueue = Mock()
        (video, status) = sys.modules["__main__"].player.getVideoObject({"action": "download", "videoid": "22804972"})
        video["download_path"] = "./tmp/"
        video["url"] = video["video_url"]
        sys.modules["__main__"].downloader._getNextItemFromQueue.side_effect = [("Interactive Talking Plush Portal Turret-[22804972].mp4", video), {}]

        self.navigation.executeAction({"action": "download", "videoid": "22804972", "async": "false"})

        assert(os.path.exists('./tmp/Interactive Talking Plush Portal Turret-[22804972].mp4'))
        assert(os.path.getsize('./tmp/Interactive Talking Plush Portal Turret-[22804972].mp4') > 100)

if __name__ == "__main__":
    nose.runmodule()
