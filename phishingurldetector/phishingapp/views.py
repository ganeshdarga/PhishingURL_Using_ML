


from django.shortcuts import render
import joblib,os
import numpy as np
import pandas as pd
# import MySQLdb
import mysql.connector
from sklearn import metrics 
import warnings
warnings.filterwarnings('ignore')
from feature import FeatureExtraction  # Assuming the FeatureExtraction class is in a file named feature_extraction.py in the same directory as your Django view

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="phishingURL"
)
cursor = conn.cursor()
#pkl

def index(request):
    phish_model = open('templates/model.pkl','rb')
    phish_model_ls = joblib.load(phish_model)
    percent1 = 100
    if request.method == 'GET':  
        y_pred = 0
        search_text = request.GET.get("search_box")
        

        cursor.execute("SELECT * from phishing_sites where phishing_URL = %s",(search_text,))
        row = cursor.fetchall()
        
        if row:
            if row[0][1] == -1:
                y_pred = -1
            elif row[0][1] == 1:
                y_pred = 1
        else:
            if search_text:
                feature_extraction = FeatureExtraction(search_text)
                x = np.array(feature_extraction.getFeaturesList()).reshape(1,30)
                y_pred = phish_model_ls.predict(x)[0]

                y_pro_phishing = phish_model_ls.predict_proba(x)[0,0]
                y_pro_non_phishing = phish_model_ls.predict_proba(x)[0,1]
                print(y_pro_phishing)
                percent1=int(y_pro_non_phishing*100)
        

        if y_pred == 1:
            result = "Secure"
            if not row:
                try:
                    cursor.execute("INSERT INTO phishing_sites (phishing_URL,type) VALUES (%s,%s)", (search_text,1))
                    conn.commit()
                except mysql.connector.IntegrityError:
                    pass
        else:
            result = "NotSecure"
            if not row:
                try:
                    # cursor.execute("INSERT INTO phishing_sites (phishing_URL) VALUES (%s)", (search_text,))
                    cursor.execute("INSERT INTO phishing_sites (phishing_URL,type) VALUES (%s,%s)", (search_text,-1))
                    conn.commit()
                except mysql.connector.IntegrityError:
                    # URL already exists in the blacklist table
                    pass


    return render(request, "index.html", {'search_text':result,'text':search_text,'percent':percent1})

    