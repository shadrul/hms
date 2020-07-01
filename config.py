import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x04\x94\x93\xf2\x1b\x1e\xfbb\xdeg\xe3S1:\xcf\x05'