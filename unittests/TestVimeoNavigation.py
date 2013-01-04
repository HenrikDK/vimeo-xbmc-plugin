# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock
import sys
from VimeoNavigation import VimeoNavigation


class TestVimeoNavigation(BaseTestCase.BaseTestCase):

    def test_listMenu_should_traverse_menustructure_correctly(self):
        sys.argv = ["something", -1, "something_else"]
        sys.modules["__main__"].settings.getSetting.return_value = "true"
        navigation = VimeoNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()
        navigation.listMenu()

        args = navigation.addListItem.call_args_list

        for arg in args:
            assert(arg[0][1]["path"].replace('/root/', '').find('/') < 0)
        assert(navigation.addListItem.call_count > 3)

    def test_listMenu_should_only_list_subfolders_to_a_path(self):
        sys.argv = ["something", -1, "something_else"]
        list = ["", "", "", ""]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: list.pop()
        navigation = VimeoNavigation()
        navigation.categories = ({"path": "/root/my_first_level"}, {"path": "/root/my_first_level/my_second_level"}, {"path": "/root/my_other_first_level"}, {"path": "/root/my_other_first_level/my_other_second_level"})
        navigation.list = Mock()
        navigation.addListItem = Mock()
        navigation.listMenu({"path": "/root/my_first_level"})

        navigation.addListItem.assert_called_with({"path": "/root/my_first_level"}, {"path": "/root/my_first_level/my_second_level"})

    def test_listMenu_should_use_visibility_from_settings_to_decide_if_items_are_displayed(self):
        sys.argv = ["something", -1, "something_else"]
        list = ["false", "true", "false", "true"]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: list.pop()
        navigation = VimeoNavigation()
        navigation.categories = ({"path": "/root/my_first_level"}, {"path": "/root/my_first_level/my_second_level1"}, {"path": "/root/my_first_level/my_second_level2"}, {"path": "/root/my_first_level/my_second_level3"})
        navigation.list = Mock()
        navigation.addListItem = Mock()
        navigation.listMenu({"path": "/root/my_first_level"})

        navigation.addListItem.assert_any_call({"path": "/root/my_first_level"}, {"path": "/root/my_first_level/my_second_level1"})
        navigation.addListItem.assert_any_call({"path": "/root/my_first_level"}, {"path": "/root/my_first_level/my_second_level3"})

    def test_listMenu_should_check_if_download_path_is_set_to_decide_if_download_folder_is_visible(self):
        sys.argv = ["something", -1, "something_else"]
        list = ["true", "true", "true", "", "true"]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: list.pop()
        navigation = VimeoNavigation()
        navigation.categories = ({"path": "/root/my_first_level/my_second_level1", "feed": "downloads"}, {"path": "/root/my_first_level/my_second_level2", "feed": "downloads"})
        navigation.list = Mock()
        navigation.addListItem = Mock()
        navigation.listMenu({"path": "/root/my_first_level"})

        navigation.addListItem.assert_called_with({"path": "/root/my_first_level"}, {"path": "/root/my_first_level/my_second_level2", "feed": "downloads"})

    def test_listMenu_should_call_list_if_api_in_params(self):
        sys.argv = ["something", -1, "something_else"]
        navigation = VimeoNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()
        navigation.listMenu({"path": "/root/some_other_path", "api": "some_feed"})

        navigation.list.assert_called_with({"path": "/root/some_other_path", "api": "some_feed"})

    def test_listMenu_should_call_list_if_feed_in_params(self):
        sys.argv = ["something", -1, "something_else"]
        navigation = VimeoNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()
        navigation.listMenu({"path": "/root/some_other_path", "feed": "some_feed"})

        navigation.list.assert_called_with({"path": "/root/some_other_path", "feed": "some_feed"})

    def test_listMenu_should_call_list_if_options_in_params(self):
        sys.argv = ["something", -1, "something_else"]
        navigation = VimeoNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()
        navigation.listMenu({"path": "/root/some_other_path", "options": "some_options"})

        navigation.list.assert_called_with({"path": "/root/some_other_path", "options": "some_options"})

    def test_listMenu_should_call_list_if_store_in_params(self):
        sys.argv = ["something", -1, "something_else"]
        navigation = VimeoNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()
        navigation.listMenu({"path": "/root/some_other_path", "store": "some_store"})

        navigation.list.assert_called_with({"path": "/root/some_other_path", "store": "some_store"})

    def test_listMenu_should_call_list_if_store_in_params(self):
        sys.argv = ["something", -1, "something_else"]
        navigation = VimeoNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()
        navigation.listMenu({"path": "/root/some_other_path", "scraper": "some_scraper"})

        navigation.list.assert_called_with({"path": "/root/some_other_path", "scraper": "some_scraper"})

    def test_listMenu_should_call_settings_getSetting_to_get_listview(self):
        sys.argv = ["something", -1, "something_else"]
        navigation = VimeoNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()
        navigation.listMenu({"path": "/root/some_other_path"})

        sys.modules["__main__"].settings.getSetting.assert_called_with("list_view")

    def test_listMenu_should_call_xbmc_executeBuiltin_correctly_if_list_view_is_set(self):
        sys.argv = ["something", -1, "something_else"]
        settings = ["1", "true", "1"]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
        navigation = VimeoNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()

        navigation.listMenu({"path": "/root/some_other_path"})

        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.SetViewMode(500)')

    def test_listMenu_should_call_xbmc_plugin_end_of_directory_correctly(self):
        sys.argv = ["something", -1, "something_else"]
        settings = ["1", "true", "1"]
        sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
        navigation = VimeoNavigation()
        navigation.list = Mock()
        navigation.addListItem = Mock()

        navigation.listMenu({"path": "/root/some_other_path"})

        sys.modules["__main__"].xbmcplugin.endOfDirectory.assert_called_with(cacheToDisc=True, handle=-1, succeeded=True)

    def test_list_should_call_feeds_if_feed_or_api_in_params(self):
        sys.argv = ["something", -1, "something_else"]
        sys.modules["__main__"].feeds.list.return_value = ("",303)
        navigation = VimeoNavigation()

        navigation.list({"path": "/root/some_path", "api": "some_api"})

        sys.modules["__main__"].feeds.list.assert_any_call({"path":"/root/some_path", "api":"some_api"})

    def test_list_should_not_call_parseVideoList_or_parseFolderList_if_return_code_is_not_200(self):
        sys.argv = ["something", -1, "something_else"]
        sys.modules["__main__"].feeds.list.return_value = ("",303)
        navigation = VimeoNavigation()
        navigation.parseVideoList = Mock()
        navigation.parseFolderList = Mock()

        navigation.list({"path": "/root/some_path", "api": "some_api"})

        assert(navigation.parseFolderList.call_count == 0)
        assert(navigation.parseVideoList.call_count == 0)

    def test_list_should_call_parseVideoList_if_folder_is_false_in_params(self):
        sys.argv = ["something", -1, "something_else"]
        sys.modules["__main__"].feeds.list.return_value = ("",200)
        navigation = VimeoNavigation()
        navigation.parseVideoList = Mock()

        navigation.list({"path": "/root/some_path", "api": "some_api", "folder":"false"})

        navigation.parseVideoList.assert_any_call({"path":"/root/some_path", "api":"some_api", "folder":"false"}, "")

    def test_list_should_call_parseVideoList_if_folder_is_not_in_params(self):
        sys.argv = ["something", -1, "something_else"]
        sys.modules["__main__"].feeds.list.return_value = ("",200)
        navigation = VimeoNavigation()
        navigation.parseVideoList = Mock()

        navigation.list({"path": "/root/some_path", "api": "some_api"})

        navigation.parseVideoList.assert_any_call({"path":"/root/some_path", "api":"some_api"}, "")

    def test_list_should_call_parseFolderList_if_folder_is_set_to_true_in_params(self):
        sys.argv = ["something", -1, "something_else"]
        sys.modules["__main__"].feeds.list.return_value = ("",200)
        navigation = VimeoNavigation()
        navigation.parseFolderList = Mock()

        navigation.list({"path": "/root/some_path", "api": "some_api", "folder":"true"})

        navigation.parseFolderList.assert_any_call({"path":"/root/some_path", "api":"some_api", "folder":"true"}, "")

    def test_list_should_call_showListingError_if_listing_failed(self):
        sys.argv = ["something", -1, "something_else"]
        sys.modules["__main__"].feeds.list.return_value = ("",303)
        navigation = VimeoNavigation()
        navigation.showListingError = Mock()

        navigation.list({"path": "/root/some_path", "api": "some_api"})

        navigation.showListingError.assert_any_call({"path": "/root/some_path", "api": "some_api"})

    def test_executeAction_should_call_login_if_action_is_settings(self):
        navigation = VimeoNavigation()

        navigation.executeAction({"action": "settings"})

        sys.modules["__main__"].login.login.assert_called_with({"action": "settings"})

    def test_executeAction_should_call_storage_editStoredSearch_if_action_is_edit_search(self):
        navigation = VimeoNavigation()
        navigation.listMenu = Mock()

        navigation.executeAction({"action": "edit_search"})

        sys.modules["__main__"].storage.editStoredSearch.assert_called_with({"action": "edit_search"})

    def test_executeAction_should_call_listMenu_if_action_is_edit_search(self):
        navigation = VimeoNavigation()
        navigation.listMenu = Mock()

        navigation.executeAction({"action": "edit_search"})

        navigation.listMenu.assert_called_with({"action": "edit_search"})

    def test_executeAction_should_call_setLike_if_action_is_remove_favorite(self):
        navigation = VimeoNavigation()
        navigation.setLike = Mock()

        navigation.executeAction({"action": "remove_favorite"})

        navigation.setLike.assert_called_with({"action": "remove_favorite"})

    def test_executeAction_should_call_setLike_if_action_is_add_favorite(self):
        navigation = VimeoNavigation()
        navigation.setLike = Mock()

        navigation.executeAction({"action": "add_favorite"})

        navigation.setLike.assert_called_with({"action": "add_favorite"})

    def test_executeAction_should_call_updateContact_if_action_is_remove_contact(self):
        navigation = VimeoNavigation()
        navigation.updateContact = Mock()

        navigation.executeAction({"action": "remove_contact"})

        navigation.updateContact.assert_called_with({"action": "remove_contact"})

    def test_executeAction_should_call_addContact_if_action_is_add_contact(self):
        navigation = VimeoNavigation()
        navigation.updateContact = Mock()

        navigation.executeAction({"action": "add_contact"})

        navigation.updateContact.assert_called_with({"action": "add_contact"})

    def test_executeAction_should_call_updateSubscription_if_action_is_remove_subscription(self):
        navigation = VimeoNavigation()
        navigation.updateSubscription = Mock()

        navigation.executeAction({"action": "remove_subscription"})

        navigation.updateSubscription.assert_called_with({"action": "remove_subscription"})

    def test_executeAction_should_call_updateSubscription_if_action_is_add_subscription(self):
        navigation = VimeoNavigation()
        navigation.updateSubscription = Mock()

        navigation.executeAction({"action": "add_subscription"})

        navigation.updateSubscription.assert_called_with({"action": "add_subscription"})

    def test_executeAction_should_call_downloader_downloadVideo_if_action_is_download(self):
        navigation = VimeoNavigation()
        navigation.downloadVideo = Mock()

        navigation.executeAction({"action": "download"})

        navigation.downloadVideo.assert_called_with({'action': 'download'})

    def test_download_should_call_downloader_downloadVideo_if_action_is_download(self):
        sys.modules["__main__"].player.getVideoObject = Mock()
        sys.modules["__main__"].player.getVideoObject.return_value = ({"videoid": "ytvideo1", "video_url": "Mock url", "Title": "Mock Title" }, "mock" )
        sys.modules["__main__"].settings.getSetting.return_value = "some_path"
        navigation = VimeoNavigation()

        navigation.executeAction({"action": "download"})

        sys.modules["__main__"].downloader.download.assert_called_with("Mock Title-[ytvideo1].mp4", {'action': 'download', 'url': 'Mock url', "download_path": "some_path", "Title": "Mock Title"})

    def test_download_should_call_showMessage_if_video_object_is_missing_a_video_url_and_contains_api_error(self):
        sys.modules["__main__"].player.getVideoObject = Mock(return_value= ({"apierror": "some_error"}, "mock" ))
        sys.modules["__main__"].settings.getSetting.return_value = "some_path"
        sys.modules["__main__"].language.return_value = ""
        navigation = VimeoNavigation()

        navigation.downloadVideo({"action": "download"})

        sys.modules["__main__"].utils.showMessage.assert_any_call("", 'some_error')

    def test_download_should_call_showMessage_if_video_object_is_empty(self):
        sys.modules["__main__"].player.getVideoObject = Mock()
        sys.modules["__main__"].player.getVideoObject.return_value = ({}, "mock" )
        sys.modules["__main__"].settings.getSetting.return_value = "some_path"
        sys.modules["__main__"].language.return_value = ""
        navigation = VimeoNavigation()

        navigation.executeAction({"action": "download"})

        sys.modules["__main__"].utils.showMessage.assert_any_call("", 'ERROR')

    def test_executeAction_should_call_player_playVideo_if_action_is_play_video(self):
        navigation = VimeoNavigation()
        navigation.playVideo = Mock()
        navigation.executeAction({"action": "play_video"})

        sys.modules["__main__"].player.playVideo.assert_called_with({"action": "play_video"})

    def test_executeAction_should_call_storage_deleteStoredSearch_if_action_is_delete_search(self):
        navigation = VimeoNavigation()

        navigation.executeAction({"action": "delete_search"})

        sys.modules["__main__"].storage.deleteStoredSearch.assert_called_with({"action": "delete_search"})

    def test_executeAction_should_call_removeWatchLater_if_action_is_remove_watch_later(self):
        navigation = VimeoNavigation()
        navigation.removeWatchLater = Mock()
        navigation.executeAction({"action": "remove_watch_later"})

        navigation.removeWatchLater.assert_called_with({"action": "remove_watch_later"})

    def test_executeAction_should_call_updateGroup_if_action_is_join_group(self):
        navigation = VimeoNavigation()
        navigation.updateGroup = Mock()
        navigation.executeAction({"action": "join_group"})

        navigation.updateGroup.assert_called_with({"action": "join_group"})

    def test_executeAction_should_call_updateGroup_if_action_is_leave_group(self):
        navigation = VimeoNavigation()
        navigation.updateGroup = Mock()
        navigation.executeAction({"action": "leave_group"})

        navigation.updateGroup.assert_called_with({"action": "leave_group"})

    def test_executeAction_should_call_playlist_createPlaylist_if_action_is_create_album(self):
        navigation = VimeoNavigation()
        navigation.executeAction({"action": "create_album"})

        sys.modules["__main__"].playlist.createAlbum.assert_called_with({"action": "create_album"})

    def test_executeAction_should_call_playlist_playAll_if_action_is_play_all(self):
        navigation = VimeoNavigation()

        navigation.executeAction({"action": "play_all"})

        sys.modules["__main__"].playlist.playAll.assert_called_with({"action": "play_all"})

    def test_executeAction_should_call_playlist_addToPlaylist_if_action_is_add_to_playlist(self):
        navigation = VimeoNavigation()

        navigation.executeAction({"action": "add_to_album"})

        sys.modules["__main__"].playlist.addToAlbum.assert_called_with({"action": "add_to_album"})

    def test_executeAction_should_call_playlist_removeFromPlaylist_if_action_is_remove_from_playlist(self):
        navigation = VimeoNavigation()

        navigation.executeAction({"action": "remove_from_album"})

        sys.modules["__main__"].playlist.removeFromAlbum.assert_called_with({"action": "remove_from_album"})

    def test_executeAction_should_call_playlist_deletePlaylist_if_action_is_delete_playlist(self):
        navigation = VimeoNavigation()

        navigation.executeAction({"action": "delete_album"})

        sys.modules["__main__"].playlist.deleteAlbum.assert_called_with({"action": "delete_album"})

    def test_executeAction_should_call_storage_reversePlaylistOrder_if_action_is_reverse_order(self):
        navigation = VimeoNavigation()

        navigation.executeAction({"action": "reverse_order"})

        sys.modules["__main__"].storage.reversePlaylistOrder.assert_called_with({"action": "reverse_order"})

    def test_setLiked_should_exit_cleanly_if_video_id_is_missing(self):
        navigation = VimeoNavigation()

        navigation.setLike()

        assert(sys.modules["__main__"].core.setLike.call_count == 0)

    def test_setLiked_should_call_core_setLiked_if_video_id_is_present_in_params(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].core.setLike.return_value = ("", 303)

        navigation.setLike({"videoid":"some_id"})

        sys.modules["__main__"].core.setLike.assert_any_call({"videoid":"some_id"})

    def test_setLiked_should_call_refresh_folder_list_if_action_is_remove_favorite_and_call_to_core_succeded(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].core.setLike.return_value = ("", 200)

        navigation.setLike({"action":"remove_favorite", "videoid":"some_id"})

        sys.modules["__main__"].xbmc.executebuiltin.assert_any_call("Container.Refresh")

    def test_setLiked_should_call_utils_show_showErrorMessage_if_call_to_core_failed(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = ""
        sys.modules["__main__"].core.setLike.return_value = ("", 303)

        navigation.setLike({"videoid":"some_id"})

        sys.modules["__main__"].utils.showErrorMessage.assert_any_call("", "", 303)

    def test_updateContact_should_exit_cleanly_if_no_contact_is_present_in_params_and_user_cancels(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].common.getUserInput.return_value = ""

        navigation.updateContact({})

        assert(sys.modules["__main__"].core.updateContact.call_count == 0)

    def test_updateContact_should_ask_user_for_contact_name_if_no_contact_is_present_in_params(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = "title"
        sys.modules["__main__"].common.getUserInput.return_value = ""

        navigation.updateContact({})

        sys.modules["__main__"].common.getUserInput.assert_any_call("title","")

    def test_updateContact_should_call_core_updateContact_if_contact_is_present_in_params(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].core.updateContact.return_value = ("", 200)

        navigation.updateContact({"contact":"some_contact"})

        sys.modules["__main__"].core.updateContact.assert_any_call({"contact":"some_contact"})

    def test_updateContact_should_call_utils_showMessage_if_call_to_core_succeeds(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = ""
        sys.modules["__main__"].core.updateContact.return_value = ("", 200)

        navigation.updateContact({"contact":"some_contact"})

        sys.modules["__main__"].utils.showMessage.assert_any_call("","some_contact")

    def test_updateContact_should_refresh_folder_listing_if_call_to_core_succeeds(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = ""
        sys.modules["__main__"].core.updateContact.return_value = ("", 200)

        navigation.updateContact({"contact":"some_contact"})

        sys.modules["__main__"].xbmc.executebuiltin.assert_any_call("Container.Refresh")

    def test_updateContact_should_call_utils_showErrorMessage_if_call_to_core_fails(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = ""
        sys.modules["__main__"].core.updateContact.return_value = ("", 303)

        navigation.updateContact({"contact":"some_contact"})

        sys.modules["__main__"].utils.showErrorMessage.assert_any_call("","", 303)

    def test_updateGroup_should_exit_cleanly_if_no_contact_is_present_in_params_and_user_cancels(self):
        navigation = VimeoNavigation()

        navigation.updateGroup({})

        assert(sys.modules["__main__"].core.updateGroup.call_count == 0)

    def test_updateGroup_should_call_core_updateGroup_if_group_is_present_in_params(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].core.updateGroup.return_value = ("", 200)

        navigation.updateGroup({"group":"some_group"})

        sys.modules["__main__"].core.updateGroup.assert_any_call({"group":"some_group"})

    def test_updateGroup_should_refresh_folder_listing_if_leave_group_is_in_params_and_call_to_core_succeeds(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = ""
        sys.modules["__main__"].core.updateGroup.return_value = ("", 200)

        navigation.updateGroup({"action":"leave_group","group":"some_group"})

        sys.modules["__main__"].xbmc.executebuiltin.assert_any_call("Container.Refresh")

    def test_updateGroup_should_call_utils_showErrorMessage_if_call_to_core_fails(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = ""
        sys.modules["__main__"].core.updateGroup.return_value = ("", 303)

        navigation.updateGroup({"group":"some_group"})

        sys.modules["__main__"].utils.showErrorMessage.assert_any_call("","", 303)

    def test_updateSubscription_should_exit_cleanly_if_no_channel_is_present_in_params_and_user_cancels(self):
        navigation = VimeoNavigation()

        navigation.updateSubscription({})

        assert(sys.modules["__main__"].core.updateSubscription.call_count == 0)

    def test_updateSubscription_should_call_core_updateSubscription_if_channel_is_present_in_params(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].core.updateSubscription.return_value = ("", 200)

        navigation.updateSubscription({"channel":"some_channel"})

        sys.modules["__main__"].core.updateSubscription.assert_any_call({"channel":"some_channel"})

    def test_updateSubscription_should_refresh_folder_listing_if_remove_subscription_is_in_params_and_call_to_core_succeeds(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = ""
        sys.modules["__main__"].core.updateSubscription.return_value = ("", 200)

        navigation.updateSubscription({"action":"remove_subscription","channel":"some_channel"})

        sys.modules["__main__"].xbmc.executebuiltin.assert_any_call("Container.Refresh")

    def test_updateSubscription_should_call_utils_showErrorMessage_if_call_to_core_fails(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = ""
        sys.modules["__main__"].core.updateSubscription.return_value = ("", 303)

        navigation.updateSubscription({"channel":"some_channel"})

        sys.modules["__main__"].utils.showErrorMessage.assert_any_call("","", 303)

    def test_removeWatchLater_should_exit_cleanly_if_no_videoid_is_present_in_params_and_user_cancels(self):
        navigation = VimeoNavigation()

        navigation.removeWatchLater({})

        assert(sys.modules["__main__"].core.removeWatchLater.call_count == 0)

    def test_removeWatchLater_should_call_core_removeWatchLater_if_videoid_is_present_in_params(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].core.removeWatchLater.return_value = ("", 200)

        navigation.removeWatchLater({"videoid":"some_videoid"})

        sys.modules["__main__"].core.removeWatchLater.assert_any_call({"videoid":"some_videoid"})

    def test_removeWatchLater_should_refresh_folder_listing_if_call_to_core_succeeds(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = ""
        sys.modules["__main__"].core.removeWatchLater.return_value = ("", 200)

        navigation.removeWatchLater({"videoid":"some_videoid"})

        sys.modules["__main__"].xbmc.executebuiltin.assert_any_call("Container.Refresh")

    def test_showListingError_should_search_categories_for_folder_name_if_external_is_not_in_params(self):
        sys.modules["__main__"].language.return_value = "some_string"
        navigation = VimeoNavigation()
        navigation.categories = ({"feed": "my_feed", "Title": "my_category_title"}, {"feed": "not_my_feed", "Title": "not_my_category_title"})

        navigation.showListingError({"feed": "my_feed"})

        sys.modules["__main__"].utils.showMessage.assert_called_with("my_category_title", "some_string")

    def test_showListingError_should_search_storage_user_options_if_external_is_in_params(self):
        sys.modules["__main__"].language.return_value = "some_string"
        sys.modules["__main__"].storage.user_options = ({"feed": "my_feed", "Title": "my_options_title"}, {"feed": "not_my_feed", "Title": "not_my_options_title"})
        navigation = VimeoNavigation()

        navigation.showListingError({"feed": "my_feed", "external": "true"})

        sys.modules["__main__"].utils.showMessage.assert_called_with("my_options_title", "some_string")

    def test_showListingError_should_use_channel_title_if_channel_is_in_params(self):
        sys.modules["__main__"].language.return_value = "some_string"
        navigation = VimeoNavigation()
        navigation.categories = ({"feed": "my_feed", "Title": "my_category_title"}, {"feed": "not_my_feed", "Title": "not_my_category_title"})

        navigation.showListingError({"feed": "my_feed", "channel": "some_channel_title"})

        sys.modules["__main__"].utils.showMessage.assert_called_with("some_channel_title", "some_string")

    def test_showListingError_should_use_language_string_if_playlist_is_in_params(self):
        sys.modules["__main__"].language.return_value = "some_string"
        navigation = VimeoNavigation()
        navigation.categories = ({"feed": "my_feed", "Title": "my_category_title"}, {"feed": "not_my_feed", "Title": "not_my_category_title"})

        navigation.showListingError({"feed": "my_feed", "playlist": "some_playlist"})

        sys.modules["__main__"].utils.showMessage.assert_called_with("some_string", "some_string")
        sys.modules["__main__"].language.assert_any_call(30615)
        sys.modules["__main__"].language.assert_any_call(30601)

    def test_showListingError_should_call_utils_showMessage_correctly(self):
        sys.modules["__main__"].language.return_value = "some_string"
        navigation = VimeoNavigation()
        navigation.categories = ({"feed": "my_feed", "Title": "my_category_title"}, {"feed": "not_my_feed", "Title": "not_my_category_title"})

        navigation.showListingError({"feed": "my_feed"})

        sys.modules["__main__"].utils.showMessage.assert_called_with("my_category_title", "some_string")

    def test_setLike_should_exit_cleanly_if_video_id_is_missing(self):
        navigation = VimeoNavigation()

        navigation.setLike()

        assert(sys.modules["__main__"].core.setLike.call_count == 0)
        assert(sys.modules["__main__"].utils.showErrorMessage.call_count == 0)

    def test_setLike_should_call_core_add_favorite(self):
        sys.modules["__main__"].core.setLike.return_value = ("", 303)
        sys.modules["__main__"].language.return_value = "some_title"
        navigation = VimeoNavigation()

        navigation.setLike({"videoid": "some_id"})

        sys.modules["__main__"].core.setLike.assert_called_with({"videoid": "some_id"})

    def test_setLike_should_show_error_message_on_failure(self):
        sys.modules["__main__"].core.setLike.return_value = ("", 303)
        sys.modules["__main__"].language.return_value = "some_title"
        navigation = VimeoNavigation()

        navigation.setLike({"videoid": "some_id"})

        sys.modules["__main__"].utils.showErrorMessage.assert_called_with("some_title", "", 303)
        sys.modules["__main__"].language.assert_called_with(30020)

    def test_setLike_should_call_refresh_folder_if_action_is_remove_favorite(self):
        sys.modules["__main__"].core.setLike.return_value = ("", 200)
        navigation = VimeoNavigation()

        navigation.setLike({"videoid": "some_id", "action":"remove_favorite"})

        assert(sys.modules["__main__"].core.setLike.call_count == 1)
        assert(sys.modules["__main__"].xbmc.executebuiltin.call_count == 1)

    def test_updateContact_should_ask_user_for_contact_name_if_missing(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = "some_title"
        sys.modules["__main__"].common.getUserInput.return_value = ""

        navigation.updateContact()

        sys.modules["__main__"].common.getUserInput.assert_called_with("some_title", "")

    def test_updateContact_should_call_core_updateContact(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].core.updateContact.return_value = ("", 200)
        sys.modules["__main__"].language.return_value = "some_title"

        navigation.updateContact({"contact": "some_contact"})

        sys.modules["__main__"].core.updateContact.assert_called_with({"contact": "some_contact"})

    def test_updateContact_should_exit_cleanly_if_contact_is_missing_and_no_contact_is_given(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = "some_title"
        sys.modules["__main__"].common.getUserInput.return_value = ""

        navigation.updateContact()

        assert(sys.modules["__main__"].core.updateContact.call_count == 0)
        assert(sys.modules["__main__"].utils.showErrorMessage.call_count == 0)
        sys.modules["__main__"].common.getUserInput.assert_called_with("some_title", "")

    def test_updateContact_should_show_error_message_on_failure(self):
        sys.modules["__main__"].core.updateContact.return_value = ("", 303)
        sys.modules["__main__"].language.return_value = "some_title"
        navigation = VimeoNavigation()

        navigation.updateContact({"contact": "some_contact"})

        sys.modules["__main__"].utils.showErrorMessage.assert_called_with("some_title", "", 303)
        sys.modules["__main__"].language.assert_any_call(30029)

    def test_updateContact_should_show_success_message_on_success(self):
        sys.modules["__main__"].core.updateContact.return_value = ("", 200)
        sys.modules["__main__"].language.return_value = "some_title"
        navigation = VimeoNavigation()

        navigation.updateContact({"contact": "some_contact"})

        sys.modules["__main__"].utils.showMessage.assert_called_with("some_title", "some_contact")
        sys.modules["__main__"].language.assert_any_call(30013)

    def test_updateContact_should_call_xbmc_executebuiltin_on_success(self):
        sys.modules["__main__"].core.updateContact.return_value = ("", 200)
        sys.modules["__main__"].language.return_value = "some_title"
        navigation = VimeoNavigation()

        navigation.updateContact({"contact": "some_contact"})

        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.Refresh')

    def test_updateGroup_should_exit_cleanly_if_group_is_missing(self):
        navigation = VimeoNavigation()

        navigation.updateGroup()

        assert(sys.modules["__main__"].core.updateGroup.call_count == 0)
        assert(sys.modules["__main__"].utils.showErrorMessage.call_count == 0)

    def test_updateGroup_should_call_core_updateGroup(self):
        sys.modules["__main__"].core.updateGroup.return_value = ("", 200)
        navigation = VimeoNavigation()

        navigation.updateGroup({"group": "some_group"})

        sys.modules["__main__"].core.updateGroup.assert_called_with({"group": "some_group"})

    def test_updateGroup_should_show_error_message_on_failure(self):
        sys.modules["__main__"].core.updateGroup.return_value = ("", 303)
        sys.modules["__main__"].language.return_value = "some_title"
        navigation = VimeoNavigation()

        navigation.updateGroup({"group": "some_group"})

        sys.modules["__main__"].utils.showErrorMessage.assert_called_with("some_title", "", 303)
        sys.modules["__main__"].language.assert_any_call(30029)

    def test_updateGroup_should_call_xbmc_execute_builtin_if_action_is_leave_group(self):
        sys.modules["__main__"].core.updateGroup.return_value = ("", 200)
        sys.modules["__main__"].language.return_value = "some_title"
        navigation = VimeoNavigation()

        navigation.updateGroup({"group": "some_group","action":"leave_group"})

        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.Refresh')

    def test_updateSubscription_should_exit_cleanly_if_channel_is_missing(self):
        navigation = VimeoNavigation()

        navigation.updateSubscription()

        assert(sys.modules["__main__"].core.updateSubscription.call_count == 0)
        assert(sys.modules["__main__"].utils.showErrorMessage.call_count == 0)

    def test_updateSubscription_should_call_core_updateSubscription(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].core.updateSubscription.return_value = ("", 200)

        navigation.updateSubscription({"channel": "some_channel"})

        sys.modules["__main__"].core.updateSubscription.assert_called_with({"channel": "some_channel"})

    def test_updateSubscription_should_show_error_message_on_failure(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = "some_message"
        sys.modules["__main__"].core.updateSubscription.return_value = ("", 303)

        navigation.updateSubscription({"channel": "some_channel"})

        sys.modules["__main__"].utils.showErrorMessage.assert_called_with("some_message", "", 303)
        sys.modules["__main__"].language.assert_called_with(30021)

    def test_updateSubscription_should_call_xbmc_execute_builtin_if_action_is_remove_subscription(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].core.updateSubscription.return_value = ("", 200)

        navigation.updateSubscription({"channel": "some_channel","action":"remove_subscription"})

        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.Refresh')

    def test_removeWatchLater_should_exit_cleanly_if_channel_is_missing(self):
        navigation = VimeoNavigation()

        navigation.removeWatchLater()

        assert(sys.modules["__main__"].core.removeWatchLater.call_count == 0)
        assert(sys.modules["__main__"].utils.showErrorMessage.call_count == 0)

    def test_removeWatchLater_should_call_core_add_subscription(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].core.removeWatchLater.return_value = ("", 200)

        navigation.removeWatchLater({"videoid": "some_videoid"})

        sys.modules["__main__"].core.removeWatchLater.assert_called_with({"videoid": "some_videoid"})

    def test_removeWatchLater_should_call_execute_builtin_on_success(self):
        navigation = VimeoNavigation()
        sys.modules["__main__"].language.return_value = "some_message"
        sys.modules["__main__"].core.removeWatchLater.return_value = ("", 200)

        navigation.removeWatchLater({"videoid": "some_videoid"})

        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.Refresh')

    def test_addListItem_should_call_addFolderListItem_if_item_is_not_an_action_and_doesnt_require_login(self):
        sys.modules["__main__"].settings.getSetting.return_value = ""
        navigation = VimeoNavigation()
        navigation.addFolderListItem = Mock()

        navigation.addListItem({}, {"feed": "some_feed", "login": "false"})

        navigation.addFolderListItem.assert_called_with({}, {"feed": "some_feed", "login": "false"})

    def test_addListItem_should_call_addFolderListItem_if_item_is_not_an_action__requires_login_and_user_is_logged_in(self):
        sys.modules["__main__"].settings.getSetting.return_value = "some_token"
        navigation = VimeoNavigation()
        navigation.addFolderListItem = Mock()

        navigation.addListItem({}, {"feed": "some_feed", "login": "true"})

        navigation.addFolderListItem.assert_called_with({}, {"feed": "some_feed", "login": "true"})

    def test_addListItem_should_call_addActionListItem_if_item_action_is_settings_user_is_logged_in_and_item_requires_login(self):
        sys.modules["__main__"].settings.getSetting.return_value = "some_token"
        navigation = VimeoNavigation()
        navigation.addActionListItem = Mock()

        navigation.addListItem({}, {"action": "settings", "login": "true"})

        navigation.addActionListItem.assert_called_with({}, {"action": "settings", "login": "true"})

    def test_addListItem_should_call_addActionListItem_if_item_action_is_settings_user_is_not_logged_in_and_item_doesnt_require_login(self):
        sys.modules["__main__"].settings.getSetting.return_value = ""
        navigation = VimeoNavigation()
        navigation.addActionListItem = Mock()

        navigation.addListItem({}, {"action": "settings", "login": "false"})

        navigation.addActionListItem.assert_called_with({}, {"action": "settings", "login": "false"})

    def test_addListItem_should_call_addActionListItem_if_item_has_action(self):
        navigation = VimeoNavigation()
        navigation.addActionListItem = Mock()

        navigation.addListItem({}, {"action": "some_action"})

        navigation.addActionListItem.assert_called_with({}, {"action": "some_action"})

    def test_addFolderListItem_should_call_utils_get_thumbnail_to_get_icon_path(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.buildItemUrl.return_value = ""
        navigation = VimeoNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []

        navigation.addFolderListItem({}, {"action": "some_action", "icon": "some_icon"})

        sys.modules["__main__"].utils.getThumbnail("some_icon")

    def test_addFolderListItem_should_call_addFolderContextMenuItems_to_get_context_menu_items(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.buildItemUrl.return_value = ""
        navigation = VimeoNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []

        navigation.addFolderListItem({}, {"action": "some_action", "icon": "some_icon"})

        navigation.addFolderContextMenuItems.assert_called_with({}, {"action": "some_action", "icon": "some_icon"})

    def test_addFolderListItem_should_call_utils_get_thumbnail_to_get_thumbnail_path(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.buildItemUrl.return_value = ""
        navigation = VimeoNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []

        navigation.addFolderListItem({}, {"action": "some_action", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].utils.getThumbnail.assert_called_with("some_thumbnail")

    def test_addFolderListItem_should_call_xbmcgui_ListItem_to_fetch_xbmc_listitem_object(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.buildItemUrl.return_value = ""
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []

        navigation.addFolderListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].xbmcgui.ListItem.assert_called_with("some_title", iconImage='some_image_path', thumbnailImage='some_image_path')

    def test_addFolderListItem_should_call_utils_buildItemUrl_to_get_proper_item_url(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.buildItemUrl.return_value = ""
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []

        navigation.addFolderListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].utils.buildItemUrl({"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

    def test_addFolderListItem_should_call_listitem_addContextMenuItems_to_add_context_menu(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.buildItemUrl.return_value = ""
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = [1, 2]

        navigation.addFolderListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].xbmcgui.ListItem().addContextMenuItems.assert_called_with([1,2], replaceItems=False)

    def test_addFolderListItem_should_call_listitem_setProperty_to_inidicate_item_is_a_folder(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.buildItemUrl.return_value = ""
        navigation = VimeoNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []

        navigation.addFolderListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].xbmcgui.ListItem().setProperty.assert_called_with('Folder', 'true')

    def ttest_addFolderListItem_should_call_settings_getSetting_to_fetch_downloadPath_if_item_feed_is_downloads(self):
        sys.argv = ["some_path", -1, "some_params"]
        navigation = VimeoNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []

        navigation.addFolderListItem({}, {"feed": "downloads", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].settings.getSetting.assert_called_with("downloadPath")

    def test_addFolderListItem_should_call_xbmcplugin_addDirectoryItem_correctly(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.buildItemUrl.return_value = ""
        navigation = VimeoNavigation()
        navigation.addFolderContextMenuItems = Mock()
        navigation.addFolderContextMenuItems.return_value = []

        navigation.addFolderListItem({}, {"feed": "downloads", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].settings.getSetting.assert_called_with("downloadPath")

    def test_addActionListItem_should_call_utils_get_thumbnail_to_get_thumbnail_path(self):
        sys.argv = ["some_path", -1, "some_params"]
        navigation = VimeoNavigation()

        navigation.addActionListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].utils.getThumbnail.assert_called_with("some_thumbnail")

    def test_addActionListItem_should_call_xbmcgui_ListItem_to_fetch_xbmc_listitem_object(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()

        navigation.addActionListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].xbmcgui.ListItem.assert_called_with("some_title",iconImage='DefaultFolder.png', thumbnailImage='some_image_path')

    def test_addActionListItem_should_call_listitem_setProperty_to_inidicate_item_is_playable_if_item_action_is_playbyid(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()

        navigation.addActionListItem({}, {"action": "playbyid", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].xbmcgui.ListItem().setProperty.assert_called_with("IsPlayable", "true")

    def test_addActionListItem_should_call_xbmcplugin_addDirectoryItem_correctly(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].xbmcgui.ListItem.return_value = []
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()

        navigation.addActionListItem({}, {"action": "some_action", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].xbmcplugin.addDirectoryItem.assert_called_with(totalItems = 0, url="some_path?path=None&action=some_action&", isFolder=True, listitem = [], handle=-1)

    def test_addVideoListItem_should_call_utils_get_thumbnail_to_get_icon_path(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        
        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].utils.getThumbnail.assert_called_with("some_icon")

    def test_addVideoListItem_should_call_xbmcgui_ListItem_to_fetch_xbmc_listitem_object(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].common.makeAscii.return_value = "some_title"
        sys.modules["__main__"].language.return_value = "some_button_string %s"

        navigation = VimeoNavigation()
        navigation.addContextMenuItems = Mock()

        navigation.addVideoListItem({"path": "/some/path"}, {"videoid": "video1", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].xbmcgui.ListItem.assert_called_with("some_title", iconImage="some_image_path", thumbnailImage="some_thumbnail")

    def test_addVideoListItem_should_call_addVideoContextMenuItems_to_get_context_menu_items(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        
        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        navigation.addVideoContextMenuItems.assert_called_with({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

    def test_addVideoListItem_should_call_listitem_addVideoContextMenuItems_to_add_context_menu(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoContextMenuItems.return_value = []
        
        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})
        
        sys.modules["__main__"].xbmcgui.ListItem().addContextMenuItems.assert_called_with([],replaceItems=True)

    def test_addVideoListItem_should_call_listitem_setProperty_to_indicate_listitem_is_video(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoContextMenuItems.return_value = []

        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].xbmcgui.ListItem().setProperty.assert_any_call("Video", "true")
        sys.modules["__main__"].xbmcgui.ListItem().setProperty.assert_any_call("IsPlayable", "true")

    def test_addVideoListItem_should_call_listitem_setInfo_to_allow_xbmc_to_sort_and_display_video_info(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoContextMenuItems.return_value = []

        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].xbmcgui.ListItem().setInfo.assert_called_with(infoLabels={'icon': 'some_icon', 'thumbnail': 'some_thumbnail', 'Title': 'some_title'}, type='Video')

    def test_addVideoListItem_should_call_xbmcplugin_addDirectoryItem_correctly(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        list_item = Mock()
        sys.modules["__main__"].xbmcgui.ListItem.return_value = list_item
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoContextMenuItems.return_value = []

        navigation.addVideoListItem({}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"})

        sys.modules["__main__"].xbmcplugin.addDirectoryItem.assert_called_with(handle=-1, url="some_path?path=None&action=play_video&videoid=None", listitem=list_item, isFolder=False, totalItems=1)

    def test_parseFolderList_should_set_cache_false_if_item_is_store_og_user_feed(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseFolderList({"user_feed": "some_feed", "path": "some_path"},[{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}])
        
        sys.modules["__main__"].xbmcplugin.endOfDirectory.assert_called_with(handle=-1,succeeded=True,cacheToDisc=False)

    def test_parseFolderList_should_call_addFolderListItem_for_each_item(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseFolderList({"user_feed": "some_feed", "path": "some_path"},[{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}])
        
        assert(navigation.addFolderListItem.call_count == 3)

    def test_parseFolderList_should_add_feed_custom_options_list_if_feed_is_contacts(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addFolderListItem = Mock()

        navigation.parseFolderList({"api": "my_contacts", "path": "some_path"},[{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}])

        navigation.addFolderListItem.assert_any_call({"api": "my_contacts", "path": "some_path"},{'feed': 'contact_option_list', 'path': 'some_path', 'icon': 'some_icon', 'thumbnail': 'some_thumbnail', 'Title': 'some_title'},1)

    def test_parseFolderList_should_call_xbmcplugin_endOfDirectory_correctly(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseFolderList({"user_feed": "some_feed", "path": "some_path"},[{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}])
        
        sys.modules["__main__"].xbmcplugin.endOfDirectory.assert_called_with(handle=-1,succeeded=True,cacheToDisc=False)

    def test_parseVideoList_should_skip_items_where_videoid_is_false(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 0
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        
        navigation.parseVideoList({"user_feed": "some_feed", "path": "some_path"},[{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}])
        
        assert(navigation.addVideoListItem.call_count == 2)

    def test_parseVideoList_should_call_addFolderListItem_to_next_item(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 0
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseVideoList({"api": "my_watch_later", "path": "some_path"},[{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"next": "true", "Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}])
        
        navigation.addFolderListItem.assert_called_with({"api": "my_watch_later", "path": "some_path"}, {"next": "true",'path': 'some_path', 'icon': 'some_icon', 'index': '3', 'thumbnail': 'some_thumbnail', 'Title': 'some_title'},3)

    def test_parseVideoList_should_call_addVideoListItem_if_item_is_not_next_item(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 0
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseVideoList({"api": "my_watch_later", "path": "some_path"},[{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "next": "true"}])
        
        navigation.addVideoListItem.assert_called_once_with({'path': 'some_path', 'api': 'my_watch_later'}, {'path': 'some_path', 'icon': 'some_icon', 'index': '1', 'thumbnail': 'some_thumbnail', 'Title': 'some_title'},3)

    def test_parseVideoList_should_call_settings_getSetting_to_get_list_view(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 0
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseVideoList({"scraper": "watch_later", "path": "some_path"},[{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "next": "true"}])
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("list_view")

    def test_parseVideoList_should_call_xbmc_executebuiltin_if_list_view_is_set(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 1
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseVideoList({"scraper": "watch_later", "path": "some_path"},[{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "next": "true"}])
        
        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.SetViewMode(500)')
        
    def test_parseVideoList_should_call_xbmcplugin_addSortMethod_for_valid_sort_methods(self):
        sys.argv = ["some_path", -1, "some_params"]
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 1
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseVideoList({"scraper": "watch_later", "path": "some_path"},[{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "next": "true"}])
        
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1,sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_UNSORTED)
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1,sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_LABEL)
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1,sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_VIDEO_RATING)
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1,sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_DATE)
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1,sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_PROGRAM_COUNT)
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1,sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
        sys.modules["__main__"].xbmcplugin.addSortMethod.assert_any_call(handle=-1,sortMethod=sys.modules["__main__"].xbmcplugin.SORT_METHOD_GENRE)
        
    def test_parseVideoList_should_call_xbmcplugin_endOfDirectory_correctly(self):
        sys.modules["__main__"].utils.getThumbnail.return_value = "some_image_path"
        sys.modules["__main__"].settings.getSetting.return_value = 1
        navigation = VimeoNavigation()
        navigation.addVideoContextMenuItems = Mock()
        navigation.addVideoListItem = Mock()
        navigation.addFolderListItem = Mock()
        
        navigation.parseVideoList({"scraper": "watch_later", "path": "some_path"},[{"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "false"}, {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "next": "true"}])
        
        sys.modules["__main__"].xbmcplugin.endOfDirectory.assert_called_with(cacheToDisc=True,handle=-1,succeeded=True)
        
    def test_addVideoContextMenuItems_should_call_utils_makeAscii_on_Title(self):
        sys.argv = ["some_plugin", -1, "some_path"]
        sys.modules["__main__"].language.return_value = "some_button_string %s"
        sys.modules["__main__"].common.makeAscii.side_effect = lambda x: x
        navigation = VimeoNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].common.makeAscii.assert_any_call("some_title")

    def prepareContestMenu(self):
        sys.argv = ["some_plugin", -1, "some_path"]
        sys.modules["__main__"].language.return_value = "some_button_string %s"
        sys.modules["__main__"].common.makeAscii.side_effect = lambda x: x
        
    def assert_context_menu_contains(self, cm, title, path):
        found = False
        for (ititle, ipath) in cm:
            if ititle == title and ipath == path :
                found = True

        if found == False:
            print "Failed to find item in context menu: " + title + " - " + path + "\r\n"
            for (title, path) in cm:
                print "item " + str(cm.index((title, path))) +": " + title + " - " + path

        assert(found)

    def assert_context_menu_doesnt_contain(self, cm, title, path):
        found = False
        for (ititle, ipath) in cm:
            if ititle == title and ipath == path:
                found = True

        if found == True:
            print "Failed to find item in context menu: " + title + " - " + path + "\r\n"

            for (title, path) in cm:
                print "item " + str(cm.index((title, path))) +": " + title + " - " + path

        assert(found == False)

    def ttest_addVideoContextMenuItems_should_add_play_all_from_video_id_to_items_in_playlists(self):
        self.prepareContestMenu()
        navigation = VimeoNavigation()
        path_params = {"playlist": "some_playlist"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30512)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=play_all&playlist=some_playlist&videoid=some_id&)')
                

    def ttest_addVideoContextMenuItems_should_add_play_all_from_video_id_to_items_in_new_subscriptions_feed(self):
        self.prepareContestMenu()
        navigation = VimeoNavigation()
        path_params = {"user_feed": "newsubscriptions"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30521)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=play_all&user_feed=newsubscriptions&contact=default&videoid=some_id&)')

    def test_addVideoContextMenuItems_should_add_download_video_to_all_video_items(self):
        self.prepareContestMenu()
        navigation = VimeoNavigation()
        path_params = {"path": "some_path"}
        item_params = {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30500)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=download&videoid=some_id)')

    def ttest_addVideoContextMenuItems_should_add_add_favorite_option_if_user_is_logged_in_and_item_is_not_in_favorites_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30503)
        sys.modules["__main__"].settings.getSetting.assert_any_call("username")
        sys.modules["__main__"].settings.getSetting.assert_any_call("oauth2_access_token")
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=add_favorite&videoid=some_id&)')

    def ttest_addVideoContextMenuItems_should_add_add_favorite_option_if_user_is_logged_in_and_item_is_in_external_users_favorites_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {"user_feed": "favorites", "contact": "some_contact"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30501)
        sys.modules["__main__"].settings.getSetting.assert_any_call("username")
        sys.modules["__main__"].settings.getSetting.assert_any_call("oauth2_access_token")
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=add_favorite&videoid=some_id&)')
        
    def ttest_addVideoContextMenuItems_should_add_remove_favorite_option_if_user_is_logged_in_and_item_is_in_favorites_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {"user_feed": "favorites"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "editid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30506)
        sys.modules["__main__"].settings.getSetting.assert_any_call("username")
        sys.modules["__main__"].settings.getSetting.assert_any_call("oauth2_access_token")
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=remove_favorite&editid=some_id&)')

    def ttest_addVideoContextMenuItems_should_add_add_subscription_option_to_channels_not_in_subscriptions_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {"user_feed": "favorites"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "editid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30512)
        self.assert_context_menu_contains(cm, "some_button_string Unknown Author", 'XBMC.RunPlugin(some_plugin?path=some_path&channel=Unknown+Author&action=add_subscription)')

    def ttest_addVideoContextMenuItems_should_add_add_subscriptions_option_to_external_users_subscriptions_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {"feed": "subscriptions_favorites", "external": "true"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "editid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30512)
        self.assert_context_menu_contains(cm, "some_button_string Unknown Author", 'XBMC.RunPlugin(some_plugin?path=some_path&channel=Unknown+Author&action=add_subscription)')

    def ttest_addVideoContextMenuItems_should_not_add_add_subscrition_option_to_users_uploads_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {"user_feed": "uploads"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "editid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        self.assert_context_menu_doesnt_contain(cm, "some_button_string Unknown Author", 'XBMC.RunPlugin(some_plugin?path=some_path&channel=Unknown+Author&action=add_subscription)')

    def ttest_addVideoContextMenuItems_should_not_add_add_subscription_option_to_subscription_favorites_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {"feed": "subscriptions_favorites"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "editid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        self.assert_context_menu_doesnt_contain(cm, "some_button_string Unknown Author", 'XBMC.RunPlugin(some_plugin?path=some_path&channel=Unknown+Author&action=add_subscription)')

    def ttest_addVideoContextMenuItems_should_not_add_add_subscription_option_to_subscription_playlists_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {"feed": "subscriptions_playlists"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "editid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        self.assert_context_menu_doesnt_contain(cm, "some_button_string Unknown Author", 'XBMC.RunPlugin(some_plugin?path=some_path&channel=Unknown+Author&action=add_subscription)')

    def ttest_addVideoContextMenuItems_should_not_add_add_subscription_option_to_subscription_uploads_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {"feed": "subscriptions_uploads"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "editid": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        self.assert_context_menu_doesnt_contain(cm, "some_button_string Unknown Author", 'XBMC.RunPlugin(some_plugin?path=some_path&channel=Unknown+Author&action=add_subscription)')

    def ttest_addVideoContextMenuItems_should_add_remove_from_playlist_option_to_items_in_playlists(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {"playlist": "some_playlist"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "playlist_entry_id": "some_id"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30530)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=remove_from_playlist&playlist=some_playlist&playlist_entry_id=some_id&)')

    def ttest_addVideoContextMenuItems_should_add_add_to_playlist_option_to_video_items_if_user_is_logged_in(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "someid"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30528)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.Container.Update(some_plugin?path=None&feed=related&videoid=someid)')

    def ttest_addVideoContextMenuItems_should_add_more_videos_by_user_if_item_is_not_in_uploads_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "someid"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30516)
        self.assert_context_menu_contains(cm, "some_button_string Unknown Author", 'XBMC.Container.Update(some_plugin?path=None&feed=uploads&channel=Unknown+Author)')

    def ttest_addVideoContextMenuItems_should_not_add_more_videos_by_user_if_item_is_in_uploads_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {"user_feed": "uploads"}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        self.assert_context_menu_doesnt_contain(cm, "some_button_string Unknown Author", 'XBMC.Container.Update(some_plugin?path=None&feed=uploads&channel=Unknown+Author)')
        
    def ttest_addVideoContextMenuItems_should_add_related_videos_option_to_video_items(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "someid"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30527)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.Container.Update(some_plugin?path=None&feed=related&videoid=someid)')

    def ttest_addVideoContextMenuItems_should_add_find_similar_option_to_video_items(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "someid"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30514)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.Container.Update(some_plugin?path=None&feed=search&search=some_title)')

    def ttest_addVideoContextMenuItems_should_add_now_playing_option_to_video_items(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "someid"}
        
        cm = navigation.addVideoContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30523)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.ActivateWindow(VideoPlaylist)')

    def test_addFolderContextMenuItems_should_not_add_any_options_to_next_folders(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "next": "true"}
        
        cm = navigation.addFolderContextMenuItems(path_params,item_params)
        
        assert(cm == [])

    def test_addFolderContextMenuItems_should_add_edit_and_delete_options_to_searches(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {}
        item_params = {"Title": "some_title", "path": "some_path", "icon": "some_icon", "thumbnail": "some_thumbnail", "videoid": "someid", "feed": "search", "search": "some_search"}
        
        cm = navigation.addFolderContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30506)
        sys.modules["__main__"].language.assert_any_call(30508)
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.Container.Update(some_plugin?path=some_path&action=edit_search&store=searches&search=some_search&)')
        self.assert_context_menu_contains(cm, "some_button_string %s", 'XBMC.RunPlugin(some_plugin?path=some_path&action=delete_search&store=searches&delete=some_search&)')

    def test_addFolderContextMenuItems_should_add_add_subscription_option_to_subscriptions_not_in_users_subscription_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {"external": "true","path": "some_path"}
        item_params = {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "channel": "some_channel"}
        
        cm = navigation.addFolderContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30512)
        self.assert_context_menu_contains(cm, "some_button_string some_title", 'XBMC.RunPlugin(some_plugin?path=some_path&channel=some_channel&action=add_subscription)')
        
    def test_addFolderContextMenuItems_should_add_remove_subscription_option_to_subscriptions_in_users_subscriptions_feed(self):
        self.prepareContestMenu()
        sys.modules["__main__"].settings.getSetting.return_value = "something"
        navigation = VimeoNavigation()
        path_params = {"path": "some_path", "api":"my_channels"}
        item_params = {"Title": "some_title", "icon": "some_icon", "thumbnail": "some_thumbnail", "channel": "some_channel", "editid": "some_editid"}
        
        cm = navigation.addFolderContextMenuItems(path_params,item_params)
        
        sys.modules["__main__"].language.assert_any_call(30513)
        self.assert_context_menu_contains(cm, "some_button_string some_title", 'XBMC.RunPlugin(some_plugin?path=some_path&channel=some_channel&action=remove_subscription)')

if __name__ == '__main__':
        nose.runmodule()
