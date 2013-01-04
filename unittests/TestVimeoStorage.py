# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
from VimeoStorage import VimeoStorage 


class TestVimeoStorage(BaseTestCase.BaseTestCase):
    def test_list_should_call_getUserOptionFolder_if_store_contact_option_is_in_params(self):
        storage = VimeoStorage()
        storage.getUserOptionFolder = Mock()
        storage.getUserOptionFolder.return_value = ("", 200)

        storage.list({"store": "contact_options"})

        storage.getUserOptionFolder.assert_called_with({"store": "contact_options"})

    def test_list_should_call_getStoredSearches_if_store_is_defined_in_params_but_not_artist_or_contact_option(self):
        storage = VimeoStorage()
        storage.getStoredSearches = Mock()
        storage.getStoredSearches.return_value = ("", 200)
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search"]

        storage.list({"store": "somestore"})

        storage.getStoredSearches.assert_called_with({"store": "somestore"})

    def test_openFile_should_call_io_open(self):
        patcher = patch("io.open")
        patcher.start()
        import io
        io.open.return_value = "my_result"
        storage = VimeoStorage()

        result = storage.openFile("someFile")
        patcher.stop()

        assert(result == "my_result")

    def test_getStoredSearches_should_call_retrieve_to_get_searches(self):
        storage = VimeoStorage()
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search"]
        storage.storeSettings = Mock()
        
        storage.getStoredSearches({"path": "some_path"})
        
        assert(storage.retrieveSettings.call_count > 0)        

    def test_getStoredSearches_should_call_retrieve_to_get_thumbnail(self):
        storage = VimeoStorage()
        storage.retrieveSettings = Mock()
        storage.retrieve = Mock()
        storage.retrieve.return_value = "thumbnail"
        storage.retrieveSettings.return_value =  ["some_search"]
        storage.storeSettings = Mock()
        
        storage.getStoredSearches({"path": "some_path"})
        
        assert(storage.retrieveSettings.call_args[0][0] == {"path": "some_path"})
        storage.retrieve.assert_any_call({"path": "some_path"}, "thumbnail", {'path': 'some_path', 'api':'search', 'icon':'search', 'search': 'some_search', 'thumbnail': 'thumbnail', 'Title': 'some_search'})

    def test_getStoredSearches_should_return_proper_list_structure(self):
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value = "some_thumbnail"
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search"]
        storage.storeSettings = Mock()
        
        (result, status) = storage.getStoredSearches({"path": "some_path"})
        
        print repr(result)
        assert(result == [{'path': 'some_path', 'api':'search', 'icon':'search', 'search': 'some_search', 'thumbnail': 'some_thumbnail', 'Title': 'some_search'}])
        
    def test_getStoredSearches_should_call_quote_plus_on_search_items(self):
        patcher = patch("urllib.quote_plus")
        patcher.start()
        import urllib
        urllib.quote_plus.return_value = "some_quoted_search"
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value = ["some_search"]
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search"]
        storage.storeSettings = Mock()
        
        (result, status) = storage.getStoredSearches({"path": "some_path"})
        args = urllib.quote_plus.call_args
        patcher.stop()

        print repr(result)
        assert(args[0][0] == "some_search")
        assert(result == [{'path': 'some_path', 'search': 'some_quoted_search', 'api':'search', 'icon':'search',  'thumbnail': ['some_search'], 'Title': 'some_search'}])
                

    def test_deleteStoredSearch_should_call_unquote_on_delete_param(self):
        patcher = patch("urllib.unquote_plus")
        patcher.start()
        import urllib
        urllib.unquote_plus.return_value = "some_unquoted_search"
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  ["some_search1"]
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search"]

        storage.storeSettings = Mock()
        
        storage.deleteStoredSearch({"delete": "some_search2"})
        args = urllib.unquote_plus.call_args
        patcher.stop()
        
        assert(args[0][0] == "some_search2")

    def test_deleteStoredSearch_should_call_retrieve_to_get_searches(self):
        storage = VimeoStorage()
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search1"]
        storage.storeSettings = Mock()
        
        storage.deleteStoredSearch({"delete": "some_search2"})
        
        storage.retrieveSettings.assert_called_with({'delete': 'some_search2'})
        assert(storage.retrieveSettings.call_count == 1)

    def test_deleteStoredSearch_should_remove_search_from_list_before_calling_store(self):
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  ["some_search2"]
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search"]

        storage.storeSettings = Mock()
        
        storage.deleteStoredSearch({"delete": "some_search2"})
        
        storage.storeSettings.assert_called_with({"delete": "some_search2"},["some_search"])

    def test_deleteStoredSearch_should_call_executebuiltin(self):
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  ["some_search2"]
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search"]
        storage.storeSettings = Mock()
        
        storage.deleteStoredSearch({"delete": "some_search2"})
        
        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.Refresh')

    def test_saveStoredSearch_should_exit_cleanly_if_search_is_not_in_params(self):
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  ["some_search2"]
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search"]

        storage.storeSettings = Mock()
        
        storage.saveStoredSearch({})
        
        assert(storage.retrieve.call_count == 0)
        assert(storage.storeSettings.call_count == 0)
        
    def test_saveStoredSearch_should_call_unquote_on_search_param(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"        
        patcher = patch("urllib.unquote_plus")
        patcher.start()
        import urllib
        urllib.unquote_plus.return_value = "some_unquoted_search"
        storage = VimeoStorage()
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search1"]
        storage.storeSettings = Mock()
        
        storage.saveStoredSearch({"search": "some_search"})

        args = urllib.unquote_plus.call_args
        patcher.stop()
        
        assert(args[0][0] == "some_search")

    def test_saveStoredSearch_should_call_unquote_on_old_search_param_if_it_exists(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"        
        patcher = patch("urllib.unquote_plus")
        patcher.start()
        import urllib
        urllib.unquote_plus.return_value = "some_unquoted_search"
        storage = VimeoStorage()
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search1"]
        storage.storeSettings = Mock()
        
        storage.saveStoredSearch({"search": "some_search1", "old_search": "some_search2"})
        
        args = urllib.unquote_plus.call_args_list
        patcher.stop()
        
        assert(args[0][0][0] == "some_search1")
        assert(args[1][0][0] == "some_search2")

    def test_saveStoredSearch_should_call_retrieve_to_get_list_of_searches(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search2"]
        storage.storeSettings = Mock()
        
        storage.saveStoredSearch({"search": "some_search1", "old_search": "some_search2"})
        
        storage.retrieveSettings.assert_called_with({"search": "some_search1", "old_search": "some_search2"})

    def test_saveStoredSearch_should_remove_old_search_from_collection_and_prepend_new_search(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search4", "some_search2", "some_search3"]
        storage.storeSettings = Mock()
        
        storage.saveStoredSearch({"search": "some_search1", "old_search": "some_search2"})
        
        storage.storeSettings.assert_called_with({"search": "some_search1", "old_search": "some_search2"},['some_search1', 'some_search4', 'some_search3'])
        
    def test_saveStoredSearch_should_limit_search_collection_before_calling_store(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search4", "some_search2", "some_search3", "", "", "", "", "", "", "", ""]
        storage.storeSettings = Mock()
        
        storage.saveStoredSearch({"search": "some_search1", "old_search": "some_search2"})
        
        assert(len(storage.storeSettings.call_args[0][1]) == 10)
        storage.storeSettings.assert_called_with({"search": "some_search1", "old_search": "some_search2"},['some_search1', 'some_search4', 'some_search3',"", "", "", "", "", "", ""])

    def test_saveStoredSearch_should_call_getSettings_to_get_max_searches_count(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search2"]
        storage.storeSettings = Mock()
        
        storage.saveStoredSearch({"search": "some_search1", "old_search": "some_search2"})
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("saved_searches")

    def test_saveStoredSearch_should_call_store_to_save_searches_collection(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search2"]
        storage.storeSettings = Mock()
        
        storage.saveStoredSearch({"search": "some_search1", "old_search": "some_search2"})
        
        assert(storage.storeSettings.call_count > 0)

    def test_editStoredSearch_should_exit_cleanly_if_search_param_is_missing(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.modules["__main__"].common.getUserInput.return_value = "some_search3"
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  ["some_search2"]

        storage.storeSettings = Mock()
        
        storage.editStoredSearch({})
        
        assert(storage.storeSettings.call_count == 0)
        assert(storage.retrieve.call_count == 0)

    def test_editStoredSearch_should_ask_user_for_new_search_phrase(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.modules["__main__"].language.return_value = "some_title"
        sys.modules["__main__"].common.getUserInput.return_value = "some_search3"
        storage = VimeoStorage()
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search2"]
        storage.storeSettings = Mock()
        
        storage.editStoredSearch({"search": "some_search1"})
        
        sys.modules["__main__"].common.getUserInput.assert_called_with('some_title', 'some_search1')

    def test_editStoredSearch_should_set_store_to_searches_if_editing_searches(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.modules["__main__"].language.return_value = "some_title"
        sys.modules["__main__"].common.getUserInput.return_value = "some_search3"
        storage = VimeoStorage()
        storage.retrieveSettings = Mock()
        storage.retrieveSettings.return_value =  ["some_search2"]
        storage.storeSettings = Mock()
        
        storage.editStoredSearch({"search": "some_search1"})
        
        assert(storage.storeSettings.call_args[0][0].has_key("api"))

    def test_editStoredSearch_should_call_saveStoredSearch(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.modules["__main__"].language.return_value = "some_title"
        sys.modules["__main__"].common.getUserInput.return_value = "some_search3"
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  ["some_search2"]
        storage.storeSettings = Mock()
        storage.saveStoredSearch = Mock()
        
        storage.editStoredSearch({"search": "some_search1", "action": "edit_search"})
        
        storage.saveStoredSearch.assert_called_with({'search': 'some_search3', 'api': 'search'})

    def test_editStoredSearch_should_remove_old_search_param_before_exiting(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.modules["__main__"].language.return_value = "some_title"
        sys.modules["__main__"].common.getUserInput.return_value = "some_search3"
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  ["some_search2"]
        storage.storeSettings = Mock()
        storage.saveStoredSearch = Mock()
        params = {"search": "some_search1", "action": "edit_disco", "old_search": "some_search4"}
        
        storage.editStoredSearch(params)
        
        assert(params.has_key("old_search") == False)
        
    def test_editStoredSearch_should_set_search_params_before_exiting(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        sys.modules["__main__"].language.return_value = "some_title"
        sys.modules["__main__"].common.getUserInput.return_value = "some_search3"
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  ["some_search2"]
        storage.storeSettings = Mock()
        storage.saveStoredSearch = Mock()
        params = {"search": "some_search1", "action": "edit_disco", "old_search": "some_search4"}
        
        storage.editStoredSearch(params)
        
        assert(params.has_key("search"))
        assert(params["search"] == "some_search3")
        
    def test_getUserOptionFolder_should_return_modified_version_of_items_in_user_options(self):
        sys.modules["__main__"].language.return_value = "some_title"
        storage = VimeoStorage()
        
        (result, status) = storage.getUserOptionFolder({})
        
        assert(len(result) == 5)
        assert(result[0]["api"] == "my_likes")
        assert(result[1]["api"] == "my_channels")
        assert(result[2]["api"] == "my_groups")
        assert(result[3]["api"] == "my_albums")
        assert(result[4]["api"] == "my_videos")

    def test_reversePlaylistOrder_should_exit_cleanly_if_playlist_params_is_missing(self):
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  "false"
        storage.store = Mock()
        
        storage.reversePlaylistOrder({})
        
        assert(storage.retrieve.call_count == 0)
        assert(storage.store.call_count == 0)
                
    def test_reversePlaylistOrder_should_call_retrieve_to_fetch_reverse_value(self):
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  "false"
        storage.store = Mock()
        
        storage.reversePlaylistOrder({"playlist": "some_playlists"})
        
        storage.retrieve.assert_called_with({'playlist': 'some_playlists'}, 'value')
        
    def test_reversePlaylistOrder_should_call_store_to_save_reverse_value(self):
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  "false"
        storage.store = Mock()
        
        storage.reversePlaylistOrder({"playlist": "some_playlists"})
        
        storage.store.assert_called_with({'playlist': 'some_playlists'}, 'true', 'value')
        
    def test_reversePlaylistOrder_should_executebuiltin_on_succes(self):
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  "false"
        storage.store = Mock()
        
        storage.reversePlaylistOrder({"playlist": "some_playlists"})
        
        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.Refresh')
        
    def test_getReversePlaylistOrder_should_return_false_if_playlist_is_not_in_params(self):
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  "true"
        storage.store = Mock()
        
        result = storage.getReversePlaylistOrder()
        
        assert(result == False)
        
    def test_getReversePlaylistOrder_should_call_retrieve_to_fetch_reverse_value(self):
        storage = VimeoStorage()
        storage.retrieve = Mock()
        storage.retrieve.return_value =  "true"
        
        result = storage.getReversePlaylistOrder({"playlist": "some_playlists"})
        
        assert(result == True)
        
    def test_getStorageKey_should_call_getValueStorageKey_if_type_is_value(self):
        storage = VimeoStorage()
        storage._getValueStorageKey = Mock()
        
        result = storage.getStorageKey({"some_param": "param_value"},"value")
        
        storage._getValueStorageKey.assert_called_with({"some_param": "param_value"},{})
        
    def test_getStorageKey_should_call_getViewModeStorageKey_if_type_is_viewmode(self):
        storage = VimeoStorage()
        storage._getViewModeStorageKey = Mock()
        
        result = storage.getStorageKey({"some_param": "param_value"}, "viewmode")
        
        storage._getViewModeStorageKey.assert_called_with({"some_param": "param_value"},{})
        
    def test_getStorageKey_should_call_getThumbnailStorageKey_if_type_is_thumbnail(self):
        storage = VimeoStorage()
        storage._getThumbnailStorageKey = Mock()
        
        result = storage.getStorageKey({"some_param": "param_value"}, "thumbnail")
        
        storage._getThumbnailStorageKey.assert_called_with({"some_param": "param_value"},{})        
        
    def test_getStorageKey_should_call_getResultSetStorageKey_if_type_is_not_set(self):
        storage = VimeoStorage()
        storage._getResultSetStorageKey = Mock()
        
        result = storage.getStorageKey({"some_param": "param_value"})
        
        storage._getResultSetStorageKey.assert_called_with({"some_param": "param_value"})
        
    def test_getThumbnailStorageKey_should_return_correct_key_for_search_path(self):
        storage = VimeoStorage()
        
        result = storage._getThumbnailStorageKey({"search": "some_search", "feed": "search"})
        
        assert(result == "search_some_search_thumb")

    def test_getThumbnailStorageKey_should_return_correct_key_for_search_item(self):
        storage = VimeoStorage()
        
        result = storage._getThumbnailStorageKey({"some_param": "something"}, {"search": "some_search", "feed": "search"})
        
        assert(result == "search_some_search_thumb")

    def test_getThumbnailStorageKey_should_return_correct_key_for_user_feed_path(self):
        storage = VimeoStorage()
        
        result = storage._getThumbnailStorageKey({"user_feed": "something"})
        
        assert(result == "something_thumb")
        
    def test_getThumbnailStorageKey_should_return_correct_key_for_channel_path(self):
        storage = VimeoStorage()
        
        result = storage._getThumbnailStorageKey({"user_feed": "some_feed", "channel": "some_channel"})
        
        assert(result == "subscriptions_some_channel_thumb")
        
    def test_getThumbnailStorageKey_should_return_correct_key_for_channel_item(self):
        storage = VimeoStorage()
        
        result = storage._getThumbnailStorageKey({"user_feed": "something"},{"channel": "some_channel"})
        
        assert(result == "subscriptions_some_channel_thumb")
        
    def test_getThumbnailStorageKey_should_return_correct_key_for_playlist_path(self):
        storage = VimeoStorage()
        
        result = storage._getThumbnailStorageKey({"user_feed": "some_feed", "playlist": "some_playlist"})
        
        assert(result == "playlist_some_playlist_thumb")

    def test_getThumbnailStorageKey_should_return_correct_key_for_playlist_item(self):
        storage = VimeoStorage()
        
        result = storage._getThumbnailStorageKey({"user_feed": "something"},{"playlist": "some_playlist"})
        
        assert(result == "playlist_some_playlist_thumb")
        
    def test_getThumbnailStorageKey_should_appen_thumb_to_key(self):
        storage = VimeoStorage()
        
        result = storage._getThumbnailStorageKey({"some_param": "something"}, {"search": "some_search"})
        
        assert(result[result.rfind("_"):] == "_thumb")
        
    def test_getValueStorageKey_should_return_correct_key_for_reverse_playlist_action(self):
        storage = VimeoStorage()
        
        result = storage._getValueStorageKey({"action": "reverse_order", "playlist": "some_playlist"})
        
        assert(result == "reverse_playlist_some_playlist")

    def test_getValueStorageKey_should_return_correct_key_for_reverse_playlist_path(self):
        storage = VimeoStorage()
        
        result = storage._getValueStorageKey({"user_feed": "playlist", "playlist": "some_playlist"})
        
        assert(result == "reverse_playlist_some_playlist")

    def test_getValueStorageKey_should_return_correct_key_for_reverse_playlist_item(self):
        storage = VimeoStorage()
        
        result = storage._getValueStorageKey({"user_feed": "playlist"}, {"playlist": "some_playlist"})
        
        assert(result == "reverse_playlist_some_playlist")

    def test_getValueStorageKey_should_handle_external_marker(self):
        storage = VimeoStorage()
        
        result = storage._getValueStorageKey({"user_feed": "playlist", "external": "true", "contact": "some_contact"}, {"playlist": "some_playlist"})
        
        assert(result == "reverse_playlist_some_playlist_external_some_contact")

    def test_getViewModeStorageKey_should_handle_external_marker(self):
        storage = VimeoStorage()
        
        result = storage._getViewModeStorageKey({"channel": "some_channel", "external": "true", "contact": "some_contact"})
        
        assert(result[:result.find("_")] == "external" )

    def test_getViewModeStorageKey_should_return_correct_key_for_channel_item(self):
        storage = VimeoStorage()
        
        result = storage._getViewModeStorageKey({},{"channel": "some_channel"})
        
        assert(result == "view_mode_some_channel")

    def test_getViewModeStorageKey_should_return_correct_key_for_channel_path(self):
        storage = VimeoStorage()
        
        result = storage._getViewModeStorageKey({"channel": "some_channel"})
        
        assert(result == "view_mode_some_channel")

    def test_getResultSetStorageKey_should_return_correct_key_for_music_category_path(self):
        storage = VimeoStorage()
        
        result = storage._getResultSetStorageKey({"scraper": "music", "category": "some_category"})
        
        assert(result == "s_music_category_some_category")

    def test_getResultSetStorageKey_should_return_correct_key_for_category_path(self):
        storage = VimeoStorage()
        
        result = storage._getResultSetStorageKey({"scraper": "categories", "category": "some_category"})
        
        assert(result == "s_categories_category_some_category")

    def test_getResultSetStorageKey_should_return_correct_key_for_show_scrapers(self):
        storage = VimeoStorage()
        
        result = storage._getResultSetStorageKey({"scraper": "show"})

        assert(result == "s_show")

    def test_getResultSetStorageKey_should_return_correct_key_for_playlist_path(self):
        storage = VimeoStorage()
        
        result = storage._getResultSetStorageKey({"api": "my_playlists", "playlist": "some_playlist"})
        
        assert(result == "result_my_playlists_some_playlist")

    def test_getResultSetStorageKey_should_return_correct_key_for_subscription_path(self):
        storage = VimeoStorage()
        
        result = storage._getResultSetStorageKey({"api": "my_channels", "channel": "some_channel"})
        
        assert(result == "result_my_channels_some_channel")

    def test_getResultSetStorageKey_should_handle_external_correctly(self):
        storage = VimeoStorage()
        
        result = storage._getResultSetStorageKey({"api": "my_playlists", "playlist": "some_playlist", "external": "true", "contact": "some_contact"})
        
        assert(result.find("external") > 0)

    def test_getResultSetStorageKey_should_return_correct_key_for_stored_searches(self):
        storage = VimeoStorage()
        
        result = storage._getResultSetStorageKey({"api": "search"})
        
        assert(result == "store_searches")

    def test_getResultSetStorageKey_should_return_correct_key_for_generic_stores(self):
        storage = VimeoStorage()
        
        result = storage._getResultSetStorageKey({"store": "pokeystore"})
        
        assert(result == "store_pokeystore")

    def test_store_should_call_getStorageKey_to_fetch_correct_storage_key(self):
        storage = VimeoStorage()
        storage.getStorageKey = Mock()
        
        result = storage.store({"store": "pokeystore"})
        
        storage.getStorageKey.assert_called_with({'store': 'pokeystore'}, '', {})

    def test_store_should_call_storeValue_if_type_is_set(self):
        storage = VimeoStorage()
        storage.storeValue = Mock()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "key"
        
        result = storage.store({}, {"store": "pokeystore"}, "value")

        print repr(result)

        storage.storeValue.assert_called_with("key", {"store": "pokeystore"})
        
    def test_store_should_call_storeResultSet_if_type_is_not_set(self):
        storage = VimeoStorage()
        storage.storeResultSet = Mock()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "key"

        storage.store({}, {"store": "pokeystore"})

        storage.storeResultSet.assert_called_with("key", {"store": "pokeystore"})

    def test_storeValue_should_call_cache_set_with_correct_params(self):
        storage = VimeoStorage()
        storage.storeResultSet = Mock()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "key"
        
        storage.storeValue("some_key", "some_value")
        
        sys.modules["__main__"].cache.set.assert_called_with("some_key", "some_value")

    def test_storeResultSet_should_call_cache_set_with_correct_params_by_default(self):
        storage = VimeoStorage()
        
        storage.storeResultSet("some_key", ["some_value"])
        
        sys.modules["__main__"].cache.set.assert_called_with("some_key", repr(["some_value"]))
        
    def test_storeResultSet_should_call_retrieveResultSet_if_prepend_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = []
        
        storage.storeResultSet("some_key", ["some_value"], {"prepend": "true"})
        
        storage.retrieveResultSet.assert_called_with("some_key")

    def test_storeResultSet_should_call_settings_getSetting_to_get_stored_searches_limit_if_prepend_is_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = []
        
        storage.storeResultSet("some_key", ["some_value"], {"prepend": "true"})
        
        sys.modules["__main__"].settings.getSetting.assert_called_with("saved_searches")
        
    def test_storeResultSet_should_call_retrieveResultSet_if_append_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = []
        
        storage.storeResultSet("some_key", ["some_value"], {"append": "true"})
        
        storage.retrieveResultSet.assert_called_with("some_key")
                
    def test_storeResultSet_should_call_cache_set_if_prepend_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = []
        
        storage.storeResultSet("some_key", "some_value", {"prepend": "true"})
        
        sys.modules["__main__"].cache.set.assert_called_with("some_key", repr(["some_value"]))
        
    def test_storeResultSet_should_call_cache_set_correctly_if_append_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = ["smokey"]
        
        storage.storeResultSet("some_key", "some_value", {"append": "true"})
        
        sys.modules["__main__"].cache.set.assert_called_with("some_key", repr(["smokey", "some_value"]))
        
    def test_storeResultSet_should_append_item_to_collection_if_append_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        
        storage.storeResultSet("some_key", "some_value", {"append": "true"})
        
        storage.retrieveResultSet().append.assert_called_with("some_value")
        
    def test_storeResultSet_should_prepend_item_to_collection_if_prepend_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = ["some_default"]
        
        storage.storeResultSet("some_key", "some_value", {"prepend": "true"})
        
        sys.modules["__main__"].cache.set.assert_called_with("some_key", repr(["some_value", "some_default"]))

    def test_storeSettings_should_call_getStorageKey_to_fetch_correct_storage_key(self):
        storage = VimeoStorage()
        storage.getStorageKey = Mock()

        result = storage.storeSettings({"storeSettings": "pokeystoreSettings"})

        storage.getStorageKey.assert_called_with({'storeSettings': 'pokeystoreSettings'}, '', {})

    def test_storeSettings_should_call_storeValueSettings_if_type_is_set(self):
        storage = VimeoStorage()
        storage.storeValueSettings = Mock()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "key"

        result = storage.storeSettings({}, {"storeSettings": "pokeystoreSettings"}, "value")

        print repr(result)

        storage.storeValueSettings.assert_called_with("key", {"storeSettings": "pokeystoreSettings"})

    def test_storeSettings_should_call_storeResultSetSettings_if_type_is_not_set(self):
        storage = VimeoStorage()
        storage.storeResultSetSettings = Mock()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "key"

        storage.storeSettings({}, {"storeSettings": "pokeystoreSettings"})

        storage.storeResultSetSettings.assert_called_with("key", {"storeSettings": "pokeystoreSettings"})

    def test_storeValueSettings_should_call_storage_setSetting_with_correct_params(self):
        storage = VimeoStorage()
        storage.storeResultSetSettings = Mock()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "key"

        storage.storeValueSettings("some_key", "some_value")

        sys.modules["__main__"].settings.setSetting.assert_called_with("some_key", "some_value")

    def test_storeResultSetSettings_should_call_cache_set_with_correct_params_by_default(self):
        storage = VimeoStorage()

        storage.storeResultSetSettings("some_key", ["some_value"])

        sys.modules["__main__"].settings.setSetting.assert_called_with("some_key", repr(["some_value"]))

    def test_storeResultSetSettings_should_call_retrieveResultSet_if_prepend_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = []

        storage.storeResultSetSettings("some_key", ["some_value"], {"prepend": "true"})

        storage.retrieveResultSet.assert_called_with("some_key")

    def test_storeResultSetSettings_should_call_settings_getSetting_to_get_storeSettingsd_searches_limit_if_prepend_is_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = []

        storage.storeResultSetSettings("some_key", ["some_value"], {"prepend": "true"})

        sys.modules["__main__"].settings.getSetting.assert_called_with("saved_searches")

    def test_storeResultSetSettings_should_call_retrieveResultSet_if_append_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = []

        storage.storeResultSetSettings("some_key", ["some_value"], {"append": "true"})

        storage.retrieveResultSet.assert_called_with("some_key")

    def test_storeResultSetSettings_should_call_cache_set_if_prepend_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = []

        storage.storeResultSetSettings("some_key", "some_value", {"prepend": "true"})

        sys.modules["__main__"].settings.setSetting.assert_called_with("some_key", repr(["some_value"]))

    def test_storeResultSetSettings_should_call_cache_set_correctly_if_append_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = ["smokey"]

        storage.storeResultSetSettings("some_key", "some_value", {"append": "true"})

        sys.modules["__main__"].settings.setSetting.assert_called_with("some_key", repr(["smokey", "some_value"]))

    def test_storeResultSetSettings_should_append_item_to_collection_if_append_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()

        storage.storeResultSetSettings("some_key", "some_value", {"append": "true"})

        storage.retrieveResultSet().append.assert_called_with("some_value")

    def test_storeResultSetSettings_should_prepend_item_to_collection_if_prepend_is_in_params(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.retrieveResultSet = Mock()
        storage.retrieveResultSet.return_value = ["some_default"]

        storage.storeResultSetSettings("some_key", "some_value", {"prepend": "true"})

        sys.modules["__main__"].settings.setSetting.assert_called_with("some_key", repr(["some_value", "some_default"]))


    def test_retrieve_should_call_getStorageKey_to_fetch_correct_storage_key(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "some_key"

        storage.retrieve("some_key", "some_value", {"prepend": "true"})

        storage.getStorageKey.assert_called_with("some_key", "some_value", {"prepend": "true"})

    def test_retrieve_should_call_retrieveValue_if_type_is_set(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "some_key"
        storage.retrieveValue = Mock()
        
        storage.retrieve("some_key", "thumbnail")
        
        storage.retrieveValue.assert_called_with("some_key")
        
    def test_retrieve_should_call_retrieveResultSet_if_type_is_not_set(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "some_key"
        storage.retrieveResultSet = Mock()
        
        storage.retrieve("some_key")
        
        storage.retrieveResultSet.assert_called_with("some_key")
        
    def test_retrieveValue_should_call_cache_get_with_correct_params(self):
        storage = VimeoStorage()
        
        storage.retrieveValue("some_key")
        
        sys.modules["__main__"].cache.get.assert_called_with("some_key")
        
    def test_retrieveResultSet_should_call_get_with_correct_params(self):
        storage = VimeoStorage()
        
        storage.retrieveResultSet("some_key")
        
        sys.modules["__main__"].cache.get.assert_called_with("some_key")

    def test_retrieveResultSet_should_evaluate_content_from_sql_get(self):
        storage = VimeoStorage()
        sys.modules["__main__"].cache.get.return_value = "['some_value']"
        
        result = storage.retrieveResultSet("some_key")
        
        assert(result == ['some_value'])

    def test_retrieveSettings_should_call_getStorageKey_to_fetch_correct_storage_key(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "some_key"

        storage.retrieveSettings("some_key", "some_value", {"prepend": "true"})

        storage.getStorageKey.assert_called_with("some_key", "some_value", {"prepend": "true"})

    def test_retrieveSettings_should_call_retrieveValueSettings_if_type_is_set(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "some_key"
        storage.retrieveValueSettings = Mock()

        storage.retrieveSettings("some_key", "thumbnail")

        storage.retrieveValueSettings.assert_called_with("some_key")

    def test_retrieveSettings_should_call_retrieveResultSetSettings_if_type_is_not_set(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        storage = VimeoStorage()
        storage.getStorageKey = Mock()
        storage.getStorageKey.return_value = "some_key"
        storage.retrieveResultSetSettings = Mock()

        storage.retrieveSettings("some_key")

        storage.retrieveResultSetSettings.assert_called_with("some_key")

    def test_retrieveValueSettings_should_call_settings_getSetting_with_correct_params(self):
        storage = VimeoStorage()

        storage.retrieveValueSettings("some_key")

        sys.modules["__main__"].settings.getSetting.assert_called_with("some_key")

    def test_retrieveResultSetSettings_should_call_get_with_correct_params(self):
        storage = VimeoStorage()

        storage.retrieveResultSetSettings("some_key")

        sys.modules["__main__"].settings.getSetting.assert_called_with("some_key")

    def test_retrieveResultSetSettings_should_evaluate_content_from_sql_get(self):
        storage = VimeoStorage()
        sys.modules["__main__"].settings.getSetting.return_value = "['some_value']"

        result = storage.retrieveResultSetSettings("some_key")

        assert(result == ['some_value'])

if __name__ == '__main__':
        nose.runmodule()
