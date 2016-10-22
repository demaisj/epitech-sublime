import sublime, sublime_plugin
import getpass, pwd, time, os, re

def get_syntax(ext):
	if ext in ['c', 'cpp', 'h', 'hpp']:
		return {
			'comment_start': '/*',
			'comment'      : '**',
			'comment_end'  : '*/'
		}
	elif ext in ['mk', 'sh']:
		return {
			'comment_start': '#',
			'comment'      : '#',
			'comment_end'  : '#'
		}

def get_ext():
	var = sublime.active_window().extract_variables()
	sext = var['file_extension']
	if var['file_extension'] == "":
		ext = "sh"
	elif var['file_name'] == "Makefile":
		ext = "mk"
	return ext

class EpitechHeaderCommand(sublime_plugin.TextCommand):
	header  = '{comment_start}\n'
	header += '{comment} {file} for Project Name in {path}\n'
	header += '{comment} \n'
	header += '{comment} Made by {name}\n'
	header += '{comment} Login   <{user}@epitech.net>\n'
	header += '{comment} \n'
	header += '{comment} Started on  {start} {name}\n'
	header += '{comment} Last update {update} {name}\n'
	header += '{comment_end}\n'

	def run(self, edit):
		self.ext = get_ext()
		if self.ext not in ['c', 'cpp', 'h', 'hpp', 'mk', 'sh']:
			return
		data = self.set_variables(edit)
		self.view.insert(edit, 0, self.header.format(**data))
		selection = self.view.sel()
		selection.clear()
		start = len(data['comment_start'] + data['comment'] + data['file']) + 7
		stop = len("Project Name") + start
		selection.add(sublime.Region(start, stop))

	def set_variables(self, edit):
		var = sublime.active_window().extract_variables()
		user = pwd.getpwnam(getpass.getuser())

		data = {
			'file'   : var['file_name'] if 'file_name' in var.keys() else 'untitled',
			'path'   : var['file_path'] if 'file_path' in var.keys() else 'nowhere',
			'name'   : user.pw_gecos.strip(','),
			'user'   : user.pw_name,
			'start'  : time.strftime('%a %b %_d %T %Y'),
			'update' : time.strftime('%a %b %_d %T %Y')
		}
		data.update(get_syntax(self.ext))
		return data

class EpitechHeader(sublime_plugin.EventListener):
	def on_pre_save(self, view):
		sublime.active_window().run_command('epitech_header_update')
		

class EpitechHeaderUpdateCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		syntax = get_syntax(get_ext())
		pattern = '^{} Last update .*'.format(re.escape(syntax['comment']))
		region = self.view.find(pattern, 0)
		string = time.strftime('{} Last update %a %b %_d %T %Y {}')
		name = pwd.getpwnam(getpass.getuser()).pw_gecos.strip(',')
		self.view.replace(edit, region, string.format(syntax['comment'], name))
