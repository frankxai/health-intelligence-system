#!/usr/bin/env python3
"""Compile platform schemas and CSVs from the canonical source. No network."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
schema = json.loads((ROOT / 'canonical/schema.json').read_text())
demo = json.loads((ROOT / 'synthetic/demo.json').read_text())
OUT = ROOT / 'adapters'
OUT.mkdir(exist_ok=True)
COMMON = ['id','schema_version','owner_id','created_at','updated_at','timezone','revision','provenance','access','deleted_at']
NAMES = {
 'profile':'Profile','daily_observation':'Daily','product':'Supplements','ingredient':'Ingredients',
 'intake':'Intakes','food':'Foods','recipe':'Recipes','meal_plan':'Meal Plans','hydration':'Hydration',
 'sleep':'Sleep','training':'Training','recovery':'Recovery','symptom':'Symptoms','biomarker':'Biomarkers',
 'clinical_document':'Documents','appointment':'Appointments','experiment':'Experiments','evidence':'Evidence',
 'purchase':'Purchases','review':'Reviews','consent':'Consent','audit_event':'Audit'
}
LABELS = {'local_date':'Date','sleep_hours':'Sleep (h)','energy_0_10':'Energy (0-10)',
 'focus_0_10':'Focus (0-10)','mood_0_10':'Mood (0-10)','stress_0_10':'Stress (0-10)',
 'fluid_ml':'Fluid (mL)','caffeine_mg':'Caffeine (mg)','protein_g':'Protein (g)','fiber_g':'Fiber (g)',
 'sodium_mg':'Sodium (mg)','calcium_mg':'Calcium (mg)','training_minutes':'Training (min)',
 'pain_0_10':'Pain (0-10)','bristol_1_7':'Bristol (1-7)','amount_per_serving':'Amount per serving',
 'name':'Name','title':'Title','display_name':'Profile name','id':'Record ID','owner_id':'Owner ID',
 'schema_version':'Schema version','created_at':'Created at','updated_at':'Updated at',
 'duration_h':'Duration (h)','duration_min':'Duration (min)','basis_g':'Basis (g)',
 'energy_kcal':'Energy (kcal)','volume_ml':'Volume (mL)','distance_km':'Distance (km)',
 'rpe_1_10':'Effort (1-10)','quality_0_10':'Quality (0-10)','severity_0_10':'Severity (0-10)',
 'score_0_10':'Rating (0-10)'}
def label(k):
 return LABELS.get(k,k.replace('_',' ').capitalize())
def flatten(r):
 out={k:v for k,v in r.items() if k not in ['provenance','access']}
 for k,v in r.get('provenance',{}).items(): out['provenance.'+k]=v
 for k,v in r.get('access',{}).items(): out['access.'+k]=v
 return out
def serial(v):
 return json.dumps(v,ensure_ascii=False,separators=(',',':')) if isinstance(v,(list,dict)) else v
definitions=[]
for entity,tab in NAMES.items():
 props=schema['$defs'][entity]['properties']
 fields=[k for k in props if k not in COMMON]+[k for k in COMMON if k not in ['provenance','access']]
 flat_props={k:props[k] for k in fields}
 for parent in ['provenance','access']:
  for k,v in props[parent]['properties'].items():
   fields.append(parent+'.'+k); flat_props[parent+'.'+k]=v
 rows=[flatten(r) for r in demo['entities'].get(entity,[])]
 # The first 16 columns are everyday inputs. Technical metadata remains to the right.
 csvdir=ROOT/'editions/google/csv'; csvdir.mkdir(parents=True,exist_ok=True)
 with (csvdir/(entity+'.csv')).open('w',newline='') as f:
  w=csv.writer(f);w.writerow(fields)
  for r in rows:w.writerow([serial(r.get(k,'')) for k in fields])
 # Native Notion fields match canonical types. Nested fields are lossless JSON text.
 title=next((k for k in ['name','title','display_name'] if k in props),None)
 notion=[];relations=[]
 for k in fields:
  p=flat_props[k]; typ=p.get('type')
  fk=p.get('description','').split('Foreign key to ')[-1].split('.id')[0] if 'Foreign key to ' in p.get('description','') else None
  if fk in NAMES:
   relations.append({'field':k,'label':label(k),'target':fk});continue
  if k==title: nt='TITLE'
  elif typ in ['number','integer']: nt='NUMBER'
  elif typ=='boolean' or isinstance(p.get('const'),bool): nt='CHECKBOX'
  elif p.get('format') in ['date','date-time']: nt='DATE'
  elif p.get('format')=='uri': nt='URL'
  elif p.get('enum') and typ=='string': nt='SELECT('+', '.join("'"+v.replace("'","''")+"'" for v in p['enum'])+')'
  else:nt='RICH_TEXT'
  notion.append({'field':k,'label':label(k),'type':nt,'schema':p})
 if not title: notion.insert(0,{'field':'_title','label':'Entry','type':'TITLE','schema':{'type':'string'}})
 ddl='CREATE TABLE ('+', '.join('"'+n['label']+'" '+n['type'] for n in notion)+')'
 definitions.append({'entity':entity,'tab':tab,'fields':fields,'headers':[label(k) for k in fields],
  'properties':flat_props,'notion':notion,'relations':relations,'ddl':ddl,'rows':rows})
(OUT/'mappings.json').write_text(json.dumps({'version':'0.1.0','definitions':definitions},indent=2))
(OUT/'notion-schema.json').write_text(json.dumps([{'entity':d['entity'],'title':d['tab'],'ddl':d['ddl'],'relations':d['relations']} for d in definitions],indent=2))
print(json.dumps({'entities':len(definitions),'rows':sum(len(d['rows']) for d in definitions),'csv_files':len(definitions)}))
