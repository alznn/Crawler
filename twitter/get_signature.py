import os
import sys
import unittest
import time
import json
import urllib.request
import urllib.parse
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from auth import OAuthSignature
from urllib.parse import urlencode


class SignatureGenerateTests(unittest.TestCase):

    def testUrl(self):
        """Base.  Is URL empty"""

        oauthCtrl = OAuthSignature()
        self.assertEqual(oauthCtrl.url, '')

    def testConsumerKey(self):
        """Base.  Is Token  empty"""

        oauthCtrl = OAuthSignature()
        self.assertEqual(oauthCtrl.secrets.get('consumer_secret'), '')

    def testTokenKey(self):
        """Base. Is Token  empty"""
        oauthCtrl = OAuthSignature()
        self.assertEqual(oauthCtrl.secrets.get('token_secret'), '')

    def testEncode(self):
        """Base. Encode gaps"""
        oauthCtrl = OAuthSignature()
        self.assertNotEqual(oauthCtrl.encode("from:twitter #auth"), 'from%3Atwitter+%23auth')

    # def testSignatureGenerate(self):
    #     """ Generate signature. The signature length 28 """
    #
    #     oauthCtrl = OAuthSignature()
    #     oauthCtrl.url = 'https://api.twitter.com/1.1/statuses/update.json'
    #     oauthCtrl.secrets = {
    #         'consumer_secret': "",
    #         'token_secret': ''
    #     }
    #
    #     params = {
    #         'oauth_version': '1.0',
    #         'oauth_consumer_key': "",
    #         'oauth_token': "",
    #         'oauth_timestamp': int(time.time()),
    #         'oauth_signature_method': 'HMAC-SHA1',
    #         'oauth_nonce': oauthCtrl.nonce()
    #     }
    #
    #     self.assertEqual(len(oauthCtrl.generate(params)), 28)
    #
    # def testDistinctionSignatures(self):
    #     """ Generate two different singatures with same parameters"""
    #
    #     oauthCtrl = OAuthSignature()
    #     oauthCtrl.url = 'https://api.twitter.com/1.1/statuses/update.json'
    #     oauthCtrl.secrets = {
    #         'consumer_secret': "",
    #         'token_secret': ''
    #     }
    #
    #     params1 = {
    #         'oauth_version': '1.0',
    #         'oauth_consumer_key': "",
    #         'oauth_token': "",
    #         'oauth_timestamp': int(time.time()),
    #         'oauth_signature_method': 'HMAC-SHA1',
    #         'oauth_nonce': oauthCtrl.nonce()
    #     }
    #
    #     params2 = {
    #         'oauth_version': '1.0',
    #         'oauth_consumer_key': "",
    #         'oauth_token': "",
    #         'oauth_timestamp': int(time.time()),
    #         'oauth_signature_method': 'HMAC-SHA1',
    #         'oauth_nonce': oauthCtrl.nonce()
    #     }
    #
    #     self.assertNotEqual(oauthCtrl.generate(params1), oauthCtrl.generate(params2))

    def testTwitterRequest(self):
        """Get a twitter record"""
        oauthCtrl = OAuthSignature()
        oauthCtrl.url = 'https://api.twitter.com/1.1/statuses/update.json'
        oauthCtrl.secrets = {
            'consumer_secret': "",
            'token_secret': ''
        }

        #
        urlParams = {
            'count': 1,
            'exclude_replies': 1
        }
        # params for signature
        params = {
            'oauth_version': '1.0',
            'oauth_consumer_key': "",
            'oauth_token': "",
            'oauth_timestamp': int(time.time()),
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_nonce': oauthCtrl.nonce()
        }
        # add url params
        params.update(urlParams)
        # generate signature
        params['oauth_signature'] = oauthCtrl.generate(params)

        # convert params to string for Authorization header
        params_str = ",".join(['%s="%s"' % (k, oauthCtrl.encode(params[k])) for k in sorted(params)])

        headers = {
            'Authorization': 'OAuth realm="%s", %s ' % (oauthCtrl.url, params_str)
        }
        # full link with url parameters
        fullURL = oauthCtrl.url + "?" + urlencode(urlParams)
        # add request object params
        req = urllib.request.Request(fullURL, headers=headers)
        # make request
        response = urllib.request.urlopen(req)
        # response -> json
        result = json.loads(response.read())

        self.assertTrue(len(result) > 0)

if __name__ == '__main__':
    unittest.main()