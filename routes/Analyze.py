from collections import defaultdict

import math
import multidict
import strip as strip
from flask import request, make_response
from flask.json import jsonify
from flask_cors import CORS, cross_origin

from models.Admin import db
import multidict

from dbconnect import app
from models.data import Call_Logs, Proximity_Logs

cors = CORS(app)

Call_ShadowIDs =[]
Associations= []
Call_Target_Scores=[]
Location_ShadowIDs=[]
Location_Associations=[]
Locations =[]

#Get Targets contacts
def GetCallShaddowIDs(POI,Level):
    print("POI : ",POI)
    ShadowIDs = db.session.query(Call_Logs.ID, Call_Logs.Contact, Call_Logs.Time_of_Contact).filter(Call_Logs.POI==POI)
    for i in ShadowIDs:
        Call_ShadowIDs.append({"ShadowID":i.Contact,"Level":Level,"RankScore":(1/math.pow(2,Level))})
        Associations.append({ 'POI': POI,'Contact':i.Contact })
        #print("Added ",i.Contact)
    return "done"


#Get Target Locations
def GetTargetsLocation(POI, Level):
    print("Location POI : ",POI)
    Temp = db.session.query(Proximity_Logs.Location,Proximity_Logs.POI).filter(Proximity_Logs.POI==POI)
    for i in Temp:
        Locations.append(i.Location)
    return ""

#Get Targets in a Location
def GetLocationShaddowIDs(Location_List,Level):
    print("Location POI : ",Location_List)
    for l in Location_List:
        ShadowIDs = db.session.query(Proximity_Logs.POI).filter(Proximity_Logs.Location==l)
        for i in ShadowIDs:
            Location_ShadowIDs.append({"ShadowID":i.POI,"Level":Level,"RankScore":(1/math.pow(2,Level))})
            #print("Added ",i.POI)
    return "done"

#Calculate Target Scores
def Calculate_Target_Scores(ShadowID_List, SecondaryList):
    Temp=SecondaryList
    for x in ShadowID_List:
        isfound = False
        #Check if list is empty and assign the first item
        if not Temp:
            Temp=[]
            #print("Initial Adding ", x['ShadowID'])
            Temp.append({"ShadowID":x['ShadowID'],"Level":x['Level'],"RankScore":x['RankScore']})
        else:
            for T in Temp:
                #print("Comparing ",T['ShadowID'], " with ",x['ShadowID'])
                if(T['ShadowID']==x['ShadowID']):
                    isfound=True
            if(isfound==True):
                #print("Modifying Scrore of ",T['ShadowID'], "with initial score ",T['RankScore'])
                T['RankScore']=T['RankScore']+x['RankScore']
                isfound = False
            else:
                #print("Adding ",x['ShadowID'], " Level ",x['Level']," Score ",1)
                Temp.append({"ShadowID": x['ShadowID'], "Level": x['Level'], "RankScore": x['RankScore']})
            isfound = False
    return sorted(Temp, key=lambda k: k['RankScore'],reverse=True)





@cross_origin()
@app.route('/analyze')
def analyze():
    Associations.clear()
    Call_ShadowIDs.clear()
    Locations.clear()
    Location_ShadowIDs.clear()
    Location_SID_Scores = []
    POI = request.args.get('POI')
    #Get Initial List of ShadowIDS
    GetCallShaddowIDs(POI,2)
    print("Associations 1")
    for x in Associations:
        print(x['POI'], " Contacted ",x['Contact'])
    print("Scores 1")
    for x in Call_ShadowIDs:
        print(x['ShadowID']," -- ",x['Level']," ---- ",x['RankScore'])

    print("Final Calculation")
    Call_Target_Scores = Calculate_Target_Scores(Call_ShadowIDs,None)
    for x in Call_Target_Scores:
        print(x['ShadowID']," -- ",x['Level']," ---- ",x['RankScore'])

    #
    #Level 3
    print("Going Level 3")
    for i in Call_Target_Scores:
        GetCallShaddowIDs(i['ShadowID'],3)

    print("New Final Calculation")
    Call_Target_Scores = Calculate_Target_Scores(Call_ShadowIDs,None)
    for x in Call_Target_Scores:
        print(x['ShadowID'], " -- ", x['Level'], " ---- ", x['RankScore'])

    x=0
    for i in Call_Target_Scores:
        if(i['ShadowID']==POI):
            Call_Target_Scores.pop(x-1)
            x = x + 1

    print("New List")
    for x in Call_Target_Scores:
        print(x['ShadowID'], " -- ", x['Level'], " ---- ", x['RankScore'])

    # Level 4
    print("Going Level 4")
    for i in Call_Target_Scores:
        GetCallShaddowIDs(i['ShadowID'], 4)

    print("New Final Calculation")
    Target_Scores = Calculate_Target_Scores(Call_ShadowIDs,None)
    for x in Call_Target_Scores:
        print(x['ShadowID'], " -- ", x['Level'], " ---- ", x['RankScore'])


    # Get Location ShadowIDs
    GetTargetsLocation(POI, 1)
    # print("Get ShadowIDs Locations on First Level")
    # for x in Locations:
    #     print(x)

    print("")
    # Get List of ShadowIDs appearing at Locations same as the POI
    GetLocationShaddowIDs(Locations, 1)
    # print("List of ShadowID Gotten from POIs Locations")
    # for S in Location_ShadowIDs:
    #     print("ShadowID ", S['ShadowID'], " Level ", S['Level'], S['RankScore'])

    Location_SID_Scores = Calculate_Target_Scores(Location_ShadowIDs,None)
    print("Location scores")
    for T in Location_SID_Scores:
        print(T['ShadowID'], " -- ", T['Level'], " ---- ", T['RankScore'])

    #newlist = sorted(Call_Target_Scores, key=lambda k: k['RankScore'],reverse=True)

    Combined_Rankings = Calculate_Target_Scores(Call_Target_Scores,Location_SID_Scores)
    print("Combined Rankings")
    for T in Combined_Rankings:
        print(T['ShadowID'], " -- ", T['Level'], " ---- ", T['RankScore'])
    return make_response(jsonify(Location_SID_Scores, Call_Target_Scores,Combined_Rankings))