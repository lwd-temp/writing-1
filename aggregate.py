#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import cached_url
import yaml
import datetime
import sys
import os
from telegram_util import compactText, matchKey
from opencc import OpenCC
cc = OpenCC('s2tw')
from util import commit
from note import Note

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

def processNote(url, title, series):
	root_note = Note(url)
	if root_note.isNewFormat():
		notes = [ Note(url) for url in root_note.evernote_urls]
		for url in root_note.evernote_urls:
			note = Note(url)
			content.append(text)
			result.append('\n\n\n==== %s  ===\n\n\n' % title + text)
			raw_result.append('\n\n\n==== %s  ===\n\n\n' % title + raw_text)
		result = clearText(''.join(result))
	# 判断format


def process(root_url):
	os.system('rm other/word_count_detail.txt')

	note = Note(root_url)
	series = None
	for item in note.soup.find_all('div'):
		if item.find('a'):
			processNote(item['href'], item.text, series)
		else:
			series = item.text.strip() or series

# def process():
# 	processOldFormat('https://www.evernote.com/l/AO8X_19lBzpIFJ2QRKX0hE_Hzrc-qBlE4Yw')

# 	# 可以每次append
# result = [([countWord(chapter) for chapter in x[0]]
# 	with open('other/word_count_detail.txt', 'w') as f:
# 		for sub_word_count, dirname, filename in result:
# 			if '大纲' not in filename:
# 				f.write('%s %d %s\n' % (filename, sum(sub_word_count), str(sub_word_count)))

if __name__ == '__main__':
	process('https://www.evernote.com/l/AO8X_19lBzpIFJ2QRKX0hE_Hzrc-qBlE4Yw')