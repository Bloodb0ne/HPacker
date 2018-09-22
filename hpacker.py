import json
import argparse
import os
import re
from pathlib import Path

parser = argparse.ArgumentParser(description="Generate a single header file from a C/C++ project.\n\
 Loads the file single_config.json by default in the current working directory")

parser.add_argument('--config_file',
	help="descriptor file listing files",
	default='single_config.json')
parser.add_argument('-o','--output_file',
	help="output file path for the single header file",
	default=None)
parser.add_argument('--g',
	help="generate a dummy config file in the current directory",
	action='store_true')


args = parser.parse_args()
nl = '\n' #os.linesep

def remove_inner_includes(files,current_file):
	str = current_file

	for fname in files:
		str = str.replace("#include \"" + fname + "\"", "")
		str = str.replace("#include <" + fname + ">", "")
	return str

def fl_expand(file_list):
	files = []
	for f in file_list:
		if "*" in f:
			files.extend([ str(x) for x in Path('.').glob(f)])
		else:
			files.append(f)
	return files

def fl_cat(flist):
	return ''.join([ nl + open(f,'r').read() + nl for f in flist ])

def wrap_define(constant,content):
	return ''.join(
		[nl,
		"#define ",constant,nl,
		content,nl,
		"#endif "," /* ",constant," */ ",nl])

def wrap_ifndef(constant,content):
	return ''.join(
		[nl,
		"#ifndef ", constant,nl,
		"#define ", constant,nl,
		content,nl,
		"#endif "," /* ",constant," */ ",nl])

def wrap_ifdef(constant,content):
	return ''.join(
		[nl,
		"#ifdef ", constant,nl,
		content,nl,
		"#endif "," /* ",constant," */ ",nl])

def wrap_comment(content):
	return ''.join([nl*2,
		"/*",nl,
		content,nl,
		"*/",nl
		])

def generateSingleHeader(config):
	fpublic = fl_expand(config['public_files'])
	impl	= fl_expand(config['implementation_files'])
	header_comment	= fl_expand(config['header'])
	footer_comment	= fl_expand(config['footer'])

	 
	return	''.join(
		[
		wrap_comment(fl_cat(header_comment)),
		wrap_ifndef(config['macro']+"_PACKED_HEADER",
			remove_inner_includes(fpublic+impl,fl_cat(fpublic))),
		wrap_ifdef(config['macro']+"_IMPLEMENTATION",
			remove_inner_includes(fpublic+impl,fl_cat(impl))),
		wrap_comment(fl_cat(footer_comment))
		])

if args.g:
	#generate a dummy config file and exit
	basic_config = "{\
	\"macro\": \"LIBNAME\",\
	\"output_destination\":\"lib_header.h\",\
	\"public_files\": [\
		\"example.h\"\
	],\
	\"implementation_files\": [\
		\"example.cpp\"\
	],\
	\"footer\": [\
		\"readme.txt\"\
	],\
	\"header\": [\
		\"readme.txt\"\
	]\
	}"
	with open('single_header.example.json','w') as fconf:
		fconf.write(basic_config)

	print('Generated a example config file at %s' % os.path.join(os.getcwd(),'single_header.example.json'))
	exit()

if not os.path.exists(args.config_file):
	print('Cannot find config file at %s .Please check the path to the file.' % args.config_file)
	exit()

with open(args.config_file) as fconf:
	try:
		conf = json.load(fconf)
		gen_header = generateSingleHeader(conf)
		
		out_file = ""
		if not args.output_file:
			if 'output_destination' in conf:
				out_file = conf['output_destination'] #using config path
			else:
				print(gen_header) #to STDOUT
				exit()
		else:
			out_file = args.output_file #using argument path

		with open(out_file,'w') as out_header:
			out_header.write(gen_header)
			print('Generated a header file at %s' % out_file)

	except json.decoder.JSONDecodeError:
		print('[Error] Malformed/Invalid JSON in the config')
		exit()
	except:
		print('[Error] Config must be a proper json file.')
		raise
		exit()
