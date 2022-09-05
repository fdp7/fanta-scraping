from this import d
import pandas as pd
import pulp
import os
 
# creating a data frame
season_0 = "2022-23/2022-23.csv"
season_1 = "2021-22/2021-22.csv"
season_2 = "2020-21/2020-21.csv"

# matches currently played in season_0
giornate_correnti = 5

# take season_0 stats
df_0 = pd.read_csv(season_0)
team_0 = df_0["Squadra"]
fm_0 = df_0["FM"]
player_0 = df_0["Calciatore"]
role_0 = df_0["Ruolo"]
games_0 = df_0["Partite Giocate"]
team_0 = df_0["Squadra"]
mv_0 = df_0["MV"]
amm_0 = df_0["Ammonizioni"]
esp_0 = df_0["Espulsioni"]
rig_0 = df_0["Rigori"]
rp_0 = df_0["Rigori Parati"]
gs_0 = df_0["Gol Subiti"]
qa_0 = df_0["QA"].apply(lambda x: float(x))
cost_0 = df_0['ExpectedCost_1000'].apply(lambda x: float(x)/2) # take expected cost on 500 credits

# take season_1 stats
df_1 = pd.read_csv(season_1)
df_1 = df_1.loc[df_1["Calciatore"].isin(df_0["Calciatore"])] # take only current players stats
team_1 = df_1["Squadra"]
fm_1 = df_1["FM"]
player_1 = df_1["Calciatore"]
role_1 = df_1["Ruolo"]
games_1 = df_1["Partite Giocate"]
team_1 = df_1["Squadra"]
mv_1 = df_1["MV"]
amm_1 = df_1["Ammonizioni"]
esp_1 = df_1["Espulsioni"]
rig_1 = df_1["Rigori"]
rp_1 = df_1["Rigori Parati"]
gs_1 = df_1["Gol Subiti"]
qa_1 = df_1["QA"].apply(lambda x: float(x))

# take season_2 stats
df_2 = pd.read_csv(season_2)
df_2 = df_2.loc[df_2["Calciatore"].isin(df_0["Calciatore"])] # take only current players stats
team_2 = df_2["Squadra"]
fm_2 = df_2["FM"]
player_2 = df_2["Calciatore"]
role_2 = df_2["Ruolo"]
games_2 = df_2["Partite Giocate"]
team_2 = df_2["Squadra"]
mv_2 = df_2["MV"]
amm_2 = df_2["Ammonizioni"]
esp_2 = df_2["Espulsioni"]
rig_2 = df_2["Rigori"]
rp_2 = df_2["Rigori Parati"]
gs_2 = df_2["Gol Subiti"]
qa_2 = df_2["QA"].apply(lambda x: float(x))


def val_partite(i): # [0, 11]
    
    # constants
    alpha = 1
    beta = 0.6
    gamma = 10

    # take partite for each season
    partite_0 = int(games_0[i])
    
    if(df_1.loc[(df_1["Calciatore"] == player_0[i])].size > 0):
        row_1 = df_1.loc[(df_1["Calciatore"] == player_0[i])] # take only current players stats
        partite_1 = row_1["Partite Giocate"].values[0]
    else:
        partite_1 = 0

    if(df_2.loc[(df_2["Calciatore"] == player_0[i])].size > 0):
        row_2 = df_2.loc[(df_2["Calciatore"] == player_0[i])] # take only current players stats
        partite_2 = row_2["Partite Giocate"].values[0]
    else:
        partite_2 = 0

    v_partite = (gamma * partite_0 ^2 / giornate_correnti) + (alpha * partite_1 ^2 / 38) + (beta * partite_2 ^2 / 38) / 10

    return v_partite

def val_fm(i): # [0, 29]
    
    # constants
    alpha = 1
    beta = 0.6
    gamma = 0.3

    # take partite for each season
    fantam_0 = float(fm_0[i].replace(',','.'))
    partite_0 = int(games_0[i])

    if(df_1.loc[(df_1["Calciatore"] == player_0[i])].size > 0):
        row_1 = df_1.loc[(df_1["Calciatore"] == player_0[i])] # take only current players stats
        partite_1 = row_1["Partite Giocate"].values[0]
        fantam_1 = row_1["FM"].values[0]
        fantam_1 = float(fantam_1.replace(",","."))
        print(fantam_1)
    else:
        fantam_1 = 0

    if(df_2.loc[(df_2["Calciatore"] == player_0[i])].size > 0):
        row_2 = df_2.loc[(df_2["Calciatore"] == player_0[i])] # take only current players stats
        partite_2 = row_2["Partite Giocate"].values[0]
        fantam_2 = row_2["FM"].values[0]
        fantam_2 = float(fantam_2.replace(",","."))
    else:
        fantam_2 = 0

    v_fantam = (gamma * fantam_0 * partite_0 / giornate_correnti) + (alpha * fantam_1 * partite_1 / 38) + (beta * fantam_2 * partite_2 / 38)

    return v_fantam

def val_mv(i): # [0, 19]
    
    # constants
    alpha = 1
    beta = 0.6
    gamma = 0.3

    # take partite for each season
    mediav_0 = float(mv_0[i].replace(',','.'))
    partite_0 = int(games_0[i])

    if(df_1.loc[(df_1["Calciatore"] == player_0[i])].size > 0):
        row_1 = df_1.loc[(df_1["Calciatore"] == player_0[i])] # take only current players stats
        partite_1 = row_1["Partite Giocate"].values[0]
        mediav_1 = row_1["MV"].values[0]
        mediav_1 = float(mediav_1.replace(",","."))
        print(mediav_1)
    else:
        mediav_1 = 0

    if(df_2.loc[(df_2["Calciatore"] == player_0[i])].size > 0):
        row_2 = df_2.loc[(df_2["Calciatore"] == player_0[i])] # take only current players stats
        partite_2 = row_2["Partite Giocate"].values[0]
        mediav_2 = row_2["MV"].values[0]
        mediav_2 = float(mediav_2.replace(",","."))
    else:
        mediav_2 = 0

    v_mediav = (gamma * mediav_0 * partite_0 / giornate_correnti) + (alpha * mediav_1 * partite_1 / 38) + (beta * mediav_2 * partite_2 / 38)

    return v_mediav


def val_rigori(i):
    rig_segnati = float(rig[i].split(" / ")[0])
    rig_totali = float(rig[i].split(" / ")[1])
    if rig_segnati != 0:
        val_rig = (rig_totali) * (rig_segnati / rig_totali)
    elif rig_segnati == 0 and rig_totali == 0:
        val_rig = 0
    elif rig_segnati == 0 and rig_totali != 0:
        val_rig = -rig_totali
    else:
        val_rig = 0
    return val_rig

def val_amm(i):
    giallo = float(amm[i])
    partite = float(games[i])
    if giallo != 0 and partite != 0:
        val_amm = giallo / partite
    else:
        val_amm = 0
    return -val_amm

def val_esp(i):
    boost_coeff = 2
    rosso = boost_coeff * float(esp[i])
    partite = float(games[i])
    if rosso != 0 and partite != 0:
        val_esp = rosso / partite
    else:
        val_esp = 0
    return -val_esp



def val(i):
    val_rig = val_rigori(i)
    val_ammo = val_amm(i)
    val_espu = val_esp(i)
    val_part = val_partite(i)
    val_fmp = val_fm(i)
    val_mvp = val_mv(i)
    val = val_rig + val_ammo + val_espu + val_part + val_fmp + val_mvp 
    return val

def print_report(model):
    model.solve()

    costo = bp = bd = bc = ba = num = 0
    selected = {'role':[],'player':[],'team':[], 'games':[], 'fm':[],'cost':[]}

    for i in range(len(df)):
        if decisions[i].value() == 1:

            costo = costo + cost[i]
            if role[i] == "p":
                bp = bp + cost[i]
            if role[i] == "d":
                bd = bd + cost[i]
            if role[i] == "c":
                bc = bc + cost[i]
            if role[i] == "a":
                ba = ba + cost[i]
            num = num + 1

            selected['role'].append(role[i])
            selected['player'].append(player[i])
            selected['team'].append(team[i])
            selected['games'].append(games[i])
            selected['fm'].append(fm[i])
            selected['cost'].append(cost[i])

    df_report = pd.DataFrame({'role':selected['role'],
            'player':selected['player'],
            'team':selected['team'],
            'games':selected['games'],
            'fm':selected['fm'],
            'cost':selected['cost']})
    
    df_report = df_report.sort_values(by=['role','cost'], ascending=False)

    filepath = season.split('/')[0]
    os.makedirs(filepath, exist_ok=True) 
    filename = filepath + '/team.csv'
    df_report.to_csv(filename)

    print(df_report)
    print("\ntotal players: " + str(num))
    print("costs: " + str(bp) +"p, "+ str(bd) +"d, "+ str(bc) +"c, "+ str(ba) +"a = "+str(costo))


num_players = 3+8+8+6
budget = 500
budget_p = 8/100 * budget
budget_d = 15/100 * budget
budget_c = 30/100 * budget
budget_a = budget - budget_p - budget_d - budget_c 

# maximization problem
model = pulp.LpProblem("Constrained value maximisation", pulp.LpMaximize)

# binary decision: take or not
decisions = [pulp.LpVariable("x{}".format(i), lowBound=0, upBound=1, cat='Integer')
             for i in range(len(df))]


# OBJECTIVE FUNCTION 
# value = fm + mv + rig + amm + esp + partite

#model += sum(decisions[i] * (val_fm(i) + val_mv(i) + val_rigori(i) + val_amm(i) + val_esp(i) + val_partite(i)) for i in range(len(df))), "Objective"
model += sum(decisions[i] * val(i) for i in range(len(df))), "Objective"

# CONSTRAINTS
# budget management
model += sum(decisions[i] * float(cost[i]) for i in range(len(df))) <= budget
model += sum(decisions[i] * float(cost[i]) for i in range(len(df)) if role[i] == "p") <= budget_p
model += sum(decisions[i] * float(cost[i]) for i in range(len(df)) if role[i] == "d") <= budget_d
model += sum(decisions[i] * float(cost[i]) for i in range(len(df)) if role[i] == "c") <= budget_c
model += sum(decisions[i] * float(cost[i]) for i in range(len(df)) if role[i] == "a") <= budget_a

# total players
model += sum(decisions) == num_players

# player for roles
# 3 portieri di cui 1 titolare
model += sum(decisions[i] for i in range(len(df)) if role[i] == "p") == 3
model += sum(decisions[i] for i in range(len(df)) if (games[i] >= 3 and role[i] == "p" and val_fm(i) >= 6)) == 1 
model += sum(decisions[i] for i in range(len(df)) if (games[i] >= 2 and role[i] == "p")) == 3 

# 8 difensori di cui 3 difensori forti
model += sum(decisions[i] for i in range(len(df)) if role[i] == "d") == 8
model += sum(decisions[i] for i in range(len(df)) if (games[i] >= 2 and role[i] == "d" and val_mv(i) >= 6.2)) == 3

# 8 centrocampisti di cui 2 molto forti e 2 ottimi 
model += sum(decisions[i] for i in range(len(df)) if role[i] == "c") == 8
model += sum(decisions[i] for i in range(len(df)) if (games[i] >= 2 and role[i] == "c" and val_fm(i) >= 7)) == 2
#model += sum(decisions[i] for i in range(len(df)) if (games[i] >= 25 and role[i] == "c" and val_fm(i) <= 7 and val_fm(i) >= 6.5)) == 2

# 6 attaccanti di cui 2 forti e 1 buono
model += sum(decisions[i] for i in range(len(df)) if role[i] == "a") == 6
model += sum(decisions[i] for i in range(len(df)) if (games[i] >= 2 and role[i] == "a" and val_fm(i) >= 7.5)) == 2
#model += sum(decisions[i] for i in range(len(df)) if (games[i] >= 25 and role[i] == "a" and val_fm(i) <= 7.5 and val_fm(i) > 7)) == 1

# SOLVE and print report
print_report(model)

