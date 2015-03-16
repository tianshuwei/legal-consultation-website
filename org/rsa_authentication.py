# -*- coding: utf-8 -*-
from rsa._compat import b
from rsa import common, transform, core
from org.settings import RSA_LOGIN_KEY
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class RSABackend(ModelBackend):
	def authenticate(self, username, password):
		UserModel = get_user_model()
		try:
			pubkey, privkey = RSA_LOGIN_KEY
			user = UserModel._default_manager.get_by_natural_key(username)
			if user.check_password(decrypt(password.decode('hex'), privkey)):
				return user
		except:
			UserModel().set_password(password) # disguise timing


def decrypt(crypto, priv_key):
	"""This has been created to work with its javascript counterpart RSA.js."""
	blocksize = common.byte_size(priv_key.n)
	encrypted = transform.bytes2int(crypto)
	decrypted = core.decrypt_int(encrypted, priv_key.d, priv_key.n)
	cleartext = transform.int2bytes(decrypted, blocksize)[25:]
	try:
		sep_idx = cleartext.rindex(b('\x00'))
		return cleartext[sep_idx+1:]
	except ValueError:
		return cleartext
