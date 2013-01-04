import sys
import time

class MockVimeoDepends:

    def mock(self):
        import string, platform
        from mock import Mock
        sys.path.append("../plugin/")
        
        #Setup default test various values 
        sys.modules[ "__main__" ].plugin = "Vimeo - IntegrationTest"
        sys.modules[ "__main__" ].dbg = True
        try:
            plat = platform.uname()
        except:
            plat = ('', '', '', '', '', '')

        if plat[0] == "FreeBSD":
            sys.modules[ "__main__" ].dbglevel = 5
        else:
            sys.modules[ "__main__" ].dbglevel = 3

        sys.modules[ "__main__" ].login = "" 
        
        sys.modules[ "__main__" ].utils = Mock()
        sys.modules[ "__main__" ].downloader = Mock()
        sys.modules[ "__main__" ].cache = Mock()
        sys.modules[ "__main__" ].cache.cacheFunction.side_effect = self.execute
        sys.modules[ "__main__" ].cache.getMulti.return_value = []
        sys.modules[ "__main__" ].cache.get.return_value = ""
    
    def mockXBMC(self):
        from mock import Mock
        sys.path.append("../xbmc-mocks/")
        import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs
        #Setup basic xbmc dependencies
        sys.modules[ "__main__" ].xbmc = Mock(spec=xbmc)
        sys.modules[ "__main__" ].xbmc.getSkinDir = Mock()
        sys.modules[ "__main__" ].xbmc.translatePath = Mock()
        sys.modules[ "__main__" ].xbmc.translatePath.return_value = "./tmp/"
        sys.modules[ "__main__" ].xbmc.log = Mock()
        sys.modules[ "__main__" ].xbmc.log.side_effect = self.log
        sys.modules[ "__main__" ].xbmc.getSkinDir = Mock()
        sys.modules[ "__main__" ].xbmc.getSkinDir.return_value = "testSkinPath"
        sys.modules[ "__main__" ].xbmc.getInfoLabel = Mock()
        sys.modules[ "__main__" ].xbmc.getInfoLabel.return_value = "some_info_label"
        sys.modules[ "__main__" ].xbmcaddon = Mock(spec=xbmcaddon)
        sys.modules[ "__main__" ].xbmcgui = Mock(spec=xbmcgui)
        sys.modules[ "__main__" ].xbmcgui.WindowXMLDialog.return_value = "testWindowXML"
        sys.modules[ "__main__" ].xbmcgui.getCurrentWindowId.return_value = 1
        
        sys.modules[ "__main__" ].xbmcplugin = Mock(spec=xbmcplugin)
        sys.modules[ "__main__" ].xbmcvfs = xbmcvfs
        sys.modules[ "__main__" ].xbmcvfs = Mock(spec=xbmcvfs)
        sys.modules[ "__main__" ].xbmcvfs.exists.return_value = False
        import xbmcSettings
        sys.modules[ "__main__" ].settings = xbmcSettings.xbmcSettings()
        import xbmcLanguage
        sys.modules[ "__main__" ].language = xbmcLanguage.xbmcLanguage()

        sys.modules["DialogDownloadProgress"] = __import__("mock")
        sys.modules["DialogDownloadProgress"].DownloadProgress = Mock()
        sys.modules["storageserverdummy"] = Mock()
    
    def log(self, description, level = 0):
        if sys.modules[ "__main__" ].dbg and sys.modules[ "__main__" ].dbglevel > level:
            import inspect
            try:
                print "%s [%s] %s : '%s'" % (time.strftime("%H:%M:%S"), "Vimeo IntegrationTest", inspect.stack()[3][3] , description.decode("utf-8","ignore")) # 3 - 3 for TestYouTubeUserFeeds.py
            except:
                print "%s [%s] %s : '%s'" % (time.strftime("%H:%M:%S"), "Vimeo IntegrationTest", inspect.stack()[3][3] , description) # 3 - 3 for TestYouTubeUserFeeds.py
        
    def execute(self, function, *args):
        return function(*args)
