import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from utils.footbothelpers import *

def radar(season,inp_player,inp_position):

    #season=input("Enter season")
    filePath="data\playerReport"+season+".csv"

    playerData=pd.read_csv(filePath)

    playerData=playerData.loc[playerData["90s Played"]>=5].reset_index()
    playerData=playerData.iloc[:,1:]
    playerData=playerData.fillna(0)

    playerData=filterPos(playerData,inp_position,positions={"forward":["FW","FW,MF"],"midfielder":["MF","MF,DF","MF,FW"],"defender":["DF,MF","DF"]})
    #inp_player,inp_position=takeInput(playerData)

    stats_dict={

    "forward":["Goals","Non Penalty Expected Goals","Assists","Expected Assisted Goals","Key Passes","Passes into Penalty Area","Shot Creating Actions","Goal Creating Actions","Touches in Attacking Penalty Area","Successful Take Ons","Take Ons Attempted","Carries into Final Third","Carries into Penalty Area","Progressive Passes Received","Aerials Won %"]
    ,
    "midfielder":["Goals","Non Penalty Expected Goals","Expected Assists", "Key Passes", "Passes into Final Third","Progressive Passes","Long Passes Completed","Shot Creating Actions","Tackles Won", "Interceptions","Successful Take Ons","Take Ons Attempted","Progressive Carries","Aerials Won %"]

    }   

    requiredStats=stats_dict[inp_position]

    raw,percentiles=findVals(playerData,requiredStats,inp_player)

    plot(requiredStats,percentiles,raw,inp_player,season)

def findSimilar(season,position,inp_player,num_players):

    #inputting season and player data
    #season=input("Enter season")
    filePath="data\playerReport"+season+".csv"

    playerData=pd.read_csv(filePath)

    playerData=playerData.loc[playerData["90s Played"]>=5].reset_index()
    playerData=playerData.iloc[:,1:]
    playerData=playerData.fillna(0)
    
    #convert all player names to title case

    playerData["Player"]=playerData["Player"].str.title()

    
    positions={"forward":["FW","FW,MF"],"midfielder":["MF","MF,DF","MF,FW"],"defender":["DF,MF","DF"]}

    #inp_position=input("Enter position")

    playerData=filterPos(playerData,position,positions) # preliminary filter based on player position

        
    #Taking input
    '''    
    leagues=playerData["Competition"].unique()

    inp_league=input(f"Enter League from {leagues}")

    tempData=playerData.loc[playerData["Competition"]==inp_league]

    teams=tempData["Squad"].unique()

    inp_team=input(f"Enter team from {teams}")

    tempData=tempData.loc[tempData["Squad"]==inp_team]

    players=tempData["Player"].unique()
    inp_pl=input(f"Enter player name from {players}")'''


    #Preparing df which contains position specific stats
    stats_dict={

    "forward":["Goals","Non Penalty Expected Goals","Assists","Expected Assisted Goals","Key Passes","Passes into Penalty Area","Shot Creating Actions","Goal Creating Actions","Touches in Attacking Penalty Area","Successful Take Ons","Take Ons Attempted","Carries into Final Third","Carries into Penalty Area","Progressive Passes Received","Aerials Won"]
    ,
    "midfielder":["Goals","Non Penalty Expected Goals","Expected Assists", "Key Passes", "Passes into Final Third","Progressive Passes","Long Passes Completed","Shot Creating Actions","Tackles Won", "Interceptions","Successful Take Ons","Take Ons Attempted","Progressive Carries","Aerials Won"]

    }
    requiredStats=stats_dict[position]
    requiredStats.insert(0,"Player")
    scoutData=playerData.loc[:,requiredStats].reset_index()

    #normalizing stats (all stats need to be between 0 and 1, else some may outweigh the other)
    for i in scoutData.columns:
        if scoutData[i].dtype=='float64':
            scoutData[i]=scoutData[i]/scoutData[i].max()


    #scoutData=scoutData.iloc[:,2:].to_numpy()
    #print(scoutData.shape)
    #scoutData.loc[scoutData["Player"]=="Rafael Leao"]

    
    players=euclidean_dist(scoutData,inp_player)

    sorted_dict = sorted([(value, key) for (key, value) in players.items()])
    
    sorted_dict=[f"{i+1}. {sorted_dict[i][1]}" for i in range(num_players)]
    return sorted_dict


