# -*- coding: utf-8 -*-
import org.rsa
from org.settings import RSA_LOGIN_KEY
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class RSABackend(ModelBackend):
	def authenticate(self, username, password):
		UserModel = get_user_model()
		try:
			pubkey, privkey = RSA_LOGIN_KEY
			user = UserModel._default_manager.get_by_natural_key(username)
			if user.check_password(org.rsa.decrypt_busted(password.decode('hex'), privkey)):
				return user
		except UserModel.DoesNotExist:
			UserModel().set_password(password) # disguise timing
