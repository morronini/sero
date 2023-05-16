import uuid

import owlready2
from owlready2 import sync_reasoner_pellet, get_ontology
import sqlite3
from os.path import realpath, dirname, join

## Setup Path, Filename, load file
folder_path = dirname(realpath(__file__))
path_dir = join(folder_path, "SERO_ont")
#IMPORTANT --> to run the reasoner, please provide the path of you java.exe, or, on windows, uncomment #join(...)
owlready2.JAVA_EXE = r'/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java' #join(dirname(dirname(dirname(folder_path))), "usr", "bin", "java")

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
    new_steelbeam.hasDamageDocumentation.append(new_DamageDocumentation)

    # Object property relation CQ1
    # Data Properties CQ1

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
        new_steelbeam.hasAge = int(args["ElementAge_YY"])

    # DAMAGE - CQ2
    cause_IRI = {
        'Radioactivity': ['http://www.sero.org/SteelElementReuseOntology#Radiation'],  # Radioactivity
        'Deformation': ['http://www.sero.org/SteelElementReuseOntology#Impact',
                        'http://www.sero.org/SteelElementReuseOntology#Fire',
                        'http://www.sero.org/SteelElementReuseOntology#Earthquake'],  # Plastic Deformation
        'Corrosion': ['http://www.sero.org/SteelElementReuseOntology#CorrosiveExposure'],  # Corrosion
        'Cracks': ['http://www.sero.org/SteelElementReuseOntology#Fire',
                   'http://www.sero.org/SteelElementReuseOntology#Impact'],  # Fatigue
        'Wear': ['http://www.sero.org/SteelElementReuseOntology#Wear'],  # Wear, Abrasion
        'Abrasion': ['http://www.sero.org/SteelElementReuseOntology#Wear'],  # Abrasion
        'Embrittlement': ['http://www.sero.org/SteelElementReuseOntology#CorrosiveExposure'],  # Embirttlement
    }

    # only if a damage is selected, a new damage should be created
    if is_given(args, "Damages_IO"):
        if args["Damages_IO"] == "Yes.":
            new_damage = onto.Damage("Damage_"+name_new_steelbeam)
            new_steelbeam.hasDamage.append(new_damage)
            if "DamageType" in args.keys():
                for key in cause_IRI.keys():
                    if args["DamageType"] == key:
                        cause = onto.search_one(iri = str(cause_IRI[key][0]))
                        new_damage.hasCausation.append(cause)

    # REUSE CLASS - CQ3
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

    # Run Reasoner
    with onto:
        sync_reasoner_pellet(debug = 0)

    # print Steelbeam and damage for checking
    print(vars(new_steelbeam))
    if is_given(args, "Damages_IO"):
        if args["Damages_IO"] == "Yes.":
            print(vars(new_damage))

    results_dic = {
        "Name_of_SteelBeam": new_steelbeam.name, #
        "Type_of_Profile": '',
        "Reusability": '',
        "Cause": '',
        "Reuse_Class": '',
        "ProfileHeight_mm":new_steelbeam.hasProfileHeight[0],
        "ProfileWidth_mm":new_steelbeam.hasProfileWidth[0],
        "WebHeight_mm": new_steelbeam.hasWebHeight[0],
        "WebThickness_mm":new_steelbeam.hasWebThickness[0],
        "FlangeThickness_mm" : new_steelbeam.hasFlangeThickness[0],
        "ElementLength_cm": new_steelbeam.hasLength[0],
        "ElementAge_YY": new_steelbeam.hasAge
    }

    # assign Type of Profile
    profiles = prof_map
    inverted_profiles = {v: k for k, v in profiles.items()}

    for i in list(profiles.values()):
        cls = getattr(onto, i, None)
        if cls and cls in new_steelbeam.is_a:
            profile_name = inverted_profiles[i]
            results_dic["Type_of_Profile"] = f'This beam is an {profile_name} steel beam'
            break
    else:
        results_dic["Type_of_Profile"] = 'This beam\'s profile cannot be determined'

    # assign Reusability
    # future to do: create dictionary with damages and causations

    if onto.NonReusableSteelBeam in new_steelbeam.is_a:
        results_dic["Reusability"] = f'This beam is not reusable! Due to: {args["DamageType"]}'
    elif args["Damages_IO"] == "Yes.":
        if "DamageType" in args.keys():
            results_dic["Reusability"] = f'This beam is reusable! Though it has damages: {args["DamageType"]}'
        else:
            results_dic["Reusability"] = f'This beam is reusable! Though it has unidentified damages.'
    else:
        results_dic["Reusability"] = f'This beam should be reusable!'

    # assing Reuse_Class
    #
    if onto.NonReusableSteelBeam in new_steelbeam.is_a:
        results_dic["Reuse_Class"] = f'This beam is not reusable!'
    elif onto.ReuseClassASteelBeam in new_steelbeam.is_a:
        results_dic["Reuse_Class"] = f'This beam is a Reuse Class A steel beam'
    elif onto.ReuseClassBSteelBeam in new_steelbeam.is_a:
        results_dic["Reuse_Class"] = f'This beam is a Reuse Class B steel beam'
    #elif not new_steelbeam.hasDamage:

    else:
        results_dic["Reuse_Class"] = f'This beams Reuse Class cannot be determined. Nevertheless, this beam should be reusable, consider it Reuse Class C!'

    # save ontology
    onto.save(file = join(path_dir,name_onto), format= "rdfxml")

    # use the individual to get displayed results

    return results_dic
