import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile,FileBlob} from '@oai/artifact-tool';
const dir=process.env.HEALTH_OS_OUTPUT;
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(dir+'/native-final.xlsx'));
const evidence={sheets:wb.worksheets.items.length,sleep:wb.worksheets.getItem('Cockpit').getRange('F9').values,exposure:wb.worksheets.getItem('Exposure').getRange('B8').values};
if(evidence.sheets!==25||Math.abs(evidence.sleep[0][0]-7.357142857142857)>1e-8||evidence.exposure[0][0]!==3.5)throw Error('Native export mismatch '+JSON.stringify(evidence));
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:50},maxChars:2000});evidence.errors=errors.ndjson;
for(const s of wb.worksheets.items){const range=s.name==='Cockpit'?'A1:O38':s.name==='Exposure'?'A1:J16':s.name==='Guide'?'A1:F16':'A1:H10';const preview=await wb.render({sheetName:s.name,range,scale:1,format:'png'});await fs.writeFile(dir+'/native-'+s.name.replaceAll(' ','-')+'.png',new Uint8Array(await preview.arrayBuffer()));}
await fs.writeFile(dir+'/native-export-verification.json',JSON.stringify(evidence,null,2));
console.log(JSON.stringify(evidence));
