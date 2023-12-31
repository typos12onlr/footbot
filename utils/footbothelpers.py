import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def takeInput(playerData):

    
    positions={"forward":["FW","MF,FW","FW,MF"],"midfielder":["MF","MF,DF","FW,MF"],"defender":["DF,MF","DF"]}

    inp_position=input("Enter position")


    playerData = playerData[playerData["Position"].str.contains('|'.join(positions[inp_position]))]

    leagues=playerData["Competition"].unique()
    userleagues=leagues
    
    inp_league=input(f"Enter League from {leagues}")
    
    tempData=playerData.loc[playerData["Competition"]==inp_league]

    teams=tempData["Squad"].unique()

    inp_team=input(f"Enter team from {teams}")

    tempData=tempData.loc[tempData["Squad"]==inp_team]

    players=tempData["Player"].unique()
    inp_pl=input(f"Enter player name from {players}")
    return inp_pl,inp_position


def findVals(playerData,requiredStats,inp_player):

    percentiles=[]
    raw=[]

    for i in requiredStats:
        rawdata=playerData[i].values

        playerstats=playerData.loc[playerData["Player"]==inp_player]
        playerstat=playerstats[i].values

        percentile_score=stats.percentileofscore(rawdata,playerstat)

        percentiles.append(percentile_score)
        raw.append(playerstat)

    percentiles=[i[0] for i in percentiles]
    raw=[i[0] for i in raw]

    return raw, percentiles

def plot(requiredStats,percentiles,raw,inp_player,season):

    #plot(requiredStats,percentiles,raw,inp_player,season)
    namelist=[inp_player]
    perclist=[percentiles]
    rawlist=[raw]
    fig= plt.figure(figsize = (16,9))
    ax = plt.subplot(121, polar=True)
    #fig.set_facecolor(bgcolor.value)
    #ax.patch.set_facecolor(bgcolor.value)
    ax.set_rorigin(-20)

    if len(namelist)==1:
        plt.title(label=f"{namelist[0]} | {season}",loc="center",fontdict={'size':20},y=1.15)
    else:
        plt.title(label=f"{namelist[0]} vs {namelist[1]} | {season}",loc="center",fontdict={'size':20},y=1.15)
    
    for i in range(1):
        percentiles=perclist[i]
        raw=rawlist[i]
        arr1 = np.asarray(percentiles)
        #arr2 = np.asarray(p2vals)
        N = len(perclist[i])
        bottom = 0.0
        theta, width = np.linspace(0.0, 2 * np.pi, N, endpoint=False, retstep=True)

        
        bars = ax.bar(
            theta, height=arr1,
            width=width,
            bottom=bottom,
            #color=c1.value, edgecolor="w",zorder=1,
            linewidth=1,
            alpha=0.4
        )


        ax.set_thetagrids((theta+width/2)* 180 / np.pi)
        ax.set_rticks(np.arange(0.0, 120.0, 20.0))
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location("N")

        ax.grid(zorder=10.0,color='black', linestyle='--', linewidth=0.5)

        ax.spines['polar'].set_visible(True)

        ticks = [i for i in requiredStats]
        ax.set_xticklabels([])

        rotations = np.rad2deg(theta)
        for x, bar, rotation, label in zip(theta, bars, rotations, ticks):
            lab = ax.text(x,105,label,ha='center', va='center',
                        rotation=-rotation,rotation_mode='anchor',fontsize=7,
                        )   
        ax.spines["polar"].set_color('black')
        ax.spines["polar"].set_linewidth(1)
        ax.set_ylim(0,100)
        ax.set_yticklabels([])


    requiredStats=["Player"]+requiredStats
    table_data=[]
    for i in range(1):
        percentiles=perclist[i]
        raw=rawlist[i]
        x=[str(round(i,2))+" ("+str(round(j,2))+")" for i,j in zip(raw,percentiles)]
        if i==0:
            x.insert(0,namelist[i]+" (Blue)")
        else:
            x.insert(0,namelist[i]+" (Orange)")
        table_data.append(x)

    ax_table = plt.subplot(122)  # Create a new subplot for the table
    ax_table.axis('off')  # Turn off axis for the table


    table_data=np.array(table_data).transpose()


    table = ax_table.table(cellText=table_data, cellLoc='center', loc='center', rowLabels=requiredStats)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)  # Adjust scaling as needed for your layout

   

    filename="player_radar.png"
    plt.tight_layout()
    plt.savefig(filename)




def plotSingle():

    season=input("Enter season")
    filePath="footbot\data\playerReport"+season+".csv"

    playerData=pd.read_csv(filePath)

    playerData=playerData.loc[playerData["90s Played"]>=5]
    playerData=playerData.fillna(0)

    inp_player,inp_position=takeInput(playerData)

    stats_dict={

    "forward":["Goals","Non Penalty Expected Goals","Assists","Expected Assisted Goals","Key Passes","Passes into Penalty Area","Shot Creating Actions","Goal Creating Actions","Touches in Attacking Penalty Area","Successful Take Ons","Take Ons Attempted","Carries into Final Third","Carries into Penalty Area","Progressive Passes Received","Aerials Won"]
    ,
    "midfielder":["Goals","Non Penalty Expected Goals","Expected Assists", "Key Passes", "Passes into Final Third","Progressive Passes","Long Passes Completed","Shot Creating Actions","Tackles Won", "Interceptions","Successful Take Ons","Take Ons Attempted","Progressive Carries","Aerials Won"],

    "defender" :["Passes into Final Third", "Passes into Penalty Area","Expected Assists","Carries into Final Third","Successful Take Ons","Successful Take on %","Dribbled Past","Progressive Carries","Progressive Passes","Aerials Won %","Tackles","Interceptions","Dribblers Tackled %"]
} 

    requiredStats=stats_dict[inp_position]

    raw,percentiles=findVals(playerData,requiredStats,inp_player)

    plot(requiredStats,percentiles,raw,inp_player,season)

def filterPos(playerData,inp_position,positions={"forward":["FW","FW,MF"],"midfielder":["MF","MF,DF","MF,FW"],"defender":["DF,MF","DF"]}):
    condition=(positions[inp_position])
    #print(condition)
    count=0
    indices_to_drop=[]
    for i in range(playerData.shape[0]):
        x=playerData.loc[i,"Position"]
        
        if x not in condition:
            indices_to_drop.append(i)

    playerData.drop(indices_to_drop,inplace=True)
    playerData=playerData.reset_index()
    playerData=playerData.iloc[:,1:]
    #playerData=playerData[playerData["Position"]!="FW,MF"]
    #playerData
    return playerData

#define euclidean distance function
def euclidean_dist(target_df,player):
    count=0
    scores={}
    #  print(target_df.shape,target_df.loc[target_df["Player"]=='Rafael Leao'])
    target_arr=target_df.loc[target_df["Player"]==player]
    target_arr=target_arr.iloc[:,2:].to_numpy()  #select target player's stats in a np arr
    
    for i in range(target_df.shape[0]):

        if target_df.loc[i,"Player"]!=player:    #if player is not target player
            count+=1
            test_arr=target_df.iloc[i,2:].to_numpy()    #select player's stats in an np arr
            euclidean_dist=np.linalg.norm(target_arr-test_arr)   #calc dist
            
            scores[target_df.loc[i,"Player"]]=euclidean_dist     #append scores

    return scores

def plotTwo(perclist,rawlist,namelist,requiredStats,season):
    fig= plt.figure(figsize = (16,9))
    ax = plt.subplot(121, polar=True)
    #fig.set_facecolor(bgcolor.value)
    #ax.patch.set_facecolor(bgcolor.value)
    ax.set_rorigin(-20)

    plt.title(label=f"{namelist[0]} vs {namelist[1]} | {season}",loc="center",fontdict={'size':20},y=1.15)
    
    for i in range(2):
        percentiles=perclist[i]
        raw=rawlist[i]
        arr1 = np.asarray(percentiles)
        #arr2 = np.asarray(p2vals)
        N = len(percentiles)
        bottom = 0.0
        theta, width = np.linspace(0.0, 2 * np.pi, N, endpoint=False, retstep=True)

        
        bars = ax.bar(
            theta, height=arr1,
            width=width,
            bottom=bottom,
            #color=c1.value, edgecolor="w",zorder=1,
            linewidth=1,
            alpha=0.4
        )


        ax.set_thetagrids((theta+width/2)* 180 / np.pi)
        ax.set_rticks(np.arange(0.0, 120.0, 20.0))
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location("N")

        ax.grid(zorder=10.0,color='black', linestyle='--', linewidth=0.5)

        ax.spines['polar'].set_visible(True)

        ticks = [i for i in requiredStats]
        ax.set_xticklabels([])

        rotations = np.rad2deg(theta)
        for x, bar, rotation, label in zip(theta, bars, rotations, ticks):
            lab = ax.text(x,105,label,ha='center', va='center',
                        rotation=-rotation,rotation_mode='anchor',fontsize=7,
                        )   
        ax.spines["polar"].set_color('black')
        ax.spines["polar"].set_linewidth(1)
        ax.set_ylim(0,100)
        ax.set_yticklabels([])


    requiredStats=["Player"]+requiredStats
    table_data=[]
    for i in range(2):
        percentiles=perclist[i]
        raw=rawlist[i]
        x=[str(round(i,2))+" ("+str(round(j,2))+")" for i,j in zip(raw,percentiles)]
        if i==0:
            x.insert(0,namelist[i]+" (Blue)")
        else:
            x.insert(0,namelist[i]+" (Orange)")
        table_data.append(x)

    ax_table = plt.subplot(122)  # Create a new subplot for the table
    ax_table.axis('off')  # Turn off axis for the table


    table_data=np.array(table_data).transpose()


    table = ax_table.table(cellText=table_data, cellLoc='center', loc='center', rowLabels=requiredStats)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)  # Adjust scaling as needed for your layout

   

    filename="player_radar.png"
    plt.tight_layout()
    plt.savefig(filename)
    
