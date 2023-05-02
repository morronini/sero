from flask import Flask, render_template, request
import argparse
import uuid
from reasoner import run
from pprint import pprint

app = Flask(__name__)

@app.route('/userinput', methods=['GET', 'POST'])
def userinput():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        form_data = rename(form_data)
        reusable_or_non_reusable = perform_calcs(form_data)
        replacements = {"reusable_or_non_reusable": reusable_or_non_reusable}
        return render_template('result.html', **replacements) #'result.html'
    else:
        return render_template('userinput_custom_05.html') #'userinput_custom.html'

def rename(data):
    rename_map = {
        'q11_heightOf11': 'profile_height_mm',
        ##'q12_widthOf12': '',
        #'q13_thicknessOf': '',
        #'q15_thicknessOf15': '',
        #'q16_widthOf16': '',
        #'q17_areThere': 'No.',
        #'q22_ageOf22': '',
        #'q23_lengthOf': '',
        #'q31_doesThe': 'Yes.',
        #'q41_doesThe41': 'Yes.',
        #'q42_doesThe42': 'Yes.',
        }
    renamed_data = {}
    for key, val in data.items():
        if key in rename_map.keys():
            renamed_data[rename_map[key]] = val
        else:
            renamed_data[key] = val
    return renamed_data


def perform_calcs(form_data):
    pprint(form_data)
    return "MORE INFORMATION NEEDED"
    if form_data["is_reusable"] == "Yes":
        return "REUSABLE"
    elif form_data["is_reusable"] == "No":
        return "NOT REUSABLE"
    else:
        return "MORE INFORMATION NEEDED"

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--deploy", help="In testing just input No", type=str, default="No")
    arguments = parser.parse_args()
    return arguments

if __name__ == "__main__":
  args = parseArguments()
  if args.deploy == "No":
    app.run(debug=True)
  else:
    from waitress import serve
    serve(app, host="0.0.0.1", port=8081)
