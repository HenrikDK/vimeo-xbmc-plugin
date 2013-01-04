# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
from VimeoPlayer import VimeoPlayer


class TestVimeoPlayer(BaseTestCase.BaseTestCase):

    def test_playVideo_should_call_getVideoObject(self):
        player = VimeoPlayer()
        player.getVideoObject = Mock(return_value=[{"apierror": "some error"}, 303])

        player.playVideo()

        player.getVideoObject.assert_called_with({})

    def test_playVideo_should_log_and_fail_gracefully_on_error(self):
        player = VimeoPlayer()
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = [{}, 303]

        result = player.playVideo()

        assert(result == False)
        assert(sys.modules["__main__" ].common.log.call_count > 0)

    def test_playVideo_should_call_xbmc_setResolvedUrl(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        player = VimeoPlayer()
        player.addSubtitles = Mock()
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = ({"Title": "someTitle", "videoid": "some_id", "thumbnail": "someThumbnail", "video_url": "someUrl"}, 200)
        sys.argv = ["test1", "1", "test2"]

        player.playVideo({"videoid": "some_id"})

        assert(sys.modules["__main__"].xbmcplugin.setResolvedUrl.call_count > 0)

    def ttest_playVideo_should_call_remove_from_watch_later_if_viewing_video_from_watch_later_queue(self):
        player = VimeoPlayer()
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.argv = ["test1", "1", "test2"]
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = ({"Title": "someTitle", "videoid": "some_id", "thumbnail": "someThumbnail", "video_url": "someUrl"}, 200)
        player.addSubtitles = Mock()
        call_params = {"videoid": "some_id", "watch_later": "true", "playlist": "playlist_id", "playlist_entry_id": "entry_id"}

        player.playVideo(call_params)

        sys.modules["__main__"].core.remove_from_watch_later.assert_called_with(call_params)

    def test_playVideo_should_update_locally_stored_watched_status(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.argv = ["test1", "1", "test2"]
        player = VimeoPlayer()
        player.getVideoObject = Mock()
        player.getVideoObject.return_value = ({"Title": "someTitle", "videoid": "some_id", "thumbnail": "someThumbnail", "video_url": "someUrl"}, 200)
        player.addSubtitles = Mock()

        player.playVideo({"videoid": "some_id"})
        sys.modules["__main__"].storage.storeValue.assert_called_with("vidstatus-some_id", "7" )

    def test_scrapeVideoInfo_should_call_fetchPage_with_correct_url(self):
        sys.modules["__main__"].common.fetchPage.return_value = {"content":"FAIL", "status":303}
        player = VimeoPlayer()

        player.scrapeVideoInfo({"videoid": "some_id"})

        sys.modules["__main__"].common.fetchPage.assert_called_with({"link": "http://www.vimeo.com/%s" % ("some_id")})

    def test_scrapeVideoInfo_should_search_for_video_config_and_parse_json(self):
        sys.modules["__main__"].common.fetchPage.return_value = {"content":'{config:{"request":{"smokey":{}}},}', "status":200}
        player = VimeoPlayer()

        result = player.scrapeVideoInfo({"videoid": "some_id"})

        assert (result.has_key("config"))
        assert (result["config"].has_key("request"))

    def test_getVideoInfo_should_fail_correctly_if_api_is_unavailable(self):
        sys.modules["__main__"].language.return_value = "some_string"
        player = VimeoPlayer()
        player.scrapeVideoInfo = Mock(return_value={})

        (video, status) = player.getVideoInfo({"videoid": "some_id"})

        sys.modules["__main__"].common.log.assert_called_with("- Couldn't parse API output, Vimeo doesn't seem to know this video id?")
        sys.modules["__main__"].language.assert_called_with(30608)
        assert(video["apierror"] == "some_string")

    def test_getVideoInfo_should_not_save_video_info_in_cache_since_it_contains_request_signature_token(self):
        sys.modules["__main__"].cache.get.return_value = {}
        result = {"config":{"video":{"title":"some_title", "hd":"1", "duration":"1", "thumbnail":"some_thumbnail", "owner":{"name":"some_name"}}, "request":{"signature":"some_signature", "timestamp":"some_stamp"}}}
        player = VimeoPlayer()
        player.scrapeVideoInfo = Mock(return_value=result)

        (video, status) = player.getVideoInfo({"videoid": "some_id"})

        assert(sys.modules["__main__"].cache.set.call_count == 0)

    def test_getVideoInfo_should_use_call_scrapeVideoInfo(self):
        player = VimeoPlayer()
        player.scrapeVideoInfo = Mock(return_value={})

        (video, status) = player.getVideoInfo({"videoid": "some_id"})

        player.scrapeVideoInfo.assert_any_call({"videoid": "some_id"})

    def test_getVideoInfo_should_return_correct_structure(self):
        sys.modules["__main__"].cache.get.return_value = {}
        result = {"config":{"video":{"title":"some_title", "hd":"1", "duration":"1", "thumbnail":"some_thumbnail", "owner":{"name":"some_name"}}, "request":{"signature":"some_signature", "timestamp":"some_stamp"}}}
        player = VimeoPlayer()
        player.scrapeVideoInfo = Mock(return_value=result)

        (video, status) = player.getVideoInfo({"videoid": "some_id"})

        assert (video.has_key("Title"))
        assert (video.has_key("Duration"))
        assert (video.has_key("Studio"))
        assert (video.has_key("videoid"))
        assert (video.has_key("thumbnail"))
        assert (video.has_key("request_signature"))
        assert (video.has_key("request_signature_expires"))
        assert (video.has_key("isHD"))

    def test_selectVideoQuality_should_prefer_720p_if_asked_to(self):
        sys.modules["__main__"].settings.getSetting.return_value = 2
        player = VimeoPlayer()

        url = player.selectVideoQuality({},{"isHD":"1"})

        print repr(url)
        assert(url == "hd")

    def test_selectVideoQuality_should_choose_720p_if_quality_is_set(self):
        sys.modules["__main__"].settings.getSetting.return_value = 2
        player = VimeoPlayer()

        url = player.selectVideoQuality({"quality":"720p"}, {"isHD":"1"})

        print repr(url)
        assert(url == "hd")

    def test_selectVideoQuality_should_choose_sd_if_quality_is_set(self):
        sys.modules["__main__"].settings.getSetting.return_value = 2
        player = VimeoPlayer()

        url = player.selectVideoQuality({"isHD":"1", "quality":"sd"}, {})

        print repr(url)
        assert(url == "sd")

    def test_selectVideoQuality_should_prefer_SD_if_asked_to(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        player = VimeoPlayer()

        url = player.selectVideoQuality({}, {})

        assert(url == "sd")

    def test_selectVideoQuality_should_limit_to_sd_if_user_has_selected_that_option(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        player = VimeoPlayer()

        url = player.selectVideoQuality({"isHD":"1"}, {})

        assert(url == "sd")

    def test_selectVideoQuality_should_use_hd_videos_download_setting_to_determine_video_quality_if_action_is_download(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        player = VimeoPlayer()

        url = player.selectVideoQuality({"isHD":"1", "action":"download"}, {})

        sys.modules["__main__"].settings.getSetting.assert_any_call("hd_videos_download")

    def test_selectVideoQuality_should_use_default_to_hd_videos_setting_if_hd_videos_download_is_unset_and_action_is_download(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["0","1"]
        player = VimeoPlayer()

        url = player.selectVideoQuality({"isHD":"1", "action":"download"}, {})

        sys.modules["__main__"].settings.getSetting.assert_any_call("hd_videos_download")
        sys.modules["__main__"].settings.getSetting.assert_any_call("hd_videos")

    def test_selectVideoQuality_should_call_userSelectsVideoQuality_if_user_selected_that_option(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        player = VimeoPlayer()
        player.userSelectsVideoQuality = Mock()

        player.selectVideoQuality({}, {"isHD":"1"})

        player.userSelectsVideoQuality.assert_called_with({})

    def test_userSelectsVideoQuality_should_select_proper_quality_based_on_user_input(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 0
        sys.modules["__main__"].language.return_value = ""
        player = VimeoPlayer()

        url = player.userSelectsVideoQuality({})

        sys.modules["__main__"].xbmcgui.Dialog().select.assert_called_with("", ["720p", "SD"])
        assert(url == "hd")

    def test_userSelectsVideoQuality_should_call_xbmc_dialog_select_to_ask_for_user_input(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        sys.modules["__main__"].xbmcgui.Dialog().select.return_value = -1
        sys.modules["__main__"].language.return_value = ""
        player = VimeoPlayer()

        url = player.userSelectsVideoQuality({})

        print repr(url)
        assert(sys.modules["__main__"].xbmcgui.Dialog().select.call_count > 0)

    def test_getVideoObject_should_get_video_information_from_getVideoInfo(self):
        sys.modules["__main__"].settings.getSetting.return_value = ""
        player = VimeoPlayer()
        player.getVideoInfo = Mock()
        player.getVideoInfo.return_value = ({}, 303)
        player._getVideoLinks = Mock()
        player._getVideoLinks.return_value = ({}, {})

        player.getVideoObject({})

        player.getVideoInfo.assert_called_with({})

    def test_getVideoObject_should_check_for_local_file_if_download_path_is_set(self):
        params = {"videoid": "some_id"}
        sys.modules["__main__"].settings.getSetting.return_value = "somePath/"
        sys.modules["__main__"].xbmcvfs.exists.return_value = True
        player = VimeoPlayer()
        player.getVideoInfo = Mock()
        player.getVideoInfo.return_value = ({"videoid": "some_id", "Title": "someTitle"}, 200)
        player._getVideoLinks = Mock()
        player._getVideoLinks.return_value = ({}, {})

        player.getVideoObject(params)

        sys.modules["__main__"].xbmcvfs.exists.assert_called_with("somePath/someTitle-[some_id].mp4")

    def test_getVideoObject_should_use_local_file_for_playback_if_found(self):
        sys.modules["__main__"].settings.getSetting.return_value = "somePath/"
        sys.modules["__main__"].xbmcvfs.exists.return_value = True
        params = {"videoid": "some_id"}
        player = VimeoPlayer()
        player.getVideoInfo = Mock()
        player.getVideoInfo.return_value = ({"videoid": "some_id", "Title": "someTitle"}, 200)
        player._getVideoLinks = Mock()
        player._getVideoLinks.return_value = ({}, {})

        (video, status) = player.getVideoObject(params)

        sys.modules["__main__"].xbmcvfs.exists.assert_called_with("somePath/someTitle-[some_id].mp4")
        assert(player._getVideoLinks.call_count == 0)
        assert(video["video_url"] == "somePath/someTitle-[some_id].mp4")

    def test_getVideoObject_should_call_fetchPage_if_local_file_not_found(self):
        params = {"videoid": "some_id"}
        sys.modules["__main__"].settings.getSetting.return_value = "somePath/"
        sys.modules["__main__"].xbmcvfs.exists.return_value = False
        sys.modules["__main__"].common.fetchPage.return_value = {"new_url":"some_url"}
        player = VimeoPlayer()
        player.getVideoInfo = Mock()
        player.getVideoInfo.return_value = ({"videoid": "some_id", "Title": "someTitle", "request_signature":"signature", "request_signature_expires":"2"}, 200)
        player._getVideoLinks = Mock()
        player.selectVideoQuality = Mock()
        player._getVideoLinks.return_value = ({}, {})

        (video, status) = player.getVideoObject(params)

        sys.modules["__main__"].xbmcvfs.exists.assert_called_with("somePath/someTitle-[some_id].mp4")
        assert(sys.modules["__main__"].common.fetchPage.call_count > 0)

    def test_getVideoObject_should_call_selectVideoQuality_if_local_file_not_found_and_remote_links_found(self):
        params = {"videoid": "some_id"}
        sys.modules["__main__"].settings.getSetting.return_value = "somePath/"
        sys.modules["__main__"].xbmcvfs.exists.return_value = False
        sys.modules["__main__"].common.fetchPage.return_value = {"new_url":"some_url"}
        player = VimeoPlayer()
        player.getVideoInfo = Mock()
        video = {"videoid": "some_id", "Title": "someTitle", "request_signature":"signature", "request_signature_expires":"2"}
        player.getVideoInfo.return_value = (video, 200)
        player.selectVideoQuality = Mock()

        (video, status) = player.getVideoObject(params)

        sys.modules["__main__"].xbmcvfs.exists.assert_called_with("somePath/someTitle-[some_id].mp4")
        player.selectVideoQuality.assert_called_with(params, video)

    def test_getVideoObject_should_handle_accents_and_utf8(self):
        params = {"videoid": "some_id"}
        sys.modules["__main__"].settings.getSetting.return_value = u"somePathé/".encode("utf-8")
        sys.modules["__main__"].xbmcvfs.exists.return_value = True
        player = VimeoPlayer()
        player.getVideoInfo = Mock()
        player.getVideoInfo.return_value = ({"videoid": "some_id", "Title": u"נלה מהיפה והחנון בסטריפ צ'אט בקליפ של חובבי ציון"}, 200)
        player._getVideoLinks = Mock()
        player._getVideoLinks.return_value = ([], {})
        player.selectVideoQuality = Mock()

        (video, status) = player.getVideoObject(params)

        sys.modules["__main__"].xbmcvfs.exists.assert_called_with(u"somePath\xe9/\u05e0\u05dc\u05d4 \u05de\u05d4\u05d9\u05e4\u05d4 \u05d5\u05d4\u05d7\u05e0\u05d5\u05df \u05d1\u05e1\u05d8\u05e8\u05d9\u05e4 \u05e6'\u05d0\u05d8 \u05d1\u05e7\u05dc\u05d9\u05e4 \u05e9\u05dc \u05d7\u05d5\u05d1\u05d1\u05d9 \u05e6\u05d9\u05d5\u05df-[some_id].mp4")

    def test_getVideoObject_should_use_return_api_error_if_video_info_fails(self):
        sys.modules["__main__"].settings.getSetting.return_value = ""
        sys.modules["__main__"].common.fetchPage.return_value = {"new_url":""}
        player = VimeoPlayer()
        player.getVideoInfo = Mock()
        player.getVideoInfo.return_value = ({"apierror":"fail"}, 303)
        player._getVideoLinks = Mock()
        player._getVideoLinks.return_value = ({}, {})
        player.selectVideoQuality = Mock()

        (result, status) = player.getVideoObject({})

        assert (result == "fail")
        assert (status == 303)

if __name__ == '__main__':
    nose.runmodule()
