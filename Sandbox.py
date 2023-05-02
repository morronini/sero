import uuid

import owlready2
from owlready2 import *
import sqlite3
from os.path import realpath, dirname

## Setup Path, Filename, load file
folder_path = dirname(realpath(__file__))
path_dir = folder_path+"SERO_ont/"
owlready2.JAVA_EXE = 'C:/Program Files/Java/jre1.8.0_351/bin/java'

name_onto =  "SERO_Scenario1.rdf"
onto = get_ontology(path_dir+name_onto).load()

#%% Functions

## Creation of new Indvidual
def new_ind(class_name,individual_name):
    if not isinstance(individual_name, str):
        individual_name = str(individual_name)
    return class_name(individual_name+"_"+str(uuid.uuid4()))

#%% Print IRI of Ontology
print(onto.base_iri)
#%% Print Data Properties of imported ontology
for i in list(onto.data_properties()): print(i)
#%% Print Object Properties aof imported ontology
for i in list(onto.object_properties()): print(i)
#%% Print Classes of imported ontology
for i in list(onto.classes()): print(i)
#%% Print all Individuals of imported ontology
for i in list(onto.individuals()): print(i)
#%% Creation of new Individuals Audit
new_RecAudit = onto.ReuseAudit('Audit_'+str(uuid.uuid4()))

#%% Competency Question 1
# Creation of new INDIVIDUALS CQ1
# SteelBeam
name_new_steelbeam = 'SteelBeam_'+str(uuid.uuid4())
new_steelbeam = onto.SteelBeam(name_new_steelbeam)

# Object property relation CQ1
new_steelbeam.coveredByReuseAudit.append(new_RecAudit)
# Data Properties CQ1
# if there is no entry, no creation of a dataProperty !
# --> intersting: dataproperties have to be functional to say dataproperty_of_individual = float(5)

new_steelbeam.hasProfileHeight.append(float(5))
new_steelbeam.hasProfileWidth.append(float(5))
new_steelbeam.hasFlangeThickness.append(float(5))
new_steelbeam.hasWebThickness.append(float(5))
new_steelbeam.hasWebHeight.append(float(5))
new_steelbeam.hasLength.append(float(5))

# Make new_steelbeam subclass of the according profile
"""new_steelbeam.is_a.append(onto.HProfile)
new_steelbeam.is_a.append(onto.IProfile)
new_steelbeam.is_a.append(onto.TProfile)
new_steelbeam.is_a.append(onto.UProfile)
new_steelbeam.is_a.append(onto.ZProfile)
new_steelbeam.is_a.append(onto.LProfile)"""

#%% Competency Question 2
# Data Properties CQ2
new_steelbeam.hasAge = float(53)

# Damage Documentation
new_DamageDocumentation = onto.DamageDocumentation('DamageDocumentation_'+name_new_steelbeam)

# Damage
# only if a damage is selected, a new damage should be created
new_damage = onto.Damage("Damage_"+name_new_steelbeam)

# Damage
cause_radio = onto.search_one(iri = 'http://www.sero.org/SteelElementReuseOntology#Radiation')
new_damage.hasCausation.append(cause_radio)
new_steelbeam.hasDamage.append(new_damage)

#%% Competency Question 3
# Creation of new DATA PROPERTIES
#None

# Creation of new INDIVIDUAL
# if selected in Browser OriginalCEMarking; OriginalMaterialDocumentation; OriginalTestCertificatesDocumentation
new_OriginalCEMarking = onto.OriginalCEMarking('OriginalCEMarking_'+name_new_steelbeam)
new_steelbeam.hasOriginalCEMarking.append(new_OriginalCEMarking)

# if selected in Browser OriginalMaterialDocumentation; OriginalTestCertificatesDocumentation
new_OriginalMaterialDocumentation = onto.OriginalMaterialDocumentation('OriginalMaterialDocumentation_'+name_new_steelbeam)
new_steelbeam.hasOriginalMaterialDocumentation.append(new_OriginalMaterialDocumentation)

# if selected in Browser OriginalTestCertificatesDocumentation
new_OriginalTestCertificatesDocumentation = onto.OriginalTestCertificatesDocumentation('OriginalTestCertificatesDocumentation_'+name_new_steelbeam)
new_steelbeam.hasOriginalTestCertificatesDocumentation.append(new_OriginalTestCertificatesDocumentation)

# if selected in Browser NewCEMarking
new_NewCEMarking = onto.NewCEMarking('NewCEMarking_'+name_new_steelbeam)
new_steelbeam.hasNewCEMarking.append(new_NewCEMarking)

# if selected in Browser ReliabilityTestingDocumentation
new_ReliabilityTestingDocumentation = onto.ReliabilityTestingDocumentation('ReliabilityTestingDocumentation_'+name_new_steelbeam)
new_steelbeam.hasReliabilityTestingDocumentation.append(new_ReliabilityTestingDocumentation)

# if selected in Browser AdequacyTestingDocumentation
new_AdequacyTestingDocumentation = onto.AdequacyTestingDocumentation('AdequacyTestingDocumentation_'+name_new_steelbeam)
new_steelbeam.hasAdequacyTestingDocumentation.append(new_AdequacyTestingDocumentation)

#%% Run Reasoner
with onto:
    sync_reasoner_pellet()

print("The steel Beam is a :", new_steelbeam.__class__)
#%% Delete all individuals of the class Steelbeam
#destroy_entity()


#%% Iterater through all instances of a class
l = []
for i in onto.SteelBeam.instances():
    l.append(i)

print(l)

#%% Save ontology
#onto.save()
onto.save(file = path_dir + name_onto, format= "rdfxml")
