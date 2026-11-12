#!/usr/bin/env python3
"""Build synthetic-only connector payloads from the same adapter map."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
defs=json.loads((root/'adapters/mappings.json').read_text())['definitions']
out=[]
for d in defs:
 pages=[]
 for idx,row in enumerate(d['rows']):
  props={}
  for n in d['notion']:
   k=n['field'];v=row.get(k)
   if k=='_title':v='Sample '+d['tab'].lower()+' '+str(idx+1)
   if v is None:continue
   if n['type']=='DATE':
    props['date:'+n['label']+':start']=v
    props['date:'+n['label']+':is_datetime']=int(n['schema'].get('format')=='date-time')
   elif n['type']=='CHECKBOX':props[n['label']]='__YES__' if v else '__NO__'
   else:props[n['label']]=json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v
  content='Synthetic demonstration record. It does not describe a real person, product, measurement or recommendation.'
  if row.get('notes'):content+='\n\n'+row['notes']
  if d['entity']=='recipe':content+='\n\n## Recipe\n\n'+row.get('instructions','')+'\n\nIngredient amounts are synthetic placeholders. Replace with verified food and recipe information before personal use.'
  pages.append({'canonical_id':row['id'],'properties':props,'content':content})
 out.append({'entity':d['entity'],'pages':pages,'relations':[{'canonical_id':r['id'],'values':{n['label']:r[n['field']] for n in d['relations'] if n['field'] in r}} for r in d['rows']]})
(root/'adapters/notion-rows.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'entities':len(out),'records':sum(len(d['pages']) for d in out)}))
