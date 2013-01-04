import inspect
import time
import sys


class MockVimeoDepends:
        common = ""

        def mock(self):
                import sys
                from mock import Mock
                sys.path.append("../plugin/")

                #Setup default test various values
                sys.modules["__main__"].plugin = "Vimeo - Unittest"
                sys.modules["__main__"].dbg = True
		try:
			plat = platform.uname()
		except:
			plat = ('', '', '', '', '', '')
		if plat[0] == "FreeBSD":
			sys.modules["__main__"].dbglevel = 5
		else:
			sys.modules["__main__"].dbglevel = 3
                sys.modules["__main__"].login = ""
                sys.modules["__main__"].language = Mock()
                sys.modules["__main__"].cookiejar = Mock()

                sys.modules["__main__"].common = Mock()
                sys.modules["__main__"].log_override = self
                sys.modules["__main__"].common.log.side_effect = sys.modules["__main__"].log_override.log
                sys.modules["__main__"].common.USERAGENT = "Mozilla/5.0 (MOCK)"

                sys.modules["__main__"].cache = Mock()
                sys.modules["__main__"].client = Mock()

                import VimeoUtils
                sys.modules["__main__"].utils = Mock(spec=VimeoUtils.VimeoUtils)
                sys.modules["__main__"].utils.INVALID_CHARS = "\\/:*?\"<>|"

                import VimeoPlaylistControl
                sys.modules["__main__"].playlist = Mock(spec=VimeoPlaylistControl.VimeoPlaylistControl)

                import VimeoLogin
                sys.modules["__main__"].login = Mock(spec=VimeoLogin.VimeoLogin)

                import VimeoCore
                sys.modules["__main__"].core = Mock(spec=VimeoCore.VimeoCore)

                import VimeoPlayer
                sys.modules["__main__"].player = Mock(spec=VimeoPlayer.VimeoPlayer)

                sys.modules["__main__"].storage = Mock()
                sys.modules["__main__"].feeds = Mock()
                sys.modules["__main__"].downloader = Mock()                
        
        def mockXBMC(self):
                import sys
                from mock import Mock
                sys.path.append("../xbmc-mocks/")
                import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs
                
                #Setup basic xbmc dependencies
                sys.modules["__main__"].xbmc = Mock(spec=xbmc)
                sys.modules["__main__"].xbmc.translatePath = Mock()
                sys.modules["__main__"].xbmc.translatePath.return_value = "testing"
                sys.modules["__main__"].xbmc.getSkinDir = Mock()
                sys.modules["__main__"].xbmc.getSkinDir.return_value = "testSkinPath"
                sys.modules["__main__"].xbmc.getInfoLabel.return_value = "some_info_label"
                sys.modules["__main__"].xbmcaddon = Mock(spec=xbmcaddon)
                sys.modules["__main__"].xbmcgui = Mock(spec=xbmcgui)
                sys.modules["__main__"].xbmcgui.WindowXMLDialog.return_value = "testWindowXML"
                
                sys.modules["__main__"].xbmcplugin = Mock(spec=xbmcplugin)
                sys.modules["__main__"].xbmcvfs = Mock(spec=xbmcvfs)
                sys.modules["__main__"].settings = Mock(spec= xbmcaddon.Addon())
                sys.modules["__main__"].settings.getAddonInfo.return_value = "somepath"
                
                sys.modules["DialogDownloadProgress"] = __import__("mock")
                sys.modules["DialogDownloadProgress"].DownloadProgress = Mock()

        def log(self, description, level = 0):
                if sys.modules["__main__"].dbg and sys.modules["__main__"].dbglevel > level:
                        try:
                                print "%s [%s] %s : '%s'" % (time.strftime("%H:%M:%S"), sys.modules["__main__"].plugin, inspect.stack()[1][3] , description.decode("utf-8","ignore"))
                        except:
                                print "%s [%s] %s : '%s'" % (time.strftime("%H:%M:%S"), sys.modules["__main__"].plugin, inspect.stack()[1][3] , description)
