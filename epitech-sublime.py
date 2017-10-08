import sublime
import sublime_plugin
import time
import os

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

default_description = "[file description here]"

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
    header = '{comment_start}\n'
    header += '{comment} EPITECH PROJECT, {year}\n'
    header += '{comment} {project}\n'
    header += '{comment} File description:\n'
    header += '{comment} {description}\n'
    header += '{comment_end}\n'
    header += '\n'

    def run(self, edit):
        self.ext = get_language(self)
        if self.ext not in supported_languages:
            sublime.message_dialog("Warning:\n\nThe current selected syntax is not supported by EPITECH_Sublime. We're adding one anyway.\nIf you want to add support for this syntax please report an issue in our GitHub repo.")
            self.ext = 'Plain text'

        data = self.set_variables(edit)
        rendered = self.header.format(**data)
        self.view.insert(edit, 0, rendered)

        selection = self.view.sel()
        selection.clear()
        start = rendered.find(default_description)
        stop = start + len(default_description)
        selection.add(sublime.Region(start, stop))

    def set_variables(self, edit):
        var = sublime.active_window().extract_variables()
        project = "Project Name"
        if "project_base_name" in var:
            project = var['project_base_name']

        data = {
            'year':        time.strftime('%Y'),
            'project':     project,
            'description': default_description
        }
        data.update(get_syntax(self.ext))
        return data