"""Rebuild the two illustrated README GIFs. Requires Pillow."""
from pathlib import Path
import math
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H, SCALE = 960, 500, 2
C = dict(bg='#f6f7f4', paper='#ffffff', ink='#172a2c', muted='#667672', line='#d4ded7',
         teal='#1b6972', soft='#e7f3f2', blue='#3465ad', bluesoft='#eaf0fb',
         gold='#9b6d24', goldsoft='#fcf2dc', red='#a34d4d', redsoft='#f8ebeb')


def font(size=20, bold=False, mono=False):
    candidates = ([('/System/Library/Fonts/Supplemental/Courier New.ttf'), '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'] if mono else
                  ['/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf',
                   '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size*SCALE)
    return ImageFont.load_default(size=size*SCALE)


class Canvas:
    def __init__(self):
        self.im = Image.new('RGB', (W*SCALE, H*SCALE), C['bg'])
        self.d = ImageDraw.Draw(self.im)

    def text(self, xy, text, size=20, color='ink', bold=False, mono=False):
        self.d.text(tuple(int(v*SCALE) for v in xy), text, font=font(size, bold, mono), fill=C.get(color, color))

    def box(self, xy, fill='paper', edge='line', radius=12, width=1):
        self.d.rounded_rectangle(tuple(int(v*SCALE) for v in xy), radius=radius*SCALE,
                                 fill=C.get(fill, fill), outline=C.get(edge, edge), width=width*SCALE)

    def line(self, points, color='line', width=2, arrow=False):
        pts = [(int(x*SCALE), int(y*SCALE)) for x, y in points]
        self.d.line(pts, fill=C[color], width=width*SCALE, joint='curve')
        if arrow:
            x, y = pts[-1]; a, b = pts[-2]; angle = math.atan2(y-b, x-a)
            end = [(x, y)] + [(int(x-11*SCALE*math.cos(angle+t)), int(y-11*SCALE*math.sin(angle+t))) for t in (-.45, .45)]
            self.d.polygon(end, fill=C[color])

    def circle(self, xy, r=6, color='teal'):
        x, y = xy
        self.d.ellipse(((x-r)*SCALE, (y-r)*SCALE, (x+r)*SCALE, (y+r)*SCALE), fill=C[color])

    def image(self):
        return self.im.resize((W, H), Image.Resampling.LANCZOS)


def save_gif(frames, durations, path):
    strip = Image.new('RGB', (W, H*len(frames)))
    for i, frame in enumerate(frames):
        strip.paste(frame, (0, H*i))
    palette = strip.resize((236, max(1, len(frames)*100))).quantize(colors=128)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(path, save_all=True, append_images=indexed[1:], duration=durations,
                    loop=0, optimize=True, disposal=2)


def measure(text, size, bold=False, mono=False):
    return font(size,bold,mono).getlength(text)/SCALE


def type_icon(c,x,y,kind,color='muted'):
    if kind in ('ai','agent'):
        c.box((x,y+3,x+14,y+14),fill='goldsoft',edge=color,radius=3)
        c.line([(x+7,y),(x+7,y+3)],color,1)
        c.circle((x+4,y+8),1,color);c.circle((x+10,y+8),1,color)
        c.line([(x+4,y+11),(x+10,y+11)],color,1)
    elif kind=='data':
        c.box((x,y+2,x+14,y+15),fill='soft',edge=color,radius=3)
        c.line([(x,y+6),(x+14,y+6)],color,1);c.line([(x,y+11),(x+14,y+11)],color,1)
    elif kind=='rule':
        c.line([(x+7,y),(x+15,y+8),(x+7,y+16),(x-1,y+8),(x+7,y)],color,1)
    elif kind=='tool':
        c.line([(x+2,y+14),(x+10,y+6),(x+14,y+7),(x+15,y+2),(x+10,y+1),(x+8,y+5)],color,2)
    else:
        c.box((x,y+1,x+12,y+16),edge=color,radius=1)
        c.line([(x+3,y+6),(x+9,y+6)],color,1);c.line([(x+3,y+10),(x+9,y+10)],color,1)


def dashed(c,points,color='line'):
    for a,b in zip(points,points[1:]):
        length=math.dist(a,b)
        for i in range(0,int(length),12):
            lo=i/max(length,1);hi=min(i+6,length)/max(length,1)
            c.line([(a[0]+(b[0]-a[0])*lo,a[1]+(b[1]-a[1])*lo),
                    (a[0]+(b[0]-a[0])*hi,a[1]+(b[1]-a[1])*hi)],color,1)
    c.line(points[-2:],color,1,arrow=True)


def classification_frame(config,scenario,index,inspect=False):
    c=Canvas()
    for y in range(10,980,18):
        for x in range(10,W,18):c.circle((x,y),.55,'line')
    names={'data':'DATA','tool':'TOOL / CODE','ai':'PAID AI','agent':'PAID AI + WEB','rule':'DECISION / CODE','output':'OUTPUT'}
    boxes={}
    for n in config['nodes']:
        width=max(measure(n['title'],12,True),measure(n.get('subtitle',''),9),measure(names[n['kind']],8,mono=True)+26)+28
        boxes[n['id']]=(n['x']-width/2,n['y']-35,width,70)
    path=scenario['path'];visited=path[:index+1]
    def port(n,side):
        x,y,w,h=boxes[n]
        return {'left':(x,y+h/2),'right':(x+w,y+h/2),'top':(x+w/2,y),'bottom':(x+w/2,y+h)}[side]
    for edge in config['edges']:
        a,b=edge['from'],edge['to'];sx,sy,sw,sh=boxes[a];tx,ty,tw,th=boxes[b]
        horizontal=sy==ty;right=tx>sx
        start=port(a,edge.get('sourcePort',('right' if right else 'left') if horizontal else 'bottom'))
        end=port(b,edge.get('targetPort',('left' if right else 'right') if horizontal else 'top'))
        via=edge.get('via',[])
        points=[start,*via,end]
        lit=any((a,b)==(path[i-1],path[i]) for i in range(1,index+1)) or (edge.get('kind')=='payload' and b in visited)
        color='teal' if lit else 'line'
        if edge.get('kind')=='payload':dashed(c,points,color)
        else:c.line(points,color,2 if lit else 1,arrow=True)
        if edge.get('label'):c.text((edge['labelX'],edge['labelY']-10),edge['label'],9,'muted')
    for label in config.get('labels',[]):c.text((label['x'],label['y']-10),label['text'],9,'muted')
    for n in config['nodes']:
        x,y,w,h=boxes[n['id']];kind=n['kind'];active=n['id']==path[index]
        fill='goldsoft' if kind in ('ai','agent') else 'soft' if kind=='data' else 'paper'
        if active:c.box((x-5,y-5,x+w+5,y+h+5),fill='soft',edge='soft',radius=9)
        c.box((x,y,x+w,y+h),fill=fill,edge='teal' if active or n['id'] in visited else 'line',radius=6)
        color='gold' if kind in ('ai','agent') else 'muted'
        type_icon(c,x+8,y+7,kind,color)
        c.text((x+29,y+10),names[kind],8,color,mono=True)
        c.line([(x+w-17,y+17),(x+w-10,y+10)],'muted',1)
        c.line([(x+w-16,y+10),(x+w-10,y+10),(x+w-10,y+16)],'muted',1)
        c.text((x+8,y+29),n['title'],12,bold=True)
        c.text((x+8,y+49),n.get('subtitle',''),9,color='muted')
    c.box((310,983,860,1025),radius=10)
    for x,label,sid in [(322,'Skip web research','direct'),(500,'Run Jev a second time','resolved')]:
        selected=scenario['id']==sid
        c.box((x,991,x+168,1018),fill='soft' if selected else 'paper',edge='teal' if selected else 'line',radius=5)
        c.text((x+9,999),label,10,'teal' if selected else 'muted')
    c.line([(696,998),(696,1011)],'teal',2);c.line([(701,998),(701,1011)],'teal',2)
    c.line([(729,1004),(714,1004)],'teal',1,arrow=True)
    c.line([(739,1004),(754,1004)],'teal',1,arrow=True)
    c.text((774,997),'1×',11,'teal')
    c.line([(818,1000),(813,1000),(813,1012),(818,1012)],'teal',1)
    c.line([(826,1000),(831,1000),(831,1012),(826,1012)],'teal',1)
    c.text((891,992),'AI · tool · data · branch',8,'muted')
    if inspect:
        c.box((833,160,1175,915),edge='line',radius=9)
        c.text((854,183),'PAID AI',10,'gold',mono=True)
        c.text((854,216),'Jev · second pass',24,bold=True)
        c.text((854,262),'All transactions + both contexts',13,'muted')
        c.text((854,308),'ILLUSTRATIVE INPUT',10,'muted',mono=True)
        lines=['{','  "transactions": [','    { "id": "t1", "merchant": "OPENAI" },','    { "id": "t2", "merchant": "OPENAI" },','    { "id": "t3", "merchant": "PARK" },','    { "id": "t4", "merchant": "PARK" },','    { "id": "t5", "merchant": "PARK" }','  ],','  "context": {','    "personal": "past corrections",','    "web": "cited merchant facts"','  }','}']
        for i,line in enumerate(lines):c.text((854,343+i*27),line,9,mono=True)
        c.box((850,748,1156,845),fill='soft',edge='soft')
        c.text((867,765),'All 5 payments stay intact.',14,'teal',bold=True)
        c.text((867,793),'Only lookup work is grouped.',12,'teal')
        c.text((867,818),'Lowest-confidence results appear first.',11,'teal')
    return c.image()


STEPS=[
('A server is like a kitchen.','A customer sends an order; the kitchen prepares an answer.'),
('The browser sends a request.','One example throughout: ask the price of two bowls of soup.'),
('The request arrives at the server.','The same request crosses the network and reaches the application.'),
('The route chooses a handler.','POST /quote tells the app which function should handle it.'),
('The handler reads the body.','The JSON carries the item and quantity: soup, 2.'),
('The handler checks the input.','The quantity must be a whole number from 1 to 10.'),
('The handler looks up the price.','The menu says one bowl of soup costs $9.'),
('The handler calculates the total.','Two bowls × $9 = $18. The browser has not received this yet.'),
('The server sends its response.','200 OK carries JSON with the calculated total.'),
('The browser displays the result.','The page reads that JSON and shows “Total: $18”.')]


def restaurant(c):
    # Guest, order ticket, and a small kitchen: the initial visual is the analogy.
    c.text((80,173),'CUSTOMER',13,'muted',mono=True)
    c.circle((155,245),28,'teal');c.box((106,281,204,372),fill='soft',edge='teal',radius=25)
    c.line([(101,373),(207,373)],'teal',3)
    c.box((268,211,465,343),fill='goldsoft',edge='gold',radius=5)
    c.text((288,229),'ORDER',13,'gold',mono=True);c.text((288,263),'2 × soup',28,'gold',True)
    c.text((288,310),'“How much?”',17,'gold')
    c.line([(475,275),(603,275)],'teal',2,arrow=True)
    c.box((637,190,1042,421),radius=10)
    c.text((659,211),'KITCHEN',13,'muted',mono=True)
    # Stove and a pot.
    c.box((663,335,819,394),fill='soft',edge='teal',radius=5)
    c.box((688,283,794,337),fill='goldsoft',edge='gold',radius=10)
    c.line([(678,283),(803,283)],'gold',3)
    c.line([(716,267),(710,255),(717,244)],'muted',2)
    c.line([(762,266),(756,252),(763,240)],'muted',2)
    # Chef with hat.
    c.circle((919,270),23,'teal');c.box((882,298,956,387),fill='soft',edge='teal',radius=12)
    c.circle((899,231),14,'paper');c.circle((919,223),18,'paper');c.circle((939,232),14,'paper')
    c.box((896,234,944,248),fill='paper',edge='line',radius=3)
    c.line([(886,333),(813,316)],'teal',3)
    mappings=[('Customer','Browser'),('Order','Request'),('Kitchen','Server'),('Answer','Response')]
    for i,(a,b) in enumerate(mappings):
        x=58+i*263;c.box((x,477,x+246,554),radius=9)
        c.text((x+14,489),a,15,'muted');c.text((x+14,518),'→ '+b,20,'teal',True)


def browser(c,stage):
    c.box((36,213,306,490),radius=11)
    c.box((36,213,306,247),fill='soft',edge='line',radius=9)
    for x in (51,62,73):c.circle((x,230),2,'muted')
    c.text((85,224),'localhost:8765',10,'muted',mono=True)
    c.text((57,269),'Soup',27,bold=True)
    # Two concrete bowls stay visible as mechanisms are added on the server.
    for x in (88,178):
        c.box((x,319,x+60,346),fill='goldsoft',edge='gold',radius=13)
        c.line([(x-5,319),(x+65,319)],'gold',2)
        c.line([(x+20,308),(x+16,299),(x+22,290)],'muted',1)
    c.text((57,367),'Quantity: 2',17,'muted')
    c.box((56,402,284,443),fill='teal',edge='teal',radius=7)
    c.text((121,414),'Get price',16,'paper',True)
    if stage>=9:
        c.box((56,453,284,481),fill='soft',edge='soft',radius=5)
        c.text((110,459),'Total: $18',17,'teal',True)


def server_frame(stage):
    c=Canvas();title,sub=STEPS[stage]
    c.text((36,23),'learn-layered · how servers work',13,'muted',mono=True)
    c.text((36,55),title,31,bold=True);c.text((36,105),sub,16,'muted')
    if stage==0:restaurant(c)
    else:
        browser(c,stage)
        c.box((660,174,1064,595),edge='teal' if stage==2 else 'line',radius=12)
        c.text((681,193),'SERVER',12,'muted',mono=True)
        c.text((894,193),'Python app',13,'muted')
        c.box((347,224,610,352),fill='bluesoft',edge='blue' if stage in (1,2,4) else 'line',radius=8)
        c.text((363,238),'REQUEST',10,'blue',mono=True)
        c.text((363,264),'POST /quote',20,'blue',True,True)
        if stage>=4:
            c.text((363,303),'item: "soup"',14,'blue',mono=True)
            c.text((363,325),'quantity: 2',14,'blue',mono=True)
        else:c.text((363,311),'Order details inside',13,'blue')
        c.line([(306,286),(347,286)],'blue',2,arrow=True)
        c.line([(610,286),(660,286)],'blue' if stage>=2 else 'line',2,arrow=True)
        rows=[('Route','POST /quote → quote()'),('Read body','item="soup", quantity=2'),('Validate','whole number, 1–10'),('Read menu','soup → $9'),('Calculate','$9 × 2 = $18'),('Respond','200 OK · JSON')]
        for i,(name,value) in enumerate(rows):
            revealed=stage>=i+3;y=235+i*56
            if not revealed:continue
            active=stage==i+3
            c.box((681,y,1043,y+47),fill='soft' if active else 'paper',edge='teal' if active else 'line',radius=6)
            c.text((694,y+6),name.upper(),9,'teal' if active else 'muted',mono=True)
            c.text((694,y+23),value,15,bold=active)
        if stage==2:c.text((690,307),'Request received.',22,'teal',True)
        if stage>=8:
            c.box((347,411,610,542),fill='soft',edge='teal',radius=8)
            c.text((363,425),'RESPONSE',10,'teal',mono=True)
            c.text((363,449),'200 OK',20,'teal',True,True)
            c.text((363,485),'total: 18',14,'teal',mono=True)
            c.text((363,510),'currency: "USD"',14,'teal',mono=True)
            c.line([(660,560),(633,560),(633,473),(610,473)],'teal',2,arrow=True)
            c.line([(347,473),(329,473),(329,457),(306,457)],'teal',2,arrow=True)
        if stage>=9:
            c.text((359,577),'Same request, now fully explained.',15,'teal',True)
    # The rail grows with the example; no universal “tiny / bigger / complete” slots.
    c.text((36,645),'ONE EXAMPLE · ONE NEW PART AT A TIME',11,'muted',mono=True)
    labels=['Analogy','Send','Arrive','Route','Read','Check','Lookup','Calculate','Respond','Display']
    for i,label in enumerate(labels):
        x=36+i*104
        c.box((x,674,x+96,714),fill='teal' if i==stage else 'soft' if i<stage else 'paper',edge='teal' if i==stage else 'line',radius=6)
        c.text((x+9,687),label,11,'paper' if i==stage else 'teal' if i<stage else 'muted',bold=i==stage)
    return c.image()


def main():
    global W,H
    (ROOT/'assets').mkdir(exist_ok=True)
    W,H=1180,1040
    config=json.loads((ROOT/'skills/acetate-flow/assets/classification.json').read_text())
    frames=[];durations=[]
    for scenario in config['scenarios']:
        indices=range(len(scenario['path'])) if scenario['id']=='direct' else range(9,len(scenario['path']))
        for i in indices:
            frames.append(classification_frame(config,scenario,i));durations.append(500 if i<len(scenario['path'])-1 else 1500)
        if scenario['id']=='resolved':
            frames.append(classification_frame(config,scenario,scenario['path'].index('jev2'),True));durations.append(2500)
    save_gif(frames,durations,ROOT/'assets/acetate-flow.gif')
    del frames
    W,H=1100,740
    frames=[server_frame(i) for i in range(len(STEPS))]
    save_gif(frames,[2900]+[2400]*7+[2900,3600],ROOT/'assets/learn-layered.gif')
    folder=ROOT/'examples/server-layers';folder.mkdir(exist_ok=True)
    for i,frame in enumerate(frames):frame.save(folder/f'{i+1:02}.png')
    for name in ('acetate-flow','learn-layered'):
        path=ROOT/'assets'/f'{name}.gif'
        with Image.open(path) as im:print(f'{name}: {im.size}, {im.n_frames} frames, {path.stat().st_size//1024} KiB')


if __name__=='__main__':
    main()
