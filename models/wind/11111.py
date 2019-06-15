import pandas as pd
import numpy as np
import os
path_images=r'C:\Users\Administrator\Desktop'
col_name = ['name', 'value']

data = pd.read_excel(
    r'C:\Users\Administrator\Desktop\energy_IEC_classification.xlsx',
    header=0, sheet_name='Sheet1', usecols=col_name)

# self.data_booster_station = self.DataBoosterStation.loc[self.DataBoosterStation['Status'] == self.Status].loc[
#     self.DataBoosterStation['Grade'] == self.Grade].loc[self.DataBoosterStation['Capacity'] == self.Capacity]

print()

data_np=np.array(data)
print(data_np.shape)


data_np_res=data_np.reshape(int(data_np.shape[0]/23),46)
print(data_np_res)
df = pd.DataFrame(data_np_res)

# a=data.loc[data['name']=='Climatology number : ']
# print(a)
newfile='energy_IEC_classification.csv'
Patt=os.path.join(path_images, '%s') % newfile


df.to_csv(Patt)