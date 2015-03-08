import re

class Enum(object):
	r_CONSTANT=re.compile(r'^[_A-Z]+\d*$')

	@classmethod
	def as_dict(cls):
		return {k:v for k,v in vars(cls).iteritems() if Enum.r_CONSTANT.match(k)}

	@classmethod
	def get_choices(cls):
		return tuple((v,k) for k,v in vars(cls).iteritems() if Enum.r_CONSTANT.match(k))

class CustomException(Exception):
	pass
