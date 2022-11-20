# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from flask import Flask, render_template, redirect, url_for, request
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "6fJrHdujsYQK3EvCJJAkXCylrXC2bAA8oyE3rkKRmkdh"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
@app.route('/')
def home():
    return render_template("main.html")

@app.route("/predict", methods = ['POST'])
def predict():
    gre = request.form["GRE Score"]
    toefl= request.form["TOEFL Score"]
    u_rate= request.form["University Rating"]
    sop= request.form["SOP"]
    lor= request.form["LOR"]
    cgpa= request.form["CGPA"]
    research= request.form["Research"]
    
    pre=[float(gre),float(toefl),float(u_rate),float(sop),float(lor),float(cgpa),float(research)]

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [ 'GRE Score',
                                        'TOEFL Score',
                                        'University Rating',
                                        'SOP',
                                        'LOR ',
                                        'CGPA',
                                        'Research'], "values": [pre]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f8a4a158-7bfb-4930-8694-305ff1860d66/predictions?version=2022-11-20', json=payload_scoring,
                                     headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    pred=response_scoring.json()
    print(pred)
    result = pred['predictions'][0]['values'][0][1][1]

    if pred['predictions'][0]['values'][0][1][1]*100>50:
        return render_template("chance.html", predict=round(pred['predictions'][0]['values'][0][1][1]*100,2))
    else:
        return render_template("nochance.html", predict=round(pred['predictions'][0]['values'][0][1][1]*100,2))


if __name__ == "__main__":
    app.run(debug=True)