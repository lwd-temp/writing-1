#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import cached_url
import yaml

def getContent(url):
	content = cached_url.get(url)
	content = yaml.load(content, Loader=yaml.FullLoader)
	b = BeautifulSoup(content['content'], 'html.parser')
	b.get_text(separator="\n")
	next_url = None
	for x in b.find_all('a'):
		if x['href'] and x['href'].startswith('https://www.evernote.com/l'):
			next_url = x['href']
			break
	return b.get_text(separator="\n"), content['title'], next_url


def download(url):
	filename = None
	content = []
	while url:
		text, title, url = getContent(url + '?json=1')
		if not filename:
			filename = title
		content.append(text)
		with open(filename, 'w') as f:
			f.write('\n\n=======\n\n'.join(content))

download('https://www.evernote.com/l/AO9Nsp2x2-5LBJCMbJvjQNK6zjezsttrIPw')