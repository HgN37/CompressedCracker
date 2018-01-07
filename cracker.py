#!/usr/bin/python3

import rarfile
import zipfile
import os
import sys
import argparse

CHARACTER = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345678.!@#$%^&*()_+=-<>?\/'

parser = argparse.ArgumentParser(description='Uncompressed', epilog='Use -h for help')
parser.add_argument('-i', '--input', help='Insert the rar/zip file path')
parser.add_argument('-o', '--output', help='Insert the output path')


args = parser.parse_args()
file_path = args.input
output_path = args.output

if not os.path.isfile(file_path):
	print('File path is not valid')
	sys.exit()
_, ext = os.path.splitext(file_path)
if not ((ext == '.rar') | (ext == '.zip')):
	print('File type isn\'t supported: ' + ext)
	sys.exit()

if output_path == None:
	output_path = './'

if ext == '.rar':
	file = rarfile.RarFile(file_path)
elif ext == '.zip':
	file = zipfile.ZipFile(file_path)

print('Open file: ' + file_path)
print('Output dir: ' + output_path)

''' Create password
'''
done = False
password = []
def passwordCreate():
	if not password:
		password.append(0)
	else:
		password[-1] += 1
		for i in range(len(password) - 1):
			if password[-1-i] >= len(CHARACTER):
				password[-1-i] = 0
				password[-2-i] += 1
			else:
				break
	if password[0] >= len(CHARACTER):
		for i in range(len(password)):
			password[i] = 0
		password.append(0)

def passwordString():
	pass_string = ''
	for i in range(len(password)):
		pass_string += CHARACTER[password[i]]
	return pass_string

if not file.needs_password():
	print('There\'s no password')
	file.extractall(path=output_path)
	print('Extract done')
	sys.exit()
else:
	print('Cracking...')
	while done is False:
		try:
			passwordCreate()
			if ext == '.rar':
				try_pwd = passwordString()
			elif ext == '.zip':
				try_pwd = passwordString().encode()
			file.extractall(path=output_path, pwd=try_pwd)
			done = True
			print('Extract done')
			print('Password: ' + passwordString())
			sys.exit()
		except rarfile.RarCRCError:
			pass
		except KeyboardInterrupt:
			sys.exit()
