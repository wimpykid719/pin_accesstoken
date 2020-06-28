import urllib.parse
import json
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

#サーバの認識するブラウザ情報
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
headers = {'User-Agent': ua}

#seleniumを使用する準備
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome('selenium/chromedriver', options=options)


login_url = 'https://accounts.pinterest.com/v3/login/handshake/'
userdata = {'username_or_email':'xxx', 'password':'xxx'}#pinterestのログインする。メール・パスワード

authorization_url = 'https://api.pinterest.com/oauth/'

payload = '?response_type=code&client_id=xxx&redirect_uri=https://0.0.0.0:9000/callbackpage&scope=read_public,write_public,read_relationships,write_relationships' # client_idはディベロッパーのページから手動で取得する

access_token_url = 'https://api.pinterest.com/v1/oauth/token'
payload2 = {'grant_type': 'authorization_code',\
            'client_id': 'xxx',\
            'client_secret':'xxx',\
            'code': '0'}# client_secretも同様にディベロッパーページから取得

def get_code():
    with requests.Session() as s:
        cookiesdata = []
        p = s.post(login_url, params=userdata)
        cookiesdata = s.cookies
        cookiesdict = cookiesdata.get_dict()
        ses = cookiesdict["_pinterest_sess"]
        # print(ses)

    driver.delete_all_cookies()
    driver.get('https://accounts-oauth.pinterest.com/login/')
    #ここもう一回確認しないと
    ses = {'name':"_pinterest_sess", 'value':ses, 'domain':".pinterest.com"}
    driver.add_cookie(ses)
    # print(driver.get_cookies())
    print('セッション移行done')
    #URLが変わるからcookieが変わってしまう？？
    #ここでクリックが必要なページになる。
    authorizationurlpayload = authorization_url + payload
    
    driver.get(authorizationurlpayload)
    print('アクセスdone')
    
    # 認証を承認する
    driver.find_element_by_xpath('//*[@id="dialog_footer"]/button[2]').click()
    print(driver.page_source)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    code = soup.body
    driver.quit()
    return code

payload2['code'] = get_code()
token = requests.post(access_token_url , params=payload2)
token = token.json()
access_token = token['access_token']
print(access_token)

# 結果 {"access_token": "ここにアクセストークンが返ってきます。", "token_type": "bearer", "scope": ["read_write_all", "read_public", "write_public", "read_private", "write_private", "read_relationships", "write_relationships"]}

