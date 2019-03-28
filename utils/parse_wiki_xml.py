#!/usr/bin/env python3

import argparse
import html
import json
import os
import re
import time
import urllib
import xml.etree.cElementTree as et

import xmltodict

## Load xml file
## Iterate
## Create JSON object
## article = {
##   "title": text
## }
## write JSON to document/graphdb db
## read article from db
## pipe article to wiki_to_html
## feed html to electron

path_to_parsoid = ''

## Regex for wikimedia markup.

def parse_out_links(text):
	links = re.findall('\[\[(\w+|\s+)+\]\]', text)
	return links


def parse_out_sections(text):
	sections = re.findall('\={2,8}.*\={2,8}', elem.text)
	return sections

def create_tree(path_to_file):
	tree = et.iterparse(path_to_file)
	return tree


def article_to_json(page_id, title, text):
	article = {
		'page_id': page_id,
		'title': title,
		'text': text
	}
	return article


def write_to_file(page_id, article):
	fname = "page_" + page_id
	with open(fname) as f:
		f.write(article)


def wikitext_to_html(page_id, wikitext):
	html = ''.join(os.popen("cat wikitext | " + path_to_parsoid_bin + "/parse.js > " + page_id + ".html"))
	return html


def create_internal_link(base_url, uri):
	internal_link = '/'.join([base_url, uri])
	return internal_link


def is_redirect(text):
	if re.match('^\#REDIRECT', text) == None:
		return False

	return True


def set_title(page, title):
	page['title'] = title
	return page


def parse_text_elem(text_elem):
	"""
	"""
	# links
	links = []
	return links


def iter_pages_xml(path_to_file, function):
	tree = create_tree(path_to_file)
	page = {}

	for event, elem in tree:
		if event == 'start':
			if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
				page = {
					'title': '',
					'page_id': '',
					'type': '',
					'text': '',
					'sections': [],
					'categories': [],
					'external_links': [],
					'internal_links': []
				}

		if event == 'end':
			if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}title':
				page['title'] = elem.text

			elif elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}id':
				page['page_id'] = elem.text

			elif elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}text':
				page['text'] = elem.text

				# Determine/set page.type
				if is_redirect(page['text']):
					page['type'] = 'redirect'
				else:
					page['type'] = 'article'

				text_elem = page['text']
				text_elem = html.unescape(text_elem)
				page['text'] = text_elem

				# Parse sections
				page['sections'] = re.findall('\={2,8}.*\={2,8}', elem.text)
				page['categories'] = re.findall('\[\[Category\:.*\]\]', elem.text)
				page['external_links'] = re.findall('\{\{.*\}\}', elem.text)
				page['internal_links'] = re.findall('\[\[.*\]\]', elem.text)

			elif elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
				## End of page, do DB writes/updates here.
				# Debugging functions.
				# print(page)
				print('')
				print("<DOC>")
				print(page['title'])
				print(page['page_id'])
				print(page['type'])
				print(page['sections'])
				print(page['categories'])
				print('EXTERNAL LINKS:')
				print(page['external_links'])
				print('INTERNAL LINKS:')
				print(page['internal_links'])
				print("<END DOC>")
				print('')

				time.sleep(1)

				# page = {}

		elem.clear()


def iter_abstracts_xml(path_to_file, function):
	tree = create_tree(path_to_file)
	doc = {}

	for event, elem in tree:
		if event == 'start' and elem.tag == 'doc':
			print(elem.text)
			doc = {
				sublinks: []
			}

		if event == 'start' and elem.tag == 'sublink':
			doc['sublinks'][len(doc['sublinks'])] = {}

		if event == 'end' and elem.tag == 'title':
			doc_title = elem.text
			doc_title = doc_title.strip('Wikipedia: ')
			doc['title'] = doc_title

		if event == 'end' and elem.tag == 'url':
			doc_url = elem.text
			doc['url'] = doc_url

		if event == 'end' and elem.tag == 'abstract':
			doc_abstract = elem.text
			doc['abstract'] = doc_abstract

		if event == 'end' and elem.tag == 'anchor':
			doc['sublinks'][len(doc['sublinks']) - 1]['anchor'] = elem.text

		if event == 'end' and elem.tag == 'link':
			doc['sublinks'][len(doc['sublinks']) - 1]['link'] = elem.text

		if event == 'end' and elem.tag == 'sublink':
			pass
			

		if event == 'end' and elem.tag == 'doc':
			## Place write/processing operations here
			print(doc)
			time.sleep(1)
			

		elem.clear()




def main():
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--filename', '-f',
		type=str,
		required=True,
		help='/path/to/filename to process.'
	)

	parser.add_argument(
		'--sections', '-s',
		type=str,
		required=True,
		help='/')

	args = vars(parser.parse_args())

	iter_pages_xml(args['filename'], 'print')

if __name__ == '__main__':
	main()
