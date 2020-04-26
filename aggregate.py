#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import cached_url
import yaml
import datetime
import sys
import os
from telegram_util import cleanFileName, compactText
import requests
from PIL import Image
from opencc import OpenCC
cc = OpenCC('s2tw')

def clearText(content):
	content = content.split('next')[0]
	content = content.split('Next')[0]
	result = []
	in_comment = False
	for x in content:
		if x == '【':
			in_comment = True
		if x == '】':
			in_comment = False
			continue
		if not in_comment:
			result.append(x)
	content = ''.join(result)
	return compactText(content).replace('~', '.')

def getContent(url):
	content = cached_url.get(url)
	content = yaml.load(content, Loader=yaml.FullLoader)
	b = BeautifulSoup(content['content'], 'html.parser')
	next_url = None
	for x in b.find_all('a'):
		if x['href'] and x['href'].startswith('https://www.evernote.com/l'):
			next_url = x['href']
			break
	for x in b.find_all('span'):
		replace = x.text
		if 'bold' in str(x.attrs):
			x.replace_with('**%s**' % replace)
		else:
			x.replace_with(replace)
	for x in b.find_all('div'):
		x.replace_with(x.text + '\n')
	for x in b.find_all('br'):
		x.replace_with('\n')
	return clearText(b.text), content['title'], next_url, b.text

def getTime():
	return datetime.datetime.now().strftime("%m/%d %H:%M")

def countWord(x):
	return len([c for c in x if c.isalpha() and ord(c) > 255])

def download(url, filename = None):
	global word_count
	content = []
	result = []
	raw_result = []
	words = []
	while url:
		text, title, url, raw_text = getContent(url + '?json=1')
		if not filename:
			filename = title
		content.append(text)
		result.append('\n\n\n==== %s  ===\n\n\n' % title + text)
		raw_result.append('\n\n\n==== %s  ===\n\n\n' % title + raw_text)
		words.append(countWord(text))
	result = clearText(''.join(result))
	with open('original/%s.md' % filename, 'w') as f:
		f.write(result)
	with open('traditional/%s.md' % cc.convert(filename), 'w') as f:
		f.write(cc.convert(result))
	old_result = ''
	try:
		with open('raw/%s.md' % filename) as f:
			old_result = f.read()
	except:
		pass
	with open('raw/%s.md' % filename, 'w') as f:
		f.write(''.join(raw_result))
	if old_result != ''.join(raw_result):
		print(filename, words, sum(words))
	word_count += sum(words)

def downloadDoc(url, filename):
	content = requests.get(url)
	os.system('mkdir html/' + filename)
	zip_name = 'html/' + filename + '/tmp.zip'
	with open(zip_name, 'wb') as f:
		f.write(content.content)
	os.system('cd html/%s && unzip -o tmp.zip' % filename)
	dname = 'html/%s/images/' % filename
	for f in os.listdir(dname):
		try:
			im = Image.open(dname + f)
			im.save(dname + f, dpi=(150,150))
		except:
			pass
	os.system('rm %s' % zip_name)

word_count = 0
download('https://www.evernote.com/l/AO_672HguTBASYJX8xYB_wpilOnLu0pXfZY', '城市的另一边')
download('https://www.evernote.com/l/AO9NCICZw1JOoL80CKiBuaKkfpdzSA8wRkw', 'Telegram群组推荐')
download('https://www.evernote.com/l/AO_jZ8RzOtpAGLoLisqlnc2KGuQyM0thtGY', '穿越进黄文我不知所措')
download('https://www.evernote.com/l/AO9AYm5PtJtHIZb5W7RvOFPjNGxENZ9uQiI', '面向对象编程')
download('https://www.evernote.com/l/AO9Nsp2x2-5LBJCMbJvjQNK6zjezsttrIPw', '乐山景然ABO')
download('https://www.evernote.com/l/AO8Z7ocFEpJJjatcpUFs4oyx1F7g9knqfPA', '学术生涯篇')
download('https://www.evernote.com/l/AO9X4c31vqVPE5Vs0fHDaQ3INH9qfsne36s', '穿越阵容有点大')
download('https://www.evernote.com/l/AO8FA3cJQNxEvo5QuwX6vu6GI3n9_KjoRFg', '三界')
download('https://www.evernote.com/l/AO-WkVchLy9OGrNULCWHoJ23CC6K8kw8CDQ', '我家是个妖精窝？')
download('https://www.evernote.com/l/AO84Q8Hc-mhJ6YNbUdtypUBDPpIeT-ZW73g', '江南台T城')
download('https://www.evernote.com/l/AO_odyI4w7xEj4MmiBa8PLBiDju8GIuJsI0')
download('https://www.evernote.com/l/AO_WUvEn1eZPP4iUJb1QI6fOlxuvo9TpaPE')
download('https://www.evernote.com/l/AO_dG7QCcrREsr-VjZ5QUJ02Riuk1GzXSNk')
download('https://www.evernote.com/l/AO_jic8bMCVBw7ylY8987nTR0rE8TENbbrc')

if 'notail' not in sys.argv:
	with open('word_count.txt', 'a') as f:
		f.write('%s\t\t%d\n' % (getTime(), word_count))
command = 'git add . && git commit -m "%s" && git push -u -f'
if len(sys.argv) > 1:
	message = sys.argv[1]
else:
	message = 'commit'
os.system(command % message)