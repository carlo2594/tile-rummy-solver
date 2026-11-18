import re, json, pathlib, html as H
SRC = pathlib.Path(__file__).resolve().parent
OUT = SRC.parent / 'site'
NAME = 'Tile Rummy Solver'
DOMAIN = 'https://tilerummysolver.com'
EMAIL = 'support@tilerummysolver.com'
TODAY = '2026-11-13'
NAV = [('index.html', 'Solver'), ('how-to-play.html', 'Rules'), ('strategy.html', 'Strategy'), ('puzzles.html', 'Puzzles'), ('faq.html', 'FAQ')]
GUIDES = [('how-to-play.html', 'How to play'), ('first-meld.html', 'First meld'), ('jokers.html', 'Jokers'), ('scoring.html', 'Scoring'),
          ('strategy.html', 'Strategy tips'), ('puzzles.html', 'Practice puzzles'), ('faq.html', 'FAQ'), ('about.html', 'About'), ('privacy.html', 'Privacy policy')]

def clean(file):
    return DOMAIN + '/' if file == 'index.html' else DOMAIN + '/' + file.replace('.html', '')

def head(file, title, desc, extra=''):
    assert len(title) <= 60, (file, len(title), title)
    assert len(desc) <= 155, (file, len(desc))
    t, d = H.escape(title), H.escape(desc)
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{clean(file)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{clean(file)}">
<meta property="og:image" content="{DOMAIN}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME}: find the best move in tile rummy">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2f5d50">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="site.css">{extra}
'''

def topbar(cur):
    cur_attr = ' aria-current="page"'
    links = ''.join(f'<a href="{h}"{cur_attr if h == cur else ""}>{t}</a>' for h, t in NAV)
    return f'''<header class="topbar"><div class="topbar-in">
  <a class="brand" href="index.html"><span class="brand-tile" aria-hidden="true">7</span>{NAME}</a>
  <nav class="nav" aria-label="Main">{links}</nav>
</div></header>'''

FOOT = f'''<footer class="sitefoot"><div class="sitefoot-in">
  <nav class="guides" aria-label="Guides">{''.join(f'<a href="{h}">{t}</a>' for h, t in GUIDES)}</nav>
  <span>© <span data-year>2026</span> {NAME} · by Carlo J · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
  <a class="tip" data-kofi href="#" hidden>☕ Support this project</a>
  <span class="tm">Works with Rummikub® and other tile rummy games. Rummikub® is a registered trademark of its owner. {NAME} is an independent fan-made tool and is not affiliated with or endorsed by the trademark owner.</span>
</div></footer>
<script src="site.js"></script>'''

def page(file, title, desc, body, extra=''):
    (OUT / file).write_text(f'''<!DOCTYPE html>
<html lang="en">
<head>
{head(file, title, desc, extra)}</head>
<body>
{topbar(file)}
<main class="prose">
{body}
</main>
{FOOT}
</body>
</html>
''')

def tl(spec):
    m = {'R': 'r', 'B': 'b', 'K': 'k', 'O': 'o'}
    out = []
    for x in spec.split():
        if x == 'J':
            out.append('<span class="t j" aria-label="joker">☺</span>')
        else:
            out.append(f'<span class="t {m[x[0]]}">{x[1:]}</span>')
    return '<span class="tiles-inline">' + ''.join(out) + '</span>'

def ld(obj):
    return '\n<script type="application/ld+json">' + json.dumps(obj) + '</script>'

# ---------------- Solver page ----------------
puzzles = json.load(open(SRC / 'puzzles.json'))
pz_js = json.dumps([{k: p[k] for k in ('id', 'table', 'rack', 'tj', 'rj', 'initial')} for p in puzzles])
t = open(SRC / 'template.html').read()
t = t.replace('/*PUZZLES*/', pz_js)
home_title = 'Tile Rummy Solver: Find the Best Move (Rummikub-Style)'
home_desc = 'Free tile rummy solver for Rummikub-style games. Enter the table and your rack to see the move that plays the most tiles, with jokers.'
app_ld = ld({"@context": "https://schema.org", "@type": "WebApplication", "name": NAME, "url": DOMAIN + "/",
             "applicationCategory": "GameApplication", "operatingSystem": "Any (web browser)",
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
             "description": home_desc, "author": {"@type": "Person", "name": "Carlo J"}})
t = re.sub(r'<meta charset="utf-8">.*?<style>', lambda m: head('index.html', home_title, home_desc, app_ld) + '<style>', t, count=1, flags=re.S)
t = t.replace('<h1>Rummikub Solver</h1>', f'<h1>{NAME}</h1>')
t = t.replace('<p class="lede">Tap your tiles. Get the best move.</p>', '<p class="lede">Tap your tiles. Get the best move. Works with Rummikub-style games.</p>')
t = t.replace('<br>Made by Carlo J.</p>', '</p>')
t = t.replace('<body>\n<main>', '<body>\n' + topbar('index.html') + '\n<main>')
t = t.replace('</main>\n\n<script src="solver.js', '</main>\n' + FOOT + '\n\n<script src="solver.js', 1)
assert 'class="topbar"' in t and 'class="sitefoot"' in t and 'fonts.googleapis' not in t and '/*PUZZLES*/' not in t
(OUT / 'index.html').write_text(t)
(OUT / 'solver.js').write_text(open(SRC / 'solver.js').read())

# ---------------- How to play ----------------
page('how-to-play.html', 'How to Play Rummikub: Rules Explained Simply',
 'The rules of Rummikub-style tile rummy in plain words: runs, groups, the 30-point first meld, jokers, rearranging the table and scoring.',
f'''<h1>How to play</h1>
<p class="intro">The rules of Rummikub and similar tile rummy games, explained in plain words. It takes about five minutes to learn.</p>

<h2>What's in the box</h2>
<p>There are 106 tiles: the numbers 1 to 13 in four colors (red, blue, black and orange), two copies of each, plus 2 jokers. The game is for 2 to 4 players.</p>

<h2>Goal</h2>
<p>Be the first to play every tile from your rack onto the table.</p>

<h2>Setup</h2>
<ol>
  <li>Turn all tiles face down and mix them.</li>
  <li>Each player takes 14 tiles and stands them on their rack so nobody else can see them.</li>
  <li>Each player draws one tile. The highest number goes first, then play passes to the left. Put those tiles back in the pool.</li>
</ol>

<h2>The two kinds of sets</h2>
<h3>Run</h3>
<p>Three or more numbers in a row, all the same color: {tl('R4 R5 R6')} or {tl('B9 B10 B11 B12')}. A run can't wrap around from 13 back to 1.</p>
<h3>Group</h3>
<p>Three or four tiles with the same number, each a different color: {tl('R8 B8 K8')} or {tl('R2 B2 K2 O2')}. A group can't have two tiles of the same color.</p>

<h2>Your first move: the 30-point meld</h2>
<p>Before you can do anything else, you must put down one or more sets from your own rack worth at least 30 points in total. For example, {tl('R10 R11 R12')} is worth 33. You can't use tiles already on the table. The <a href="first-meld.html">first meld guide</a> covers this in detail.</p>

<h2>A normal turn</h2>
<p>After your first meld, on each turn you either:</p>
<ul>
  <li><strong>Play</strong> one or more tiles from your rack, or</li>
  <li><strong>Draw</strong> one tile from the pool if you can't (or don't want to) play. Your turn then ends.</li>
</ul>
<p>Many groups play with a time limit of one minute per turn.</p>

<h2>Rearranging the table</h2>
<p>This is what makes the game fun. On your turn you can move tiles already on the table, as long as every set is valid when you finish and you've played at least one tile from your rack. You can:</p>
<ul>
  <li><strong>Add</strong> to a set: put {tl('R7')} on the end of {tl('R4 R5 R6')}.</li>
  <li><strong>Take</strong> a tile from a set of four or more to use somewhere else.</li>
  <li><strong>Split</strong> a long run: {tl('B3 B4 B5 B6 B7 B8')} becomes {tl('B3 B4 B5')} and {tl('B6 B7 B8')}, or you can insert a tile in the middle.</li>
  <li><strong>Combine</strong> tiles from several sets into new ones.</li>
</ul>
<p>Finding these moves is the hard part, and it's exactly what the <a href="index.html">solver</a> does when you're practicing. Try the <a href="puzzles.html">practice puzzles</a> to see each kind of move.</p>

<h2>Jokers</h2>
<p>A joker can stand in for any tile. If you hold the exact tile a joker on the table stands for, you can swap it in and take the joker, but you must use the joker again on the same turn. See the <a href="jokers.html">joker guide</a>.</p>

<h2>Winning and scoring</h2>
<p>The first player to empty their rack wins the round. Everyone else loses the value of the tiles left on their rack, and a joker left over costs 30. The <a href="scoring.html">scoring guide</a> has a full example.</p>

<div class="callout"><strong>House rules vary.</strong> Some groups use a different first-meld total or turn timer. Agree before you start.</div>

<a class="cta" href="index.html">Try the solver</a>''')

# ---------------- First meld ----------------
page('first-meld.html', 'Rummikub First Meld: The 30-Point Rule Explained',
 'How the 30-point initial meld works in Rummikub-style games: what counts, jokers, examples, common mistakes and how to find your opening play.',
f'''<h1>The first meld (30 points)</h1>
<p class="intro">Your opening play has its own rule. Until you make it, you can't touch the table at all.</p>

<h2>The rule</h2>
<p>Your first play must be one or more valid sets, all from your own rack, worth at least <strong>30 points</strong> in total. Each tile is worth its number. You add up every set you lay down that turn.</p>
<ul>
  <li>{tl('R10 R11 R12')} = 33 points. That's enough on its own.</li>
  <li>{tl('B5 K5 O5')} = 15 and {tl('O7 O8 O9')} = 24. Together that's 39, which is enough.</li>
  <li>{tl('R1 B1 K1')} = 3. Low tiles barely help.</li>
</ul>

<h2>What you can't do on the first meld</h2>
<ul>
  <li>Use tiles that are already on the table, or add to other players' sets.</li>
  <li>Rearrange the table. That's allowed from your next turn onward.</li>
  <li>Count tiles that aren't in a finished, valid set.</li>
</ul>
<p>Once your first meld is down, some groups let you keep playing on that same turn, and others make you wait a turn. Agree before the game.</p>

<h2>Jokers in the first meld</h2>
<p>A joker counts as the number it stands for. In {tl('R9 J R11')}, the joker is a 10, so the run is worth 30.</p>

<h2>If you can't make 30</h2>
<p>Draw one tile and your turn ends. That's common in the first few rounds. Keep your high tiles together, because they get you to 30 fastest.</p>

<h2>Tips</h2>
<ul>
  <li>Look for high runs and groups first (10s to 13s).</li>
  <li>Two small sets can add up. Don't stop at the first set you see.</li>
  <li>If you make 30 with tiles to spare, think about holding some back so you have options next turn.</li>
</ul>

<h2>Let the solver check</h2>
<p>In the <a href="index.html">solver</a>, mark your rack in step 2 and tick <em>First meld</em>. It finds the highest-scoring opening play from your own tiles, or tells you to draw if you can't reach 30. Try <a href="index.html#puzzle-6">this example</a>.</p>

<div class="callout"><strong>House rules:</strong> some groups play with a 50-point first meld or no minimum at all. The solver uses the standard 30.</div>''')

# ---------------- Jokers ----------------
page('jokers.html', 'Rummikub Joker Rules: How to Play and Take Jokers',
 'How jokers work in Rummikub-style tile rummy: what they can stand for, how to take one from the table, the 30-point penalty and smart ways to use them.',
f'''<h1>Joker rules and tips</h1>
<p class="intro">There are only two jokers, and they're the most powerful tiles in the game.</p>

<h2>What a joker can do</h2>
<p>A joker stands in for any tile you need to finish a set: {tl('R6 J R8')} is a red run with the joker as red 7, and {tl('B11 K11 J')} is a group with the joker as red or orange 11.</p>

<h2>Taking a joker from the table</h2>
<p>If a joker is on the table and you hold the exact tile it stands for, you can swap your tile in and take the joker. In {tl('R6 J R8')}, a player holding {tl('R7')} can take the joker.</p>
<ul>
  <li>You must use the joker again <strong>on the same turn</strong>, in a new or existing set, together with at least one tile from your rack.</li>
  <li>In a group of three, the joker could be either missing color. Players usually allow either one to take it.</li>
  <li>Many groups require you to have made your first meld before taking a joker.</li>
</ul>

<h2>The 30-point penalty</h2>
<p>A joker left on your rack when someone else goes out costs you <strong>30 points</strong>. Holding one until the very end is a gamble.</p>

<h2>Smart joker play</h2>
<ul>
  <li><strong>Play it where it's safe.</strong> A joker standing for a tile whose two copies are already on the table can't be taken.</li>
  <li><strong>Don't waste it early.</strong> A joker that completes a big rearrangement later is worth more than one spent on an easy set now.</li>
  <li><strong>Get rid of it when the round is ending.</strong> When someone is down to two or three tiles, play your joker before it costs you 30.</li>
</ul>

<h2>Jokers in the solver</h2>
<p>Use the + buttons next to each grid to add jokers on the table and in your rack. The solver decides what each joker should stand for and shows it as ☺ in the answer. Try the <a href="index.html#puzzle-5">joker puzzle</a>.</p>
<p><strong>Save my jokers</strong> is on by default. The solver then keeps the jokers in your rack unless playing them lets you empty your rack and win the round, so you don't hand an opponent a free joker. Untick it to see every move that uses your jokers.</p>''')

# ---------------- Scoring ----------------
page('scoring.html', 'Rummikub Scoring: How to Count Points at the End',
 'How scoring works in Rummikub-style tile rummy: penalty points, the joker 30, a worked example, what happens when the pool runs out, and keeping score.',
f'''<h1>How scoring works</h1>
<p class="intro">A game is usually several rounds. Here's how to count points at the end of each one.</p>

<h2>When a round ends</h2>
<p>The round ends as soon as one player plays their last tile. That player wins the round.</p>

<h2>Counting the points</h2>
<ol>
  <li>Every other player adds up the numbers on the tiles still on their rack.</li>
  <li>A joker left on a rack counts as <strong>30</strong>.</li>
  <li>Each of those players writes their total as a <strong>minus</strong> score.</li>
  <li>The winner scores the <strong>sum of everyone else's totals</strong> as a plus score.</li>
</ol>

<h2>Example</h2>
<p>Ana goes out. The others have:</p>
<ul>
  <li>Ben: {tl('R3 K9')} = −12</li>
  <li>Cara: {tl('B12 J')} = −42</li>
  <li>Dev: {tl('O1 O2')} = −3</li>
</ul>
<p>Ana scores +57 (12 + 42 + 3). The scores for the round always add up to zero.</p>

<h2>If the pool runs out</h2>
<p>If the pool is empty and nobody can play, the round ends. The player with the lowest total on their rack wins, and everyone counts the difference between their total and the winner's total.</p>

<h2>Keeping score across rounds</h2>
<p>Write each round's scores in a column per player. Play a set number of rounds, or until someone passes a target, and the highest total wins.</p>

<h2>Scoring tips</h2>
<ul>
  <li>Late in a round, get rid of high tiles and jokers first. A 13 left on your rack costs more than a 2.</li>
  <li>When an opponent is down to a few tiles, playing two high tiles beats drawing.</li>
</ul>
<p>The <a href="index.html">solver</a> breaks ties by playing higher tiles, so it already leans toward moves that cut your penalty.</p>

<div class="callout"><strong>House rules:</strong> some groups score only the winner's points, or count the joker as 50. Agree before you start.</div>''')

# ---------------- Strategy ----------------
page('strategy.html', 'Rummikub Strategy: 8 Tips to Play More Tiles',
 'Practical Rummikub-style strategy: when to hold tiles, how to find hidden moves by splitting runs, using jokers well and avoiding big penalties.',
f'''<h1>Strategy tips</h1>
<p class="intro">Ways to play more tiles, spot hidden moves and lose fewer points.</p>
<ol class="tips">
  <li><h3>Make your first meld early</h3><p>Until you've put down 30 points you can't touch the table at all, so every turn without a meld is a turn spent drawing. If you have a valid meld, it's usually worth playing it soon. See <a href="first-meld.html">first meld</a>.</p></li>
  <li><h3>Don't empty your rack too fast</h3><p>Playing every tile you can as soon as you can leaves you with nothing to work with later. Hold a few tiles that fit almost anywhere, such as middle numbers like 5 to 9, to unlock rearrangements on later turns.</p></li>
  <li><h3>Look at long runs first</h3><p>A run of six or more tiles can often split into two runs, and a run of four can lend its end tile. When you're stuck, look for the longest runs on the table: that's where hidden moves usually are. For example, {tl('O2 O3 O4 O5 O6 O7')} can take an {tl('O4')} in the middle by becoming {tl('O2 O3 O4')} and {tl('O4 O5 O6 O7')}.</p></li>
  <li><h3>Groups of four are spare parts</h3><p>A four-color group can give up any one tile and still be valid. Treat every group of four as a source of tiles for your other sets.</p></li>
  <li><h3>Track the second copies</h3><p>Every tile exists exactly twice. If both copies of a tile you need are already on the table and locked in sets you can't take apart, stop waiting for it and plan around it.</p></li>
  <li><h3>Play the joker carefully</h3><p>A joker on the table can be taken by anyone who holds the tile it stands for. It's safer in a set where both copies of that tile are already played. Holding one until the end costs 30 if someone else goes out first. More in the <a href="jokers.html">joker guide</a>.</p></li>
  <li><h3>Watch the other racks</h3><p>When an opponent gets down to two or three tiles, the round is about to end. Get rid of your high tiles and any joker first so a loss costs you less. See <a href="scoring.html">scoring</a>.</p></li>
  <li><h3>Review your games</h3><p>After a game, enter a few tricky positions in the <a href="index.html">solver</a> and compare its answer with what you played, or work through the <a href="puzzles.html">practice puzzles</a>. You'll start seeing those moves on your own.</p></li>
</ol>
<div class="callout"><strong>Fair play:</strong> use the solver to practice and to review games, not during a real game against other people. Online Rummikub apps and tournaments don't allow outside help.</div>''')

# ---------------- Puzzles ----------------
CL = 'RBKO'
def tiles_from_grid(g):
    return ' '.join(f'{CL[c]}{v}' for c in range(4) for v in range(1, 14) for _ in range(g[c][v]))
def answer_html(a):
    out = []
    for s in a['sets']:
        tiles = ''.join(
            f'<span class="t {"j" if t["j"] else "rbko"[t["c"]]}{" new" if t["r"] else ""}">{"☺" if t["j"] else t["v"]}</span>'
            for t in s['tiles'])
        out.append(f'<span class="tiles-inline">{tiles}</span>')
    return '<div class="sets">' + ''.join(out) + '</div>'
cards = []
for i, p in enumerate(puzzles, 1):
    table = p['tableSpec'] + (' J' * p['tj'])
    rack = p['rackSpec'] + (' J' * p['rj'])
    a = p['answer']
    cards.append(f'''<section class="puzzle" id="{p['id']}">
  <span class="lvl">Puzzle {i} · {p['level']}{' · First meld' if p['initial'] else ''}</span>
  <h2>{p['title']}</h2>
  <div class="row"><b>Table</b>{' '.join(tl(x) for x in p['tableSets']) if table.strip() else '<span class="updated">Empty: this is your opening play.</span>'}</div>
  <div class="row"><b>Rack</b>{tl(rack.strip())}</div>
  <details><summary>Hint</summary><p>{H.escape(p['hint'])}</p></details>
  <details><summary>Show the answer</summary>
    <p>Play <strong>{a['count']} tile{'s' if a['count'] != 1 else ''}</strong> ({a['value']} points). The table ends up as (your tiles outlined):</p>
    {answer_html(a)}
  </details>
  <div class="actions"><a class="cta" href="index.html#{p['id']}">Open in the solver</a></div>
</section>''')
page('puzzles.html', 'Rummikub Practice Puzzles: Find the Hidden Move',
 'Six practice puzzles for Rummikub-style tile rummy, from easy to hard: extend runs, split runs, borrow tiles, rebuild the table and free the joker.',
f'''<h1>Practice puzzles</h1>
<p class="intro">Each puzzle shows a table and a rack. Find the move that plays the most tiles, then check the answer or open it in the solver.</p>
{''.join(cards)}
<p>Made up your own? Enter any position in the <a href="index.html">solver</a>. More tips are on the <a href="strategy.html">strategy page</a>.</p>''')

# ---------------- FAQ ----------------
faqs = [
 ('Is Tile Rummy Solver free?', 'Yes. The solver and all the guides are free to use, with no account and no download.'),
 ('Does it work with Rummikub?', 'Yes. It follows the standard Rummikub rules: 4 colors, numbers 1 to 13, two copies of each tile, 2 jokers, runs and groups, and a 30-point first meld. It works with other tile rummy games that use the same tiles.'),
 ('Is using the solver cheating?', 'It is if you use it during a game against other people, and online apps and tournaments don\'t allow it. It\'s meant for practice: reviewing a game afterwards, settling an argument about whether a move existed, or working through the practice puzzles.'),
 ('How does it find the best move?', 'It checks every legal way to arrange the table tiles plus your rack into runs and groups, using a method called dynamic programming. The answer is the move that plays the most tiles from your rack, with higher tiles breaking ties. The About page explains more.'),
 ('Why does it say a tile doesn\'t fit any set?', 'The tiles you marked as on the table can\'t all be arranged into valid sets, which usually means a tile was missed or tapped by mistake. The tiles that don\'t fit are outlined in red. If you solve anyway, they\'re set aside and listed in the answer.'),
 ('How do I enter two copies of the same tile?', 'Tap the tile twice. The two dots under the number show how many copies you\'ve marked. A third tap clears it, and a grey dot means that copy is already marked in the other grid.'),
 ('Can it handle jokers?', 'Yes. Add jokers with the + buttons next to the table and the rack. The solver decides what each joker should stand for. With Save my jokers ticked (the default), it only plays a joker from your rack when that wins you the round, since a joker on the table can be taken by an opponent.'),
 ('Does it save my board?', 'Yes, on your own device. Your last board is kept in your browser so it\'s still there next time, and Back and Forward let you step through your changes. Start over clears everything. Nothing is sent to a server.'),
 ('Does it work on my phone?', 'Yes. On a phone the grids show one color at a time with bigger tiles: use the Red, Blue, Black and Orange tabs to switch.'),
 ('Can it find my first meld?', 'Yes. Mark your rack, tick First meld, and it finds the highest-scoring opening play from your own tiles, or tells you to draw if you can\'t reach 30.'),
]
faq_ld = ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
page('faq.html', 'Tile Rummy Solver FAQ: Common Questions Answered',
 'Answers about Tile Rummy Solver: is it free, does it work with Rummikub, is it cheating, jokers, saving your board, phones and the first meld.',
 '<div class="faq">\n<h1>Frequently asked questions</h1>\n<p class="intro">Quick answers about the solver and the game.</p>\n'
 + ''.join(f'<h2>{H.escape(q)}</h2>\n<p>{H.escape(a)}</p>\n' for q, a in faqs)
 + f'<p>Still stuck? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>\n<a class="cta" href="index.html">Open the solver</a>\n</div>', faq_ld)

# ---------------- About ----------------
page('about.html', 'About Tile Rummy Solver',
 'Who made Tile Rummy Solver, how the solver finds the best move in Rummikub-style games, and how to use it fairly.',
f'''<h1>About</h1>
<p class="intro">{NAME} is a free tool that shows the best move in Rummikub and other tile rummy games. It's made by Carlo J.</p>

<h2>Why it exists</h2>
<p>The hardest part of tile rummy is seeing how to rebuild the table to fit your tiles in. Most players miss moves that were there all along. This tool shows you those moves so you can learn to spot them yourself.</p>

<h2>How the solver works</h2>
<p>You mark which tiles are on the table and which are in your rack. The solver then checks every legal way to arrange those tiles into runs and groups. It uses a method called dynamic programming: it goes through the numbers from 1 to 13, keeps track of which runs are still open, and remembers the best result for each situation so it never has to repeat work.</p>
<p>Because it checks every possibility, the answer is the true best move: the one that plays the most tiles from your rack, with higher-value tiles breaking ties. It runs in your browser in a background thread, so the page stays responsive even on a crowded table. Nothing is sent to a server.</p>

<h2>Use it fairly</h2>
<p>This is a training and review tool. Please don't use it during games against other people, online or in person.</p>

<h2>Support the project</h2>
<p>The solver is free and supported by ads. If it helped you, a small tip helps pay for new features like scanning tiles with your camera.</p>
<p><a class="tip" data-kofi href="#" hidden>☕ Support this project</a></p>

<h2>Contact</h2>
<p>Questions, bug reports or ideas: <a href="mailto:{EMAIL}">{EMAIL}</a>. I read every message.</p>''')

# ---------------- Privacy ----------------
page('privacy.html', 'Privacy Policy · Tile Rummy Solver',
 'Privacy policy for Tile Rummy Solver: what is stored on your device, how Google AdSense ads and cookies work, and your choices.',
f'''<h1>Privacy policy</h1>
<p class="updated">Last updated: November 13, 2026</p>

<h2>Summary</h2>
<p>{NAME} ({DOMAIN.replace('https://', '')}) has no accounts and asks for no personal information. The solver runs entirely in your browser.</p>

<h2>What is stored on your device</h2>
<p>To save you from re-entering a board, the solver keeps your last table, rack and settings in your browser's local storage. This stays on your device, is never sent to us, and you can remove it at any time with the Start over button or by clearing your browser's site data.</p>

<h2>Advertising and cookies</h2>
<p>This site uses Google AdSense to show ads. Because of this:</p>
<ul>
  <li>Third-party vendors, including Google, use cookies to serve ads based on your earlier visits to this and other websites.</li>
  <li>Google's advertising cookies let Google and its partners serve ads to you based on your visits to this site and other sites on the internet.</li>
  <li>You can turn off personalized advertising in <a href="https://adssettings.google.com">Google's Ad Settings</a>, or opt out of some third-party vendors' cookies at <a href="https://www.aboutads.info/choices/">aboutads.info</a>.</li>
  <li>To learn more, see <a href="https://policies.google.com/technologies/partner-sites">how Google uses information from sites that use its services</a>.</li>
</ul>
<p>Visitors in the European Economic Area, the UK and Switzerland are asked for consent through Google's consent message before personalized ads or non-essential cookies are used, and can change their choice at any time.</p>

<h2>Hosting</h2>
<p>The site is hosted by Cloudflare, which processes basic technical data (such as IP addresses) to deliver pages and protect against abuse. The site uses your device's built-in fonts and loads no third-party fonts.</p>

<h2>Analytics</h2>
<p>We may use privacy-friendly analytics to count visits and see which pages are used. This data is anonymous and is not used to identify you.</p>

<h2>Tips and payments</h2>
<p>If you send a tip, the payment is handled by the tip service (such as Ko-fi). We don't see or store your card details. That service's own privacy policy applies.</p>

<h2>Children</h2>
<p>This site is not directed at children under 13, and we don't knowingly collect information from them.</p>

<h2>Changes</h2>
<p>If this policy changes, the date at the top of this page will change too.</p>

<h2>Contact</h2>
<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''')

# ---------------- 404 ----------------
page('404.html', 'Page Not Found · Tile Rummy Solver', 'This page does not exist. Go back to the Tile Rummy Solver.',
f'''<h1>That page isn't on the table</h1>
<p class="intro">The link may be old or mistyped.</p>
<a class="cta" href="index.html">Go to the solver</a>
<p style="margin-top:16px">Or read <a href="how-to-play.html">how to play</a>, the <a href="strategy.html">strategy tips</a> or the <a href="faq.html">FAQ</a>.</p>''')
(OUT / '404.html').write_text((OUT / '404.html').read_text().replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"'))

# ---------------- robots, sitemap, ads.txt, _headers ----------------
pages = ['index.html', 'how-to-play.html', 'first-meld.html', 'jokers.html', 'scoring.html', 'strategy.html', 'puzzles.html', 'faq.html', 'about.html', 'privacy.html']
(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{clean(p)}</loc><lastmod>{TODAY}</lastmod></url>\n' for p in pages) + '</urlset>\n')
(OUT / 'ads.txt').write_text('''# ads.txt for tilerummysolver.com
# After AdSense approves you, replace the line below with the one AdSense shows you
# (AdSense > Sites > ads.txt), then remove the "# " at its start.
# Your publisher ID is in AdSense > Account > Account information (it starts with pub-).
# google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0
''')
(OUT / '_headers').write_text('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

/*.png
  Cache-Control: public, max-age=604800

/*.svg
  Cache-Control: public, max-age=604800
''')
print('built:', sorted(p.name for p in OUT.iterdir()))
