#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from opencc import OpenCC
from note import Note, clearText
from bs4 import BeautifulSoup
import cached_url
cc = OpenCC('s2tw')

def mkdirs(*args):
	for arg in args:
		os.system('mkdir %s > /dev/null 2>&1' % arg)

def getRaw(notes):
	return ''.join(['\n\n\n==== %s  ===\n\n\n' % note.title + 
		note.raw_text for note in notes])

def getContent(notes):
	outline_count = sum(['大纲' in note.title for note in notes])
	if outline_count < len(notes) / 2:
		notes = [note for note in notes if '【大纲】' not in note.title]
	text = ''.join(['\n\n\n==== %s  ===\n\n\n' % note.title + 
		note.text for note in notes])
	return clearText(text)

def processNote(url, title, dirname):
	root_note = Note(url)

	if root_note.isNewFormat():
		notes = [ Note(sub_url) for sub_url in root_note.evernote_urls]
	else:
		sub_url = root_note.next_url
		notes = [root_note]
		while sub_url:
			note = Note(sub_url)
			notes.append(note)
			sub_url = note.next_url

	mkdirs(dirname, 'txt', 'traditional', 'raw')
	content = getContent(notes)
	with open('%s/%s.md' % (dirname, title), 'w') as f:
		f.write(content)
	with open('txt/%s.txt' % title, 'w') as f:
		f.write(content)
	with open('traditional/%s.md' % cc.convert(title), 'w') as f:
		f.write(cc.convert(content))
	with open('raw/%s.md' % title, 'w') as f:
		f.write(getRaw(notes))
	if dirname in ['critics', 'original']:
		word_count = [note.word_count for note in notes]
		with open('other/word_count_detail.txt', 'a') as f:
			f.write('%s %d %s\n' % (title, sum(word_count), str(word_count)))

def getDirName(series):
	if not series:
		return 'critics'
	series_map = {
		'笔记': 'critics', 
		'旧稿': 'other', 
		'其他': 'other', 
		'大纲': 'other'}
	for key in series_map:
		if key in series:
			return series_map[key]
	return 'original'

def process(root_url):
	mkdirs('other')
	note = Note(root_url)
	series = None
	for item in note.soup.find_all('div'):
		link = item.find('a')
		if link and 'active' in item.text:
			processNote(link['href'], link.text, getDirName(series))
		else:
			series = item.text.strip() or series

def processTelegraphSingle(url, title, dirname):
	raw_content = cached_url.get(url)
	soup = BeautifulSoup(raw_content, 'html.parser').find('article')
	for tag in ['br', 'p', 'li', 'h4']:
		for item in soup.find_all(tag):
			item.replace_with('\n' + item.text.strip() + '\n')
	content = soup.text
	for _ in range(10):
		content.replace('\n\n\n', '\n\n')
	with open('%s/%s.md' % (dirname, title), 'w') as f:
		f.write(content.strip())

def processTelegraph(root_url):
	note = Note(root_url)
	for item in note.soup.find_all('div'):
		link = item.find('a')
		if link:
			processTelegraphSingle(link['href'], link.text, 'critics')

if __name__ == '__main__':
	os.system('rm other/word_count_detail.txt')
	os.system('touch other/word_count_detail.txt')
	process('https://www.evernote.com/shard/s239/sh/17ff5f65-073a-4814-9d90-44a5f4844fc7/ceb73ea81944e18c4bb6a1f5542edd6d')