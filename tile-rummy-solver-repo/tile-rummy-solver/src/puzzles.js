const {solve}=require(__dirname+'/solver.js');
const C=['R','B','K','O'];
const empty=()=>[0,1,2,3].map(()=>Array(14).fill(0));
function put(g,s){if(s)s.split(' ').forEach(x=>{g[C.indexOf(x[0])][+x.slice(1)]++;});return g;}
const P=[
 {id:'puzzle-1',title:'Extend a run',level:'Easy',table:'R3 R4 R5 B7 K7 O7',rack:'R6 B2',tj:0,rj:0,initial:false,
  hint:'Look at the end of the red run.'},
 {id:'puzzle-2',title:'Split a long run',level:'Easy',table:'B2 B3 B4 B5 B6 B7',rack:'B4 K9',tj:0,rj:0,initial:false,
  hint:'A run of six can become two runs of three or more.'},
 {id:'puzzle-3',title:'Borrow from a group of four',level:'Medium',table:'R8 B8 K8 O8 K1 K2 K3',rack:'R9 R10 O4',tj:0,rj:0,initial:false,
  hint:'A group of four still works with three tiles.'},
 {id:'puzzle-4',title:'Turn runs into groups',level:'Medium',table:'R4 R5 R6 B4 B5 B6 K4 K5 K6',rack:'O4 O5',tj:0,rj:0,initial:false,
  hint:'Two orange tiles can’t make a run on their own. What if the table were groups instead?'},
 {id:'puzzle-5',title:'Free the joker',level:'Hard',table:'R10 R12 K4 K5 K6',rack:'R11 B11 O11',tj:1,rj:0,initial:false,
  hint:'The joker is standing in for a tile you have.'},
 {id:'puzzle-6',title:'Make your first meld',level:'Easy',table:'',rack:'R10 R11 R12 B1 K1 O1 B7',tj:0,rj:0,initial:true,
  hint:'You need 30 points from your own tiles. Every set you lay down counts.'},
];
const out=P.map(p=>{
  const T=put(empty(),p.table),R=put(empty(),p.rack);
  const strictTable = p.table||p.tj ? solve(T,empty(),p.tj,0,false,false) : 'n/a';
  const r=solve(T,R,p.tj,p.rj,p.initial,false);
  const sets=r.sets.map(s=>({kind:s.kind,tiles:s.tiles.map(t=>({c:t.c,v:t.v,j:!!t.joker,r:t.src==='rack'}))}));
  console.error(p.id,'tableValid',!!strictTable,'count',r.count,'value',r.value, sets.map(s=>s.tiles.map(t=>(t.j?'J':'')+C[t.c]+t.v+(t.r?'*':'')).join(' ')).join(' | '));
  return Object.assign({},p,{tableSpec:p.table,rackSpec:p.rack,table:T,rack:R,answer:{count:r.count,value:r.value,sets}});
});
const SETS={'puzzle-1':['R3 R4 R5','B7 K7 O7'],'puzzle-2':['B2 B3 B4 B5 B6 B7'],'puzzle-3':['R8 B8 K8 O8','K1 K2 K3'],'puzzle-4':['R4 R5 R6','B4 B5 B6','K4 K5 K6'],'puzzle-5':['R10 J R12','K4 K5 K6'],'puzzle-6':[]};
out.forEach(p=>p.tableSets=SETS[p.id]);
require('fs').writeFileSync(__dirname+'/puzzles.json',JSON.stringify(out));
