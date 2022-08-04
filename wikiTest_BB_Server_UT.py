from appium import webdriver
import time
import unittest
import requests

class BasicTest(unittest.TestCase):
    def setUp(self):

        # Put your username and authey below
        # You can find your authkey at crossbrowsertesting.com/account
        self.username = ""
        self.authkey  = ""

        self.api_session = requests.Session()
        self.api_session.auth = (self.username,self.authkey)

        self.test_result = None

        capabilities = {
        'bitbar_apiKey': '',
        'bitbar_device': 'Google Pixel 3 XL -US',
        'bitbar_app': '163292258',
        'platformName': 'Android',
        'deviceName': 'Android Phone',
        'automationName': 'Appium',
        'bitbar_project': 'Wiki Testing',
        'bitbar_testrun': 'First One',
        "automationName": "UiAutomator2",
        "appActivity": "org.wikipedia.main.MainActivity",
        "noReset": "true",
        "appPackage": "org.wikipedia"
    }

    #     capabilities = {
    #         "platformName": "android",
    #         #"deviceName": "emulator-5554",
    #         "deviceName": "520083e9c0fd9587",
    #         "automationName": "UiAutomator2",
    #         "appActivity": "org.wikipedia.main.MainActivity",
    #         "noReset": "true",
    #         "appPackage": "org.wikipedia"
    # }
        # start the remote browser on our server
        #self.driver = webdriver.Remote("https://us-west-mobile-hub.bitbar.com/wd/hub", capabilities)
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(20)

    def test_WIKI(self):
        # We wrap this all in a try/except so we can set pass/fail at the end
        try:
            # we need to reset our app to replicate testing on a fresh BB device
            # only for local operation
            #self.driver.reset()

            # let's hit the skip button for selecting language and setting up the app
            self.driver.find_element_by_id('org.wikipedia:id/fragment_onboarding_skip_button').click()
            
            time.sleep(5)

            # click in the search field            
            self.driver.find_element_by_id('org.wikipedia:id/search_container').click()
            # enter SmartBear in the search field
            self.driver.find_element_by_id('org.wikipedia:id/search_src_text').send_keys("SmartBear")
            
            time.sleep(5)
            
            # this is the search term description we are looking for
            searchTermVerify = "American information technology company"
            # instanitation of our placeholder var for the search term description.
            searchDescription = ""
            # return the search term description of the first result, which should be SmartBear.
            Description = self.driver.find_elements_by_id('org.wikipedia:id/page_list_item_description')
            # search through all the terms, but we are stopping on the first one.
            for value in Description:
                searchDescription = str(value.text)
                searchDescription = searchDescription.replace(u'\xa0', u' ')
                print("searchDescription = ", searchDescription)
                break

            if searchDescription == searchTermVerify:
                print("title matches!")
            else:
                print("title does not match!")

            #assert searchDescription == searchTermVerify
            

            print('Checking Search Description')
            self.assertEqual("American information technology company", searchDescription)

            # if we are still in the try block after all of our assertions that 
            # means our test has had no failures, so we set the status to "pass"
            #self.test_result = 'pass'

        except AssertionError as e:

            # if any assertions are false, we take a snapshot of the screen, log 
            # the error message, and set the score to "during tearDown()".
            self.driver.quit()
            raise

    def tearDown(self):
        print("Done with session %s" % self.driver.session_id)
        self.driver.quit()
    
        


if __name__ == '__main__':
    unittest.main()