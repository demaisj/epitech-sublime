import sublime, sublime_plugin
import getpass, pwd, time, os, re

supported_languages = [
	'C',
	'CSS',
	'C++',
	'Lisp',
	'Shell-Unix-Generic',
	'Makefile',
	'Perl',
	'Java',
	'LaTeX',
	'Pascal',
	'Plain text',
	'HTML',
	'PHP',
	'TeX',
	'Python',
	'JavaScript'
]

def get_syntax(ext):
	if ext in ['C', 'CSS', 'C++', 'Java', 'JavaScript']:
		return {
			'comment_start': '/*',
			'comment'      : '**',
			'comment_end'  : '*/'
		}
	elif ext in ['LaTeX', 'TeX']:
		return {
			'comment_start': '%%',
			'comment'      : '%%',
			'comment_end'  : '%%'
		}
	elif ext in ['Lisp']:
		return {
			'comment_start': ';;',
			'comment'      : ';;',
			'comment_end'  : ';;'
		}
	elif ext in ['Makefile', 'Plain text']:
		return {
			'comment_start': '##',
			'comment'      : '##',
			'comment_end'  : '##'
		}
	elif ext in ['Python']:
		return {
			'comment_start': '#!/usr/bin/env python\n##',
			'comment'      : '##',
			'comment_end'  : '##'
		}
	elif ext in ['Shell-Unix-Generic']:
		return {
			'comment_start': '#!/bin/bash\n##',
			'comment'      : '##',
			'comment_end'  : '##'
		}
	elif ext in ['Perl']:
		return {
			'comment_start': '#!/usr/bin/env perl\n##',
			'comment'      : '##',
			'comment_end'  : '##'
		}
	elif ext in ['Pascal']:
		return {
			'comment_start': '{',
			'comment'      : '  ',
			'comment_end'  : '}'
		}
	elif ext in ['HTML']:
		return {
			'comment_start': '<!--',
			'comment'      : '  --',
			'comment_end'  : '  -->'
		}
	elif ext in ['PHP']:
		return {
			'comment_start': '#!/usr/bin/env php\n<?php\n/*',
			'comment'      : '**',
			'comment_end'  : '*/'
		}

def get_language(self):
	package = self.view.settings().get('syntax')
	name = os.path.splitext(os.path.basename(package))[0]
	return name

class EpitechHeaderCommand(sublime_plugin.TextCommand):
	header  = '{comment_start}\n'
	header += '{comment} {file} for {project} in {path}\n'
	header += '{comment} \n'
	header += '{comment} Made by {name}\n'
	header += '{comment} Login   <{user}@epitech.net>\n'
	header += '{comment} \n'
	header += '{comment} Started on  {start} {name}\n'
	header += '{comment} Last update {update} {name}\n'
	header += '{comment_end}\n'
	header += '\n'

	def run(self, edit):
		global supported_languages

		self.ext = get_language(self)
		if self.ext not in supported_languages:
			sublime.message_dialog("Warning:\n\nThe current selected syntax is not supported by EPITECH_Sublime. We're adding one anyway.\nIf you want to add support for this syntax please report an issue in our GitHub repo.")
		data = self.set_variables(edit)
		self.view.insert(edit, 0, self.header.format(**data))
		selection = self.view.sel()
		selection.clear()
		start = len(data['comment_start'] + data['comment'] + data['file']) + 7
		stop = len(data['project']) + start
		selection.add(sublime.Region(start, stop))

	def set_variables(self, edit):
		var = sublime.active_window().extract_variables()
		user = pwd.getpwnam(getpass.getuser())
		project = "Project Name"
		if "project_base_name" in var:
			project = var['project_base_name']

		data = {
			'file'   : var['file_name'] if 'file_name' in var.keys() else 'untitled',
			'path'   : var['file_path'] if 'file_path' in var.keys() else 'nowhere',
			'name'   : user.pw_gecos.strip(','),
			'user'   : user.pw_name,
			'start'  : time.strftime('%a %b %_d %T %Y'),
			'update' : time.strftime('%a %b %_d %T %Y'),
			'project': project
		}
		data.update(get_syntax(self.ext))
		return data

class EpitechHeader(sublime_plugin.EventListener):
	def on_pre_save(self, view):
		sublime.active_window().run_command('epitech_header_update')
		

class EpitechHeaderUpdateCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global supported_languages

		self.ext = get_language(self)
		if self.ext not in supported_languages:
			return
		syntax = get_syntax(self.ext)
		pattern = '^{} Last update .*'.format(re.escape(syntax['comment']))
		region = self.view.find(pattern, 0)
		string = time.strftime('{} Last update %a %b %_d %T %Y {}')
		name = pwd.getpwnam(getpass.getuser()).pw_gecos.strip(',')
		self.view.replace(edit, region, string.format(syntax['comment'], name))
