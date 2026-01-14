import pandas as pd, numpy as np, sys
def s(x): return '' if x is None else str(x).strip()
def to_float(x):
  try: return float(str(x).strip())
  except: return np.nan
df=pd.read_csv(sys.argv[1])
for c in df.columns: df[c]=df[c].apply(s)
for c in ['NodeID','Elev_ft','BaseDemand_gpm']:
  if c not in df.columns: df[c]=''
reasons=[]
seen=set()
for i,r in df.iterrows():
  R=[]
  nid=s(r['NodeID'])
  if nid=='': R.append('Missing NodeID')
  if nid in seen: R.append('Duplicate NodeID')
  seen.add(nid)
  if np.isnan(to_float(r['Elev_ft'])): R.append('Elev_ft must be numeric')
  bd=to_float(r.get('BaseDemand_gpm',''))
  if r.get('BaseDemand_gpm','')!='' and (np.isnan(bd) or bd<0): R.append('BaseDemand_gpm must be >= 0 or blank')
  reasons.append('; '.join(R))
df['Reject_Reason']=reasons
df[df['Reject_Reason'].str.len()==0].to_csv('Nodes_READY.csv', index=False)
df[df['Reject_Reason'].str.len()>0].to_csv('Nodes_REJECTS.csv', index=False)
