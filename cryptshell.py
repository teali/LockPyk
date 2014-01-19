#!/usr/bin/python

import sys, getopt, itertools, getpass, os, shutil

# -h,--help : lists commands
# -f, --files : decrypts and displays files
# -d <file_name>, --decrypt <file_name>: decrypts and outputs file
# -s <file_path>, --save <file_path>: saves file and deletes it
# -c , --changepassword: changes password
# -i , --init: initializes system
# -r <file_name>, --remove <file_name> : removes encrypted file
#string used for validation, change to whatever you want
VAL_STRING = "10cc4a10-e51d-4775-bd84-91998b377325"
path = "./.files/"

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"hfd:s:cir:",["help","files","decrypt=","save=","changepassword","init","remove="])
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2)
	if len(opts) == 0:sys.exit()
	[o,a] = opts[0]

	#validates password
	if o not in ("-h","-i","--help","--init"):
		PASS = getpass.getpass("Password: ")
		if PassEval(PASS):
			cypher = CreateCypher(PASS)
		else:
			print "Invalid password."
			sys.exit()	

	if o in ("-h","--help"):
		print " -h,--help :\n    lists commands\n"
		print " -f, --files :\n    decrypts and displays files\n"
		print " -d <file_id>, --decrypt <file_id>:\n    decrypts and outputs file\n"
		print " -s <file_path>, --save <file_path>:\n    saves file and deletes non-encrypted file\n"
		print " -r <file_name>, --remove <file_name>:\n    removes the encrypted file\n"
		print " -c , --changepassword:\n    changes password\n"
		print " -i , --init:\n    initializes system\n"
		sys.exit()
	
	elif o in("-f","--files"): 
		dirFiles = os.listdir(path)
		if len(dirFiles) > 0:
			print "\n".join([decrypt(i,cypher) for i in dirFiles])
	
	elif o in("-d","--decrypt"):
		files = os.listdir(path)
		fileName = encrypt(a,cypher)
		if fileName in files:
			WriteToFile(
				open(path+encrypt(a,cypher)),
				open(a,"w"),
				decrypt,
				cypher)
		else:
			print "File does not exist"
			sys.exit()

	elif o in("-s","--save"):
		WriteToFile(
			open(a),
			open((path + encrypt(a.split("/")[-1].strip("."),cypher)),"w"),
			encrypt,
			cypher)
		os.unlink(a)
	
	elif o in("-r","--remove"):
		os.unlink(path + encrypt(a,cypher))

	elif o in("-c","--changepassword"):
		NEWPASS = getpass.getpass("New password: ")
		newcypher = CreateCypher(NEWPASS)
		for i in os.listdir(path):
			ChangeCypher(i,cypher,newcypher)
		open(".val.txt","w").write(encrypt(VAL_STRING,newcypher))
		
	elif o in("-i","--init"):
		cypher = CreateCypher(getpass.getpass("Password: "))
		open(".val.txt","w").write(encrypt(VAL_STRING,cypher))
		if os.path.exists('./.files'): shutil.rmtree(path)
		os.mkdir(path)
	
	else:
		assert False, "unhandled option"

def ChangeCypher(filename, cypher_old, cypher_new):
		fin = open(path + filename)
		print  encrypt(decrypt(filename,cypher_old),cypher_new)
		fout = open(path + encrypt(decrypt(filename,cypher_old),cypher_new),"w")
		while True:
			c = fin.read(1)
			if not c: break
			fout.write(encrypt(decrypt(c,cypher_old),cypher_new))
		fin.close()
		fout.close()
		os.unlink(path + filename)

def WriteToFile(fin, fout, func, cypher):
	while True:
		c = fin.read(1)
		if not c: break
		fout.write(func(c,cypher))
	fin.close()
	fout.close()

def CreateCypher(PASS):
	dir=[i for i in xrange(256)]
	nextChr = itertools.cycle(list(PASS))
	for j in xrange(256):
		c = nextChr.next()
		tempIndex = (j+ord(c))%256
		#swap
		dir[i] += dir[tempIndex] 
		dir[tempIndex] = dir[i] - dir[tempIndex]
		dir[i] -= dir[tempIndex]
	
	return dir

def PassEval(PASS):
	cypher = CreateCypher(PASS)
	fin = open(".val.txt")
	valstring = ''
	while True:
		c = fin.read(1)
		if not c: break
		valstring += decrypt(c,cypher)
	if valstring == VAL_STRING: return True
	else: return False
	

def decrypt(string,cypher):
	return "".join(chr(cypher.index(ord(i))) for i in list(string))

def encrypt(string, cypher):
	return "".join(chr(cypher[ord(i)]) for i in list(string))

if __name__ == "__main__":
	main(sys.argv[1:])
