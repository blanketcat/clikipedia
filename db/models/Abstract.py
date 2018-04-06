#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declared_attr


class Abstract(object):
	__tablename__ = 'abstract'

	id = Column(Integer, primary_key=True)
	
	title = Column(String, nullable=True)
	# category = Column(String, nullable=True)
	content_location = Column(String, nullable=True)

	def __repr__(self):
		return """<File (title='%s', content_location='%s')>""" % (
			self.title, self.content_location
		)


def main():
	print(dir(Abstract))


if __name__ == '__main__':
	main()
