from flask import Flask, render_template, request
import argparse
import uuid

app = Flask(__name__)

@app.route('/userinput', methods=['GET', 'POST'])
def userinput():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        reusable_or_non_reusable = perform_calcs(form_data)
        replacements = {"reusable_or_non_reusable": reusable_or_non_reusable}
        return render_template('result.html', **replacements) #'result.html'
    else:
        return render_template('userinput_custom_05.html') #'userinput_custom.html'

def perform_calcs(form_data):
    print(form_data)
    if form_data["is_reusable"] == "Yes":
        return "REUSABLE"dddd
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
