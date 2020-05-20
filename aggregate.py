#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import cached_url
import yaml
import datetime
import sys
import os
from telegram_util import compactText
from opencc import OpenCC
cc = OpenCC('s2tw')

def clearText(content):
	for key in ['next', 'Next', 'previous', 'Previous']:
		content = content.split(key)[0]	
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
	return compactText(content)

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
		x.replace_with(x.text + '\n\n')
	for x in b.find_all('br'):
		x.replace_with('\n\n')
	text = compactText(b.text.replace('~', '.'))
	return clearText(text), content['title'], next_url, text

def getTime():
	return datetime.datetime.now().strftime("%m/%d %H:%M")

def countWord(x):
	return len([c for c in x if c.isalpha() and ord(c) > 255])

def mkdirs(*args):
	for arg in args:
		os.system('mkdir %s > /dev/null 2>&1' % arg)

def download(filename = None, url = None, dirname = 'original'):
	content = [] # no chapter name, no comments
	result = [] # with chapter name, no comments
	raw_result = [] # with chapter name and comments
	while url:
		text, title, url, raw_text = getContent(url + '?json=1')
		if not filename:
			filename = title
			if '大纲' in filename:
				dirname = 'other'
		content.append(text)
		result.append('\n\n\n==== %s  ===\n\n\n' % title + text)
		raw_result.append('\n\n\n==== %s  ===\n\n\n' % title + raw_text)
	result = clearText(''.join(result))
	mkdirs(dirname, 'txt', 'traditional', 'raw')
	with open('%s/%s.md' % (dirname, filename), 'w') as f:
		f.write(result)
	with open('txt/%s.txt' % filename, 'w') as f:
		f.write(result)
	with open('traditional/%s.md' % cc.convert(filename), 'w') as f:
		f.write(cc.convert(result))
	with open('raw/%s.md' % filename, 'w') as f:
		f.write(''.join(raw_result))
	return content, dirname, filename

def process():
	word_count = 0
	result = [
		download('学霸要同我困觉', url = 'https://www.evernote.com/l/AO-wRhOju25ISYFo1zTtJkbB_ngPEfsEm6U'),
		download('我喜欢的Omega要上我', url = 'https://www.evernote.com/l/AO_feS-OQUdCELC_K55hc4B_iQ7cq2SwAMc'),
		download('城市的另一边', url = 'https://www.evernote.com/l/AO_672HguTBASYJX8xYB_wpilOnLu0pXfZY'),
		download('Telegram群组推荐', url = 'https://www.evernote.com/l/AO9NCICZw1JOoL80CKiBuaKkfpdzSA8wRkw', dirname = 'other'),
		download('穿越进黄文我不知所措', url = 'https://www.evernote.com/l/AO_jZ8RzOtpAGLoLisqlnc2KGuQyM0thtGY'),
		download('面向对象编程', url = 'https://www.evernote.com/l/AO9AYm5PtJtHIZb5W7RvOFPjNGxENZ9uQiI'),
		download('乐山景然ABO', url = 'https://www.evernote.com/l/AO9Nsp2x2-5LBJCMbJvjQNK6zjezsttrIPw'),
		download('学术生涯篇', url = 'https://www.evernote.com/l/AO8Z7ocFEpJJjatcpUFs4oyx1F7g9knqfPA', dirname = 'other'),
		download('穿越阵容有点大', url = 'https://www.evernote.com/l/AO9X4c31vqVPE5Vs0fHDaQ3INH9qfsne36s'),
		download('三界', url = 'https://www.evernote.com/l/AO8FA3cJQNxEvo5QuwX6vu6GI3n9_KjoRFg'),
		download('我家是个妖精窝？', url = 'https://www.evernote.com/l/AO-WkVchLy9OGrNULCWHoJ23CC6K8kw8CDQ'),
		download('江南台T城', url = 'https://www.evernote.com/l/AO84Q8Hc-mhJ6YNbUdtypUBDPpIeT-ZW73g'),
		download(url = 'https://www.evernote.com/l/AO_odyI4w7xEj4MmiBa8PLBiDju8GIuJsI0', dirname = 'critics'),
		download(url = 'https://www.evernote.com/l/AO_WUvEn1eZPP4iUJb1QI6fOlxuvo9TpaPE', dirname = 'critics'),
		download(url = 'https://www.evernote.com/l/AO_dG7QCcrREsr-VjZ5QUJ02Riuk1GzXSNk', dirname = 'critics'),
		download(url = 'https://www.evernote.com/l/AO_jic8bMCVBw7ylY8987nTR0rE8TENbbrc', dirname = 'other'),
		download(url = 'https://www.evernote.com/l/AO_aeRztT0BOsrziVg2JkOguEXPdXd1g1oQ', dirname = 'other'),
		download(url = 'https://www.evernote.com/l/AO8Kzrbwz3RFMaBNpVHK761skS4nm3LbD1Y', dirname = 'other'),
		download(url = 'https://www.evernote.com/l/AO_c2o2SX7NCUJkHIkCzX70YOBMrS_3VeCM', dirname = 'other'),
	]

	result = [([countWord(chapter) for chapter in x[0]], 
		x[1], x[2]) for x in result]

	with open('other/word_count_detail.txt', 'w') as f:
		for sub_word_count, filename, dirname in result:
			if '大纲' not in filename:
				f.write('%s %d %s\n' % (filename, sum(sub_word_count), str(sub_word_count)))

	if 'notail' not in sys.argv:
		total_words = sum([sum(x[0]) for x in result 
			if x[1] in ['original', 'critics']])
		with open('other/word_count_history.txt', 'a') as f:
			f.write('%s\t\t%d\n' % (getTime(), total_words))

	command = 'git add . && git commit -m "%s" && git push -u -f'
	if len(sys.argv) > 1:
		message = sys.argv[1]
	else:
		message = 'commit'
	if message == 'notail':
		message = 'auto_commit'
	os.system(command % message)

if __name__ == '__main__':
	process()