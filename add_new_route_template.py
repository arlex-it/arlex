from distutils.dir_util import copy_tree
import os


def copy_template_directory():
	from_directory = "route_template/"
	to_directory = "API/"
	copy_tree(from_directory, to_directory)


def rename_endpoint(dir_name):
	new_name = ""
	endpoint_path = "API/" + dir_name + "/endpoints/"
	for i, c in enumerate(dir_name):
		if dir_name[i].isupper():
			if i == 0:
				new_name += dir_name[i].lower()
			else:
				new_name += '_' + dir_name[i].lower()
		else:
			new_name += dir_name[i]
	new_name += ".py"
	os.rename(endpoint_path + "route_template.py", endpoint_path + new_name)


def rename_process():
	dir_name = ""
	while len(dir_name) == 0:
		dir_name = input("Directory name: ")
		if len(dir_name) == 0:
			print("You have to chose a directory name")
	os.rename("API/RouteTemplate", "API/" + dir_name)
	rename_endpoint(dir_name)


def launcher():
	copy_template_directory()
	rename_process()


if __name__ == '__main__':
	launcher()
