import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class InstagramScrap():
    
    def __init__(self, username, password):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options=options)
        self.username = username
        self.password = password

    # We need to authorize, otherwise bot would be redirected to login page (even for public profiles)
    def auth(self):
        self.browser.get('https://www.instagram.com/accounts/login/')

        username_input = self.browser.find_elements_by_css_selector('form input')[0]
        password_input = self.browser.find_elements_by_css_selector('form input')[1]

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(2)

    def get_followers_count(self, username):
        user_url = 'https://www.instagram.com/' + username
        
        if self.browser.current_url != user_url:
            self.browser.get(user_url)

        followers = self.browser.find_element_by_css_selector('ul li a span')
        return followers.text
  

    def get_user_followers(self, username, max):
        self.browser.get('https://www.instagram.com/' + username)
        followers_link = self.browser.find_element_by_css_selector('ul li a')
        followers_link.click()
        time.sleep(2)
        followers_list = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        number_of_followers_in_list = len(followers_list.find_elements_by_css_selector('li'))

        followers_list.click()
        followers = []
        action_chain = webdriver.ActionChains(self.browser)
        while (number_of_followers_in_list < max):
            action_chain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            number_of_followers_in_list += len(followers_list.find_elements_by_css_selector('li'))
            followers += followers_list.find_elements_by_css_selector('li')
            print(number_of_followers_in_list)

        follower_usernames = []

        for user in followers:
            # Some user tends to have unclickable avatar, thus we need to catch those scenarios
            try:
                username = user.find_elements_by_css_selector('a')[1].text
            except IndexError:
                username = user.find_element_by_css_selector('a').text
            #print(userlink)
            follower_usernames.append(username)
            if (len(follower_usernames) == max):
                break
        return follower_usernames

    def close_browser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_browser()

bot = InstagramScrap('andreysumko', 'ght3thdfnbd')
bot.auth()
followers = bot.get_user_followers('shaiworth', 20)


for follower in followers:
    print(follower + ' with ' + bot.get_followers_count(follower) + ' followers')