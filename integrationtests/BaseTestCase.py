import sys
import os
import time
import unittest2
import MockVimeoDepends

MockVimeoDepends.MockVimeoDepends().mockXBMC()

sys.path.append('../plugin/')
sys.path.append('../plugin/vimeo')
sys.path.append('../external-modules/')
sys.path.append('../xbmc-mocks/')

if not os.path.exists("tmp"):
    os.mkdir("tmp")
else:
    for old_file in os.listdir("tmp"):
        os.remove("./tmp/" + old_file)

class BaseTestCase(unittest2.TestCase):  #pragma: no cover
    def setUp(self):
        time.sleep(10)
        MockVimeoDepends.MockVimeoDepends().mock()
        MockVimeoDepends.MockVimeoDepends().mockXBMC()
        self.initializeVimeoClient()
        self.initializePlugin()

    def initializeVimeoClient(self):
        import vimeo

        if len(sys.modules["__main__"].settings.getSetting("oauth_token_secret")) > 0 and len(sys.modules["__main__"].settings.getSetting("oauth_token")) > 0:
            sys.modules["__main__"].client = vimeo.VimeoClient(token=sys.modules["__main__"].settings.getSetting("oauth_token").encode('ascii'), token_secret=sys.modules["__main__"].settings.getSetting("oauth_token_secret").encode('ascii'))
        else:
            sys.modules["__main__"].client = vimeo.VimeoClient()

    def initializePlugin(self):
        import CommonFunctions
        sys.modules["__main__"].common = CommonFunctions
        sys.modules["__main__"].common.log = sys.modules["__main__"].xbmc.log
        sys.modules["__main__"].xbmcaddon.Addon.return_value = sys.modules["__main__"].settings
        sys.modules["__main__"].xbmcvfs.exists.return_value = True

        import SimpleDownloader
        sys.modules["__main__"].downloader = SimpleDownloader.SimpleDownloader()

        import cookielib
        import urllib2
        sys.modules["__main__"].cookiejar = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(sys.modules["__main__"].cookiejar))
        urllib2.install_opener(opener)

        sys.argv = ["something", -1, "something_else"]

        import VimeoUtils
        sys.modules["__main__"].utils = VimeoUtils.VimeoUtils()

        import VimeoLogin
        sys.modules["__main__"].login = VimeoLogin.VimeoLogin()

        import VimeoCore
        sys.modules["__main__"].core = VimeoCore.VimeoCore()

        import VimeoStorage
        sys.modules["__main__"].storage = VimeoStorage.VimeoStorage()

        import VimeoFeeds
        sys.modules["__main__"].feeds = VimeoFeeds.VimeoFeeds()

        import VimeoPlayer
        sys.modules["__main__"].player = VimeoPlayer.VimeoPlayer()

        import VimeoPlaylistControl
        sys.modules["__main__"].playlist = VimeoPlaylistControl.VimeoPlaylistControl()

        import VimeoNavigation
        self.navigation = VimeoNavigation.VimeoNavigation()

    def assert_directory_count_greater_than_or_equals(self, count):
        args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list

        if len(args) < count:
            print "Directory list length %s is not greater than or equal to expected list lengt %s" % (repr(len(args)), repr(count))
        
        assert(len(args) >= count)
    
    def assert_directory_count_less_than_or_equals(self, count):
        args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
        
        if len(args) > count:
            print "Directory list length %s is not less than or equal to expected list lengt %s" % (repr(len(args)), repr(count))
        
        assert(len(args) <= count)

    def assert_directory_count_equals(self, count):
        args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
        
        if len(args) != count:
            print "Expected directory list length %s does not match actual list lengt %s" % (repr(count), repr(len(args)))
        
        assert(len(args) == count)
    
    def assert_directory_is_a_video_list(self):
        folder_count = 0
        args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
        
        for call in args:
            if call[1]["isFolder"] == True:
                folder_count += 1
        
        if folder_count > 1:
            print "Directory is not a video list, it contains %s folders (Max 1 allowed)" % folder_count
            print "Directory list: \r\n" + repr(args)

        assert(folder_count <= 1)
        
    def assert_directory_is_a_folder_list(self):
        video_count = 0
        args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
        
        for call in args:
            if call[1]["isFolder"] == False:
                video_count += 1
        
        if video_count > 0:
            print "Directory is not a folder list, it contains %s videos" % video_count
            print "Directory list: \r\n" + repr(args)
            
        assert(video_count == 0)
        
    def assert_directory_contains_only_unique_video_items(self):
        video_ids = []
        non_unique = []
        args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
        
        for call in args:
            url = call[1]["url"]
            if url.find("videoid=") > -1:
                video = url[url.find("videoid=") + len("videoid="):]
                if video.find("&") > -1:
                    video = video[:video.find("&")]
                
                if video:
                    if video in video_ids:
                        non_unique.append(video)
                    video_ids.append(video)
        
        if len(non_unique) > 0:
            print "Directory contains one or more duplicate videoids.\r\n Duplicates: %s \r\n Full List: %s" % (repr(non_unique), repr(video_ids)) 
            print "Directory list: \r\n" + repr(args)
            
        assert(len(non_unique) == 0)
    
    def assert_directory_contains_almost_only_unique_video_items(self):
        video_ids = []
        non_unique = []
        args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
        
        for call in args:
            url = call[1]["url"]
            if url.find("videoid=") > -1:
                video = url[url.find("videoid=") + len("videoid="):]
                if video.find("&") > -1:
                    video = video[:video.find("&")]
                
                if video:
                    if video in video_ids:
                        non_unique.append(video)
                    video_ids.append(video)
        
        if len(non_unique) > 1:
            print "Directory contains two or more duplicate videoids.\r\n Duplicates: %s \r\n Full List: %s" % (repr(non_unique), repr(video_ids)) 
            print "Directory list: \r\n" + repr(args)
            
        assert(len(non_unique) <= 1)
    
    def assert_directory_items_should_have_external_thumbnails(self):
        args = sys.modules["__main__"].xbmcgui.ListItem.call_args_list
        
        missing_thumb_count = 0
        for call in args:
            if call[1]["thumbnailImage"].find("http://") == -1: 
                missing_thumb_count += 1
        
        if missing_thumb_count > 1:
            print "Directory contains more than 3 item with an invalid thumbnail: " 
            print "List Items: \r\n" + repr(args)
        
        assert(missing_thumb_count <= 3)

    def assert_half_of_all_directory_items_should_have_thumbnails(self):
        args = sys.modules["__main__"].xbmcgui.ListItem.call_args_list

        missing_thumb_count = 0
        total_count = 0
        for call in args:
            total_count += 1
            if len(call[1]["thumbnailImage"]) <= 7:
                missing_thumb_count += 1

        if missing_thumb_count > (total_count / 2):
            print "More than half of all Directory items contain a invalid thumbnail: "
            print "List Items: \r\n" + repr(args)

        assert(missing_thumb_count <= (total_count / 2))

    def assert_directory_items_should_have_thumbnails(self):
        args = sys.modules["__main__"].xbmcgui.ListItem.call_args_list
        
        missing_thumb_count = 0
        for call in args:
            if len(call[1]["thumbnailImage"]) <= 7: 
                missing_thumb_count += 1
        
        if missing_thumb_count > 1:
            print "Directory contains more than one item with an invalid thumbnail: " 
            print "List Items: \r\n" + repr(args)
        
        assert(missing_thumb_count <= 1)
        
    def assert_directory_items_should_have_poster_thumbnails(self):
        args = sys.modules["__main__"].xbmcgui.ListItem.call_args_list
        
        missing_poster_count = 0
        for call in args:
            if call[1]["thumbnailImage"].find("poster") == -1: 
                missing_poster_count += 1
        
        if missing_poster_count > 1:
            print "Directory contains more than one item with an invalid thumbnail: " 
            print "List Items: \r\n" + repr(args)
        
        assert(missing_poster_count <= 1)
    
    def assert_directory_should_have_next_folder(self):
        args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
        
        next_folder_count = 0
        
        for call in args:
            if call[1]["url"].find("page=") > 0:
                next_folder_count += 1
        
        if next_folder_count != 1:
            print "Expected Directory Listing to contain a next folder but didn't find any:"
            print "List Items: \r\n" + repr(args)
        assert(next_folder_count == 1)
        
    def assert_directory_item_urls_contain(self, param, limit = 1):
        args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
        
        missing_count = 0
        
        for call in args:
            url = call[1]["url"]
            if url.find(param + "=") < 0:
                missing_count += 1
            else:
                value = url[url.find(param + "=") + len(param + "="):]
                if value.find("&") > -1:
                    value = value[:value.find("&")]

                if len(value) == 0:
                    missing_count += 1
        
        if missing_count > limit:
            print 'Expected directory items url\'s to contain the "%s" but more than one item was missing this property' % param
            print "Directory list: \r\n" + repr(args)
            
        assert(missing_count <= limit)

    def reset_xbmc_mocks(self):
        sys.modules["__main__"].xbmcplugin.addDirectoryItem.reset_mock()
        sys.modules["__main__"].xbmcplugin.reset_mock()
        sys.modules["__main__"].xbmc.PlayList().add.reset_mock()
        sys.modules["__main__"].xbmc.PlayList().reset_mock()
        sys.modules["__main__"].xbmc.reset_mock()
        sys.modules["__main__"].xbmcgui.ListItem.reset_mock()
        sys.modules["__main__"].xbmcgui.reset_mock()

    def assert_directory_item_urls_contain_at_least_one(self, param):
        args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list

        found = False

        for call in args:
            print repr(call)
            url = call[1]["url"]
            if url.find(param) > -1:
                found = True

        if not found:
            print 'Couldnt find %s in list of directory item title\'s' % param
            print "Directory list: \r\n" + repr(args)

        assert(found == True)
    
    def assert_directory_item_titles_contain(self, param):
        args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
        
        found = False
        
        for call in args:
            title = call[1]["Title"]
            if title.find(param) > -1:
                found = True 
        
        if not found:
            print 'Couldnt find %s in list of directory item title\'s' % param
            print "Directory list: \r\n" + repr(args)
            
        assert(found == True)

    def assert_directory_item_titles_does_not_contain(self, param):
        args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
        
        found = False
        
        for call in args:
            title = call[1]["Title"]
            if title.find(param) > -1:
                found = True 
        
        if found:
            print 'Found %s in list of directory item title\'s' % param
            print "Directory list: \r\n" + repr(args)
            
        assert(found == False)
                
    def assert_playlist_count_greater_than_or_equals(self, count):
        args = sys.modules["__main__"].xbmc.PlayList().add.call_args_list
        
        if len(args) < count:
            print "Playlist list length %s is not greater than or equal to expected list lengt %s" % (repr(len(args)), repr(count))
        
        assert(len(args) >= count)
        
    def assert_playlist_count_less_than_or_equals(self, count):
        args = sys.modules["__main__"].xbmc.PlayList().add.call_args_list
        
        if len(args) > count:
            print "Playlist list length %s is not less than or equal to expected list lengt %s" % (repr(len(args)), repr(count))
        
        assert(len(args) <= count)

    def assert_playlist_count_equals(self, count):
        args = sys.modules["__main__"].xbmc.PlayList().add.call_args_list
        
        if len(args) != count:
            print "Playlist list length %s does not equal expected list lengt %s" % (repr(len(args)), repr(count))
        
        assert(len(args) == count)

    def assert_playlist_contains_only_unique_video_items(self):
        video_ids = []
        non_unique = []
        args = sys.modules["__main__"].xbmc.PlayList().add.call_args_list
        
        for call in args:
            url = call[0][0]
            if url.find("videoid=") > -1:
                video = url[url.find("videoid=") + len("videoid="):]
                if video.find("&") > -1:
                    video = video[:video.find("&")]
                
                if video:
                    if video in video_ids:
                        non_unique.append(video)
                    video_ids.append(video)
        
        if len(non_unique) > 0:
            print "Playlist contains one or more duplicate videoids.\r\n Duplicates: %s \r\n Full List: %s" % (repr(non_unique), repr(video_ids)) 
            print "Playlist: \r\n" + repr(args)
            
        assert(len(non_unique) == 0)
    
    def assert_playlist_videos_contain(self, videoid):
        video_ids = []
        args = sys.modules["__main__"].xbmc.PlayList().add.call_args_list
        
        for call in args:
            url = call[0][0]
            if url.find("videoid=") > -1:
                video = url[url.find("videoid=") + len("videoid="):]
                if video.find("&") > -1:
                    video = video[:video.find("&")]
                
                if video not in video_ids:
                    video_ids.append(video)
        
        print repr(video_ids)
        
        if videoid not in video_ids:
            print 'Expected to find %s in playlist items' % videoid
            print "Playlist items: \r\n" + repr(args)
        
        assert(videoid in video_ids)

    def assert_playlist_videos_does_not_contain(self, videoid):
        video_ids = []
        args = sys.modules["__main__"].xbmc.PlayList().add.call_args_list
        
        for call in args:
            url = call[0][0]
            if url.find("videoid=") > -1:
                video = url[url.find("videoid=") + len("videoid="):]
                if video.find("&") > -1:
                    video = video[:video.find("&")]
                
                if video not in video_ids:
                    video_ids.append(video)
        
        if videoid in video_ids:
            print 'Expected not to find %s in playlist items' % videoid
            print "Playlist items: \r\n" + repr(args)
            
        assert(videoid not in video_ids)

    def assert_xbmc_recived_video_url(self):
        args = sys.modules["__main__"].xbmcgui.ListItem.call_args_list

        if sys.modules["__main__"].xbmcgui.ListItem.call_count == 0 :
            print "Expected XBMC to recieve a video url item, but no such item was recieved"
            assert (sys.modules["__main__"].xbmcgui.ListItem.call_count > 0)

        for call in args:
            if not call[1].has_key("path"):
                print "Expected to find videourl in xbmc video item, but path was not set: " + repr(call)
            assert (call[1].has_key("path"))

    def assert_video_url_contains(self, param):
        args = sys.modules["__main__"].xbmcgui.ListItem.call_args_list

        for call in args:

            if (call[1]["path"].find(param) < 0):
                print "Failed to find '" + param + "' in videourl: " + repr(call)
            assert (call[1]["path"].find(param) >= 0)

    def assert_plugin_reported_that_url_was_resolved_correctly(self):
        args = sys.modules[ "__main__" ].xbmcplugin.setResolvedUrl.call_args_list

        if not args[0][1].has_key("listitem"):
            print "Args: " + repr(args)
            print repr(args[0][1].has_key("listitem"))
            print repr(args[0][1]["handle"] == -1)
            print repr(args[0][1]["succeeded"] == True)

        assert(args[0][1].has_key("listitem"))
        assert(args[0][1]["handle"] == -1)
        assert(args[0][1]["succeeded"] == True)
