from flask import Flask, request, render_template
import json
import boto3
from werkzeug.utils import secure_filename
textractclient = boto3.client("textract", aws_access_key_id="AKIAYRVCKL2B4FBREBWO",
                              aws_secret_access_key="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", region_name="us-east-2")
s3 = boto3.client('s3',
                    aws_access_key_id="ASIARAVRXUFNALU5QDGA",
                    aws_secret_access_key="4D+O/QtaIImUeBaIqAjLLlI50oqQnqGVrHMdUiqS",
                    aws_session_token="FwoGZXIvYXdzENj//////////wEaDIeyW6qOiQgg1ERYmiLCAWhQ0DGpHLcD7JZGbkFcnrGiyvADfsF4TUXGWdeTQUw0STzjjO+W6pyyV9IsazbaTiaLshCEYhgPNt3alsZjxsGgP/sw8gclvK03nKTYGrDUPqpbxsNp3YD5VOdg5t6GETLzx1lBIO4yXl/8SEmUW0csVp2FCW7FLDqGLl9DJzlZE8PVbPGXUNSdN3jqHXw/bKDb9ZQMPp6QaG2AHd/awC26SnAD5aQBPqQwYDMwT9BCPZHniYefYoOtR93afbpEL1NSKMjUwYkGMi394ktE2answHRaqzsMvJqqxYexXdFa47444GG/XzuqLOx7L7x4ILUnfIwcbPw="
                     )
app = Flask(__name__)
@app.route("/", methods=["GET"])
def main():
    return render_template("index.html", jsonData=json.dumps({}))
@app.route("/english",methods=["GET"])
def english():
    return render_template("english.html" ,jsonData=json.dumps({}))
@app.route("/italiana",methods=["GET"])
def italiana():
    return render_template("italiana.html" ,jsonData=json.dumps({}))
@app.route("/german",methods=["GET"])
def german():
    return render_template("german.html" ,jsonData=json.dumps({}))
@app.route("/espanol",methods=["GET"])
def espanol():
    return render_template("spanish.html" ,jsonData=json.dumps({}))
@app.route("/french",methods=["GET"])
def french():
    return render_template("french.html" ,jsonData=json.dumps({}))
@app.route("/portugese",methods=["GET"])
def portugese():
    return render_template("portuguese.html" ,jsonData=json.dumps({}))   
@app.route("/extract", methods=["POST"])
def extractImage():
    file = request.files.get("filename")
    binaryFile = file.read()
    response = textractclient.detect_document_text(
        Document={
            'Bytes': binaryFile
        }
    )
    extractedText = ""
    for block in response['Blocks']:
        if block["BlockType"] == "LINE":
            # print('\033[94m' + item["Text"] + '\033[0m')
            extractedText = extractedText+block["Text"]+" "
    responseJson = {
        "text": extractedText
    }
    print(responseJson)
    return render_template("english.html", jsonData=json.dumps(responseJson))
BUCKET_NAME='easyextractwebsite'
@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
                msg = "Upload Done ! "
    return render_template("index.html",msg =msg)
app.run("0.0.0.0", port=5000, debug=True)