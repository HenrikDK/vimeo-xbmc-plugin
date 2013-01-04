# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock
import sys
from  VimeoPlaylistControl import VimeoPlaylistControl

class TestVimeoPlaylistControl(BaseTestCase.BaseTestCase):
    
    def test_playAll_should_call_getUserFeed_if_api_is_playlist_in_params(self):
        control = VimeoPlaylistControl()
        control.getUserFeed = Mock()
        control.getUserFeed.return_value = ""
        
        control.playAll({"album":"someid"})
        
        control.getUserFeed.assert_called_with({"album":"someid", 'fetch_all': 'true'})

    def test_playAll_should_call_getUserFeed_if_api_is_favorites_in_params(self):
        control = VimeoPlaylistControl()
        control.getUserFeed = Mock()
        control.getUserFeed.return_value = ""
        
        control.playAll({"api":"my_likes"})
        
        control.getUserFeed.assert_called_with({"api":"my_likes", 'login':'true','fetch_all': 'true'})

    def test_playAll_should_call_getUserFeed_if_api_is_subscriptions_in_params(self):
        control = VimeoPlaylistControl()
        control.getUserFeed = Mock()
        control.getUserFeed.return_value = ""
        
        control.playAll({"api":"my_newsubscriptions"})
        
        control.getUserFeed.assert_called_with({"api":"my_newsubscriptions", 'login':"true", 'fetch_all': 'true'})
        
    def test_playAll_should_not_call_xbmc_player_if_params_is_empty(self):
        control = VimeoPlaylistControl()
        
        control.playAll({})
        
        assert(sys.modules["__main__"].xbmc.Player.call_count == 0)
        assert(sys.modules["__main__"].xbmc.Player().call_count == 0)
        
    def test_playAll_should_call_xbmc_player_stop_if_player_is_playing(self):
        control = VimeoPlaylistControl()
        control.getUserFeed = Mock()
        control.getUserFeed.return_value = [{"Title":"someTitle", "videoid":"some_id","thumbnail":"some_thumbnail"}]
        
        control.playAll({"album":"someid"})
        
        sys.modules["__main__"].xbmc.Player.assert_called_with()
        sys.modules["__main__"].xbmc.Player().isPlaying.assert_called_with()
        sys.modules["__main__"].xbmc.Player().stop.assert_called_with()
        
    def test_playAll_should_call_xbmc_PlayList_clear_if_results_is_not_empty(self):
        playlist_value = Mock()
        sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
        control = VimeoPlaylistControl()
        control.getUserFeed = Mock()
        control.getUserFeed.return_value = [{"Title":"someTitle", "videoid":"some_id","thumbnail":"some_thumbnail"}]
        
        control.playAll({"album":"someid"})
        
        playlist_value.clear.assert_called_with()
        
    def test_playAll_should_call_xbmc_player_shuffle_if_shuffle_is_in_params(self):
        playlist_value = Mock()
        sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
        control = VimeoPlaylistControl()
        control.getUserFeed = Mock()
        control.getUserFeed.return_value = [{"Title":"someTitle", "videoid":"some_id","thumbnail":"some_thumbnail"}]
        
        control.playAll({"album":"someid","shuffle":"true"})
        
        sys.modules["__main__"].xbmc.Player.assert_called_with()
        sys.modules["__main__"].xbmc.Player().isPlaying.assert_called_with()
        sys.modules["__main__"].xbmc.Player().stop.assert_called_with()
        playlist_value.shuffle.assert_called_with()
        
    def test_playAll_should_queue_all_items_in_result_list(self):
        playlist_value = Mock()
        sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
        control = VimeoPlaylistControl()
        control.getUserFeed = Mock()
        control.getUserFeed.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
        
        control.playAll({"album":"someid","shuffle":"true"})
        
        assert(playlist_value.add.call_count == 2)
        
    def test_playAll_should_queue_all_items_in_result_list_after_provided_videoid(self):
        playlist_value = Mock()
        sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
        control = VimeoPlaylistControl()
        control.getUserFeed = Mock()
        control.getUserFeed.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"},{"Title":"someTitle3", "videoid":"some_id3","thumbnail":"some_thumbnail3"},{"Title":"someTitle4", "videoid":"some_id4","thumbnail":"some_thumbnail4"}]
        
        control.playAll({"album":"someid","shuffle":"true","videoid":"some_id3"})
        
        assert(playlist_value.add.call_count == 2)
	
    def test_playAll_should_start_playback_of_playlist_if_result_list_is_not_empty(self):
        playlist_value = Mock()
        sys.modules["__main__"].xbmc.PlayList.return_value = playlist_value
        control = VimeoPlaylistControl()
        control.getUserFeed = Mock()
        control.getUserFeed.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
        
        control.playAll({"album":"someid"})
        
        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('playlist.playoffset(video , 0)')

    def test_getUserFeed_should_call_feeds_list_all(self):
        control = VimeoPlaylistControl()
        
        control.getUserFeed({"album":"some_album"})
        
        assert(sys.modules["__main__"].feeds.listAll.call_count > 0)

    def test_getUserFeed_should_call_core_list_all_with_correct_params(self):
        sys.modules["__main__"].feeds.listAll.return_value = ("",200)
        control = VimeoPlaylistControl()
        
        control.getUserFeed({"contact":"some_contact", "user_feed":"favorites"})
        
        assert(sys.modules["__main__"].feeds.listAll.call_count == 1)
        sys.modules["__main__"].feeds.listAll.assert_called_with({"user_feed":"favorites","contact":"some_contact"})

    def test_addToPlaylist_should_call_list_all_if_playlist_is_not_in_params(self):
        sys.modules["__main__"].feeds.listAll.return_value = ([])
        control = VimeoPlaylistControl()
        control.createPlayList = Mock()
        
        control.addToAlbum({})
        
        sys.modules["__main__"].feeds.listAll.assert_called_with({'api': 'my_albums', 'login': 'true', 'folder': 'album'})
        assert(sys.modules["__main__"].feeds.listAll.call_count == 1)

    def test_addToPlaylist_should_ask_user_for_album_if_album_is_not_in_params(self):
        sys.modules["__main__"].feeds.listAll.return_value = ([{"Title":"Album1"},{"Title":"Album2"}])
        sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 0
        control = VimeoPlaylistControl()
        control.createPlayList = Mock()

        control.addToAlbum({})
        
        assert(sys.modules["__main__"].xbmcgui.Dialog.call_count == 2)
        assert(sys.modules["__main__"].xbmcgui.Dialog().select.call_count == 1)

    def test_addToPlaylist_should_call_createPlaylist_if_user_selects_create_option(self):
        sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 0
        sys.modules["__main__"].feeds.listAll.return_value =([{"Title":"Album1"},{"Title":"Album2"}])
        control = VimeoPlaylistControl()
        control.createAlbum = Mock()
        
        control.addToAlbum({})
        
        control.createAlbum.assert_called_with({})

    def test_addToPlaylist_should_call_core_addToAlbum_if_playlist_is_in_params(self):
        control = VimeoPlaylistControl()
        control.createPlayList = Mock()
        
        control.addToAlbum({"album":"album1"})
        
        sys.modules["__main__"].core.addToAlbum.assert_called_with({'album': 'album1'})

    def test_addToPlaylist_should_call_core_add_to_playlist_if_user_has_selected_playlist(self):
        sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 1
        sys.modules["__main__"].feeds.listAll.return_value = ([{"Title":"Album1","album":"album1"},{"Title":"Album2","album":"album2"}])
        control = VimeoPlaylistControl()
        control.createPlayList = Mock()
        
        control.addToAlbum({})
        
        sys.modules["__main__"].core.addToAlbum.assert_called_with({'album': 'album1'})

    def test_createPlayList_should_ask_user_for_input(self):
        sys.modules["__main__"].common.getUserInput.return_value = ""
        sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 1
        sys.modules["__main__"].language.return_value = "my_string"
        control = VimeoPlaylistControl()
        
        control.createAlbum({})
        
        sys.modules["__main__"].common.getUserInput.assert_called_with("my_string")
        sys.modules["__main__"].language.assert_called_with(30033)

    def test_createPlayList_should_call_createAlbum_if_user_provided_playlist_name(self):
        sys.modules["__main__"].common.getUserInput.return_value = "my_album_name"
        sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 1
        sys.modules["__main__"].language.return_value = "my_string"
        control = VimeoPlaylistControl()
        
        control.createAlbum({"videoid":"some_id"})
        
        sys.modules["__main__"].core.createAlbum.assert_called_with({"title":"my_album_name","videoid":"some_id"})
        
    def test_createPlayList_should_not_call_createAlbum_if_user_cancels(self):
        sys.modules["__main__"].common.getUserInput.return_value = ""
        sys.modules["__main__"].xbmcgui.Dialog().select.return_value = 1
        sys.modules["__main__"].language.return_value = "my_string"
        control = VimeoPlaylistControl()
        
        control.createAlbum({})
        
        assert(sys.modules["__main__"].core.createAlbum.call_count == 0)

    def test_removeFromPlaylist_should_exit_cleanly_if_album_or_video_id_is_missing(self):
        control = VimeoPlaylistControl()
        
        control.removeFromAlbum({})
        
        assert(sys.modules["__main__"].core.removeFromAlbum.call_count == 0)

    def test_removeFromPlaylist_should_call_core_removeFromAlbum(self):
        sys.modules["__main__"].core.removeFromAlbum.return_value = ("",200)
        control = VimeoPlaylistControl()

        control.removeFromAlbum({"videoid":"some_id", "album":"some_album"})
        
        sys.modules["__main__"].core.removeFromAlbum.assert_called_with({"videoid":"some_id", "album":"some_album"})

    def test_removeFromPlaylist_should_show_error_message_if_remove_call_failed(self):
        sys.modules["__main__"].core.removeFromAlbum.return_value = ("fail",303)
        sys.modules["__main__"].language.return_value = "my_string"
        control = VimeoPlaylistControl()
        
        control.removeFromAlbum({"videoid":"some_id", "album":"some_album"})
        
        sys.modules["__main__"].utils.showErrorMessage.assert_called_with("my_string","fail",303)
	
    def test_removeFromPlaylist_should_call_xbmc_execute_builtin_on_success(self):
        control = VimeoPlaylistControl()
        sys.modules["__main__"].core.removeFromAlbum.return_value = ("",200)
        
        control.removeFromAlbum({"videoid":"some_id", "album":"some_album"})
        
        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with("Container.Refresh")
	
    def test_deletePlaylist_should_exit_cleanly_if_playlist_is_missing(self):
        sys.modules["__main__"].core.deleteAlbum.return_value = ("",200)
        control = VimeoPlaylistControl()
        
        control.deleteAlbum({})
        
        assert(sys.modules["__main__"].core.deleteAlbum.call_count == 0)
	
    def test_deletePlaylist_should_call_core_delete_album(self):
        sys.modules["__main__"].core.deleteAlbum.return_value = ("",200)
        control = VimeoPlaylistControl()
        
        control.deleteAlbum({"album":"some_album"})
        
        sys.modules["__main__"].core.deleteAlbum.assert_called_with({"album":"some_album"})
	
    def test_deletePlaylist_should_show_error_message_if_delete_call_failed(self):
        sys.modules["__main__"].core.deleteAlbum.return_value = ("fail",303)
        sys.modules["__main__"].language.return_value = "my_string"
        control = VimeoPlaylistControl()
        
        control.deleteAlbum({"album":"some_album"})
        
        sys.modules["__main__"].utils.showErrorMessage.assert_called_with("my_string","fail",303)
	
    def test_deletePlaylist_should_call_xbmc_execute_builtin_on_success(self):
        sys.modules["__main__"].core.deleteAlbum.return_value = ("",200)
        control = VimeoPlaylistControl()
        
        control.deleteAlbum({"album":"some_album"})
        
        sys.modules["__main__"].xbmc.executebuiltin.assert_called_with("Container.Refresh")	

if __name__ == '__main__':
    nose.runmodule()
