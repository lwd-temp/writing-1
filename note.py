from telegram_util import compactText
import cached_url
import yaml
from bs4 import BeautifulSoup
import time

def clearText(content):
	for key in ['next', 'Next', 'previous', 'Previous']:
		content = content.split(key)[0]	
	result = []
	in_comment = 0
	for x in content:
		if x == '【':
			in_comment += 1
		if x == '】':
			in_comment -= 1
			continue
		if not in_comment:
			result.append(x)
	content = ''.join(result)
	return compactText(content)

def getEvernoteUrls(soup):
	for item in soup.find_all('a'):
		if item['href'] and item['href'].startswith('https://www.evernote.com/l'):
			yield item['href']

def getTextSoup(content):
	soup = BeautifulSoup(content, 'html.parser')
	for item in soup.find_all('span'):
		if 'bold' in str(item.attrs):
			item.replace_with('**%s**' % item.text)
		else:
			item.replace_with(item.text)
	for item in soup.find_all('div'):
		item.replace_with(item.text + '\n\n')
	for item in soup.find_all('br'):
		item.replace_with('\n\n')
	return soup

class Note(object):
	def __init__(self, url):
		content = cached_url.get(url + '?json=1')
		content = yaml.load(content, Loader=yaml.FullLoader)
		self.title = content['title']
		self.soup = BeautifulSoup(content['content'], 'html.parser')
		self.evernote_urls = list(getEvernoteUrls(self.soup))
		self.next_url = self.evernote_urls and self.evernote_urls[0]
		self.text_soup = getTextSoup(content['content'])
		self.raw_text = compactText(
			self.text_soup.text.replace('~', '.'))
		self.text = clearText(self.raw_text)
		self.word_count = len([c for c in self.text 
			if c.isalpha() and ord(c) > 255])

	def isNewFormat(self):
		for item in [self.soup.text, self.title]:
			if 'new_format' in item:
				return True
			if 'old_format' in item:
				return False
		if len(self.evernote_urls) == 0:
			return False
		if len(self.text) < sum(
			[len(url) for url in self.evernote_urls]):
			return True
		return len(self.evernote_urls) > 3
