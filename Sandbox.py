import uuid

import owlready2
from owlready2 import sync_reasoner_pellet, get_ontology
import sqlite3
from os.path import realpath, dirname, join

## Setup Path, Filename, load file
folder_path = dirname(realpath(__file__))
path_dir = join(folder_path, "SERO_ont")
owlready2.JAVA_EXE = r'/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java' #join(dirname(dirname(dirname(folder_path))), "usr", "bin", "java")
name_onto =  "SERO_Scenario1.rdf"

onto = get_ontology(path_dir+name_onto).load()

for i in onto.data_properties():
    print(str(i) + " has " + str(i.range))
"""print(onto.hasProfileHeight.domain)
print(onto.hasProfileHeight.range)
"""
"""#%% Print IRI of Ontology
print(onto.base_iri)
#%% Print Data Properties of imported ontology
for i in list(onto.data_properties()): print(i)
#%% Print Object Properties aof imported ontology
for i in list(onto.object_properties()): print(i)
#%% Print Classes of imported ontology
for i in list(onto.classes()): print(i)
#%% Print all Individuals of imported ontology
for i in list(onto.individuals()): print(i)"""

"""new_steelbeam.hasProfileHeight.append()
new_steelbeam.hasProfileWidth.append(float(5))
new_steelbeam.hasFlangeThickness.append(float(5))
new_steelbeam.hasWebThickness.append(float(5))
new_steelbeam.hasWebHeight.append(float(5))
new_steelbeam.hasLength.append(float(5))
"""

"""#%% Run Reasoner
with onto:
    sync_reasoner_pellet()"""

"""#onto.save()
onto.save(file = path_dir + name_onto, format= "rdfxml")"""
