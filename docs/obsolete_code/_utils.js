function rsa_encryption(string){
	setMaxDigits(19);
	var key = new RSAKeyPair(
 		"16d1507964604313b5121c52c1051115",  //e
 		"",  
 		"70a6c76c3631387e7eaca739f7f5cbe7"   //n
	);
	return encryptedString(key,string);
}

function rsa_decryption(en_string){          //测试时用的解密函数，之后可删
	setMaxDigits(19);
	var key = new RSAKeyPair(
 		"16d1507964604313b5121c52c1051115",  //e
 		"55afdcf744d8f5fe0c655fee417b3765",  //d
 		"70a6c76c3631387e7eaca739f7f5cbe7"   //n
	);
	return decryptedString(key,en_string);
}