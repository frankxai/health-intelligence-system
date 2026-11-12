"""Emit bounded source-file content for one Git tree, excluding runtime output."""
import json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
allowed={'.md','.json','.py','.mjs','.csv','.html','.txt'}
files=sorted(p for p in root.rglob('*') if p.is_file() and (p.suffix in allowed or p.name=='LICENSE') and '__pycache__' not in p.parts)
parts=[]
for p in files:
 text=p.read_text()
 for offset in range(0,len(text),9000):parts.append({'path':'products/personal-health-intelligence-os/'+str(p.relative_to(root)),'offset':offset,'content':text[offset:offset+9000]})
if len(sys.argv)==1:print(json.dumps({'parts':len(parts),'files':len(files)}))
else:print(json.dumps(parts[int(sys.argv[1])],ensure_ascii=False,separators=(',',':')))
