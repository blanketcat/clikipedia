#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declared_attr


class Category(object):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	
	name = Column(String, nullable=True)

	def __repr__(self):
		return """<Category (id='%d', name='%s')>""" % (self.id, self.name)


def main():
	print(dir(Article))


if __name__ == '__main__':
	main()
