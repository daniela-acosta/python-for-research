#cd C:\Users\Daniela\Desktop\Using_Python_for_Research\Case_Studies\5Bird_Migration

import pandas as pd
birddata = pd.read_csv("bird_tracking.csv")

#graficando trayectorias de los pájaros
import matplotlib.pyplot as plt
import numpy as np

bird_names = pd.unique(birddata.bird_name)
plt.figure(figsize=(7,7))
for bird_name in bird_names:
    ix = birddata.bird_name == bird_name
    x , y = birddata.longitude[ix], birddata.latitude[ix]
    plt.plot(x,y,".", label=bird_name)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(loc="lower right")
plt.savefig("3traj.pdf")

#Velocidades de vuelo
ix = birddata.bird_name == "Eric"
speed  = birddata.speed_2d[ix]
ind = np.isnan(speed)
plt.hist(speed[~ind]) # ~ es el conjunto complemento
plt.savefig("hist.pdf")

plt.figure(figsize=(8,4))
speed = birddata.speed_2d[birddata.bird_name == "Eric"]
ind = np.isnan(speed)
plt.hist(speed[~ind], bins=np.linspace(0, 30, 20), normed=True)
plt.xlabel("2D speed (m/s)")
plt.ylabel("frequency"); 

#También se puede hacer esto usando pandas para evitar el problema de los NaN's
birddata.speed_2d.plot(kind='hist', range=[0, 30])
plt.xlabel("2D speed (m/s)")
plt.savefig("pd_hist.pdf")

# Datos de fecha y cómo manejarlos
import datetime

#Primero convertimos el string con la fecha a un objeto de datatime
timestamps = []
for k in range(len(birddata)):
    timestamps.append(datetime.datetime.strptime(birddata.date_time.iloc[k][:-3], "%Y-%m-%d %H:%M:%S"))

#Creamos un dataframe de pandas con estos objetos y lo agregamos como nueva columna a birddata
birddata["timestamp"] = pd.Series(timestamps, index = birddata.index)

#Calculamos el timepo que ha transcurrido desde el inicio, y graficamos los días transcurridos para cada dato
times = birddata.timestamp[birddata.bird_name == "Eric"]
elapsed_time = [time - times[0] for time in times]
elapsed_days = np.array(elapsed_time)/datetime.timedelta(days=1)
plt.plot(elapsed_days)
plt.xlabel("Observation")
plt.ylabel("Elapsed time (days)")
plt.savefig("timeplot.pdf")

#Obtenemos la velocidad media diaria
data = birddata[birddata.bird_name == "Eric"]

next_day = 1
inds = []
daily_mean_speed = []
for (i, t) in enumerate(elapsed_days):
    if t < next_day:
        inds.append(i)
    else:
        daily_mean_speed.append(np.mean(data.speed_2d[inds]))
        next_day += 1
        inds = []
plt.figure(figsize=(8,6))
plt.plot(daily_mean_speed)
plt.xlabel("Day")
plt.ylabel("Mean Speed (m/s)");
plt.savefig("dms.pdf")

#HOMEWORK

#Exercise 1
# First, use `groupby` to group up the data.
grouped_birds = birddata.groupby("bird_name")
# Now operations are performed on each group.
mean_speeds = grouped_birds.speed_2d.mean()
# The `head` method prints the first 5 lines of each bird.
grouped_birds.head()
# Find the mean `altitude` for each bird.
# Assign this to `mean_altitudes`.
mean_altitudes = grouped_birds.altitude.mean()

#Exercise 2
# Convert birddata.date_time to the `pd.datetime` format.
birddata.date_time = pd.to_datetime(birddata.date_time)
# Create a new column of day of observation
birddata["date"] = birddata.date_time.dt.date
# Check the head of the column.
birddata.date.head()
grouped_bydates = birddata.groupby("date")
mean_altitudes_perday = grouped_bydates.altitude.mean()

#Exercise 3
grouped_birdday = birddata.groupby(["bird_name","date"])
mean_altitudes_perday = grouped_birdday.altitude.mean()
# look at the head of `mean_altitudes_perday`.
mean_altitudes_perday.head()

#Exercise 4
eric_daily_speed  = grouped_birdday.speed_2d.mean()["Eric"]
sanne_daily_speed = grouped_birdday.speed_2d.mean()["Sanne"]
nico_daily_speed  = grouped_birdday.speed_2d.mean()["Nico"]
eric_daily_speed.plot(label="Eric")
sanne_daily_speed.plot(label="Sanne")
nico_daily_speed.plot(label="Nico")
plt.legend(loc="upper left")
plt.show()


