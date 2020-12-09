from flask import Flask, request, render_template, send_from_directory, jsonify
import sqlite3
from PIL import Image
from Preprocessing import convert_to_image_tensor, invert_image
import torch
from Model import SiameseConvNet, distance_metric
from io import BytesIO
import json
import math


app = Flask(__name__, static_folder='./frontend/build/static', template_folder='./frontend/build')

def load_model():
    device = torch.device('cpu')
    model = SiameseConvNet().eval()
    model.load_state_dict(torch.load('Models/model_large_epoch_20', map_location=device))
    return model


def connect_to_db():
    conn = sqlite3.connect('user_signatures.db')
    return conn


def get_file_from_db(customer_id):
    cursor = connect_to_db().cursor()
    select_fname = """SELECT sign1,sign2,sign3 from signatures where customer_id = ?"""
    cursor.execute(select_fname, (customer_id,))
    item = cursor.fetchone()
    cursor.connection.commit()
    return item


def main():
    CREATE_TABLE = """CREATE TABLE IF NOT EXISTS signatures (customer_id TEXT PRIMARY KEY,sign1 BLOB, sign2 BLOB, sign3 BLOB)"""
    cursor = connect_to_db().cursor()
    cursor.execute(CREATE_TABLE)
    cursor.connection.commit()
    # For heroku, remove this line. We'll use gunicorn to run the app
    app.run() # app.run(debug=True) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file1 = request.files['uploadedImage1']
    file2 = request.files['uploadedImage2']
    file3 = request.files['uploadedImage3']
    customer_id = request.form['customerID']
    print(customer_id)
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = """DELETE FROM signatures where customer_id=?"""
        cursor.execute(query, (customer_id,))
        cursor = conn.cursor()
        query = """INSERT INTO signatures VALUES(?,?,?,?)"""
        cursor.execute(query, (customer_id, file1.read(), file2.read(), file3.read()))
        conn.commit()
        return jsonify({"error": False})
    except Exception as e:
        print(e)
        return jsonify({"error": True})

@app.route('/verify', methods=['POST'])
def verify():
    try:
        customer_id = request.form['customerID']
        input_image = Image.open(request.files['newSignature'])
        input_image_tensor = convert_to_image_tensor(invert_image(input_image)).view(1,1,220,155)
        customer_sample_images = get_file_from_db(customer_id)
        if not customer_sample_images:
            return jsonify({'error':True})
        anchor_images = [Image.open(BytesIO(x)) for x in customer_sample_images]
        anchor_image_tensors = [convert_to_image_tensor(invert_image(x)).view(-1, 1, 220, 155) 
                        for x in anchor_images]
        model = load_model()
        mindist = math.inf
        for anci in anchor_image_tensors:
            f_A, f_X = model.forward(anci, input_image_tensor)
            dist = float(distance_metric(f_A, f_X).detach().numpy())
            mindist = min(mindist, dist)

            if dist <= 0.145139:  # Threshold obtained using Test.py
                return jsonify({"match": True, "error": False, "threshold":"%.6f" % (0.145139), "distance":"%.6f"%(mindist)})
        return jsonify({"match": False, "error": False, "threshold":0.145139, "distance":round(mindist, 6)})
    except Exception as e:
        print(e)
        return jsonify({"error":True})

@app.route("/manifest.json")
def manifest():
    return send_from_directory('./frontend/build', 'manifest.json')

@app.route("/favicon.ico")
def favicon():
    return send_from_directory('./frontend/build', 'favicon.ico')

if __name__=='__main__':
    main()
