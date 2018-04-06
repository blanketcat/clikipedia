#!/usr/bin/env python3

import json, html, lxml, os, re, sys

from lxml import etree
from db.pg_utils import *
from db.mongo_utils import *


## Make this shit dynamic as we're going to be iterating through many XML files.
path_to_xml_file = os.path.dirname(os.path.realpath(__file__)) + '/../data/enwiki/enwiki-20170601-pages-articles01.xml-p10p30302'


class Page:
	"""
		The Page object.
	"""

	## Corresponds directly to the Page DB model. (more hassle than it's worth to the db model here)
	def __init__(self):
		self.xml_object = None
		self.html_text = ''
		self.title = ''
		self.raw_page_text = ''
		## Ordered tuples of ('section_title', 'section_text')
		self.sections = []
		self.categories = []
		self.links = []
		return self

	def __repr__(self):
		return """<Page (title='%s', text='%s', categories='%s')""" % (
			self.title, self.text, ', '.join(self.categories)
			)


def list_shuffle(target_list):
	## Huh? I'm not gonna check how many elements you have in it.
	if len(target_list) > 0:
		target_list.insert(len(target_list), target_list[0])
		target_list.remove(target_list[0])
		return target_list
	else:
		return None


def files_in_dir(path_to_dir, return_list=False, reverse=False):
	## Return a generator object or a list with the file names in path_to_dir.
	## If return_list is set to True, simply returns the list of file names.
	## If reverse is set to True, reverse the file names before returning them.
	## Sometimes it's that straight forward?

	if return_list == True:
		## List
		try:
			f_list = os.listdir(path_to_dir)
			f_list.sort()
			if reverse == True:
				f_list.reverse()
				return f_list
			else:
				return f_list

		except PermissionError as err:
			print(err)
			print('You do not have permission to access this directory')
			return None

		except FileNotFoundError as err:
			print (err)
			print('It does not seem like this directory exists, or the path is wrong.')
			return None

	else:
		## Generator
		try:
			f_list = os.listdir(path_to_dir)
			f_list.sort()
			if reverse == True:
				f_list.reverse()

		except PermissionError as err:
			print(err)
			print('You do not have permission to access this directory')
			return None

		except FileNotFoundError as err:
			print (err)
			print('It does not seem like this directory exists, or the path is wrong.')
			return None

		if reverse == True:
			f_list.reverse()

			while len(f_list) > 0:
				try:
					yield f_list.pop()
					list_shuffle()

				except StopIteration:
					return True

		else:
			list_shuffle(f_list)
			
			while len(f_list) < 0:
				try:
					yield f_list.pop()
					list_shuffle(f_list)
			
				except StopIteration:
					return True


def strip_ns_from_tag(elem_tag):
	## Return a string of the elements tag, sans the lingering ns info.
	tag = elem_tag
	tag.replace('{http://www.mediawiki.org/xml/export-0.10/}', '')
	return tag


def create_tree(path_to_xml_file):
	## Return a generator that moves through items in the XML tree.
	## First: if using on large files: set ```event, root = next(tree)```
	## and run ```root.clear()``` when you're done with an element.
	tree = etree.iterparse(path_to_xml_file, events=('start', 'end'))
	return tree


def get_page(tree):
	## Return an XML etree element object for a variable so we can call it's methods
	page = tree[1]
	return page


def get_page_branches(page):
	## Return a list of all the XML elements for a variable.
	## From there we can assign the indexed elements to varaibles so we can
	## call their methods.
	branches = [branch for branch in page.iterdescendants()]
	return branches


def get_text_of_branches(branches):
	## Return a list of tuples containing the elements tag name and it's text
	## content for a variable.
	## Normally a dict would work, but the wikimedia data format is pretty
	## dirty. (also: altruistic, an incredible gift to humanity, and in
	## everyone's defense; legacy as fuck) Pre JSON-popularity design leaves
	## it doubling up in the name space frequently.
	branch_texts = []
	for branch in branches:
		tag = strip_ns_from_tag(branch.tag)
		branch_texts.append((tag, branch.text))
	return branch_texts


def get_title_from_branch_texts(branch_texts):
	## This is going to add about 10 unecessary checks per page.
	## We can make it nicer but we already agreed on the data structure
	## in the get_text_of_branches() functions...
	## It saves us from having to deal with identical tags in a dictionary
	page_title = ''
	for text in branch_texts:
		if text[0] == 'title':
			page_title = text[1]
		elif text[0] == 'redirect':
			page_title = text[1]
			return page_title
		else:
			pass

	return page_title


def get_article_from_branch_texts(branch_texts):
	## Returns a string of the content from the page.
	for text in branch_texts:
		if text[0] == 'text':
			article = text[1]
			return article
		else:
			return None


def get_section_titles(page_text):
	## Return a list of pages sections if any exist, or an empty list.
	section_titles = re.findall('(^\={2,}(\s|[A-Za-z0-9]).*?\={2,}$)', page_text)
	section_titles = [i[0] for i in section_titles]

	if len(section_titles) > 0:
		section_titles = [i.replace('=', '').replace(' ', _) for i in section_titles]
		section_titles = [i[1:] for i in section_titles if i[0] == ' ']
	
	return section_titles


def get_section_text(section_title, page_text):
	## Return a string with the isolated text of the section 'section_title'
	section_text = re.search('^\={2,}' + section_title + '\={2,}.*?(^\={2}|(\<\/text\>', page_text)
	
	if len(section_text) > 0:
		content_depth = section_text[0].split(section_title)
		content_depth = len(content_depth[0])
		section_text = section_text.split('=' * content_depth)
	section_text



def get_section_texts(section_titles):
	## Return a list of tuples containing the section title and the section
	## text in order
	section_texts = []

	if len(section_titles) > 0:
		for sect in section_titles:
			section_title = sect[0]
			section_text = get_section_text(section_title)
			section_texts.append((section_title, section_text))
	
	return section_texts


def get_categories(page_text):
	## Return a list of pages categories if any exist, or an empty list.
	cats = re.findall("\[\[Category:.+?\]\]", page_text)
	amazing_cats = []

	if len(cats) > 0:
		cats = [i[0] for i in cats]
	else:
		return cats
	
	for i in cats:
		cat_name = i.split(':')
		cat_name = cat_name.pop()
		cat_name = cat_name.replace(']', '').replace(' ', '_').replace('| ', '')
		amazing_cats.append(cat_name)

	return amazing_cats


def get_internal_links(text):
	## Return a list of pages links to other pages if they exist, or
	## an empty list.
	## Should just pull in a library for the {{ish}}, [[Poop|PooPoo]]
	links = re.search("\[\[.+?\]\]", text)
	return links


def get_files(text):
	## Return a list of pages file links if they exist, or an empty list.
	files = re.search("\[\[File:.+", text)
	return files


def get_infoboxes(text):
	## Fuck all of this one.
	## This gets so convoluted, so quickly. I couldn't put it down fast
	## enough.
	## If you nail this one without resorting to external resources you
	## basically win at programming forever.
	pass


def get_math_expressions(page_text):
	## Return a list of pages mathematical expressions in latex if they exist,
	## or an empty list.
	maths = re.search("\&lt\;math\&gt\;.*?\&lt\;/math\&gt\;", text)
	return maths


def get_references(page_text):
	## Return a list of pages references if they exist, or an empty list.
	refs = re.search("\&lt\;ref\&gt\;.*?\&lt\;/math\&gt\;")
	return refs


def get_html_escapes(page_text)
	## Return a list of pages text html escapes if they exist, or an empty list.
	## This is the precursor to the convert_escaped_html() function.
	## I can see why they did the escapes on certain elements.
	## If they would have say left the ref tags whole, it would have added
	## another layer of depth to the XML.
	escapes = re.search("\&.{1,6}\;", page_text)
	return escapes


def escape_html(unescaped_text):
	## Return a string of the html escaped text of a page.
	## Not sure whether or not to use the quote=True parameter to escape quotes.
	## We may want to use this as a precursor to some other parsing.
	## Maybe dupe it with quotes escaped for rendering, and/or JSON storage.
	escaped_text = html.escape(unescaped_text)
	return escaped_text


def unescape_html(escaped_text):
	## Return a string of the html unescaped text of a page.
	## Preparsing to convert ref, math, etc.. tags into tags again.
	unescaped_text = html.unescape(escaped_text)
	return unescaped_text


def create_div(div_id, additional_class=[]):
	## Return a tuple containing the div open and close tags in order.
	div_open = '<div id="' + div_id + '" class="' + ' '.join([c for c in additional_class]) + '">'
	div_close = '</div>'
	return (div_open, div_close)


def create_internal_link(link_markup, server_addr, port):
	## Return a string containing an anchor tag from a wikimedia "[[ link ]]"
	## object.
	link = link_markup.split('|')
	if len(link) == 1:
		text = link
	elif len(link) == 2:
		if link[1] == ' ]]'
			text = link[0]
		else:
			text = link[1]
	
	uri = link[0]
	uri = url.replace(' ', '_')
	url = ''
	
	anchor = '<a href="http://' + server_addr + ':' + port + '/' + uri + '">' + text + '</a>'
	
	return anchor


def parse_page(elem):
	## Return a dictionary object with the data you want to store, display,
	## manipulate, or disregard.
	
	## This all might do better as a methods of the Page object.
	## You gotta know when hold them, know when to object orient them?
	page_data = Page()
	page_data.xml_object = elem
	
	## This seems silly but we have to assign it to a temporary variable in
	## order to call the methods on the XML object..
	## Now that we've locked it in, we only want to operate on the objects version.
	page = page_data.xml_object
	branches = get_page_branches(page)
	branch_texts = get_text_of_branches(branches)

	## Get the page title
	title = get_title_from_branch_texts(branch_texts)
	page_data.title = title

	## Get the raw article text
	page_text = [i[1] for i in branch_texts if i[0] == 'text'].pop()
	page_data.raw_page_text = page_text.text

	## Get the page sections
	page_section_titles = get_section_titles(page_text.text)
	page_section_text = []

	for title in page_section_titles:
		page_section_text = get_section_text(title, page_text)
		page_data.sections.append(page_section_text)

	## Get the page categories
	page_categories = [i for i in get_categories(page_text.text)]
	page_data.categories = page_categories

	return page_data


def write_page_data_to_dbs(page_object):
	## Write the page data to databases.
	## We're going to need a lot of sanity checks here.
	## The formating is super inconsistent as it's been over a decade on the same
	## codebase now.
	pass


def setup(path_to_data_dir, no_xml_files=-1):
	tree = create_tree(path_to_xml_file)
	event, root = next(tree)

	for event, elem in tree:
		elem_tag = strip_ns_from_tag(elem.tag)

		if event == 'start' and elem_tag == 'page':
			cur_page = parse_page(elem)
			write_page_data_to_dbs(cur_page)


			etree.parse(page)
		if event == 'end' and elem.tag[-4] == 'text':
			print(elem.tag)
			print(elem.text)
			print('\n' * 3)
		root.clear()


def main():
	setup()


if __name__ == '__main__':
	main()
