import sublime
import sublime_plugin 
from latex2utf import * 

# uncomment all the update phantoms() 
class concealTex(sublime_plugin.ViewEventListener):
	def __init__(self, view):
		self.view = view
		self.phantom_set = sublime.PhantomSet(view)
		self.timeout_scheduled = False
		self.needs_update = False

		# self.update_phantoms()

	@classmethod
	def is_applicable(cls, settings):
		syntax = settings.get('syntax')
		return syntax == 'Packages/Text/Plain text.tmLanguage'
		# return syntax == 'Packages/LaTeX/LaTeX.sublime-syntax'

	def update_phantoms(self):
		phantoms = []

		# Don't do any calculations on 1MB or larger files
		if self.view.size() < 2**20:
			# candidates = self.view.find_all('\$.*\$')
			candidates = self.view.find_all('12340982382')

			
			for r in candidates:
			
				self.view.fold(r) 
				line_region = self.view.line(r.a)

				line = self.view.substr(r)[1:-1]
				leftTag = "<small style = \"color:#696969; background-color:#161C23;\"> "
				rightTag =  "</small>"
				utf = leftTag + latex2utf(line) + rightTag 

				idx = r.a - line_region.a
				if idx != -1:
					op_pt = line_region.a + idx

					phantoms.append(sublime.Phantom(
						sublime.Region(r.b),
						str(utf),
						sublime.LAYOUT_INLINE))
			
		self.phantom_set.update(phantoms)

	def handle_timeout(self):
		self.timeout_scheduled = False
		if self.needs_update:
			self.needs_update = False
			# self.update_phantoms()

	def on_modified(self):
		# Call update_phantoms(), but not any more than 10 times a second
		if self.timeout_scheduled:
			self.needs_update = True
		else:
			sublime.set_timeout(lambda: self.handle_timeout(), 100)
			# self.update_phantoms()