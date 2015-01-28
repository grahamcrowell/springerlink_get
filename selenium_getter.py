from selenium import webdriver
import os, http.cookiejar, urllib.request, http.cookies

browser = webdriver.Firefox()
springer_link_login = r'https://login.ezproxy.library.ubc.ca/login?auth=shibboleth&url=http://link.springer.com/'
browser.get(springer_link_login)

username = browser.find_element_by_name('j_username')
username.send_keys('gcrowell')

password = browser.find_element_by_name('j_password')
password.send_keys('2AND2is5!')

form = browser.find_element_by_name('action')
form.submit()

cookies = browser.get_cookies()
print('Cookies are dicts')
b = browser
# params = ['version', 'name', 'value', 'port', 'port_specified', 'domain', 'domain_specified', 'domain_initial_dot', 'path', 'path_specified', 'secure', 'expires', 'discard', 'comment', 'comment_url', 'rest', 'rfc2109']
params = ['version', 'name', 'value', 'port', 'port_specified', 'domain', 'domain_specified', 'domain_initial_dot', 'path', 'path_specified', 'secure', 'expires', 'comment_url', 'rest', 'rfc2109']
cj = http.cookiejar.CookieJar()

book_url = r'http://link.springer.com.ezproxy.library.ubc.ca/content/pdf/10.1007%2F978-3-642-33590-7.pdf'
# book_url = r'http://real-chart.finance.yahoo.com/table.csv?s=AAPL&d=11&e=12&f=2014&g=d&a=11&b=12&c=1980&ignore=.csv'
# r = opener.open(book_url)
C = b.get_cookies()
# for c in C:
	# for p in params:
		# if p not in c:
			# c[p] = None
	# ck = http.cookies.SimpleCookie(c['version'], c['name'], c['value'], c['port'], c['port_specified'], c['domain'], c['domain_specified'], c['domain_initial_dot'], c['path'], c['path_specified'], c['secure'], c['expires'], c['discard'], c['comment'], c['comment_url'], c['rest'], c['rfc2109'])
	# cj.set_cookie(ck)
# book_url = r'http://download.springer.com.ezproxy.library.ubc.ca/static/pdf/312/bok%253A978-1-4471-4835-7.pdf?auth66=1418756584_758c19ed9cde401f32172fb574e685fa&ext=.pdf'
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
r = opener.open(book_url)
os.chdir('c:/users/graham/desktop/')
file = open('c:/users/graham/desktop/text.pdf','wb')
file.write(r)
file.close()
cj.save(ignore_discard=True)
