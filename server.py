from flask import Flask, request, jsonify
import psycopg2
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
import tempfile
from scipy.io import wavfile
from pyspark.sql import SparkSession, functions as F
import os
import numpy as np

app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Certificate Authority Server", 200
    
@app.route('/frequency_analysis', methods=['POST'])
def frequency_analysis():
    file = request.files['file']
    if not file:
        return jsonify({"status": "failure", "error": "No file uploaded"}), 400

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file.save(tmp)
        tmp_path = tmp.name

    # Read wav file
    fs, data = wavfile.read(tmp_path)
    os.remove(tmp_path)

    # Create a Spark DataFrame
    rdd = spark.sparkContext.parallelize(data)
    df = spark.createDataFrame(rdd.map(lambda x: (int(x),)), ["amplitude"])

    # Perform frequency analysis to get amplitude frequencies
    freq_df = df.groupBy("amplitude").agg(F.count("amplitude").alias("frequency"))

    # Perform FFT to find frequency peaks
    freq_data = np.fft.fft(data)
    freq_magnitude = np.abs(freq_data)
    freq_peaks = np.argpartition(freq_magnitude, -4)[-4:]
    freq_peaks_sorted = freq_peaks[np.argsort(freq_magnitude[freq_peaks])][::-1]

    # Assuming the serial number is embedded as a sequence of peaks
    serial_number = ''.join(map(str, freq_peaks_sorted))

    return jsonify({"frequencies": serial_number}), 200
# Database connection
try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        database="mydatabase",
        user="myuser",
        password="mypassword"
    )
    print("Database connected successfully.")  # Debug line
except Exception as e:
    print(f"An error occurred while connecting to the database: {e}")

def authenticate_device(device_id, password):
    try:
        cur = conn.cursor()
        cur.execute("SELECT password FROM devices WHERE device_id = %s;", (device_id,))
        db_password = cur.fetchone()
        print(f"Database password for {device_id}: {db_password}")  # Debug line
        if db_password and db_password[0] == password:
            return True
    except Exception as e:
        print(f"An error occurred in authenticate_device: {e}")
        conn.rollback()
    return False

    
def generate_device_certificate(device_id):
    # Generate key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Generate a self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"MyCompany"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).sign(private_key, hashes.SHA256(), default_backend())

    # Serialize certificate to PEM format
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    return cert_pem.decode('utf-8')

@app.route('/generate_certificate', methods=['POST'])
def generate_certificate():
    data = request.json
    print(f"Received data: {data}")  # Debug line
    device_id = data.get('device_id')
    password = data.get('password')
    
    if authenticate_device(device_id, password):
        certificate = generate_device_certificate(device_id)
        return jsonify({"status": "success", "certificate": certificate}), 200
    else:
        return jsonify({"status": "failure", "error": "Authentication failed"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

