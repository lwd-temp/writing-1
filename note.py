from telegram_util import compactText

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

class Note(object):
	def __init__(self, title, raw_note):
		self.title = title
		self.raw_note = raw_note
		self.note = clearText(raw_note)