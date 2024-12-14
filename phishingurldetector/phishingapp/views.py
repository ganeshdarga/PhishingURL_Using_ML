
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

from rest_framework import status


import datetime
from rest_framework.decorators import action
import pickle as pkl

from phishingapp.models import phishing
from phishingapp.serializers import phishingSerializers
from django.shortcuts import render
import joblib,os
import numpy as np
import pandas as pd
# import MySQLdb
import psycopg2
import mysql.connector
from sklearn import metrics 
import warnings
warnings.filterwarnings('ignore')
from feature import FeatureExtraction  # Assuming the FeatureExtraction class is in a file named feature_extraction.py in the same directory as your Django view



class phishingViewSet(viewsets.ModelViewSet):
    queryset = phishing.objects.all()
    serializer_class = phishingSerializers

    @action(detail=False, methods=['post'])
    def addphishing(self,request):
        addPhishing = request.data.get("addPhishing")
        addType = request.data.get("addType")

        try:
            new_request = phishing.objects.create(phishing_URL=addPhishing,type=addType)
            serializer = phishingSerializers(new_request,cotext={'request':request})
            return Response(phishingSerializers(new_request).data,status=201)
        except Exception as e:
            print(e)
            return Response({"message":'unable to set data'},status=400)



def index(request):
    phish_model = open('templates/model.pkl','rb')
    phish_model_ls = joblib.load(phish_model)
    percent1 = 100
    result = ""

    search_text = request.GET.get("search_box")
    if search_text:  
        site = phishing.objects.filter(phishing_URL=search_text).first()
        
        
        if site:
            y_pred = site.type
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
            if not site:
                phishing.objects.create(phishing_URL=search_text, type=1)
                
        else:
            result = "NotSecure"
            if not site:
                phishing.objects.create(phishing_URL=search_text, type=-1)


    return render(request, "index.html", {'search_text':result,'text':search_text,'percent':percent1})

    