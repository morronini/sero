import uuid

import owlready2
from owlready2 import sync_reasoner_pellet, get_ontology
import sqlite3
from os.path import realpath, dirname, join

## Setup Path, Filename, load file
folder_path = dirname(realpath(__file__))
path_dir = join(folder_path, "SERO_ont")
owlready2.JAVA_EXE = r'/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java' #join(dirname(dirname(dirname(folder_path))), "usr", "bin", "java")
name_onto = "SERO_Scenario1.rdf"

onto = get_ontology(join(path_dir,name_onto)).load()


#for i in onto.classes():print(i)
#for y in onto.rules(): print(y)
#for x in onto.object_properties(): print(x)
