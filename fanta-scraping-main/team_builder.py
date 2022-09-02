import pandas as pd
import pulp
import os
 
# creating a data frame
season = "2022-23/2022-23.csv"
#season = "2021-22/2021-22.csv"

df = pd.read_csv(season)

# split columns
team = df["Squadra"]
fm = df["FM"]
player = df["Calciatore"]
role = df["Ruolo"]
games = df["Partite Giocate"]
team = df["Squadra"]
mv = df["MV"]
amm = df["Ammonizioni"]
esp = df["Espulsioni"]
rig = df["Rigori"]

if season == "2022-23/2022-23.csv":
    qa = df["QA"].apply(lambda x: float(x))
    cost = df['ExpectedCost_1000'].apply(lambda x: float(x)/2) # fors previous season there is "-" instead of a value
else:
    cost = df["QA"].apply(lambda x: float(x)*2)

print(df.head())

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

def val_partite(i):
    boost1 = 0.6
    boost2 = 0.4
    boost3 = 0.1
    partite = float(games[i])
    if partite != 0:
        if partite <= 10:
            val_partite = partite * boost1
        elif partite > 10 and partite < 20:
            val_partite = partite * boost2
        else:
            val_partite = partite * boost3
    else:
        val_partite = 0
    return val_partite

def val_fm(i):
    val_fm = float(fm[i].replace(',','.'))
    return val_fm

def val_mv(i):
    val_mv = float(mv[i].replace(',','.'))
    return val_mv

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

