from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import zipfile,os
from names import *
import random


def proxy_chrome(PROXY_HOST,PROXY_PORT,PROXY_USER,PROXY_PASS):
    manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%(host)s",
                port: parseInt(%(port)d)
              },
              bypassList: ["foobar.com"]
            }
          };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%(user)s",
                password: "%(pass)s"
            }
        };
    }
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
        """ % {
            "host": PROXY_HOST,
            "port": PROXY_PORT,
            "user": PROXY_USER,
            "pass": PROXY_PASS,
        }


    pluginfile = 'extension/proxy_auth_plugin.zip'

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    co = Options()
    #extension support is not possible in incognito mode for now
    #co.add_argument('--incognito')
    co.add_argument('--disable-gpu')
    #disable infobars
    co.add_argument('--disable-infobars')
    co.add_argument("--no-sandbox")
    co.add_argument("--disable-dev-shm-usage")
    co.add_argument("user-agent=whatever you want")
    #co.add_argument("--headless=new")
    co.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    #location of chromedriver, please change it according to your project.
    chromedriver = os.getcwd()+'/Chromedriver/chromedriver'
    #chromedriver = '/Users/venksta/PycharmProjects/teslavote/venv/lib/python3.9/site-packages/selenium/webdriver/chrome'
    co.add_extension(pluginfile)
    #driver = webdriver.Remote("http://localhost:4444", options=co)
    driver = webdriver.Remote("http://selserver:4444", options=co)
    #return the driver with added proxy configuration.
    return driver


def get_random_ua():
    # Combine the two lists
    combined = user_agents_desktop + user_agents_mobile

    # Select a random entry from the combined list
    random_ua = random.choice(combined)

    # Return the 'ua' value of the selected entry
    return random_ua['ua']
