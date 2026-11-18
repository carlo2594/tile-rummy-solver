// Rummikub solver: dynamic programming over tile numbers 1..13
// (approach after van Rijn, Takes & Vis, "The Complexity of Rummikub Problems").
// table[c][v], rack[c][v]: counts (0..2) for color c (0..3), number v (1..13).
// relax = true: table tiles may be left out (each one costs a big penalty). Used to find
// which table tiles don't fit, and to still give an answer when the table is entered wrong.
const PAIRS = [], PIDX = {};
for (let a = 0; a < 4; a++) for (let b = a; b < 4; b++) { PIDX[a * 4 + b] = PAIRS.length; PAIRS.push([a, b]); }
const pidx = (x, y) => x <= y ? PIDX[x * 4 + y] : PIDX[y * 4 + x];

function slotActions(L) {
  if (L === 0) return [['n', 0, 0], ['e', 1, 1]];
  if (L === 1 || L === 2) return [['e', L + 1, 1]];
  return [['n', 0, 0], ['e', 3, 1], ['r', 1, 1]];
}

const optCache = new Map();
function colorOptions(pi, lo, hi, jRem) {
  const key = ((pi * 5 + lo) * 5 + hi) * 5 + jRem;
  if (optCache.has(key)) return optCache.get(key);
  const [a, b] = PAIRS[pi];
  const out = [], seen = new Set();
  for (const s0 of slotActions(a)) for (const s1 of slotActions(b)) {
    const e = s0[2] + s1[2];
    const np = pidx(s0[1], s1[1]);
    for (let u = lo; u <= hi; u++) for (let j = 0; j <= Math.min(jRem, 2); j++) {
      const g = u + j - e;
      if (g < 0 || g > 2) continue;
      const sig = np + ':' + u + ':' + j + ':' + g;
      if (seen.has(sig)) continue;
      seen.add(sig);
      out.push({ np, a0: s0[0], a1: s1[0], u, j, g });
    }
  }
  optCache.set(key, out);
  return out;
}

const groupsOk = (gs, mg) => gs === 0 || (mg <= 1 && gs >= 3 && gs <= 4) || (gs >= 6 && gs <= 8);

function rummySolve(table, rack, tableJ, rackJ, initial, relax, saveJ) {
  if (initial) { tableJ = 0; relax = false; }
  // saveJ: keep rack jokers unless playing them empties the rack (wins the round this turn)
  let rackReal = 0;
  for (let c = 0; c < 4; c++) for (let v = 1; v <= 13; v++) rackReal += rack[c][v];
  const J = tableJ + rackJ;
  const enc = (ps, j, gs, mg) => (((((ps[0] * 10 + ps[1]) * 10 + ps[2]) * 10 + ps[3]) * 3 + j) * 9 + gs) * 3 + mg;
  const better = (x, y) => {
    if (x.miss !== y.miss) return x.miss < y.miss;
    return initial ? (x.val * 100 + x.cnt > y.val * 100 + y.cnt) : (x.cnt * 1000 + x.val > y.cnt * 1000 + y.val);
  };
  let cur = new Map();
  cur.set(0, { ps: [0, 0, 0, 0], j: 0, gs: 0, mg: 0, cnt: 0, val: 0, miss: 0, prev: null, ch: null });
  for (let v = 1; v <= 13; v++) {
    for (let c = 0; c < 4; c++) {
      const t = initial ? 0 : table[c][v], r = rack[c][v];
      const next = new Map();
      for (const node of cur.values()) {
        const opts = relax ? colorOptions(node.ps[c], 0, t + r, J - node.j) : colorOptions(node.ps[c], t, t + r, J - node.j);
        for (const o of opts) {
          const gs = node.gs + o.g; if (gs > 8) continue;
          const mg = Math.max(node.mg, o.g);
          const ps = node.ps.slice(); ps[c] = o.np;
          const j = node.j + o.j;
          const fromTable = Math.min(o.u, t), fromRack = o.u - fromTable;
          const played = fromRack + o.j;
          const nn = { ps, j, gs, mg, cnt: node.cnt + played, val: node.val + played * v,
            miss: node.miss + (t - fromTable), prev: node, ch: { c, v, t, o } };
          const k = enc(ps, j, gs, mg);
          const ex = next.get(k);
          if (!ex || better(nn, ex)) next.set(k, nn);
        }
      }
      cur = next;
    }
    const reset = new Map();
    for (const n of cur.values()) {
      if (!groupsOk(n.gs, n.mg)) continue;
      const nn = Object.assign({}, n, { gs: 0, mg: 0 });
      const k = enc(nn.ps, nn.j, 0, 0);
      const ex = reset.get(k);
      if (!ex || better(nn, ex)) reset.set(k, nn);
    }
    cur = reset;
  }
  let best = null;
  for (const n0 of cur.values()) {
    if (!n0.ps.every(p => PAIRS[p].every(L => L === 0 || L === 3))) continue;
    const jt = Math.min(n0.j, tableJ);           // table jokers that were placed
    if (!relax && jt < tableJ) continue;
    const jr = n0.j - jt;                        // rack jokers played
    const n = Object.assign({}, n0, { cnt: n0.cnt - jt, miss: n0.miss + (tableJ - jt) });
    if (saveJ && jr > 0 && n.cnt < rackReal + rackJ) continue;   // joker only if it wins
    if (initial && n.val < 30) continue;
    if (!best || better(n, best)) best = n;
  }
  if (!best) return null;
  const choices = [];
  for (let n = best; n && n.ch; n = n.prev) choices.push(n.ch);
  choices.reverse();
  return build(choices, tableJ, best);
}

function build(choices, tableJ, best) {
  const slots = [0, 1, 2, 3].map(() => [[], []]);
  const sets = [], leftover = [];
  let jokerCount = 0;
  const close = s => { if (s.length) sets.push({ kind: 'run', tiles: s.slice() }); s.length = 0; };
  let idx = 0;
  for (let v = 1; v <= 13; v++) {
    const groupTiles = [];
    for (let c = 0; c < 4; c++) {
      const { t, o } = choices[idx++];
      const fromTable = Math.min(o.u, t);
      for (let i = 0; i < t - fromTable; i++) leftover.push({ c, v });
      const tiles = [];
      for (let i = 0; i < fromTable; i++) tiles.push({ c, v, src: 'table' });
      for (let i = 0; i < o.u - fromTable; i++) tiles.push({ c, v, src: 'rack' });
      for (let i = 0; i < o.j; i++) { tiles.push({ c, v, joker: true, src: jokerCount < tableJ ? 'table' : 'rack' }); jokerCount++; }
      const order = [0, 1].sort((x, y) => Math.min(slots[c][x].length, 3) - Math.min(slots[c][y].length, 3));
      [o.a0, o.a1].forEach((act, i) => {
        const s = slots[c][order[i]];
        if (act === 'n') close(s);
        else if (act === 'e') s.push(tiles.shift());
        else { close(s); s.push(tiles.shift()); }
      });
      groupTiles.push(tiles);
    }
    const total = groupTiles.reduce((a, g) => a + g.length, 0);
    if (total) {
      const maxg = Math.max(...groupTiles.map(g => g.length));
      const G = (total <= 4 && maxg <= 1) ? 1 : 2;
      const groups = Array.from({ length: G }, () => []);
      groupTiles.filter(g => g.length === 2).forEach(g => { groups[0].push(g[0]); groups[1].push(g[1]); });
      groupTiles.filter(g => g.length === 1).forEach(g => {
        const tgt = groups.reduce((m, gr) => gr.length < m.length ? gr : m, groups[0]);
        tgt.push(g[0]);
      });
      groups.forEach(gr => sets.push({ kind: 'group', tiles: gr }));
    }
  }
  slots.forEach(cs => cs.forEach(close));
  const played = sets.flatMap(s => s.tiles).filter(t => t.src === 'rack');
  const leftoverJ = Math.max(0, tableJ - Math.min(jokerCount, tableJ));
  const value = played.reduce((a, t) => a + t.v, 0);
  return { sets, played, count: best.cnt, value, leftover, leftoverJ };
}

if (typeof module !== 'undefined') module.exports = { solve: rummySolve, rummySolve };

// ---- Web Worker entry: the page sends {id, mode, ...}; we reply {id, res, ms} ----
if (typeof importScripts === 'function') {
  const blank = () => [0, 1, 2, 3].map(() => Array(14).fill(0));
  self.onmessage = e => {
    const d = e.data, t0 = Date.now();
    let res;
    if (d.mode === 'check') {
      res = rummySolve(d.table, blank(), d.tj, 0, false, true);
    } else {
      res = rummySolve(d.table, d.rack, d.tj, d.rj, d.initial, false, d.saveJ);
      if (!res && !d.initial) { res = rummySolve(d.table, d.rack, d.tj, d.rj, false, true, d.saveJ); if (res) res.relaxed = true; }
    }
    self.postMessage({ id: d.id, res, ms: Date.now() - t0 });
  };
}
