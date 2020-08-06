import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def stepHeatmap(data):
    print("===== Begin Visualization of StepHeatmap =====")
    dayData = {}
    numData = len(data)
    print(f"{numData} data points")
    granularity = "hour"

    for datum in data:
        currentTime = datum["startDate"]
        endTime = datum["endDate"]
        day = str(currentTime.month) + "/" + str(currentTime.day)
        steps = int(datum["value"])
        # add 1 to avoid division by 0
        if granularity == "minute":
            minutesSpanned = int((currentTime - endTime).seconds / 60) + 1
            stepsPerMin = steps / minutesSpanned
            for i in range(minutesSpanned):
                hour = appendZero(currentTime.hour)
                minute = appendZero(currentTime.minute)
                hourMinute = hour + ":" + minute
                if day in dayData:
                    hourlyData = dayData[day]
                    if hourMinute in hourlyData:
                        hourlyData[hourMinute] += stepsPerMin
                    else:
                        hourlyData[hourMinute] = stepsPerMin
                else:
                    dayData[day] = {hourMinute: stepsPerMin}
            currentTime += timedelta(minutes=1)
        else:
            hourMinute = hourMinuteBucket(currentTime.hour, currentTime.minute)
            if day in dayData:
                hourlyData = dayData[day]
                if hourMinute in hourlyData:
                    hourlyData[hourMinute] += steps
                else:
                    hourlyData[hourMinute] = steps
            else:
                dayData[day] = {hourMinute: steps}

    df = pd.DataFrame(dayData)
    df = df.fillna(1)
    df = df.sort_index(ascending=False)

    f, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.cm.rocket_r
    sns.heatmap(df, cmap=cmap)
    plt.show()


def appendZero(unformattedTime):
    if unformattedTime < 10:
        return "0" + str(unformattedTime)
    else:
        return str(unformattedTime)


def hourMinuteBucket(hour, minute):
    frac = minute / 60
    if frac < 0.25:
        return hour
    elif frac < 0.5:
        return hour + 0.25
    elif frac < 0.75:
        return hour + 0.5
    else:
        return hour + 0.75
