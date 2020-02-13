#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import cached_url

def getContent(url):
	content = cached_url.get(url)
	b = BeautifulSoup(content, 'html.parser')
	text = b.find('div', {'id': 'container'}).text
	title = b.find('h1').text
	next_url = None
	for x in b.find_all('a'):
		if x.href and x.href.startsWith('https://www.evernote.com/l'):
			next_url = x.href
			break
	return text, title, next_url


def download(url):
	filename = None
	content = []
	while url:
		text, title, url = getContent(url)
		if not filename:
			filename = title
		content.append(text)
		with open(filename, 'w') as f:
			f.write('\n\n=======\n\n'.join(content))

download('https://www.evernote.com/l/AO9Nsp2x2-5LBJCMbJvjQNK6zjezsttrIPw')