Single Header Packer for C/C++

#What is it?
Its a simple script written in Python 3 for assembling a project into a single header for easy use in complex applications. Greatly reduce the complexity of including multiple files and removing conflicts. Adds flexibiliy of developing a complex library in multiple files just like any project but including in with a single header in the end.

#How to use
Your project should contain a configuration JSON file that describes how the files should be ordered in the final header file.

**Example configuration:**
```
{
	"macro": "SIMPLE_WINDOW",
	"output_destination": "single_window.h",
	"public_files": [
		"EventHandler.h",
		"BasicWindowEvents.h",
		"Window.h"
	],
	"implementation_files": [
		"EventHandler.cpp",
		"Window.cpp"
	],
	"footer": [
	],
	"header": [
	]
}
```

Public files are the ones included into the header without having any definitions before them.
Implementation files holds an array of files that implement anything defined in the header.
Header and footer contain files that are shown in a comment at the top or bottom of the final header file respectivly. Usually you add some information about the library in the header and licenses in the footer.

Macro defines the keyword used in the defines used in the final header.

Output destination is not required its used to describe where the script writes the "compiled" header file. This can be added using a parameter to the script depends on how you wanna integrate it in your build environment.

**Sample usage of the script:**

Using the passed parameters loads the config file and outputs at the defined in *-o* path.
```
hpack.py --config_file <path to config> -o <output file>
```


Running without any parameters the script runs the config file named "single_config.json" in the current working directory and outputs it into **STDOUT** ( if no path for the output is defined in the config )

```
hpack.py
```

#Creating a sample config file
```
hpack.py --g
```
Generates a example config in the current working directory the script was ran.

#Requirements
Make sure everything is ordered the correct way in the configuration and avoid using declarations like "extern" to eliminate conficts in the produced header.

#Structure of the final header
```
/*
Header content
*/
#ifndef <MACRO>_PACKED_HEADER
#define <MACRO>_PACKED_HEADER
	//CONTENT OF THE HEADER FILES
#endif

#ifdef <MACRO>_IMPLEMENTATION
	//CONTENT OF THE IMPLEMENTATION FILES
#endif


/*
Footer content
*/
```

#Using the "compiled" header
```
#define <MACRO>_IMPLEMENTATION
#include "final_header.h"
```

All internal includes( those within the project ) are being stripped in the final header. If the script is ran with option *--noh_includes* it does not remove includes in the header files so if there is no "#define <MACRO>_IMPLEMENTATION" you can use it for including all the files of the implementation in the project you add the final header. This gives you the option to have all file and not just a single header (its optional just to give flexibility its really dependent on project structure and usage).


#Credit

This project is inspired by [this website](http://apoorvaj.io/single-header-packer.html). It offers similar functionality in the form of a web app and its also another python script for local usage.

#To be done
- [ ]  Do some hoisting of includes( move all includes of the implementation at the top for readability and to remove duplication of includes )