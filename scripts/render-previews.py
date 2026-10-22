"""Rebuild the two illustrated README GIFs. Requires Pillow."""
from pathlib import Path
import math
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


def receipt(c, x, y, label='ONE RECEIPT', small=False):
    width, height = (155, 150) if not small else (125, 122)
    c.box((x, y, x+width, y+height), edge='teal', radius=3)
    c.text((x+17, y+14), label, size=13 if small else 15, bold=True, color='teal')
    for i, length in enumerate([width-34, width-52, width-34]):
        c.line([(x+17, y+48+i*18), (x+17+length, y+48+i*18)], width=2)
    c.text((x+17, y+height-29), 'order-123', size=12 if small else 14, mono=True)


def save_gif(frames, durations, path):
    strip = Image.new('RGB', (W, H*len(frames)))
    for i, frame in enumerate(frames):
        strip.paste(frame, (0, H*i))
    palette = strip.resize((240, max(1, len(frames)*125))).quantize(colors=128)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(path, save_all=True, append_images=indexed[1:], duration=durations,
                    loop=0, optimize=True, disposal=2)


NODES = {'order': (30, 150, 180, 'Order received', 'DATA'),
         'validate': (260, 150, 180, 'Validate', 'TOOL / CODE'),
         'payment': (490, 150, 200, 'Approved?', 'BRANCH'),
         'fulfill': (740, 150, 180, 'Fulfill order', 'OUTPUT'),
         'declined': (490, 295, 200, 'Another card', 'OUTPUT')}
PATHS = [['order', 'validate', 'payment', 'fulfill'], ['order', 'validate', 'payment', 'declined']]


def edge_points(a, b):
    x, y, width, *_ = NODES[a]; tx, ty, tw, *_ = NODES[b]
    return [(x+width, y+38), (tx, ty+38)] if y == ty else [(x+width/2, y+76), (tx+tw/2, ty)]


def flow_frame(route, index, progress=None, inspect=False):
    c = Canvas()
    for y in range(105, 405, 18):
        for x in range(18, W, 18):
            c.circle((x, y), .6, 'line')
    c.text((30, 24), 'acetate-flow', 15, color='muted', mono=True)
    c.text((30, 52), 'One checkout. Two possible paths.', 29, bold=True)
    for a, b in [('order','validate'),('validate','payment'),('payment','fulfill'),('payment','declined')]:
        lit = any((a, b) == (route[i-1], route[i]) for i in range(1, index+1))
        c.line(edge_points(a, b), 'teal' if lit else 'line', 3 if lit else 2, arrow=True)
    c.text((701, 163), 'yes', 12, color='muted')
    c.text((606, 252), 'no', 12, color='muted')
    for key, (x, y, width, title, kind) in NODES.items():
        active = key == route[index]
        fill = 'soft' if key == 'order' else 'paper'
        if key == 'payment': fill = 'goldsoft'
        if active: c.box((x-5,y-5,x+width+5,y+81), fill='soft', edge='soft')
        c.box((x,y,x+width,y+76), fill=fill, edge='teal' if active else 'line', width=2 if active else 1)
        c.text((x+12,y+10), kind, 10, color='muted', mono=True)
        c.text((x+12,y+33), title, 17, bold=True)
    if progress is not None and index+1 < len(route):
        a,b=edge_points(route[index],route[index+1]);c.circle((a[0]+(b[0]-a[0])*progress,a[1]+(b[1]-a[1])*progress),6)
    c.box((30, 425, 930, 476), radius=9)
    c.text((46, 441), 'Payment approved' if route[-1] == 'fulfill' else 'Payment declined', 16, color='teal', bold=True)
    c.text((660, 442), f'{index+1} / {len(route)} steps', 13, color='muted', mono=True)
    if inspect:
        c.box((30, 275, 425, 395), edge='teal')
        c.text((46, 287), 'EXPAND A STEP', 10, color='muted', mono=True)
        c.text((46, 311), 'Example data', 17, bold=True)
        c.text((46, 343), '{ "approved": '+('true' if route[-1]=='fulfill' else 'false')+' }', 15, mono=True)
    return c.image()


def flow_preview():
    frames, durations = [], []
    for route in PATHS:
        for index in range(len(route)):
            frames.append(flow_frame(route,index));durations.append(500)
            if index+1<len(route):
                for t in (.33,.67):
                    frames.append(flow_frame(route,index,t));durations.append(120)
        frames.append(flow_frame(route,len(route)-1,inspect=True));durations.append(1400)
    save_gif(frames,durations,ROOT/'assets/acetate-flow.gif')


STAGES = ['Visual','Analogy','Tiny','Bigger','Complete']
TITLES = ['Same request. One receipt.', 'The cashier recognizes your order.',
          'Remember what was handled.', 'Return the saved result.', 'Three attempts. One creation.']


def learning_frame(stage):
    c=Canvas();c.text((34,24),'learn-layered',15,color='muted',mono=True)
    c.text((34,55),TITLES[stage],30,bold=True)
    c.text((34,102),f'{stage+1:02}  {STAGES[stage].upper()}',13,color='teal',mono=True)
    if stage==0:
        for y in (167,237,307):
            c.box((50,y,240,y+47),fill='bluesoft',edge='bluesoft');c.text((66,y+13),'order-123',17,mono=True)
            c.line([(240,y+24),(340,y+24),(390,260)],arrow=True)
        c.box((390,226,550,294),fill='soft',edge='teal');c.text((414,249),'Handle once',17,bold=True)
        c.line([(550,260),(660,260)],color='teal',arrow=True);receipt(c,690,181)
    elif stage==1:
        c.box((70,180,330,332),fill='goldsoft',edge='gold');c.text((91,203),'ORDER NUMBER',13,color='gold',mono=True)
        c.text((91,240),'123',48,bold=True,color='gold');c.text((91,300),'same number on every retry',14,color='gold')
        c.line([(352,258),(460,258)],color='teal',arrow=True)
        c.box((490,180,895,360));c.text((510,199),'CASHIER’S RECORD',12,color='muted',mono=True)
        c.text((510,239),'Order 123',21,bold=True);c.text((510,277),'Receipt already exists.',18,color='teal')
        c.text((510,315),'Give the same receipt back.',16,color='muted')
    elif stage==2:
        c.box((55,170,550,343));c.text((78,191),'Keep a record',20,bold=True)
        c.text((78,239),'receipts = {"order-123": result}',17,mono=True)
        c.text((78,282),'if order_id in receipts:',17,mono=True);c.text((78,312),'    return receipts[order_id]',17,mono=True)
        receipt(c,660,180)
    elif stage==3:
        c.box((55,166,570,353));c.text((78,184),'New request → create and save',18,bold=True)
        c.text((78,221),'if order_id not in receipts:',17,mono=True)
        c.text((78,253),'    receipts[order_id] = result',17,mono=True)
        c.text((78,291),'return receipts[order_id]',17,mono=True)
        c.text((78,327),'Retry → reuse the saved result',16,color='teal')
        receipt(c,675,182)
    else:
        c.box((55,165,540,355));c.text((77,183),'RUN THE EXAMPLE',12,color='muted',mono=True)
        for i in range(3):
            c.text((77,222+i*34),f'Attempt {i+1} → receipt-1',20,mono=True)
        receipt(c,650,165);c.box((630,331,860,375),fill='soft',edge='soft');c.text((650,343),'Receipts created: 1',18,bold=True,color='teal')
    for i,label in enumerate(STAGES):
        x=34+i*181;c.box((x,430,x+170,472),fill='teal' if i==stage else 'paper',edge='teal' if i==stage else 'line',radius=7)
        c.text((x+14,443),f'{i+1}  {label}',14,color='paper' if i==stage else 'muted',bold=i==stage)
    return c.image()


def main():
    (ROOT/'assets').mkdir(exist_ok=True)
    flow_preview()
    frames=[learning_frame(i) for i in range(5)]
    save_gif(frames,[2300,2700,3100,3100,3500],ROOT/'assets/learn-layered.gif')
    for name in ('acetate-flow','learn-layered'):
        path=ROOT/'assets'/f'{name}.gif'
        with Image.open(path) as im:
            print(f'{name}: {im.size}, {im.n_frames} frames, {path.stat().st_size//1024} KiB')


if __name__=='__main__':
    main()
