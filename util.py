def commit():
	command = 'git add . && git commit -m auto_commit && git push -u -f'
	os.system(command % message)