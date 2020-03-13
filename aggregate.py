#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import cached_url
import yaml
import datetime
import sys
import os
from telegram_util import cleanFileName

def getContent(url):
	content = cached_url.get(url)
	content = yaml.load(content, Loader=yaml.FullLoader)
	b = BeautifulSoup(content['content'], 'html.parser')
	with open('html/' + cleanFileName(content['title']) + '.html', 'w') as f:
		f.write(content['content'])
	with open('html/' + cleanFileName(content['title']) + '.json', 'w') as f:
		f.write(str(content))
	next_url = None
	for x in b.find_all('a'):
		if x['href'] and x['href'].startswith('https://www.evernote.com/l'):
			next_url = x['href']
			break
	return b.get_text(separator="\n\n"), content['title'], next_url

def getTime():
	return datetime.datetime.now().strftime("%m/%d %H:%M")

def countWord(x):
	return len([c for c in x if c.isalpha() and ord(c) > 255])

def download(url, filename = None):
	global word_count
	content = []
	result = []
	while url:
		text, title, url = getContent(url + '?json=1')
		if not filename:
			filename = title
		content.append(text)
		result.append('\n\n\n==== %s  ===\n\n\n' % title + text)
	with open(filename, 'w') as f:
		f.write(''.join(result))
	word_count += sum([countWord(x) for x in content])

def downloadDoc(url, filename):
	content = cached_url.get(url)
	with open('html/' + filename + '.pdf', 'w') as f:
		f.write(content)

word_count = 0
# download('https://www.evernote.com/l/AO9AYm5PtJtHIZb5W7RvOFPjNGxENZ9uQiI', '面向对象编程')
# download('https://www.evernote.com/l/AO9Nsp2x2-5LBJCMbJvjQNK6zjezsttrIPw', '乐山景然ABO')
# download('https://www.evernote.com/l/AO8Z7ocFEpJJjatcpUFs4oyx1F7g9knqfPA', '学术生涯篇')
# download('https://www.evernote.com/l/AO9X4c31vqVPE5Vs0fHDaQ3INH9qfsne36s', '穿越阵容有点大')
# download('https://www.evernote.com/l/AO8FA3cJQNxEvo5QuwX6vu6GI3n9_KjoRFg', '三界')
downloadDoc('https://docs.google.com/document/export?format=pdf&id=1gB1hxccoplM1UOJue4DW0HNIgm4Ve1karRmy4zpZ3o8&includes_info_params=true', '妓女的荣耀')
with open('word_count.txt', 'a') as f:
	f.write('%s\t\t%d\n' % (getTime(), word_count))
command = 'git add . && git commit -m "%s" && git push -u -f'
if len(sys.argv) > 1:
	message = sys.argv[1]
else:
	message = 'commit'
os.system(command % message)