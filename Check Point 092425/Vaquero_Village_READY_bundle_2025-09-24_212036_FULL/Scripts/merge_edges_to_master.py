import pandas as pd, numpy as np, glob
from pathlib import Path
def s(x):
  return '' if x is None else str(x).strip()
def to_float(x):
  try: return float(str(x).strip())
  except: return np.nan
def validate(df):
  df=df.copy()
  for c in df.columns: df[c]=df[c].apply(s)
  exp=['LinkID','Type','NodeID1','NodeID2','Length_ft','Diameter_in','Roughness','InitialStatus','MinorLoss_K','Power_HP','Setting','CurveID','Valve','Type.1','Tag']
  for c in exp:
    if c not in df.columns: df[c]=''
  nf={}
  for c in ['Length_ft','Diameter_in','Roughness','MinorLoss_K','Power_HP','Setting']:
    nf[c]=df[c].apply(to_float)
  rej=[]
  for i,r in df.iterrows():
    R=[]
    if s(r['LinkID'])=='': R.append('Missing LinkID')
    if s(r['NodeID1'])=='': R.append('Missing NodeID1')
    if s(r['NodeID2'])=='': R.append('Missing NodeID2')
    if s(r['Type']).lower() not in {'pipe','pump','valve'}: R.append("Invalid Type '")+r['Type']+"'")
    if np.isnan(nf['Diameter_in'].iat[i]) or nf['Diameter_in'].iat[i]<=0: R.append('Diameter_in must be > 0 (in)')
    if np.isnan(nf['Roughness'].iat[i]) or nf['Roughness'].iat[i]<0: R.append('Roughness must be >= 0 (Darcy ε, ft)')
    if not np.isnan(nf['Length_ft'].iat[i]) and nf['Length_ft'].iat[i]<0: R.append('Length_ft cannot be negative')
    rej.append('; '.join(R))
  df['Reject_Reason']=rej
  return df[df['Reject_Reason'].str.len()==0], df[df['Reject_Reason'].str.len()>0]
if __name__=='__main__':
  files=sorted(glob.glob('Zone*.csv'))
  frames=[pd.read_csv(f) for f in files]
  merged=pd.concat(frames, ignore_index=True)
  ready,rejects=validate(merged)
  ready.to_csv('Edges_MASTER.csv', index=False)
  rejects.to_csv('Edges_MASTER_REJECTS.csv', index=False)
