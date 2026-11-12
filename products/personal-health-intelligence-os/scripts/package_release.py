#!/usr/bin/env python3
"""Package a synthetic-only source kit. Never include runtime/customer files."""
import hashlib,json,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root.parent/'outputs/health-os-0.1.0';out.mkdir(parents=True,exist_ok=True)
allowed={'.md','.json','.py','.mjs','.csv','.html','.txt'}
files=sorted(p for p in root.rglob('*') if p.is_file() and (p.suffix in allowed or p.name=='LICENSE') and '__pycache__' not in p.parts)
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
target=out/'Personal-Health-Intelligence-OS-0.1.0.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,'personal-health-intelligence-os/'+str(p.relative_to(root)))
 z.writestr('personal-health-intelligence-os/SHA256SUMS.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(target) as z:
 assert z.testzip() is None
 assert not any('__pycache__' in n or n.endswith(('.xlsx','.png')) for n in z.namelist())
print(json.dumps({'file':str(target),'source_files':len(files),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))
