import os,sys,glob,subprocess,wave
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from functools import lru_cache
@lru_cache(maxsize=32)
def font_cached(path,size):return ImageFont.truetype(path,size)
ROOT=os.path.dirname(os.path.abspath(__file__))
OUT=os.getenv('OUT',os.path.abspath(os.path.join(ROOT,'..'))); os.makedirs(OUT,exist_ok=True)
FONT=ROOT+'/fonts/NotoSansCJK-Regular.ttc';BOLD=ROOT+'/fonts/NotoSansCJK-Bold.ttc'
chapters=[(0,5,'塑料颗粒','如何变成精密产品？','FEEDING / 原料输送'),(5,10,'01｜加热塑化','塑料颗粒逐渐熔融','PLASTICIZING / 螺杆旋转 · 计量后退'),(10,16,'02｜高压注射','熔融塑料填充模具型腔','INJECTION / 模具闭合 · 螺杆前进'),(16,22,'03｜保压冷却','稳定尺寸，让产品逐渐定型','COOLING / 保压补缩 · 水路循环'),(22,27,'04｜开模顶出','一个塑胶产品诞生了！','EJECTION / 先开模 · 再顶出'),(27,30,'注塑成型','从塑料颗粒到精密产品','PRECISION / 精密源于每一道工序')]
def overlay(im,t):
 w,h=im.size;s=w/1080; layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer)
 if t>=27:
  for x,y,sx,sy in [(150,660,1,1),(930,660,-1,1),(150,1370,1,-1),(930,1370,-1,-1)]:
   d.line([(x*s,(y+75*sy)*s),(x*s,y*s),((x+75*sx)*s,y*s)],fill=(30,116,167,140),width=max(1,int(2*s)))
 def text(x,y,txt,size,color=(240,248,255,255),bold=False):d.text((int(x*s),int(y*s)),txt,font=font_cached(BOLD if bold else FONT,int(size*s)),fill=color)
 d.line((72*s,105*s,1008*s,105*s),fill=(38,104,153,200),width=max(1,int(2*s)))
 text(72,58,'瑞晨欣  /  工艺观察',24,(131,165,187,255));text(846,58,'30s · 3D',24,(131,165,187,255))
 a,b,title,sub,small=next(c for c in chapters if c[0]<=t<c[1]);u=t-a;alpha=int(255*min(1,u/.35));slide=45*(1-min(1,u/.5))**3
 text(72-slide,185,small,23,(61,180,246,alpha))
 shown=title[:max(0,int(u*11))] if a==0 else title
 text(68-slide,244,shown,65,(61,185,255,alpha),True)
 text(72,340,sub if a else sub[:max(0,int((u-.55)*12))],38,(239,245,251,alpha))
 # lower explanatory status kept clear of machinery
 labels=['颗粒落料 → 螺槽输送','加热 + 剪切 → 熔体积聚','喷嘴 → 流道 → 浇口 → 型腔','保压补缩 → 循环冷却 → 凝固','动模后移 → 顶针前推 → 脱模','瑞晨欣塑胶模具']
 idx=chapters.index((a,b,title,sub,small))
 d.rounded_rectangle((60*s,1580*s,1020*s,1695*s),radius=12*s,fill=(6,19,34,220),outline=(31,86,123,230),width=max(1,int(s)))
 text(91,1612,labels[idx],34,(205,227,240,255),idx==5)
 for j in range(6):
  x=72+j*158;d.rectangle((x*s,1760*s,(x+138)*s,1764*s),fill=(34,66,91,255));progress=max(0,min(1,(t-chapters[j][0])/(chapters[j][1]-chapters[j][0])))
  if progress:d.rectangle((x*s,1760*s,(x+138*progress)*s,1764*s),fill=(39,180,255,255))
 text(72,1790,'注塑成型全过程  /  工艺剖面示意',23,(116,149,175,255));text(890,1790,f'{int(t):02d} / 30',22,(116,149,175,255))
 return Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
def video(folder,dest,fps):
 files=sorted(glob.glob(folder+'/*.png'));w,h=Image.open(files[0]).size
 p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{w}x{h}','-framerate',str(fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',dest],stdin=subprocess.PIPE)
 for i,f in enumerate(files):
  p.stdin.write(overlay(Image.open(f),min(29.999,i/fps)).tobytes())
 p.stdin.close();assert p.wait()==0

def audio():
 sr=48000;n=30*sr;t=np.arange(n)/sr;rng=np.random.default_rng(20);noise=rng.normal(0,1,n)
 def env(a,b,fade=.2):return np.clip((t-a)/fade,0,1)*np.clip((b-t)/fade,0,1)
 def wav(name,x):
  # stereo subtly decorrelated, headroom for later narration
  st=np.stack([x,np.roll(x,73)*.97],axis=1);st=np.clip(st,-.9,.9)
  with wave.open(OUT+'/'+name+'.wav','wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((st*32767).astype('<i2').tobytes())
 motor=(.035*np.sin(2*np.pi*64*t)+.012*np.sin(2*np.pi*128*t)+.008*noise)*(env(.2,10)+.35*env(10,22))
 grains=np.zeros(n)
 for a in rng.uniform(.2,4.7,150):
  u=t-a;grains+=.055*np.exp(-np.maximum(u,0)*110)*np.sin(2*np.pi*rng.uniform(1800,4300)*u)*(u>=0)*(u<.06)
 hydraulic=(.04*np.sin(2*np.pi*(95*t+5*t*t))+.022*noise)*(env(10,13)+env(22,23.8)+.6*env(24.2,25.5))
 cooling=np.convolve(noise,np.ones(12)/12,'same')*.055*env(16.7,21.8)
 impacts=np.zeros(n)
 for a in [22.1,23.8,24.25,25.5,26.5]:
  u=t-a;impacts+=(u>=0)*(u<.5)*np.exp(-np.maximum(u,0)*20)*(.11*np.sin(2*np.pi*160*u)+.035*noise)
 transition=np.zeros(n)
 for a in [5,10,16,22,27,29.4]:
  u=t-a;transition+=(u>=0)*(u<.38)*np.sin(2*np.pi*(750*u+850*u*u))*.025*np.sin(np.clip(u/.38,0,1)*np.pi)**2
 stems={'motor':motor,'pellets':grains,'hydraulics':hydraulic+impacts,'cooling_water':cooling,'transitions':transition}
 for k,v in stems.items():wav(k,v)
 mix=sum(stems.values());wav('sound_effects',mix);print('Audio peak dBFS',20*np.log10(np.max(np.abs(mix))))
if __name__=='__main__':
 if sys.argv[1]=='audio':audio()
 else:video(sys.argv[2],sys.argv[3],float(sys.argv[4]))
