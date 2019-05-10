from flask import Flask, request, render_template
import sqlite3
from PIL import Image
from Preprocessing import convert_to_image_tensor, invert_image
import torch
from Model import SiameseConvNet, distance_metric
from io import BytesIO

app = Flask(__name__)


def load_model():
    device = torch.device('cpu')
    model = SiameseConvNet().eval()
    model.load_state_dict(torch.load('Models/model_large_epoch_20', map_location=device))
    return model


def connect_to_db():
    conn = sqlite3.connect('user_signatures.db')
    cursor = conn.cursor()
    return cursor


def get_file_from_db(customer_id):
    cursor = connect_to_db()
    select_fname = """SELECT file from signatures where customer_id = ?"""
    cursor.execute(select_fname, (customer_id,))
    item = cursor.fetchone()
    file = item[0]
    cursor.connection.commit()
    return file


def main():
    CREATE_TABLE = """CREATE TABLE IF NOT EXISTS signatures  (customer_id TEXT,file BLOB)"""
    cursor = connect_to_db()
    cursor.execute(CREATE_TABLE)
    cursor.connection.commit()
    app.run()


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('signature')
        print('Added')
        id = request.form.get('customer_id')
        print("filename={}, id={}".format(file.filename, id))
        insert_query = """INSERT INTO signatures VALUES(?, ?)"""
        cursor = connect_to_db()
        cursor.execute(insert_query, (id, file.read()))
        cursor.connection.commit()
        return render_template('upload.html', result="<h6>File uploaded successfully</h6>")
    else:
        return render_template('upload.html', result='')


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        file = request.files.get('signature')
        id = request.form.get('customer_id')
        X = Image.open(file.stream)
        X = convert_to_image_tensor(invert_image(X)).view(1, 1, 220, 155)
        anchor_img_file = get_file_from_db(id)
        A = Image.open(BytesIO(anchor_img_file))
        A = convert_to_image_tensor(invert_image(A)).view(1, 1, 220, 155)
        model = load_model()
        f_A, f_X = model.forward(A, X)
        dist = distance_metric(f_A, f_X).detach().numpy()
        print('Dist={}'.format(dist))
        if dist <= 0.145139:  # Threshold obtained using Test.py
            return render_template('verify.html', result="<h6>Signatures are the same</h6>")
        else:
            return render_template('verify.html', result="<h6>Signatures are different</h6>")
    else:
        return render_template('verify.html', result='')


@app.route('/')
def home():
    return render_template('home.html')


main()
