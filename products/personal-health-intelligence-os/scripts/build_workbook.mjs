import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const root=process.env.HEALTH_OS_ROOT;
if(!root)throw new Error('Set HEALTH_OS_ROOT to the product directory.');
const outputDir=path.join(path.dirname(root),'outputs','health-os-0.1.0');
await fs.mkdir(outputDir,{recursive:true});
const {definitions}=JSON.parse(await fs.readFile(path.join(root,'adapters/mappings.json'),'utf8'));
const tokens=JSON.parse(await fs.readFile(path.join(root,'design/tokens.json'),'utf8'));
const c=tokens.color, wb=Workbook.create(),tables=[];
const cockpit=wb.worksheets.add('Cockpit');
const exposure=wb.worksheets.add('Exposure');
const byEntity=Object.fromEntries(definitions.map(d=>[d.entity,d]));
for(const d of definitions)wb.worksheets.add(d.tab);
const guide=wb.worksheets.add('Guide');
const col=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
// Google conversion drops OOXML t=d cells. Numeric serials retain date semantics.
const serialDate=v=>Date.parse(v)/86400000+25569;
const address=(entity,field,r)=>`'${byEntity[entity].tab}'!${col(byEntity[entity].fields.indexOf(field))}${r}`;
const range=(entity,field)=>`'${byEntity[entity].tab}'!$${col(byEntity[entity].fields.indexOf(field))}$6:$${col(byEntity[entity].fields.indexOf(field))}$505`;
const styles=(s,rect)=>{s.showGridLines=false;s.getRange(rect).format.font={name:'Arial',size:11,color:c.ink};s.getRange(rect).format.rowHeight=25;s.getRange(rect).format.verticalAlignment='center';};
for(const d of definitions){
 const s=wb.worksheets.getItem(d.tab),last=col(d.fields.length-1),end=5+Math.max(1,d.rows.length);
 styles(s,`A1:${last}${Math.max(end,10)}`);
 s.getRange('A1').values=[[d.tab]];s.getRange('A1').format.font={name:'Arial',size:16,bold:true,color:c.ink};
 s.mergeCells(`A2:${col(Math.min(6,d.fields.length-1))}2`);
 s.getRange('A2').values=[['Synthetic examples. Clear sample rows in your private copy. Unknown values stay blank.']];
 s.getRange('A2').format.font={name:'Arial',size:10,color:c.muted};
 s.getRange(`A5:${last}5`).values=[d.headers];
 s.getRange(`A5:${last}5`).format={fill:c.forest,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:48,horizontalAlignment:'center'};
 const matrix=d.rows.map(r=>d.fields.map(k=>{const v=r[k];if(v===undefined)return null;if(typeof v==='object')return JSON.stringify(v);if(d.properties[k].format==='date')return serialDate(v+'T00:00:00Z');if(d.properties[k].format==='date-time')return serialDate(v);return v;}));
 if(matrix.length)s.getRange(`A6:${last}${5+matrix.length}`).values=matrix;
 const t=s.tables.add(`A5:${last}${end}`,true,'PHI_'+d.entity);t.showBandedRows=false;
 for(let i=0;i<d.fields.length;i++){
  const k=d.fields[i],p=d.properties[k],l=col(i),r=s.getRange(`${l}6:${l}505`);
  s.getRange(`${l}5:${l}${end}`).format.columnWidthPx=k==='notes'?360:k==='id'||k.endsWith('_id')?286:p.type==='number'||p.type==='integer'?138:180;
  if(p.format==='date')r.setNumberFormat('yyyy-mm-dd');
  else if(p.format==='date-time')r.setNumberFormat('yyyy-mm-dd hh:mm');
  else if(p.type==='number')r.setNumberFormat('0.0');
  else if(p.type==='integer')r.setNumberFormat('0');
  if(p.enum&&p.type==='string')r.dataValidation={rule:{type:'list',values:p.enum}};
  if(['number','integer'].includes(p.type)&&p.minimum!==undefined&&p.maximum!==undefined)s.dataValidations.add({range:`${l}6:${l}505`,rule:{type:p.type==='integer'?'whole':'decimal',operator:'between',formula1:p.minimum,formula2:p.maximum}});
  if(k.includes('_0_10'))r.conditionalFormats.add('colorScale',{colors:[c.clayLight,c.forestLight],thresholds:[0,10]});
 }
 s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(1);
 s.getRange(`A6:${last}${end}`).format.wrapText=true;
 s.getRange(`A6:${last}${end}`).format.autofitRows();
 tables.push({entity:d.entity,sheet:d.tab,name:'PHI_'+d.entity,header_row:5,start_row:4,end_row:end,column_count:d.fields.length,dropdowns:d.fields.map((f,i)=>({index:i,options:d.properties[f].enum})).filter(x=>x.options)});
}
styles(cockpit,'A1:O62');cockpit.getRange('A1:O62').format.fill=c.canvas;
cockpit.getRange('A1:O62').format.columnWidthPx=90;
cockpit.getRange('A1:A62').format.columnWidthPx=25;
cockpit.getRange('B2').values=[['Your health, in context']];cockpit.getRange('B2').format.font={name:'Arial',size:17,bold:true,color:c.ink};
cockpit.mergeCells('B4:N4');cockpit.getRange('B4').values=[['Synthetic demonstration. Descriptive trends only. Choose your own priorities and leave unknowns blank.']];cockpit.getRange('B4').format.font={name:'Arial',size:11,color:c.muted};
cockpit.getRange('B6:D6').values=[['Review ends',serialDate('2026-10-14T00:00:00Z'),'']];cockpit.getRange('C6').setNumberFormat('yyyy-mm-dd');cockpit.getRange('C6').format.fill='#FFF0CC';
cockpit.mergeCells('F6:N6');cockpit.getRange('F6').values=[['First daily entry: date, sleep, energy, one note. Open the Daily tab.']];
const metrics=[['B8:D8','B9:D10','Days with one entry',`=COUNTIFS(G43:G49,1)`,'0'],['F8:H8','F9:H10','Mean sleep (h)',`=IF(COUNT(C43:C49)=0,"",AVERAGE(C43:C49))`,'0.0'],['J8:L8','J9:L10','Mean energy (0-10)',`=IF(COUNT(D43:D49)=0,"",AVERAGE(D43:D49))`,'0.0']];
for(const [labelR,valueR,label,f,num]of metrics){cockpit.mergeCells(labelR);cockpit.getRange(labelR).values=[[label]];cockpit.getRange(labelR).format.fill=c.surface;cockpit.mergeCells(valueR);cockpit.getRange(valueR).formulas=[[f]];cockpit.getRange(valueR).setNumberFormat(num);cockpit.getRange(valueR).format={fill:c.surface,font:{name:'Arial',size:18,bold:true,color:c.forest},horizontalAlignment:'left'};}
cockpit.mergeCells('B12:N12');cockpit.getRange('B12').values=[['LAST SEVEN DAYS']];cockpit.getRange('B12').format.font={name:'Arial',size:11,bold:true,color:c.muted};
cockpit.getRange('B42:G42').values=[['Date','Sleep (h)','Energy (0-10)','Fluid (mL)','Training (min)','Entries']];
for(let r=43;r<=49;r++){
 cockpit.getRange(`B${r}`).formulas=[[`=INT($C$6)-${49-r}`]];cockpit.getRange(`B${r}`).setNumberFormat('mmm d');
 const dates=range('daily_observation','local_date'),deleted=range('daily_observation','deleted_at');
 cockpit.getRange(`G${r}`).formulas=[[`=COUNTIFS(${dates},">="&B${r},${dates},"<"&B${r}+1)-COUNTIFS(${dates},">="&B${r},${dates},"<"&B${r}+1,${deleted},">0")`]];
 const fields=['sleep_hours','energy_0_10','fluid_ml','training_minutes'];
 for(let i=0;i<fields.length;i++){
  const dr=range('daily_observation','local_date'),vr=range('daily_observation',fields[i]);
  cockpit.getRange(`${col(i+2)}${r}`).formulas=[[`=IF(AND(G${r}=1,COUNTIFS(${dr},">="&B${r},${dr},"<"&B${r}+1,${vr},"<>")-COUNTIFS(${dr},">="&B${r},${dr},"<"&B${r}+1,${vr},"<>",${deleted},">0")=1),SUMIFS(${vr},${dr},">="&B${r},${dr},"<"&B${r}+1)-SUMIFS(${vr},${dr},">="&B${r},${dr},"<"&B${r}+1,${deleted},">0"),"")`]];
 }
}
const chart=(r,title,pos,color)=>{const ch=cockpit.charts.add('line',r);ch.title=title;ch.titleTextStyle.typeface='Arial';ch.titleTextStyle.fontSize=13;ch.hasLegend=false;ch.xAxis={axisType:'textAxis',textStyle:{typeface:'Arial',fontSize:11}};ch.yAxis={numberFormatCode:'0.0',numberFormatSourceLinked:false,textStyle:{typeface:'Arial',fontSize:11}};ch.series.items[0].line={fill:color,style:'solid',width:2};ch.setPosition(...pos);return ch;};
// String category labels keep dates readable in both Excel and Sheets.
cockpit.getRange('H42:I42').values=[['Day','Sleep (h)']];cockpit.getRange('K42:L42').values=[['Day','Energy (0-10)']];
for(let r=43;r<=49;r++){cockpit.getRange(`H${r}:I${r}`).formulas=[[`=TEXT(B${r},"mmm d")`,`=IF(C${r}="","",C${r})`]];cockpit.getRange(`K${r}:L${r}`).formulas=[[`=TEXT(B${r},"mmm d")`,`=IF(D${r}="","",D${r})`]];}
chart(cockpit.getRange('H42:I49'),'Sleep duration (h)',['B14','H27'],c.forest);
chart(cockpit.getRange('K42:L49'),'Energy reported (0-10)',['I14','O27'],c.clay);
cockpit.mergeCells('B29:N29');cockpit.getRange('B29').values=[['Weekly review']];cockpit.getRange('B29').format.font={name:'Arial',size:15,bold:true};
cockpit.mergeCells('B31:N31');cockpit.getRange('B31').values=[['Review coverage, missing values, changes and confounders. Record one chosen next action in Reviews.']];
cockpit.mergeCells('B33:F33');cockpit.getRange('B33').values=[['Mean logged fluid (mL)']];cockpit.getRange('G33:H33').merge();cockpit.getRange('G33').formulas=[['=IF(COUNT(E43:E49)=0,"",AVERAGE(E43:E49))']];cockpit.getRange('G33').setNumberFormat('#,##0');
cockpit.mergeCells('J33:M33');cockpit.getRange('J33').values=[['Training logged (min)']];cockpit.getRange('N33').formulas=[['=IF(COUNT(F43:F49)=0,"",SUM(F43:F49))']];
cockpit.mergeCells('B36:N37');cockpit.getRange('B36').values=[['Use Supplements, Foods, Experiments and Reviews as your libraries. Check Exposure for ingredient overlap arithmetic. Detailed event tabs do not automatically add to Daily summaries.']];cockpit.getRange('B36').format.wrapText=true;
cockpit.mergeCells('B40:N40');cockpit.getRange('B40').values=[['Chart data. Duplicate daily dates or missing measurements produce gaps, not invented zeros.']];
cockpit.getRange('B42:F49').format.columnWidthPx=90;

styles(exposure,'A1:J22');exposure.getRange('A1:J22').format.columnWidthPx=160;
exposure.getRange('A2').values=[['Supplement exposure (UTC day)']];exposure.getRange('A2').format.font={name:'Arial',size:16,bold:true};
exposure.mergeCells('A4:J4');exposure.getRange('A4').values=[['Taken events by UTC day. Both labels must be verified. Unsupported units block the total. No dose recommendation.']];
exposure.getRange('A6:B8').values=[['Date',serialDate('2026-10-01T00:00:00Z')],['Ingredient','vitamin_b6'],['Mass total (mg)',null]];exposure.getRange('B6').setNumberFormat('yyyy-mm-dd');exposure.getRange('B6:B7').format.fill='#FFF0CC';
exposure.getRange('A12:J12').values=[['Ingredient','Product ID','Per serving','Unit','Servings taken','Exposure','Mass (mg)','Ingredient label verified','Product label verified','Inclusion']];exposure.getRange('A12:J12').format={fill:c.forest,font:{name:'Arial',bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:48};
exposure.getRange('B12:B30').format.columnWidthPx=286;
for(let r=13;r<=32;r++){
 const sr=r-7;
 for(const [dest,field]of [['A','ingredient_name'],['B','product_id'],['C','amount_per_serving'],['D','unit'],['H','label_verified']])exposure.getRange(`${dest}${r}`).formulas=[[`=IF(${address('ingredient','ingredient_name',sr)}="","",${address('ingredient',field,sr)})`]];
 const intakeArgs=`${range('intake','servings')},${range('intake','product_id')},B${r},${range('intake','taken_at')},">="&INT($B$6),${range('intake','taken_at')},"<"&INT($B$6)+1,${range('intake','event_status')},"taken"`;
 exposure.getRange(`E${r}`).formulas=[[`=IF(A${r}="","",SUMIFS(${intakeArgs})-SUMIFS(${intakeArgs},${range('intake','deleted_at')},">0"))`]];
 exposure.getRange(`F${r}`).formulas=[[`=IF(A${r}="","",C${r}*E${r})`]];
 exposure.getRange(`I${r}`).formulas=[[`=IF(A${r}="","",IF(COUNTIFS(${range('product','id')},B${r})=1,INDEX(${range('product','label_verified')},MATCH(B${r},${range('product','id')},0)),FALSE))`]];
 exposure.getRange(`J${r}`).formulas=[[`=IF(A${r}="","",IF(OR(${address('ingredient','deleted_at',sr)}<>"",COUNTIFS(${range('product','id')},B${r},${range('product','deleted_at')},">0")>0),IF(E${r}>0,"review source","excluded"),IF(AND(H${r}=TRUE,I${r}=TRUE,ISNUMBER(${address('ingredient','amount_per_serving',sr)}),COUNTIFS(${range('product','id')},B${r})=1),IF(OR(D${r}="mg",D${r}="g",D${r}="mcg"),"included","unsupported unit"),"review source")))`]];
 exposure.getRange(`G${r}`).formulas=[[`=IF(J${r}<>"included","",IF(D${r}="mg",F${r},IF(D${r}="g",F${r}*1000,F${r}/1000)))`]];
}
exposure.getRange('B8').formulas=[[`=IF(OR(NOT(ISNUMBER(B6)),B7=""),"",IF(COUNTIFS(${range('ingredient','ingredient_name')},B7)>COUNTIFS(A13:A32,B7),"Extend Exposure",IF(COUNTIFS(A13:A32,B7,J13:J32,"unsupported unit")+COUNTIFS(A13:A32,B7,J13:J32,"review source")>0,"Review source",IF(COUNTIFS(A13:A32,B7,J13:J32,"included")=0,"",SUMIFS(G13:G32,A13:A32,B7,J13:J32,"included")))))`]];
exposure.getRange('B8').setNumberFormat('0.0');

styles(guide,'A1:F24');guide.getRange('A1:F24').format.columnWidthPx=150;
const lines=[['Start in your own workspace',''],['1. Make a private copy','Copy this workbook and the supplied protocols. Retain the product master unchanged.'],['2. Practice once','Change the review date and edit a synthetic Daily row. Confirm the cockpit changes.'],['3. Remove examples','Clear data rows on all 22 record tabs in your own copy. Preserve headers and formulas on Cockpit and Exposure.'],['4. First check-in','Add date, sleep, energy and a note. Unknown values stay blank.'],['5. Identity and provenance','The steward assigns UUIDs and source metadata before export. Optional AI access is disabled by default.'],['6. Review weekly','Use Reviews. Separate observations from hypotheses. No overall health score is calculated.'],['7. Export','Download your own workbook as XLSX and export record tabs as CSV. Keep attachments separately.'],['8. Upgrade','Copy a new template, export your current data, map by stable ID, preview conflicts, then import. Never overwrite records with sample data.'],['Capacity','Dashboard formulas cover input rows 6-505. Exposure shows the first 20 ingredient lines. Extend these ranges before exceeding the limits.'],['Complete Edition','Google owns measurements and files. Notion owns narrative reviews. No automatic synchronization is active.'],['Privacy','Workspace permissions enforce access. Consent columns document choices and do not enforce OAuth scopes.'],['Data types','Date-time columns and the Exposure day use UTC. Date-only fields retain their local calendar date. The source IANA zone remains in Timezone.'],['Evidence','All included health numbers and product labels are synthetic, not nutrient reference data.']];
for(let i=0;i<lines.length;i++){guide.getRange(`A${i+2}:B${i+2}`).merge();guide.getRange(`A${i+2}`).values=[[lines[i][0]]];guide.getRange(`C${i+2}:F${i+2}`).merge();guide.getRange(`C${i+2}`).values=[[lines[i][1]]];guide.getRange(`C${i+2}`).format.wrapText=true;guide.getRange(`A${i+2}:F${i+2}`).format.rowHeight=52;}
guide.getRange('A2').format.font={name:'Arial',size:16,bold:true};

wb.recalculate();
const expected=definitions.find(d=>d.entity==='daily_observation').rows.slice(-7);
const ev={expected_sleep_mean:expected.reduce((n,r)=>n+r.sleep_hours,0)/7,actual_sleep_mean:cockpit.getRange('F9').values,exposure:exposure.getRange('B8').values};
if(Math.abs(cockpit.getRange('F9').values[0][0]-ev.expected_sleep_mean)>1e-6)throw new Error('Sleep aggregate mismatch');
if(exposure.getRange('B8').values[0][0]!==3.5)throw new Error('Exposure mismatch: '+JSON.stringify({summary:ev,rows:exposure.getRange('A13:J14').values}));
// Input perturbation proves recalculation, then restore before export.
const daily=wb.worksheets.getItem('Daily'),v=daily.getRange('B19').values[0][0];
daily.getRange('B19').values=[[v+1]];const changed=cockpit.getRange('F9').values[0][0];
if(Math.abs(changed-ev.expected_sleep_mean-1/7)>1e-6)throw new Error('Input recalculation failed');
daily.getRange('B19').values=[[v]];wb.recalculate();ev.perturbation_pass=true;
// Independent boundary cases use temporary synthetic edits and restore every input.
const boundaryChecks=[];
const inputCell=(entity,field,row=6)=>wb.worksheets.getItem(byEntity[entity].tab).getRange(`${col(byEntity[entity].fields.indexOf(field))}${row}`);
const expect=(actual,expected,label)=>{if(actual!==expected)throw new Error(`${label}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);boundaryChecks.push(label);};
const setTemporary=(cell,value)=>{const previous=cell.values?.[0]?.[0];cell.values=[[value]];return()=>{if(previous===undefined||previous===null||previous==='')cell.clear({applyTo:'contents'});else cell.values=[[previous]];};};
let undo=setTemporary(inputCell('daily_observation','sleep_hours',19),0);
expect(cockpit.getRange('C49').values[0][0],0,'Recorded zero remains zero');undo();
const sleepCell=inputCell('daily_observation','sleep_hours',19),sleepOriginal=sleepCell.values[0][0];sleepCell.clear({applyTo:'contents'});
expect(cockpit.getRange('C49').values[0][0],'','Missing sleep remains a chart gap');sleepCell.values=[[sleepOriginal]];
undo=setTemporary(inputCell('daily_observation','local_date',20),inputCell('daily_observation','local_date',19).values[0][0]);
expect(cockpit.getRange('C49').values[0][0],'','Duplicate date with blank measurement is not silently selected');
expect(cockpit.getRange('B9').values[0][0],6,'Duplicate daily rows cannot inflate coverage');undo();
undo=setTemporary(inputCell('daily_observation','deleted_at',19),serialDate('2026-10-15T00:00:00Z'));
expect(cockpit.getRange('C49').values[0][0],'','Tombstoned daily row does not contribute');undo();
undo=setTemporary(inputCell('product','label_verified'),false);
expect(exposure.getRange('B8').values[0][0],'Review source','Unverified product blocks the total');undo();
undo=setTemporary(inputCell('ingredient','label_verified'),false);
expect(exposure.getRange('B8').values[0][0],'Review source','Unverified ingredient blocks the total');undo();
undo=setTemporary(inputCell('ingredient','unit'),'IU');
expect(exposure.getRange('B8').values[0][0],'Review source','Unsupported unit cannot disappear from a partial sum');undo();
const amount=inputCell('ingredient','amount_per_serving'),amountOriginal=amount.values[0][0];amount.clear({applyTo:'contents'});
expect(exposure.getRange('B8').values[0][0],'Review source','Missing label amount cannot become zero');amount.values=[[amountOriginal]];
undo=setTemporary(inputCell('intake','deleted_at'),serialDate('2026-10-15T00:00:00Z'));
expect(exposure.getRange('B8').values[0][0],1.5,'Tombstoned taken event is excluded');undo();
undo=setTemporary(inputCell('product','id',8),inputCell('product','id').values[0][0]);
expect(exposure.getRange('B8').values[0][0],'Review source','Duplicate product identity blocks lookup');undo();
const undoAmount=setTemporary(inputCell('ingredient','amount_per_serving',7),1500),undoUnit=setTemporary(inputCell('ingredient','unit',7),'mcg');
expect(exposure.getRange('B8').values[0][0],3.5,'Mass units normalize before summation');undoUnit();undoAmount();
wb.recalculate();
expect(exposure.getRange('B8').values[0][0],3.5,'Exposure source restored after boundary checks');
expect(cockpit.getRange('F9').values[0][0],ev.expected_sleep_mean,'Daily source restored after boundary checks');
ev.boundary_checks=boundaryChecks;
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},maxChars:3000});ev.error_scan=errors.ndjson;
await fs.writeFile(path.join(outputDir,'workbook-verification.json'),JSON.stringify(ev,null,2));
for(let i=0;i<wb.worksheets.items.length;i++){
 const s=wb.worksheets.items[i],rect=s.name==='Cockpit'?'A1:O38':s.name==='Exposure'?'A1:H16':s.name==='Guide'?'A1:F16':'A1:H10';
 const image=await wb.render({sheetName:s.name,range:rect,scale:1,format:'png'});
 await fs.writeFile(path.join(outputDir,'preview-'+s.name.replaceAll(' ','-')+'.png'),new Uint8Array(await image.arrayBuffer()));
}
await fs.writeFile(path.join(outputDir,'tables.json'),JSON.stringify(tables,null,2));
const output=await SpreadsheetFile.exportXlsx(wb);await output.save(path.join(outputDir,'Personal-Health-Intelligence-OS-0.1.0.xlsx'));
console.log(JSON.stringify({outputDir,sheets:wb.worksheets.items.length,verification:ev}));
