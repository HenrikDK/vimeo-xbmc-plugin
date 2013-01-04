# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock
import sys
from VimeoCore import VimeoCore

class TestVimeoCore(BaseTestCase.BaseTestCase):

    def test_setLike_should_call_vimeo_client_correctly_if_action_is_add_favorites(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.setLike({"action":"add_favorite" , "videoid":"some_id"})

        sys.modules["__main__"].client.vimeo_videos_setLike.assert_any_call(like="true", video_id="some_id", oauth_token="token")

    def test_setLike_should_call_vimeo_client_correctly_if_action_is_remove_favorites(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.setLike({"action":"remove_favorite" , "videoid":"some_id"})

        sys.modules["__main__"].client.vimeo_videos_setLike.assert_any_call(like="false", video_id="some_id", oauth_token="token")

    def test_updateContact_should_call_vimeo_client_correctly_if_action_is_add_contact(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.updateContact({"action":"add_contact", "contact":"some_contact"})

        sys.modules["__main__"].client.vimeo_people_addContact.assert_any_call(user_id="some_contact", oauth_token="token")

    def test_updateContact_should_call_vimeo_client_correctly_if_action_is_remove_contact(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.updateContact({"action":"remove_contact", "contact":"some_contact"})

        sys.modules["__main__"].client.vimeo_people_removeContact.assert_any_call(user_id="some_contact", oauth_token="token")

    def test_addToWatchLater_should_call_vimeo_client_correctly(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.addToWatchLater({"videoid":"some_id"})

        sys.modules["__main__"].client.vimeo_albums_addToWatchLater.assert_any_call(video_id="some_id", oauth_token="token")

    def test_addToAlbum_should_call_vimeo_client_correctly(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.addToAlbum({"album":"some_album","videoid":"some_id"})

        sys.modules["__main__"].client.vimeo_albums_addVideo.assert_any_call(album_id="some_album", video_id="some_id", oauth_token="token")

    def test_removeFromAlbum_should_call_vimeo_client_correctly(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.removeFromAlbum({"album":"some_album","videoid":"some_id"})

        sys.modules["__main__"].client.vimeo_albums_removeVideo.assert_any_call(album_id="some_album", video_id="some_id", oauth_token="token")

    def test_deleteAlbum_should_call_vimeo_client_correctly(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.deleteAlbum({"album":"some_album"})

        sys.modules["__main__"].client.vimeo_albums_delete.assert_any_call(album_id="some_album", oauth_token="token")

    def test_createAlbum_should_call_vimeo_client_correctly(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.createAlbum({"title":"some_title","videoid":"some_id"})

        sys.modules["__main__"].client.vimeo_albums_create.assert_any_call(title="some_title",video_id="some_id", oauth_token="token")

    def test_removeWatchLater_should_call_vimeo_client_correctly(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.removeWatchLater({"videoid":"some_id"})

        sys.modules["__main__"].client.vimeo_albums_removeFromWatchLater.assert_any_call(video_id="some_id", oauth_token="token")

    def test_updateGroup_should_call_vimeo_client_correctly_if_action_is_join_group(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.updateGroup({"action":"join_group", "group":"some_group"})

        sys.modules["__main__"].client.vimeo_groups_join.assert_any_call(group_id="some_group", oauth_token="token")

    def test_updateGroup_should_call_vimeo_client_correctly_if_action_is_leave_group(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.updateGroup({"action":"leave_group", "group":"some_group"})

        sys.modules["__main__"].client.vimeo_groups_leave.assert_any_call(group_id="some_group", oauth_token="token")

    def test_updateSubscription_should_call_vimeo_client_correctly_if_action_is_add_subscription(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.updateSubscription({"action":"add_subscription", "channel":"some_channel"})

        sys.modules["__main__"].client.vimeo_channels_subscribe.assert_any_call(channel_id="some_channel", oauth_token="token")

    def test_updateSubscription_should_call_vimeo_client_correctly_if_action_is_remove_subscription(self):
        sys.modules["__main__"].settings.getSetting.return_value = "token"
        core = VimeoCore()
        core._get_return_status = Mock()

        core.updateSubscription({"action":"remove_subscription", "channel":"some_channel"})

        sys.modules["__main__"].client.vimeo_channels_unsubscribe.assert_any_call(channel_id="some_channel", oauth_token="token")

    def test_list_should_call_vimeo_client_correctly_if_channel_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"channel":"some_channel"})

        sys.modules["__main__"].client.vimeo_channels_getVideos.assert_any_call(channel_id="some_channel", page=1, per_page=15, full_response="true")

    def test_list_should_call_vimeo_client_correctly_if_album_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"album":"some_album"})

        sys.modules["__main__"].client.vimeo_albums_getVideos.assert_any_call(album_id="some_album", page=1, per_page=15, full_response="true")

    def test_list_should_call_vimeo_client_correctly_if_group_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "1"
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"group":"some_group"})

        sys.modules["__main__"].client.vimeo_groups_getVideos.assert_any_call(group_id="some_group", page=1, per_page=15, full_response="true")

    def test_list_should_call_vimeo_client_correctly_if_api_is_my_videos_in_params(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["1","1","1","user_id", "1"]
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"api":"my_videos"})

        sys.modules["__main__"].client.vimeo_videos_getAll.assert_any_call(user_id="user_id", page=1, per_page=15, full_response="true")

    def test_list_should_call_vimeo_client_correctly_if_api_is_search_in_params(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["1","1","1","user_id", "1"]
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"api":"search", "search":"some_query"})

        sys.modules["__main__"].client.vimeo_videos_search.assert_any_call(query="some_query", page=1, per_page=15, full_response="true")

    def test_list_should_call_vimeo_client_correctly_if_api_is_my_likes_in_params(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["1","1","1","user_id", "1"]
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"api":"my_likes"})

        sys.modules["__main__"].client.vimeo_videos_getLikes.assert_any_call(user_id="user_id", page=1, per_page=15, full_response="true")

    def test_list_should_call_vimeo_client_correctly_if_api_is_my_watch_later_in_params(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["1","1","1","user_id", "1"]
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"api":"my_watch_later"})

        sys.modules["__main__"].client.vimeo_albums_getWatchLater.assert_any_call(page=1, per_page=15, full_response="true")

    def test_list_should_call_vimeo_client_correctly_if_api_is_my_newsubscriptions_in_params(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["1","1","1","user_id", "1"]
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"api":"my_newsubscriptions"})

        sys.modules["__main__"].client.vimeo_videos_getSubscriptions.assert_any_call(user_id="user_id", page=1, per_page=15, full_response="true", sort="newest")

    def test_list_should_call_vimeo_client_correctly_if_api_is_my_albums_in_params(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["1","1","1","user_id", "1"]
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"api":"my_albums"})

        sys.modules["__main__"].client.vimeo_albums_getAll.assert_any_call(user_id="user_id", page=1, per_page=15, full_response="true")

    def test_list_should_call_vimeo_client_correctly_if_api_is_my_groups_in_params(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["1","1","1","user_id", "1"]
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"api":"my_groups"})

        sys.modules["__main__"].client.vimeo_groups_getAll.assert_any_call(user_id="user_id", page=1, per_page=15, full_response="true")

    def test_list_should_call_vimeo_client_correctly_if_api_is_my_channels_in_params(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["1","1","1","user_id", "1"]
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"api":"my_channels"})

        sys.modules["__main__"].client.vimeo_channels_getAll.assert_any_call(user_id="user_id", page=1, per_page=15, full_response="true")

    def test_list_should_call_vimeo_client_correctly_if_api_is_my_contacts_in_params(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["1","1","1","user_id", "1"]
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"api":"my_contacts"})

        sys.modules["__main__"].client.vimeo_contacts_getAll.assert_any_call(user_id="user_id", page=1, per_page=15, full_response="true")

    def test_list_should_call_getVideoInfo_if_folder_is_not_in_params(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["1","1","1","user_id", "1"]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        core._getvideoinfo = Mock()

        core.list({"api":"my_contacts"})

        core._getvideoinfo.assert_any_call("222", {"api":"my_contacts"})

    def test_list_should_call_get_contacts_if_folder_is_contact_in_params(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["1","1","1","user_id", "1"]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        core._get_contacts = Mock()

        core.list({"api":"my_contacts","folder":"contact"})

        core._get_contacts.assert_any_call("222")

    def test_list_should_call_get_list_if_folder_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        core._get_list = Mock()

        core.list({"api":"my_contacts","folder":"true"})

        core._get_list.assert_any_call("true","222")

    def test_get_return_status_should_call_parseDOM(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.return_value = ["ok"]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()

        core._get_return_status("")

        assert (sys.modules["__main__"].common.parseDOM.call_count > 0)

    def test_get_return_status_should_call_return_status_200_on_success(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.return_value = ["ok"]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()

        (result, status) = core._get_return_status("")

        assert (status == 200)

    def test_get_return_status_should_call_return_status_303_on_fail(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.return_value = ["fail"]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()

        (result, status) = core._get_return_status("")

        assert (status == 303)

    def test_get_return_status_should_call_return_status_303_if_vimeo_failed_to_respond(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.return_value = []
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()

        (result, status) = core._get_return_status("")

        assert (status == 303)

    def test_get_list_should_call_parseDOM(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.return_value = []
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()

        core._get_list("some_tag", "some_html_string")

        sys.modules["__main__"].common.parseDOM.assert_any_call("some_html_string","some_tag")

    def test_get_list_should_construct_proper_item_list(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.return_value = ["some_value"]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()

        result = core._get_list("some_tag", "some_html_string")

        print repr(result)
        assert (result[0].has_key("some_tag"))
        assert (result[0].has_key("Description"))
        assert (result[0].has_key("Title"))

    def test_get_list_should_add_thumbnail_to_group_list(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.return_value = ["some_value"]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()

        result = core._get_list("group", "some_html_string")

        print repr(result)
        assert (result[0].has_key("thumbnail"))

    def test_get_list_should_add_thumbnail_to_channel_list(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.return_value = ["some_value"]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()

        result = core._get_list("channel", "some_html_string")

        print repr(result)
        assert (result[0].has_key("thumbnail"))

    def test_get_list_should_add_thumbnail_to_album_list(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.return_value = ["some_value"]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        core.getThumbnail = Mock(return_value="some_value")

        result = core._get_list("album", "some_html_string")

        print repr(result)
        assert (result[0].has_key("thumbnail"))

    def test_get_list_should_call_getThumbnail_on_album_lists(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.return_value = ["some_value"]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        core.getThumbnail = Mock(return_value="some_value")

        result = core._get_list("album", "some_html_string")

        print repr(result)
        core.getThumbnail.assert_any_call("some_value","default")

    def test_get_list_should_call_parseDOM(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.return_value = []
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()

        core._get_list("some_tag", "some_html_string")

        sys.modules["__main__"].common.parseDOM.assert_any_call("some_html_string","some_tag")

    def test_get_contacts_should_call_parseDOM(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.return_value = []
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        core.getThumbnail = Mock(return_value="some_value")

        result = core._get_contacts("some_html_string")

        print repr(result)
        assert (sys.modules["__main__"].common.parseDOM.call_count > 0)

    def test_get_contacts_should_construct_proper_list_items(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.side_effect =[ ["some_value"],["some_value"],["some_value"],["2"],["some_value"]]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        core.getThumbnail = Mock(return_value="some_value")

        result = core._get_contacts("some_html_string")

        print repr(result)
        assert (result[0].has_key("contact"))
        assert (result[0].has_key("thumbnail"))
        assert (result[0].has_key("Title"))

    def test_getvideoinfo_should_add_thumbnail_to_group_list(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_value"],["some_value"],["some_value"],["some_value"],["some_value"],["some_value"],["3"]]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        core.checkIfMorePagesExist = Mock()
        core.getThumbnail = Mock(return_value="some_value")

        result = core._getvideoinfo("some_html_string", {})

        print repr(result)
        assert (result[0].has_key("thumbnail"))

    def test_getvideoinfo_should_add_thumbnail_to_channel_list(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_value"],["some_value"],["some_value"],["some_value"],["some_value"],["some_value"],["3"]]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        core.checkIfMorePagesExist = Mock()
        core.getThumbnail = Mock(return_value="some_value")

        result = core._getvideoinfo("some_html_string", {})

        print repr(result)
        assert (result[0].has_key("thumbnail"))

    def test_getvideoinfo_should_add_thumbnail_to_album_list(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_value"],["some_value"],["some_value"],["some_value"],["some_value"],["some_value"],["3"]]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        core.checkIfMorePagesExist = Mock(return_value=True)
        core.getThumbnail = Mock(return_value="some_value")

        result = core._getvideoinfo("some_html_string", {})

        print repr(result)
        assert (result[0].has_key("thumbnail"))

    def test_getvideoinfo_should_call_getThumbnail_on_album_lists(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_value"],["some_value"],["some_value"],["some_value"],["some_value"],["some_value"],["3"]]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        core.checkIfMorePagesExist = Mock(return_value=True)
        core.getThumbnail = Mock(return_value="some_value")

        result = core._getvideoinfo("some_html_string", {})

        print repr(result)
        core.getThumbnail.assert_any_call("some_value","default")

    def test_getvideoinfo_should_construct_proper_item_list(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.side_effect = [["some_value"],["some_value"],["some_value"],["some_value"],["some_value"],["some_value"],["3"]]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        core.checkIfMorePagesExist = Mock(return_value=True)
        core.getThumbnail = Mock(return_value="some_value")

        result = core._getvideoinfo("some_html_string", {})

        print repr(result)
        assert (result[0].has_key("videoid"))
        assert (result[0].has_key("Overlay"))
        assert (result[0].has_key("contact"))
        assert (result[0].has_key("Studio"))
        assert (result[0].has_key("Duration"))
        assert (result[0].has_key("Title"))

    def test_getThumbnail_should_use_parseDOM(self):
        sys.modules["__main__"].settings.getSetting.return_value = "2"
        sys.modules["__main__"].common.parseDOM.side_effect = [["1"],["some_value"]]
        sys.modules["__main__"].client.vimeo_contacts_getAll.return_value = "222"
        core = VimeoCore()
        result = core.getThumbnail("album", "some_html_string")

        print repr(result)
        assert (sys.modules["__main__"].common.parseDOM.call_count > 0)

    def test_getThumbnail_should_use_return_low_quality_thumb_if_hq_thumbs_is_not_set(self):
        sys.modules["__main__"].settings.getSetting.return_value = "false"
        sys.modules["__main__"].common.parseDOM.side_effect = [["200","640"],["low_quality","high_quality"]]

        core = VimeoCore()

        result = core.getThumbnail("album", "some_html_string")

        assert (result == "low_quality")

    def test_getThumbnail_should_use_return_low_quality_thumb_if_hq_thumbs_is_set(self):
        sys.modules["__main__"].settings.getSetting.return_value = "true"
        sys.modules["__main__"].common.parseDOM.side_effect = [["200","640"],["low_quality","high_quality"]]

        core = VimeoCore()

        result = core.getThumbnail("album", "some_html_string")

        assert (result == "high_quality")

if __name__ == '__main__':
        nose.runmodule()
