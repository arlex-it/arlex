#!/usr/bin/python3

from distutils.dir_util import copy_tree
import os

dir_name = ""
dir_path = ""
endpoint_name = ""
endpoint_path = ""


def endpoint_modifications():
	description = input("Route description: ")
	# Read in the file
	with open(endpoint_path + endpoint_name + ".py", 'r') as file:
		filedata = file.read()

	# Replace the target string
	filedata = filedata.replace('RouteTemplateBusiness', dir_name)
	filedata = filedata.replace('RouteTemplateModels', dir_name)
	filedata = filedata.replace('get_route_template', 'get_' + endpoint_name)
	filedata = filedata.replace('route_template_input', endpoint_name + '_input')
	filedata = filedata.replace('template_namespace', endpoint_name)
	filedata = filedata.replace('template_description', description)
	filedata = filedata.replace('TemplateCollection', dir_name + "Collection")

	# Write the file out again
	with open(endpoint_path + endpoint_name + ".py", 'w') as file:
		file.write(filedata)


def business_modifications():
	with open(dir_path + "business.py", 'r') as file:
		filedata = file.read()

	filedata = filedata.replace('get_route_template', 'get_' + endpoint_name)

	with open(dir_path + "business.py", 'w') as file:
		file.write(filedata)


def models_modifications():
	with open(dir_path + "models.py", 'r') as file:
		filedata = file.read()

	filedata = filedata.replace('route_template_input', endpoint_name + '_input')

	with open(dir_path + "models.py", 'w') as file:
		file.write(filedata)


def main_modifications():
	with open("main.py", 'r') as file:
		filedata = file.read()

	filedata = filedata.replace("# templates import marker",
								"from API."+dir_name+".endpoints."+endpoint_name+" import ns as "+endpoint_name+"\n# templates import marker")
	filedata = filedata.replace("# templates namespace marker",
								"api.add_namespace("+endpoint_name+")\n\t# templates namespace marker")

	with open("main.py", 'w') as file:
		file.write(filedata)


def copy_template_directory():
	from_directory = "route_template/"
	to_directory = "API/"
	copy_tree(from_directory, to_directory)


def rename_process():
	# rename directory
	os.rename("API/RouteTemplate", "API/" + dir_name)
	# rename endpoint
	os.rename(endpoint_path + "route_template.py", endpoint_path + endpoint_name + ".py")


def get_dir_name():
	global dir_name
	global dir_path
	global endpoint_name
	global endpoint_path

	while len(dir_name) == 0:
		dir_name = input("Directory name: ")
		if len(dir_name) == 0:
			print("You have to chose a directory name")

	for i, c in enumerate(dir_name):
		if dir_name[i].isupper():
			if i == 0:
				endpoint_name += dir_name[i].lower()
			else:
				endpoint_name += '_' + dir_name[i].lower()
		else:
			endpoint_name += dir_name[i]
	dir_path = "API/" + dir_name + "/"
	endpoint_path = "API/" + dir_name + "/endpoints/"

	print("directory: '", dir_name, "'")
	print("directory_path: '", dir_path, "'")
	print("endpoint_name: '", endpoint_name, "'")
	print("endpoint_path: '", endpoint_path, "'")


def launcher():
	get_dir_name()
	copy_template_directory()
	rename_process()
	endpoint_modifications()
	business_modifications()
	models_modifications()
	main_modifications()


if __name__ == '__main__':
	launcher()
