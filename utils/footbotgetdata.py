import pandas as pd
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import numpy as np
from unidecode import unidecode


modes=[ "shooting" ,"passing", "passing_types", "gca", "defense","possession","playingtime", "misc"]


def getPlayerData(modes,season="2023-2024"):
    i=0
    master_df=pd.DataFrame()
    for mode in modes:
        url="https://fbref.com/en/comps/Big5/"+season+"/"+mode+"/players/"+season+"-Big-5-European-Leagues-Stats"
        dfs=pd.read_html(url)
        df=dfs[0]
        if i==0:
            new=[]
            for column in df.columns:
                new.append(column[1])
            df.columns=new
            stats_to_drop=['Matches']
            df.drop(columns=stats_to_drop,axis=1,inplace=True)
            master_df=pd.concat([master_df,df],axis=1)
        else:
            new=[]
            for column in df.columns:
                new.append(column[1])
            df.columns=new
            stats_to_drop=['Rk','Player','Nation','Pos', 'Squad', 'Comp', 'Age', 'Born', '90s','Matches']
            df.drop(columns=stats_to_drop, axis=1, inplace=True)

            master_df=pd.concat([master_df,df],axis=1)
    
        i+=1
        

    

    return master_df

def renameCols(df):
    rename=[["Rk","Rk"],
    ["Player","Player"],
    ["Nation","Nation"],
    ["Position","Position"],
    ["Squad","Squad"],
    ["Comp","Competition"],
    ["Age","Age"],
    ["Born","Born"],
    ["90s","90s Played"],
    ["Gls","Goals"],
    ["Sh","Shots Total"],
    ["SoT","Shots on Target"],
    ["SoT%","Shots on Target %"],
    ["Sh/90","Shots per 90"],
    ["SoT/90","Shots on Target per 90"],
    ["G/Sh","Goals per Shot"],
    ["G/SoT","Goals per Shot on Target"],
    ["Dist","Avg Shot Distance"],
    ["FK","Free Kicks"],
    ["PK","Penatly Kicks"],
    ["PKatt","Penalty Kicks Attempted"],
    ["xG","Expected Goals"],
    ["npxG","Non Penalty Expected Goals"],
    ["npxG/Sh","Non Penalty Expected Goals per shot"],
    ["G-xG","Goals - Expected Goals"],
    ["np,G-xG","Non Penalty Goals - Expected Goals"],
    ["Cmp","Total Passes Completed"],
    ["Att","Total Passes Attempted"],
    ["Cmp%","Total Pass Completion %"],
    ["TotDist","Total Passing Distance"],
    ["PrgDist","Progressive Passing Distance"],
    ["Cmp","Short Passes Completed"],
    ["Att","Short Passes Attempted"],
    ["Cmp%","Short Pass Completion %"],
    ["Cmp","Medium Passes Completed"],
    ["Att","Medium Passes Attempted"],
    ["Cmp%","Medium Pass Completion %"],
    ["Cmp","Long Passes Completed"],
    ["Att","Long Passes Attempted"],
    ["Cmp%","Long Pass Completion %"],
    ["Ast","Assists"],
    ["xAG","Expected Assisted Goals"],
    ["xA","Expected Assists"],
    ["A-xAG","Assists - Expected Assisted Goals"],
    ["KP","Key Passes"],
    ["1/3","Passes into Final Third"],
    ["PPA","Passes into Penalty Area"],
    ["CrsPA","Crosses into Penalty Area"],
    ["PrgP","Progressive Passes"],
    ["Att","Total Passes Attempted"],
    ["Live","Live-Ball Passes"],
    ["Dead","Dead-Ball Passes"],
    ["FK","Passes from Free Kicks"],
    ["TB","Through Balls"],
    ["Sw","Switches"],
    ["Crs","Crosses"],
    ["TI","Throw Ins Taken"],
    ["CK","Corner Kicks"],
    ["In","Inswinging Corner Kicks"],
    ["Out","Outswinging Corner Kicks"],
    ["Str","Straight Corner Kicks"],
    ["Cmp","Total Passes Completed"],
    ["Off","Total Passes Offside"],
    ["Blocks","Total Passes Blocked"],
    ["SCA","Shot Creating Actions"],
    ["SCA90","Shot Creating Actions per 90"],
    ["PassLive","SCA Pass Live"],
    ["PassDead","SCA Pass Dead"],
    ["TO","SCA Take Ons"],
    ["Sh","SCA Shot"],
    ["Fld","SCA Fouls Drawn"],
    ["Def","SCA Defensive Actions"],
    ["GCA","Goal Creating Actions"],
    ["GCA90","Goal Creating Actions per 90"],
    ["PassLive","GCA Pass Live"],
    ["PassDead","GCA Pass Dead"],
    ["TO","GCA Take Ons"],
    ["Sh","GCA Shot"],
    ["Fld","GCA Fouls Drawn"],
    ["Def","GCA Defensive Actions"],
    ["Tkl","Tackles"],
    ["TklW","Tackles Won"],
    ["Def 3rd","Tackles in Defensive Third"],
    ["Mid 3rd","Tackles in Middle Third"],
    ["Att 3rd","Tackles in Attacking Third"],
    ["Tkl","Number of Dribblers Tackled"],
    ["Att","Number of Dribbles Challenged"],
    ["Tkl%","Dribblers Tackled %"],
    ["Lost","Dribbled Past"],
    ["Blocks","Total Blocks"],
    ["Sh","Shots Blocked"],
    ["Pass","Passes Blocked"],
    ["Int","Interceptions"],
    ["Tkl+Int","Tackles + Interceptions"],
    ["Clr","Clearances"],
    ["Err","Errors"],
    ["Touches","Touches"],
    ["Def Pen","Touches in Defensive Penalty"],
    ["Def 3rd","Touches in Defensive Third"],
    ["Mid 3rd","Touches in Middle Third"],
    ["Att 3rd","Touches in Attacking Third"],
    ["Att Pen","Touches in Attacking Penalty Area"],
    ["Live","Live Ball Touches"],
    ["Att","Take Ons Attempted"],
    ["Succ","Successful Take Ons"],
    ["Succ%","Successful Take on %"],
    ["Tkld","Times Tackled"],
    ["Tkld%","Tackled %"],
    ["Carries","Number of Carries"],
    ["TotDist","Total Carrying Distance"],
    ["PrgDist","Progressive Carrying Distance"],
    ["PrgC","Progressive Carries"],
    ["1/3","Carries into Final Third"],
    ["CPA","Carries into Penalty Area"],
    ["Mis","Miscontrols"],
    ["Dis","Dispossessed"],
    ["Rec","Passes Received"],
    ["PrgR","Progressive Passes Received"],
    ["MP","Matches Played"],
    ["Min","Minutes Played"],
    ["Mn/MP","Minutes per Match"],
    ["Min%","Total Minutes Played %"],
    ["Starts","Starts"],
    ["Mn/Start","Minutes per Start"],
    ["Compl","Complete Matches Played"],
    ["Subs","Subbed On"],
    ["Mn/Sub","Minutes per Sub"],
    ["unSub","Subbed Off"],
    ["PPM","PPM"],
    ["onG","onG"],
    ["onGA","onGA"],
    ["+/-","Goals +/-"],
    ["+/-90","Goals +/- per 90"],
    ["On-Off","On-Off"],
    ["onxG","onxG"],
    ["onxGA","onxGA"],
    ["xG+/-","xG+/-"],
    ["xG+/-90","xG+/-90"],
    ["On-Off","On-Off"],
    ["CrdY","Yellow Cards"],
    ["CrdR","Red Cards"],
    ["2CrdY","Second Yellows"],
    ["Fls","Fouls Committed"],
    ["Fld","Fouls Drawn"],
    ["Off","Offside"],
    ["Crs","Crs"],
    ["Int","Int"],
    ["TklW","Tackles Won"],
    ["PKwon","Penalty Kicks Won"],
    ["PKcon","Penalty Kicks Converted"],
    ["OG","Own Goals"],
    ["Recov","Loose Balls Recovered"],
    ["Won","Aerials Won"],
    ["Lost","Aerials Lost"],
    ["Won%","Aerials Won %"]]
    
    newCols=[i[1] for i in rename]


    df.columns=newCols

    return df

def clean_master_df(master_df):
    master_df.dropna(subset=['Player'], inplace=True)

    rows,cols=master_df.shape
    for i in range(25,rows,26):
        master_df.drop(index=i,inplace=True)
    master_df['Player'] = master_df['Player'].apply(unidecode)
    master_df['Squad'] = master_df['Squad'].apply(unidecode)

    return master_df

def convertType(df):
    df.fillna(0,inplace=True)
    rows,cols=df.shape
    for i in range(8,cols):
        df.iloc[:,i] = pd.to_numeric(df.iloc[:,i], errors='coerce')
        df.iloc[:,i]=df.iloc[:,i].astype('float')

    return df

def convertToPer90(df):
    columns=df.columns
    cols=df.shape[1]
    for i in range(9,cols):
        if columns[i][-1]!="%":
            df.iloc[:, i] = df.iloc[:, i].div(df['90s Played'], axis=0)
    return df



def getTeamData(season="2023-2024"):
    
    url="https://fbref.com/en/comps/Big5/"+season+"/"+"possession"+"/squads/"+season+"-Big-5-European-Leagues-Stats"

    dfs=pd.read_html(url)
    df=dfs[0]
    newCols=[]
    for i in df.columns:
        newCols.append(i[1])

    df.columns=newCols

    df.iloc[:,4]=df.iloc[:,4].astype('float')

    return df

def addPossData(playerData,teamData):
    possData=teamData[['Squad','Poss']]
    playerData = playerData.merge(possData, on='Squad', how='left')

    return playerData

def filter90s(df):
    df_new = df[df['90s Played'] > 0]
    return df_new

def possAdj(df,stats):
    def sigmoid(x):
        return 2/( 1+np.exp(-0.1*(x-50)))
    df["Poss"]=df["Poss"].apply(lambda x: sigmoid(x))
    for i in stats:
        rows=df.shape[0]
        #print(i)
        for j in range(rows):
            factor=df.loc[j,"Poss"]
            df.loc[j,i]=df.loc[j,i]*factor

    return df

def makeDataset(season):
    modes=[ "shooting" ,"passing", "passing_types", "gca",     
    "defense","possession","playingtime", "misc"]
    

    playerData=getPlayerData(modes,season)
    playerData=clean_master_df(playerData)
    playerData=renameCols(playerData)
    playerData=convertType(playerData)
    playerData=filter90s(playerData)
    playerData=convertToPer90(playerData)
    teamData=getTeamData(season)
    playerData=addPossData(playerData,teamData)
    playerData=possAdj(playerData,def_stats)


    filename="footbot\data\playerReport"+season+".csv"
    playerData.to_csv(filename)

def_stats=   [ ["Tkl","Tackles"],
    ["TklW","Tackles Won"],
    ["Def 3rd","Tackles in Defensive Third"],
    ["Mid 3rd","Tackles in Middle Third"],
    ["Att 3rd","Tackles in Attacking Third"],
    ["Tkl","Number of Dribblers Tackled"],
    ["Att","Number of Dribbles Challenged"],
   # ["Tkl%","Dribblers Tackled %"],
    ["Lost","Dribbled Past"],
    ["Blocks","Total Blocks"],
    ["Sh","Shots Blocked"],
    ["Pass","Passes Blocked"],
    ["Int","Interceptions"],
    ["Tkl+Int","Tackles + Interceptions"],
    ["Clr","Clearances"],
    ["Err","Errors"]]
def_stats=[i[1] for i in def_stats]

'''
seasons=["2021-2022","2022-2023","2023-2024"]
for i in seasons:
  print(f"Making Dataset for {i}")
  makeDataset(i)'''
