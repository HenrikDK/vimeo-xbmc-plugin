import BaseTestCase
import nose
import sys


class TestVimeoLogin(BaseTestCase.BaseTestCase):

    def test_plugin_should_perform_basic_login_correctly(self):
        sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
        assert(sys.modules["__main__"].settings.getSetting("userid") == "")
        assert(sys.modules["__main__"].settings.getSetting("oauth_token_secret") == "")
        assert(sys.modules["__main__"].settings.getSetting("oauth_token") == "")

        print "user_id: " + sys.modules["__main__"].settings.getSetting("userid")
        print "user_email: " + sys.modules["__main__"].settings.getSetting("user_email")
        print "user_password: " + sys.modules["__main__"].settings.getSetting("user_password")
        print "oauth_token: " + sys.modules["__main__"].settings.getSetting("oauth_token")
        print "oauth_token_secret: " + sys.modules["__main__"].settings.getSetting("oauth_token_secret")

        self.navigation.executeAction({"action": "settings"})

        user_id = sys.modules["__main__"].settings.getSetting("userid")
        oauth_token = sys.modules["__main__"].settings.getSetting("oauth_token")
        oauth_token_secret = sys.modules["__main__"].settings.getSetting("oauth_token_secret")
        print "user_id: " + user_id + " - " + str(len(user_id))
        print "user_email: " + sys.modules["__main__"].settings.getSetting("user_email")
        print "user_password: " + sys.modules["__main__"].settings.getSetting("user_password")
        print "oauth_token: " + oauth_token + " - " + str(len(oauth_token))
        print "oauth_token_secret: " + " - " + str(len(oauth_token_secret))
        assert(len(user_id.strip()) > 0 )
        assert(len(oauth_token) > 20)
        assert(len(oauth_token_secret) > 20)

if __name__ == "__main__":
    nose.runmodule()
