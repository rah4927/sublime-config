import sublime
import sublime_plugin 
from latex2utf import * 

def line2indices(content):
	indices = []
	isPaired = True  
	for index in range(len(content)):
		if content[index] == '$': 
			indices.append(index)
	# print(indices)
	return indices 

# uncomment all the update phantoms() 
class TexconcealCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		point = self.view.sel()[0]
		line = self.view.line(point)
		content = self.view.substr(line)
		# print(content)
		indices = line2indices(content)
		# print(indices)
		index = 0 
		while index + 1 < len(indices):
			left  = indices[index]
			right = indices[index + 1] 
			reg = sublime.Region(line.a + left, line.a + right + 1)
			
			self.view.fold(reg)

			allcontent = self.view.substr(reg)[1:-1]
			leftTag = "<small style = \"color:#5e81ac; background-color:#161C23;\"> <b>"
			# leftTag = "<small style = \"color:#696969; background-color:#161C23;\"> "
			# leftTag = "<small style = \"color:orange; background-color:#161C23;\"> "
			rightTag =  "</b> </small>"
			utf = leftTag + latex2utf(allcontent) + rightTag
			
			self.view.add_phantom("", sublime.Region(reg.b), str(utf), sublime.LAYOUT_INLINE)
			print(index)

			index += 2 

# for every cursor press, update phantoms in the previous line perhaps? but that's unnecessary and too much 
# but this is what we have for now i guess 
# for current line, clear all phantoms sorted by key 
# for previous line, create phantoms by line  number 
# so when we split a line into two these phantoms disappear and are replaced right? 
# yep i believe so 
# yeah this makes a lot of sense 
# the only question is, are we allowed to make multiple phantomsets per view 
# otherwise there probably isn't any reason no? 		