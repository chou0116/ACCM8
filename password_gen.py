from passlib.hash import sha256_crypt

enteredPassword = "root"
pw = sha256_crypt.hash(enteredPassword)
print(pw)