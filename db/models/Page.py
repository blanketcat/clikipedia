#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declared_attr


class Page(object):
	__tablename__ = 'page'

	id = Column(Integer, primary_key=True)
	
	title = Column(String, nullable=True)
	# categories = Column(String, nullable=True)
	content_location = Column(String, nullable=True)

	def __repr__(self):
		return """<File (title='%s', content_location='%s')>""" % (
			self.title, self.content_location
		)


def main():
	print(dir(Page))


if __name__ == '__main__':
	main()
