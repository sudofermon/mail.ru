import requests
import sys
import  random
import string

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','DNT': '1',
           'Upgrade-Insecure-Requests': '1'}
marker1 = '''qc-login-row " onclick="return {'type': 'Login'};">'''
marker2 = '" class="flr years mt0 mb0 qc-select-year"'
marker3 = '<input type="hidden" name="x_reg_id" value="'
marker4 = '" class="fll days mt0 mb0 qc-select-day"'
marker5 = '<label class="sig1" for="'
marker6 = 'qc-lastname-row " onclick="return {};">'
marker7 = '<input type="radio" class="vtm" name="'
marker9 = '''qc-login-row " onclick="return {'type': 'Login'}'''
marker10 = '''qc-pass-row " onclick="return {'type': 'Password'};"'''
marker11 = 'qc-passverify-row " id="signRePassword"'
marker12 = '<input type="hidden" name="ID" value="'
marker13 = '''qc-mail-row" onclick="return {'type': 'Email', 'noreq': true}'''
marker14 = 'class="inPut form__captcha-old__input" type="text" name="'
m_select = '<select name="'
m_label = '<label for="'

reg_name = input('First name: ')[1]
reg_last_name = input('Last name: ')
[2]
reg_birth_year = random.randint(1980, 1992)
reg_birth_month = random.randint(1, 12)
reg_birth_day = random.randint(1, 28)
reg_sex = 1
reg_password = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(15)])
cookies = {}
resp = requests.get('https://e.mail.ru/signup?from=main_noc', headers=headers)
cookies['mrcu'] = resp.cookies['mrcu']
html = resp.content.decode('utf-8')

sig1 = html.split(marker1)[1].split(m_label)[1].split('"')[0]
sig_year = html.split(marker2)[0].split(m_select)[-1]
x_reg_id = html.split(marker3)[1].split('"')[0]
sig_day = html.split(marker4)[0].split(m_select)[-1]
sig_name = html.split(marker5)[1].split('"')[0]
sig_last_name = html.split(marker6)[1].split(m_label)[1].split('"')[0]
sig_sex = html.split(marker7)[1].split('"')[0]
sig_mailbox = html.split(marker9)[1].split(m_label)[1].split('"')[0]
sig_password = html.split(marker10)[1].split(m_label)[1].split('"')[0]
sig_password_retype = html.split(marker11)[1].split(m_label)[1].split('"')[0]
sig_alt_email = html.split(marker13)[1].split(m_label)[1].split('"')[0]
sig_captcha = html.split(marker14)[1].split('"')[0]
captcha_url = 'https://c.mail.ru/' + html.split('<img src="//c.mail.ru/')[1].split('"')[0]
reg_id = html.split(marker12)[1].split('"')[0]

print('Sig1: {}\nReg id: {}\nSig year: {}\nSig birth day: {}\nSig name: {}\nSig last name: {}\nSig sex: {}'
      '\nSig mailbox: {}\nSig password: {}\nSig password retype: {}\nSig alt email: {}\nSig captcha: {}\n'
      'Captcha url: {}\nID: {}'
      .format(sig1, x_reg_id, sig_year, sig_day, sig_name, sig_last_name, sig_sex, sig_mailbox, sig_password,
              sig_password_retype, sig_alt_email, sig_captcha, captcha_url, reg_id))

post_data = {'RegistrationDomain': 'mail.ru', 'Signup_utf8': '1', 'LANG': 'en_US', sig1: '', 'x_reg_id': x_reg_id,
             sig_year: reg_birth_year, 'BirthMonth': reg_birth_month, sig_day: reg_birth_day, sig_name: reg_name,
             sig_last_name: reg_last_name, sig_sex: reg_sex}
resp = requests.post('https://e.mail.ru/cgi-bin/checklogin', data=post_data, headers=headers, cookies=cookies)
resp = resp.content.decode('utf-8')
emails = resp.split('\n')
if '@' in resp:
    print('\nPossible emails for {} {}:'.format(reg_name, reg_last_name))
    for i in range(len(emails[1:])):
        print(str(i + 1) + '.', emails[1:][i])
else:
    print(resp)
    print('Error')
    exit()
emails = emails[1:]
chosen_email = emails[int(input('Choose email: ')) - 1].split('@')
email_name = chosen_email[0]
email_domain = chosen_email[1]

with open('captcha.jpg', 'wb') as f:
    f.write(requests.get(captcha_url, headers=headers, cookies=cookies).content)
captcha_text = input('Captcha from captcha.jpg: ')

headers['Referer'] = 'https://e.mail.ru/signup?from=main_noc'
register_data = {'signup_b': '1', 'sms': '1', 'no_mobile': '0', 'Signup_utf8': '1', 'LANG': 'en_US', 'ID': reg_id,
                 'Count': '1', 'back': '', 'Mrim.Country': '0', 'Mrim.Region': '0', 'x_reg_id': x_reg_id,
                 'security_image_id': '', 'geo_countryId': 'undefined', 'geo_cityId': 'undefined',
                 'geo_regionId': 'undefined', 'geo_country': '', 'geo_place': '', 'lang': 'en_US', 'new_captcha': '1',
                 sig_name: reg_name, sig_last_name: reg_last_name, sig_day: reg_birth_day,
                 'BirthMonth': reg_birth_month, sig_year: reg_birth_year, sig_mailbox: email_name,
                 'RegistrationDomain': email_domain, sig_password: reg_password, sig_password_retype: reg_password,
                 'SelectPhoneCode': '7', 'RemindPhone': '', 'RemindPhoneCode': '7', sig_alt_email: '',
                 sig_captcha: captcha_text, sig_sex: reg_sex}
resp = requests.post('https://e.mail.ru/reg?from=main_noc', data=register_data, headers=headers, cookies=cookies,
                     allow_redirects=False)
html = resp.content.decode('utf-8')
if 'The code was entered incorrectly.' in html:
    print('Incorrect captcha')
    exit()
if 'Phone number not confirmed' in html:
    print('Phone number requested, try another ip')
    exit()
redirect_url = resp.headers['Location']
resp = requests.get(redirect_url, headers=headers, cookies=cookies, allow_redirects=False)
print('Account registered\n', '@'.join(chosen_email), reg_password + '\nMpop:', resp.cookies['Mpop'])
