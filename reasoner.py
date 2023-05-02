import uuid

import owlready2
from owlready2 import sync_reasoner_pellet, get_ontology
import sqlite3
from os.path import realpath, dirname, join

## Setup Path, Filename, load file
folder_path = dirname(realpath(__file__))
path_dir = join(folder_path, "SERO_ont")
owlready2.JAVA_EXE = join(dirname(dirname(dirname(folder_path))), "usr", "bin", "java")

## Creation of new Indvidual
def new_ind(class_name,individual_name):
    if not isinstance(individual_name, str):
        individual_name = str(individual_name)
    return class_name(individual_name+"_"+str(uuid.uuid4()))

def is_given(di, key):
    if key not in di.keys():
        return False
    elif di[key] == "":
        return False
    else:
        return True

def run_reasoner(args):
    '''
    Inputs:
        args: dictionary with named keys (all data from form)
            - sometimes empty inputs are ignored
            - sometimes they are returned as empty
            Mandatory Fields:

            Optional Fields:

    TODO
        field DamageType only allows 1 input

    '''
    mandatory_fields = [
        "ProfileHeight_mm",
        "ProfileWidth_mm",
        "FlangeThickness_mm",
        "WebThickness_mm",
        "WebHeight_mm",
        "ElementLength_cm",
    ]
    # Load ontology
    if any([i not in args.keys() for i in mandatory_fields]):
        raise ValueError("Not all required fields are contained in the args dict")
    name_onto =  "SERO_Scenario1.rdf"
    onto = get_ontology(join(path_dir,name_onto)).load()

    # Create defaults
    new_RecAudit = onto.ReuseAudit('Audit_'+str(uuid.uuid4()))
    name_new_steelbeam = 'SteelBeam_'+str(uuid.uuid4())
    new_steelbeam = onto.SteelBeam(name_new_steelbeam)
    new_steelbeam.coveredByReuseAudit.append(new_RecAudit)
    new_DamageDocumentation = onto.DamageDocumentation('DamageDocumentation_'+name_new_steelbeam)

    # Object property relation CQ1
    # Data Properties CQ1
    # if there is no entry, no creation of a dataProperty !
    # --> intersting: dataproperties have to be functional to say dataproperty_of_individual = float(5)

    new_steelbeam.hasProfileHeight.append(float(args["ProfileHeight_mm"]))
    new_steelbeam.hasProfileWidth.append(float(args["ProfileWidth_mm"]))
    new_steelbeam.hasFlangeThickness.append(float(args["FlangeThickness_mm"]))
    new_steelbeam.hasWebThickness.append(float(args["WebThickness_mm"]))
    new_steelbeam.hasWebHeight.append(float(args["WebHeight_mm"]))
    new_steelbeam.hasLength.append(float(args["ElementLength_cm"]))

    # Make new_steelbeam subclass of the according profile
    prof_map = {
        "H-Profile": "HProfile",
        "I-Profile": "IProfile",
        "T-Profile": "TProfile",
        "U-Profile": "UProfile",
        "Z-Profile": "ZProfile",
        "L-Profile": "LProfile",
    }
    if "ProfileType_str" in args.keys():
        pass
    elif prof_map["ProfileType_str"] == "Not Known.":
        pass
    else:
        new_steelbeam.is_a.append(getattr(onto, prof_map["ProfileType_str"]))

    # Data Properties CQ2
    if is_given(args, "ElementAge_YY"):
        new_steelbeam.hasAge = float(args["ElementAge_YY"])

    # Damage
    # only if a damage is selected, a new damage should be created
    if is_given(args, "Damages_IO"):
        if args["Damages_IO"] == "Yes.":
            new_damage = onto.Damage("Damage_"+name_new_steelbeam)
            if "DamageType" in args.keys():
                if args["DamageType"] == "Radioactivity":
                    cause_radio = onto.search_one(iri = 'http://www.sero.org/SteelElementReuseOntology#Radiation')
                    new_damage.hasCausation.append(cause_radio)
                    new_steelbeam.hasDamage.append(new_damage)

    # Creation of new INDIVIDUAL
    # if selected in Browser OriginalCEMarking; OriginalMaterialDocumentation; OriginalTestCertificatesDocumentation
    if is_given(args, "OriginalCE"):
        if args["OriginalCE"] == "Yes.":
            new_OriginalCEMarking = onto.OriginalCEMarking('OriginalCEMarking_'+name_new_steelbeam)
            new_steelbeam.hasOriginalCEMarking.append(new_OriginalCEMarking)

    # if selected in Browser OriginalMaterialDocumentation; OriginalTestCertificatesDocumentation
    if is_given(args, "OriginalMaterialDoc"):
        if args["OriginalMaterialDoc"] == "Yes.":
            new_OriginalMaterialDocumentation = onto.OriginalMaterialDocumentation('OriginalMaterialDocumentation_'+name_new_steelbeam)
            new_steelbeam.hasOriginalMaterialDocumentation.append(new_OriginalMaterialDocumentation)

    # if selected in Browser OriginalTestCertificatesDocumentation
    if is_given(args, "OriginalTestCertificatesDoc"):
        if args["OriginalTestCertificatesDoc"] == "Yes.":
            new_OriginalTestCertificatesDocumentation = onto.OriginalTestCertificatesDocumentation('OriginalTestCertificatesDocumentation_'+name_new_steelbeam)
            new_steelbeam.hasOriginalTestCertificatesDocumentation.append(new_OriginalTestCertificatesDocumentation)

    # if selected in Browser NewCEMarking
    if is_given(args, "NewCE"):
        if args["NewCE"] == "Yes.":
            new_NewCEMarking = onto.NewCEMarking('NewCEMarking_'+name_new_steelbeam)
            new_steelbeam.hasNewCEMarking.append(new_NewCEMarking)

    # if selected in Browser ReliabilityTestingDocumentation
    if is_given(args, "ReliabilityTesting"):
        if args["ReliabilityTesting"] == "Yes.":
            new_ReliabilityTestingDocumentation = onto.ReliabilityTestingDocumentation('ReliabilityTestingDocumentation_'+name_new_steelbeam)
            new_steelbeam.hasReliabilityTestingDocumentation.append(new_ReliabilityTestingDocumentation)

    # if selected in Browser AdequacyTestingDocumentation
    if is_given(args, "AdequacyTesting"):
        if args["AdequacyTesting"] == "Yes.":
            new_AdequacyTestingDocumentation = onto.AdequacyTestingDocumentation('AdequacyTestingDocumentation_'+name_new_steelbeam)
            new_steelbeam.hasAdequacyTestingDocumentation.append(new_AdequacyTestingDocumentation)
    print(new_steelbeam)
    print(vars(new_steelbeam))
    with onto:
        sync_reasoner_pellet()
    print(vars(new_steelbeam))

    print("The steel Beam is a :", new_steelbeam.__class__)
    l = []
    for i in onto.SteelBeam.instances():
        l.append(i)
    print(l)
    #onto.save()
    onto.save(file = path_dir + name_onto, format= "rdfxml")

    # use the individual to get displayed results
    results = {
        "type_of_profile": new_steelbeam.cq, # TODO Leo
        "reusable_or_non_reusable": new_steelbeam.cq, # TODO Leo
        "reuse_class": new_steelbeam.cq, # TODO Leo
    }
    return results