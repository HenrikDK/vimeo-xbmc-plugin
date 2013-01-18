# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
from VimeoLogin import VimeoLogin


class TestVimeoLogin(BaseTestCase.BaseTestCase):

    def test_login_should_call_settings_openSettings(self):
        login = VimeoLogin()
        login._login = Mock(return_value=("",200))

        login.login()

        sys.modules["__main__"].settings.openSettings.assert_any_call()

    def test_login_should_not_perform_login_if_username_isnt_set(self):
        login = VimeoLogin()
        sys.modules["__main__"].settings.getSetting.return_value = ""

        login._login = Mock(return_value=("",200))

        login.login()

        assert(login._login.call_count == 0)

    def test_login_should_call__login_if_username_is_set(self):
        login = VimeoLogin()
        login._login = Mock(return_value=("",200))

        login.login()

        login._login.assert_any_call()

    def test_login_should_display_message(self):
        login = VimeoLogin()
        login._login = Mock(return_value=("",200))

        login.login()

        assert (sys.modules["__main__"].utils.showMessage.call_count > 0)

    def test_login_should_refresh_folder(self):
        login = VimeoLogin()
        login._login = Mock(return_value=("",200))

        login.login()

        sys.modules["__main__"].xbmc.executebuiltin.assert_any_call("Container.Refresh")

    def test__login_should_reset_tokens_folder(self):
        login = VimeoLogin()
        login.login_get_verifier = Mock(return_value=("",200))
        sys.modules["__main__"].client.get_access_token.return_value = "some_token"

        login._login()

        sys.modules["__main__"].settings.setSetting.assert_any_call("userid", "")
        sys.modules["__main__"].settings.setSetting.assert_any_call("oauth_token_secret", "")
        sys.modules["__main__"].settings.setSetting.assert_any_call("oauth_token", "")

    def test__login_should_call_get_request_token(self):
        login = VimeoLogin()
        login.login_get_verifier = Mock(return_value=("",200))
        sys.modules["__main__"].client.get_access_token.return_value = "some_token"

        login._login()

        sys.modules["__main__"].client.get_request_token.assert_any_call()

    def test__login_should_call_get_authorization_url(self):
        login = VimeoLogin()
        login.login_get_verifier = Mock(return_value=("",200))
        sys.modules["__main__"].client.get_access_token.return_value = "some_token"

        login._login()

        sys.modules["__main__"].client.get_authorization_url.assert_any_call("write")

    def test__login_should_call_login_get_verifier(self):
        login = VimeoLogin()
        login.login_get_verifier = Mock(return_value=("",200))
        sys.modules["__main__"].client.get_authorization_url.return_value = ""
        sys.modules["__main__"].client.get_access_token.return_value = "some_token"

        login._login()

        login.login_get_verifier.assert_any_call("")

    def test__login_should_exit_if_login_get_verifier_fails(self):
        login = VimeoLogin()
        login.login_get_verifier = Mock(return_value=("",303))
        sys.modules["__main__"].client.get_authorization_url.return_value = ""
        sys.modules["__main__"].client.get_access_token.return_value = "some_token"

        login._login()

        assert(sys.modules["__main__"].client.set_verifier.call_count == 0)

    def test__login_should_call_set_verifier(self):
        login = VimeoLogin()
        login.login_get_verifier = Mock(return_value=("",200))
        sys.modules["__main__"].client.get_authorization_url.return_value = ""
        sys.modules["__main__"].client.get_access_token.return_value = "some_token"

        login._login()

        sys.modules["__main__"].client.set_verifier.assert_any_call("")

    def test__login_should_call_get_access_token(self):
        login = VimeoLogin()
        login.login_get_verifier = Mock(return_value=("",200))
        sys.modules["__main__"].client.get_authorization_url.return_value = ""
        sys.modules["__main__"].client.get_access_token.return_value = "some_token"

        login._login()

        sys.modules["__main__"].client.get_access_token.assert_any_call()

    def test__login_should_exit_if_no_token_is_found(self):
        login = VimeoLogin()
        login.login_get_verifier = Mock(return_value=("",200))
        sys.modules["__main__"].client.get_authorization_url.return_value = ""
        sys.modules["__main__"].client.get_access_token.return_value = "blablalba=2&oauth_token_secret=123&oauth_token=321&komkom=f&"

        (result, status) = login._login()

        assert (status == 303)

    def test__login_should_set_new_token_if_token_is_found(self):
        login = VimeoLogin()
        login.login_get_verifier = Mock(return_value=("",200))
        sys.modules["__main__"].client.get_authorization_url.return_value = ""
        sys.modules["__main__"].client.get_access_token.return_value = 'oauth_token_secret=123&oauth_token=321'

        login._login()

        sys.modules["__main__"].settings.setSetting.assert_any_call("oauth_token_secret", "123")
        sys.modules["__main__"].settings.setSetting.assert_any_call("oauth_token", "321")

    def test__login_should_exit_if_token_is_found(self):
        login = VimeoLogin()
        login.login_get_verifier = Mock(return_value=("",200))
        sys.modules["__main__"].client.get_authorization_url.return_value = ""
        sys.modules["__main__"].client.get_access_token.return_value = 'oauth_token_secret=123&oauth_token=321'

        (result, status) = login._login()

        assert (status == 200)

    def test_getAuth_should_call_settings_to_get_oauth_token(self):
        login = VimeoLogin()
        login._login = Mock(return_value=("",200))
        sys.modules["__main__"].settings.getSetting.return_value = "some_token"

        result = login._getAuth()

        sys.modules["__main__"].settings.getSetting.assert_any_call("oauth_token")


    def test_getAuth_should_return_oauth_token_from_settings_if_found(self):
        login = VimeoLogin()
        login._login = Mock(return_value=("",200))
        sys.modules["__main__"].settings.getSetting.return_value = "some_token"

        result = login._getAuth()

        assert (result == "some_token")

    def test_getAuth_should_call_login_if_oauth_is_not_found(self):
        login = VimeoLogin()
        login._login = Mock(return_value=("",200))
        sys.modules["__main__"].settings.getSetting.return_value = ""

        result = login._getAuth()

        login._login.assert_any_call()

    def ttest_getAuth_should_call_login_if_oauth_has_expired(self):
        #not implemented yet
        login = VimeoLogin()
        login._login = Mock(return_value=("",200))
        sys.modules["__main__"].settings.getSetting.side_effect = ["some_token","12"]

        result = login._getAuth()

        login._login.assert_any_call()

    def test_getAuth_should_call_return_new_oauth_token_after_calling_login(self):
        login = VimeoLogin()
        login._login = Mock(return_value=("",200))
        sys.modules["__main__"].settings.getSetting.side_effect = ["","some_new_token",""]

        result = login._getAuth()

        print repr(result)
        login._login.assert_any_call()
        assert (result == "some_new_token")

    def test_getAuth_should_return_false_if_login_fails(self):
        login = VimeoLogin()
        login._login = Mock(return_value=("",303))
        sys.modules["__main__"].settings.getSetting.side_effect = ["","some_new_token",""]

        result = login._getAuth()

        print repr(result)
        login._login.assert_any_call()
        assert (result == False)

    def test_login_get_verifier_should_return_verifier_on_success(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        login = VimeoLogin()
        login.extractCrossSiteScriptingToken = Mock(return_value ="some_token")
        login.extractUserId = Mock(return_value="some_userid")
        login.checkIfHttpLoginFailed = Mock(return_value="")
        login.extractLoginTokens = Mock(return_value=("some_token", "some_other_token"))
        login.authorizeAndExtractVerifier = Mock(return_value=("some_verifier"))
        login.performHttpLogin = Mock()

        (verifier, status) = login.login_get_verifier("some_url")

        print repr(verifier)
        assert(verifier == "some_verifier")

    def test_login_get_verifier_should_call_extractCrossSiteScriptingToken(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        login = VimeoLogin()
        login.extractCrossSiteScriptingToken = Mock(return_value ="some_token")
        login.extractUserId = Mock(return_value="some_userid")
        login.checkIfHttpLoginFailed = Mock(return_value="")
        login.extractLoginTokens = Mock(return_value=("some_token", "some_other_token"))
        login.authorizeAndExtractVerifier = Mock(return_value=("some_verifier"))
        login.performHttpLogin = Mock()

        login.login_get_verifier("some_url")

        login.extractCrossSiteScriptingToken.assert_any_call()

    def test_login_get_verifier_should_call_performHttpLogin(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        login = VimeoLogin()
        login.extractCrossSiteScriptingToken = Mock(return_value =["some_token"])
        login.extractUserId = Mock(return_value="some_userid")
        login.checkIfHttpLoginFailed = Mock(return_value="")
        login.extractLoginTokens = Mock(return_value=("some_token", "some_other_token"))
        login.authorizeAndExtractVerifier = Mock(return_value=("some_verifier"))
        login.performHttpLogin = Mock()

        login.login_get_verifier("some_url")

        login.performHttpLogin.assert_any_call("some_token")

    def test_login_get_verifier_should_call_extractUserId(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        login = VimeoLogin()
        login.extractCrossSiteScriptingToken = Mock(return_value ="some_token")
        login.extractUserId = Mock(return_value="some_userid")
        login.checkIfHttpLoginFailed = Mock(return_value="")
        login.extractLoginTokens = Mock(return_value=("some_token", "some_other_token"))
        login.authorizeAndExtractVerifier = Mock(return_value=("some_verifier"))
        login.performHttpLogin = Mock(return_value={"content":"tests"})

        login.login_get_verifier("some_url")

        login.extractUserId.assert_any_call({"content":"tests"})
        login.checkIfHttpLoginFailed.assert_any_call({"content":"tests"})

    def test_login_get_verifier_should_call_checkIfHttpLoginFailed(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        login = VimeoLogin()
        login.extractCrossSiteScriptingToken = Mock(return_value ="some_token")
        login.extractUserId = Mock(return_value="some_userid")
        login.checkIfHttpLoginFailed = Mock(return_value="")
        login.extractLoginTokens = Mock(return_value=("some_token", "some_other_token"))
        login.authorizeAndExtractVerifier = Mock(return_value=("some_verifier"))
        login.performHttpLogin = Mock(return_value={"content":"tests"})

        login.login_get_verifier("some_url")

        login.checkIfHttpLoginFailed.assert_any_call({"content":"tests"})

    def test_login_get_verifier_should_call_extractLoginTokens(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        login = VimeoLogin()
        login.extractCrossSiteScriptingToken = Mock(return_value ="some_token")
        login.extractUserId = Mock(return_value="some_userid")
        login.checkIfHttpLoginFailed = Mock(return_value="")
        login.extractLoginTokens = Mock(return_value=("some_token", "some_other_token"))
        login.authorizeAndExtractVerifier = Mock(return_value=("some_verifier"))
        login.performHttpLogin = Mock(return_value={"content":"tests"})

        login.login_get_verifier("some_url")

        login.extractLoginTokens.assert_any_call("some_url")

    def test_login_get_verifier_should_exit_cleanly_if_HttpLoginFailed(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        login = VimeoLogin()
        login.extractCrossSiteScriptingToken = Mock(return_value ="some_token")
        login.extractUserId = Mock(return_value="some_userid")
        login.checkIfHttpLoginFailed = Mock(return_value="true")
        login.extractLoginTokens = Mock(return_value=("some_token", "some_other_token"))
        login.authorizeAndExtractVerifier = Mock(return_value=("some_verifier"))
        login.performHttpLogin = Mock()

        (result, status) = login.login_get_verifier("some_url")

        assert (status == 303)

    def test_login_get_verifier_should_exit_cleanly_if_userid_is_missing(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        login = VimeoLogin()
        login.extractCrossSiteScriptingToken = Mock(return_value ="some_token")
        login.extractUserId = Mock(return_value="")
        login.checkIfHttpLoginFailed = Mock(return_value="")
        login.extractLoginTokens = Mock(return_value=("some_token", "some_other_token"))
        login.authorizeAndExtractVerifier = Mock(return_value=("some_verifier"))
        login.performHttpLogin = Mock()

        (result, status) = login.login_get_verifier("some_url")

        assert (status == 303)

    def test_login_get_verifier_should_exit_cleanly_if_no_login_tokens_are_found(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        login = VimeoLogin()
        login.extractCrossSiteScriptingToken = Mock(return_value ="some_token")
        login.extractUserId = Mock(return_value="some_user_id")
        login.checkIfHttpLoginFailed = Mock(return_value="")
        login.extractLoginTokens = Mock(return_value=("", ""))
        login.authorizeAndExtractVerifier = Mock(return_value=("some_verifier"))
        login.performHttpLogin = Mock()

        (result, status) = login.login_get_verifier("some_url")

        assert (status == 303)

    def test_login_get_verifier_should_exit_cleanly_if_no_verifier_is_found(self):
        sys.modules["__main__"].settings.getSetting.return_value = "0"
        login = VimeoLogin()
        login.extractCrossSiteScriptingToken = Mock(return_value ="some_token")
        login.extractUserId = Mock(return_value="some_user_id")
        login.checkIfHttpLoginFailed = Mock(return_value="")
        login.extractLoginTokens = Mock(return_value=("some_token", "some_other_token"))
        login.authorizeAndExtractVerifier = Mock(return_value=(""))
        login.performHttpLogin = Mock()

        (result, status) = login.login_get_verifier("some_url")

        assert (status == 303)

    def test_authorizeAndExtractVerifier_should_call_fetch_page_with_proper_data(self):
        sys.modules["__main__"].common.fetchPage.return_value = {"new_url":"some_url","status":200}
        sys.modules["__main__"].common.getParameters.return_value = {"oauth_verifier":"some_verifier"}
        login = VimeoLogin()
        login.authorizeAndExtractVerifier("some_token","some_other_token")

        data = {'token': "some_token",
                'oauth_token': "some_other_token",
                'permission': 'write',
                'accept': 'Allow'}

        sys.modules["__main__"].common.fetchPage.assert_any_call({"link":"https://vimeo.com/oauth/confirmed", "post_data":data})

    def test_authorizeAndExtractVerifier_should_call_getParameters(self):
        sys.modules["__main__"].common.fetchPage.return_value = {"new_url":"some_url","status":200}
        sys.modules["__main__"].common.getParameters.return_value = {"oauth_verifier":"some_verifier"}
        login = VimeoLogin()
        login.authorizeAndExtractVerifier("some_token","some_other_token")

        assert(sys.modules["__main__"].common.getParameters.call_count > 0)

    def test_extractLoginTokens_should_call_fetch_page(self):
        sys.modules["__main__"].common.fetchPage.return_value = {"content":"","status":200}
        sys.modules["__main__"].common.parseDOM.return_value = ""
        login = VimeoLogin()

        login.extractLoginTokens("some_link")

        sys.modules["__main__"].common.fetchPage.assert_any_call({"link":"some_link"})

    def test_extractLoginTokens_should_use_parseDOM_to_find_both_tokens(self):
        sys.modules["__main__"].common.fetchPage.return_value = {"content":"","status":200}
        sys.modules["__main__"].common.parseDOM.return_value = ""
        login = VimeoLogin()

        login.extractLoginTokens("some_link")

        assert(sys.modules["__main__"].common.parseDOM.call_count == 2)

    def test_checkIfHttpLoginFailed_should_use_parseDOM(self):
        sys.modules["__main__"].common.parseDOM.return_value = ""
        login = VimeoLogin()

        login.checkIfHttpLoginFailed({"content":"test"})

        sys.modules["__main__"].common.parseDOM.assert_any_call("test", "body", attrs={'class': 'logged_out'})

    def test_checkIfHttpLoginFailed_should_return_string_if_user_is_logged_out(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["kokok",""]
        login = VimeoLogin()

        failure = login.checkIfHttpLoginFailed({"content":"test"})

        assert (failure == "true")

    def test_performHttpLogin_should_call_fetchPage_with_proper_data(self):
        sys.modules["__main__"].settings.getSetting.side_effect = ["email", "password"]
        sys.modules["__main__"].common.fetchPage.return_value = {"content":"","status":200}
        sys.modules["__main__"].common.parseDOM.return_value = ""
        login = VimeoLogin()
        request = {'action': 'login', 
                   'service': 'vimeo',
                   'email': "email",
                   'password': "password",
                   'token': "token"}

        login.performHttpLogin("token")

        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "https://vimeo.com/log_in", "post_data": request,
                                                                  "refering": "https://www.vimeo.com/log_in"})

    def test_extractCrossSiteScriptingToken_should_call_fetchPage(self):
        sys.modules["__main__"].common.fetchPage.return_value = {"content":"","status":200}
        sys.modules["__main__"].common.parseDOM.return_value = ""
        login = VimeoLogin()

        login.extractCrossSiteScriptingToken()

        sys.modules["__main__"].common.fetchPage.assert_any_call({"link": "https://vimeo.com/log_in"})

    def test_extractCrossSiteScriptingToken_should_use_parseDOM(self):
        sys.modules["__main__"].common.fetchPage.return_value = {"content":"","status":200}
        sys.modules["__main__"].common.parseDOM.return_value = ""
        login = VimeoLogin()

        login.extractCrossSiteScriptingToken()

        assert(sys.modules["__main__"].common.parseDOM.call_count > 0)

    def test_extractCrossSiteScriptingToken_should_return_crossSiteScriptinToken(self):
        sys.modules["__main__"].common.fetchPage.return_value = {"content":"","status":200}
        sys.modules["__main__"].common.parseDOM.return_value = ["some_token"]
        login = VimeoLogin()

        result = login.extractCrossSiteScriptingToken()

        assert(result == ["some_token"])

    def test_extractUserId_should_use_parseDOM(self):
        sys.modules["__main__"].common.parseDOM.return_value = ["some_token"]
        login = VimeoLogin()

        login.extractUserId({"content":"smokey"})

        assert (sys.modules["__main__"].common.parseDOM.call_count > 0)

    def test_extractUserId_should_find_user_id_as_first_element(self):
        sys.modules["__main__"].common.parseDOM.return_value = ["some_user_id","some_token","some_other_token"]
        login = VimeoLogin()

        result = login.extractUserId({"content":"smokey"})

        assert (result == "some_user_id")

    def test_extractUserId_should_return_empty_string_if_user_id_isnt_found(self):
        sys.modules["__main__"].common.parseDOM.return_value = []
        login = VimeoLogin()

        result = login.extractUserId({"content":"smokey"})

        assert (result == "")
if __name__ == '__main__':
    nose.runmodule()
