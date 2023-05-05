import uuid

import owlready2
from owlready2 import *
import sqlite3
from os.path import realpath, dirname, join


## Setup Path, Filename, load file
folder_path = dirname(realpath(__file__))
path_dir = join(folder_path, "SERO_ont")
#IMPORTANT --> to run the reasoner, please provide the path of you java.exe, or, on windows, uncomment #join(...)
owlready2.JAVA_EXE = r'/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java' #join(dirname(dirname(dirname(folder_path))), "usr", "bin", "java")
name_onto =  "SERO_Scenario1.rdf"

# Load ontology
onto = get_ontology(join(path_dir,name_onto)).load()

# Create a new world and set it as the default world
world = World()
world.get_ontology(join(path_dir,name_onto)).load()


print(onto.base_iri)
#for i in onto.classes():print(i)
#for y in onto.rules(): print(y)
#for x in onto.object_properties(): print(x)
#for j in onto.individuals(): print(j)

# Perform SPARQL-Quieres

query =  """
    SELECT *
        """

results = list(default_world.sparql(query))

# Process the results
for result in results:
    print("Class:", result.x, "Label:", result.label)


#onto.save(file = join(path_dir,name_onto), format= "rdfxml")
