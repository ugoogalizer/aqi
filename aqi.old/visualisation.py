import json

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

from aqi.sensor import READINGS_FILE


with open(READINGS_FILE, 'r') as f:
    readings = pd.DataFrame(
        [_f for _f in json.load(f, encoding='utf-8') if _f]
    )

sns.set()
plot = sns.relplot(data=readings, x='time', y='Overall AQI', kind='line')
plot.set(ylim=(0, None))
plt.show()
