import pandas as pd
import pulp
import os
 
# creating a data frame
route = ""#"/home/federico/fanta-scraping/fanta-scraping-main/fanta-scraping/fanta-scraping-main/"
season_0 = route + "2022-23/2022-23.csv"
season_1 = route + "2021-22/2021-22.csv"
season_2 = route + "2020-21/2020-21.csv"

# matches currently played in season_0
giornate_correnti = 5

# take season_0 stats
df_0 = pd.read_csv(season_0)
team_0 = df_0["Squadra"]
class_0 = df_0["Classifica"]
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
class_1 = df_1["Classifica"]
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
class_2 = df_2["Classifica"]
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
    partite_0 = float(games_0[i])
    
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

    v_partite = (gamma * partite_0 * partite_0 / giornate_correnti) + (alpha * partite_1 * partite_1 / 38) + (beta * partite_2 * partite_2 / 38) / 10

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
    else:
        fantam_1 = 0
        partite_1 = 0

    if(df_2.loc[(df_2["Calciatore"] == player_0[i])].size > 0):
        row_2 = df_2.loc[(df_2["Calciatore"] == player_0[i])] # take only current players stats
        partite_2 = row_2["Partite Giocate"].values[0]
        fantam_2 = row_2["FM"].values[0]
        fantam_2 = float(fantam_2.replace(",","."))
    else:
        fantam_2 = 0
        partite_2 = 0

    v_fantam = (gamma * fantam_0 * partite_0 / giornate_correnti) + (alpha * fantam_1 * partite_1 / 38) + (beta * fantam_2 * partite_2 / 38)

    return v_fantam

def val_mv(i): # [0, 19]
    
    # constants
    alpha = 1
    beta = 0.6
    gamma = 0.3

    mediav_0 = float(mv_0[i].replace(',','.'))
    partite_0 = int(games_0[i])

    if(df_1.loc[(df_1["Calciatore"] == player_0[i])].size > 0):
        row_1 = df_1.loc[(df_1["Calciatore"] == player_0[i])] # take only current players stats
        partite_1 = row_1["Partite Giocate"].values[0]
        mediav_1 = row_1["MV"].values[0]
        mediav_1 = float(mediav_1.replace(",","."))
    else:
        mediav_1 = 0
        partite_1 = 0

    if(df_2.loc[(df_2["Calciatore"] == player_0[i])].size > 0):
        row_2 = df_2.loc[(df_2["Calciatore"] == player_0[i])] # take only current players stats
        partite_2 = row_2["Partite Giocate"].values[0]
        mediav_2 = row_2["MV"].values[0]
        mediav_2 = float(mediav_2.replace(",","."))
    else:
        mediav_2 = 0
        partite_2 = 0

    v_mediav = (gamma * mediav_0 * partite_0 / giornate_correnti) + (alpha * mediav_1 * partite_1 / 38) + (beta * mediav_2 * partite_2 / 38)

    return v_mediav

def val_rigori(i): # [0, n]

    # constants
    alpha = 1
    beta = 0.6
    gamma = 1

    rig_segnati_0 = float(rig_0[i].split(" / ")[0])
    rig_totali_0 = float(rig_0[i].split(" / ")[1])
    # avoid 0/0 division
    if(rig_totali_0 == 0):
        rig_totali_0 = 1

    if(df_1.loc[(df_1["Calciatore"] == player_0[i])].size > 0):
        row_1 = df_1.loc[(df_1["Calciatore"] == player_0[i])] # take only current players stats
        rigori_1 = row_1["Rigori"].values[0]
        rig_segnati_1 = float(rigori_1.split(" / ")[0])
        rig_totali_1 = float(rigori_1.split(" / ")[1])
        # avoid 0/0 division
        if(rig_totali_1 == 0):
            rig_totali_1 = 1
    else:
        rig_segnati_1 = 0
        rig_totali_1 = 1

    if(df_2.loc[(df_2["Calciatore"] == player_0[i])].size > 0):
        row_2 = df_2.loc[(df_2["Calciatore"] == player_0[i])] # take only current players stats
        rigori_2 = row_2["Rigori"].values[0]
        rig_segnati_2 = float(rigori_2.split(" / ")[0])
        rig_totali_2 = float(rigori_2.split(" / ")[1])
        # avoid 0/0 division
        if(rig_totali_2 == 0):
            rig_totali_2 = 1
    else:
        rig_segnati_2 = 0
        rig_totali_2 = 1

    v_rig = (gamma * rig_segnati_0 * (rig_segnati_0/rig_totali_0)) + (alpha * rig_segnati_1 * (rig_segnati_1/rig_totali_1)) + (beta * rig_segnati_2 * (rig_segnati_2/rig_totali_2))

    return v_rig

def val_rigori_parati(i): # [0, n]
    
    # constants
    alpha = 1

    rparati_0 = rp_0[i]

    if(df_1.loc[(df_1["Calciatore"] == player_0[i])].size > 0):
        row_1 = df_1.loc[(df_1["Calciatore"] == player_0[i])] # take only current players stats
        rparati_1 = row_1["Rigori Parati"].values[0]
    else:
        rparati_1 = 0

    if(df_2.loc[(df_2["Calciatore"] == player_0[i])].size > 0):
        row_2 = df_2.loc[(df_2["Calciatore"] == player_0[i])] # take only current players stats
        rparati_2 = row_2["Rigori Parati"].values[0]
    else:
        rparati_2 = 0

    v_rparati = alpha * (rparati_0 + rparati_1 + rparati_2) 

    return v_rparati

def val_gol_subiti(i):
    
    # constants [-n,0]
    alpha = 10

    gsub_0 = gs_0[i]
    partite_0 = games_0[i]

    if(df_1.loc[(df_1["Calciatore"] == player_0[i])].size > 0):
        row_1 = df_1.loc[(df_1["Calciatore"] == player_0[i])] # take only current players stats
        gsub_1 = row_1["Gol Subiti"].values[0]
        partite_1 = row_1["Partite Giocate"].values[0]
    else:
        gsub_1 = 0
        partite_1 = 0

    if(df_2.loc[(df_2["Calciatore"] == player_0[i])].size > 0):
        row_2 = df_2.loc[(df_2["Calciatore"] == player_0[i])] # take only current players stats
        gsub_2 = row_2["Gol Subiti"].values[0]
        partite_2 = row_2["Partite Giocate"].values[0]
    else:
        gsub_2 = 0
        partite_2 = 0

    if(partite_0 == partite_1 == partite_2 == 0):
        partite_0 = 1 

    v_gsub = - alpha * (gsub_0 + gsub_1 + gsub_2) / (partite_0 + partite_1 + partite_2)

    return v_gsub

def val_amm(i): # [-n, 0]

    # constants
    alpha = 0.7
    beta = 0.5
    gamma = 0.4
    role_malus = 1.5

    giallo_0 = float(amm_0[i])
    partite_0 = float(games_0[i])
    # avoid 0/0 division
    if(partite_0 == 0):
        partite_0 = 1

    if(df_1.loc[(df_1["Calciatore"] == player_0[i])].size > 0):
        row_1 = df_1.loc[(df_1["Calciatore"] == player_0[i])] # take only current players stats
        partite_1 = row_1["Partite Giocate"].values[0]
        giallo_1 = row_1["Ammonizioni"].values[0]
        giallo_1 = float(giallo_1)
    else:
        giallo_1 = 0
        partite_1 = 1

    if(df_2.loc[(df_2["Calciatore"] == player_0[i])].size > 0):
        row_2 = df_2.loc[(df_2["Calciatore"] == player_0[i])] # take only current players stats
        partite_2 = row_2["Partite Giocate"].values[0]
        giallo_2 = row_2["Ammonizioni"].values[0]
        giallo_2 = float(giallo_2)
    else:
        giallo_2 = 0
        partite_2 = 1

    if((partite_0 == 0 and giallo_0 == 0) or (partite_1 == 0 and giallo_1 == 0) or(partite_2 == 0 and giallo_2 == 0)):
        v_amm = 0
    elif role_0[i] == 'a':
        v_amm = - role_malus * ((gamma * giallo_0 * giornate_correnti / partite_0) + (alpha * giallo_1 * 38 / partite_1) + (beta * giallo_2 * 38 / partite_2))
    else:
        v_amm = - ((gamma * giallo_0 * giornate_correnti / partite_0) + (alpha * giallo_1 * 38 / partite_1) + (beta * giallo_2 * 38 / partite_2))

    return v_amm

def val_esp(i): # [-n, 0]

    # constants
    alpha = 0.5
    beta = 0.3
    gamma = 0.2
    role_malus = 2

    rosso_0 = float(esp_0[i])
    partite_0 = float(games_0[i])
    # avoid 0/0 division
    if(partite_0 == 0):
        partite_0 = 1

    if(df_1.loc[(df_1["Calciatore"] == player_0[i])].size > 0):
        row_1 = df_1.loc[(df_1["Calciatore"] == player_0[i])] # take only current players stats
        partite_1 = row_1["Partite Giocate"].values[0]
        rosso_1 = row_1["Espulsioni"].values[0]
        rosso_1 = float(rosso_1)
    else:
        rosso_1 = 0
        partite_1 = 1

    if(df_2.loc[(df_2["Calciatore"] == player_0[i])].size > 0):
        row_2 = df_2.loc[(df_2["Calciatore"] == player_0[i])] # take only current players stats
        partite_2 = row_2["Partite Giocate"].values[0]
        rosso_2 = row_2["Espulsioni"].values[0]
        rosso_2 = float(rosso_2)
    else:
        rosso_2 = 0
        partite_2 = 1
    
    if((partite_0 == 0 and rosso_0 == 0) or (partite_1 == 0 and rosso_1 == 0) or(partite_2 == 0 and rosso_2 == 0)):
        v_esp = 0
    elif role_0[i] == 'a':
        v_esp = - role_malus * ((gamma * rosso_0 * giornate_correnti / partite_0) + (alpha * rosso_1 * 38 / partite_1) + (beta * rosso_2 * 38 / partite_2))
    else:
        v_esp = - ((gamma * rosso_0 * giornate_correnti / partite_0) + (alpha * rosso_1 * 38 / partite_1) + (beta * rosso_2 * 38 / partite_2))

    return v_esp

def val_squadra(i): # [1.5, 7.5]

    # constants
    gamma = 1.5

    if class_0[i] <= 4:
        classifica_0 = 5
    elif class_0[i] >= 5 and class_0[i] <= 7:
        classifica_0 = 4
    elif class_0[i] >= 8 and class_0[i] <= 12:
        classifica_0 = 3
    elif class_0[i] >= 13 and class_0[i] <= 17:
        classifica_0 = 2
    elif class_0[i] >= 18 and class_0[i] <= 20:
        classifica_0 = 1
    
    v_squadra = (gamma * classifica_0)

    return v_squadra

def val(i):
    
    val = val_partite(i) + val_fm(i) + val_mv(i) + val_rigori(i) + val_rigori_parati(i) + val_amm(i) + val_esp(i) + val_squadra(i) + val_gol_subiti(i) 

    return val

def print_report(model):
    model.solve()

    costo = bp = bd = bc = ba = num = 0
    selected = {'role':[],'player':[],'team':[], 'games':[], 'fm':[],'cost':[]}

    for i in range(len(df_0)):
        if decisions[i].value() == 1:

            costo = costo + cost_0[i]
            if role_0[i] == "p":
                bp = bp + cost_0[i]
            if role_0[i] == "d":
                bd = bd + cost_0[i]
            if role_0[i] == "c":
                bc = bc + cost_0[i]
            if role_0[i] == "a":
                ba = ba + cost_0[i]
            num = num + 1

            selected['role'].append(role_0[i])
            selected['player'].append(player_0[i])
            selected['team'].append(team_0[i])
            selected['games'].append(games_0[i])
            selected['fm'].append(fm_0[i])
            selected['cost'].append(cost_0[i])

    df_report = pd.DataFrame({'role':selected['role'],
            'player':selected['player'],
            'team':selected['team'],
            'games':selected['games'],
            'fm':selected['fm'],
            'cost':selected['cost']})
    
    df_report = df_report.sort_values(by=['role','cost'], ascending=False)

    filepath = route + season_0.split('/')[0]
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
             for i in range(len(df_0))]


# OBJECTIVE FUNCTION 
# value = fm + mv + rig + amm + esp + partite

#model += sum(decisions[i] * (val_fm(i) + val_mv(i) + val_rigori(i) + val_amm(i) + val_esp(i) + val_partite(i)) for i in range(len(df))), "Objective"
model += sum(decisions[i] * val(i) for i in range(len(df_0))), "Objective"

# CONSTRAINTS
# budget management
model += sum(decisions[i] * float(cost_0[i]) for i in range(len(df_0))) <= budget
model += sum(decisions[i] * float(cost_0[i]) for i in range(len(df_0)) if role_0[i] == "p") <= budget_p
model += sum(decisions[i] * float(cost_0[i]) for i in range(len(df_0)) if role_0[i] == "d") <= budget_d
model += sum(decisions[i] * float(cost_0[i]) for i in range(len(df_0)) if role_0[i] == "c") <= budget_c
model += sum(decisions[i] * float(cost_0[i]) for i in range(len(df_0)) if role_0[i] == "a") <= budget_a

# total players
model += sum(decisions) == num_players

# player for roles
# 3 portieri di cui 1 titolare
model += sum(decisions[i] for i in range(len(df_0)) if role_0[i] == "p") == 3
#model += sum(decisions[i] for i in range(len(df_0)) if (games_0[i] >= 3 and role_0[i] == "p" and val_fm(i) >= 6)) == 1 
#model += sum(decisions[i] for i in range(len(df_0)) if (games_0[i] >= 2 and role_0[i] == "p")) == 3 

# 8 difensori di cui 3 difensori forti
model += sum(decisions[i] for i in range(len(df_0)) if role_0[i] == "d") == 8
#model += sum(decisions[i] for i in range(len(df_0)) if (games_0[i] >= 2 and role_0[i] == "d" and val_mv(i) >= 6.2)) == 3

# 8 centrocampisti di cui 2 molto forti e 2 ottimi 
model += sum(decisions[i] for i in range(len(df_0)) if role_0[i] == "c") == 8
#model += sum(decisions[i] for i in range(len(df_0)) if (games_0[i] >= 2 and role_0[i] == "c" and val_fm(i) >= 7)) == 2
#model += sum(decisions[i] for i in range(len(df)) if (games[i] >= 25 and role[i] == "c" and val_fm(i) <= 7 and val_fm(i) >= 6.5)) == 2

# 6 attaccanti di cui 2 forti e 1 buono
model += sum(decisions[i] for i in range(len(df_0)) if role_0[i] == "a") == 6
#model += sum(decisions[i] for i in range(len(df_0)) if (games_0[i] >= 2 and role_0[i] == "a" and val_fm(i) >= 7.5)) == 2
#model += sum(decisions[i] for i in range(len(df)) if (games[i] >= 25 and role[i] == "a" and val_fm(i) <= 7.5 and val_fm(i) > 7)) == 1

# SOLVE and print report
print_report(model)

