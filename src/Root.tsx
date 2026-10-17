import React from 'react';
import {AbsoluteFill, Composition, Sequence, interpolate, useCurrentFrame, Easing, staticFile} from 'remotion';
import './style.css';

const GOLD = '#F7C948';
const WHITE = '#F4F4EE';
const DIM = '#82847F';
const clamp = (v: number) => Math.min(1, Math.max(0, v));
const ease = (f: number, a: number, d = 25) => Easing.bezier(.22, 1, .36, 1)(clamp((f-a)/d));
const lerp = (a:number,b:number,t:number)=>a+(b-a)*t;
const stages = ['创意构思','功能整合','结构设计','模具开发','试模优化','量产交付'];

const Stroke: React.FC<{d:string; p?:number; color?:string; width?:number; opacity?:number; dash?:boolean}> = ({d,p=1,color=GOLD,width=3,opacity=1,dash=false}) => <path d={d} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={dash?'.015 .02':1} strokeDashoffset={dash?0:1-clamp(p)} opacity={opacity}/>;
const Label: React.FC<{x:number;y:number;children:React.ReactNode;color?:string;size?:number;anchor?:'start'|'middle'|'end';opacity?:number}> = ({x,y,children,color=WHITE,size=25,anchor='middle',opacity=1})=><text x={x} y={y} fill={color} fontFamily="MotionCJK, sans-serif" fontSize={size} textAnchor={anchor} opacity={opacity}>{children}</text>;
const Dot = ({x,y,r=5,color=GOLD}:{x:number;y:number;r?:number;color?:string})=><circle cx={x} cy={y} r={r} fill={color}/>;
const Reveal: React.FC<{text:string;f:number;at?:number;className?:string}> = ({text,f,at=0,className})=><span className={className}>{Array.from(text).map((c,i)=><span key={i} style={{display:'inline-block',opacity:ease(f,at+i*2,15),transform:`translateY(${(1-ease(f,at+i*2,18))*20}px)`}}>{c===' '?'\u00a0':c}</span>)}</span>;

const Concept = ({f}:{f:number})=>{
 const split=ease(f,15,45), resolve=ease(f,118,45);
 const pts=[[390,74],[154,346],[626,346]];
 return <svg viewBox="0 0 780 500">
  <Stroke d="M390 74 L154 346 L626 346 Z" p={split} color="#454740" width={2}/>
  {pts.map(([x,y],i)=><g key={i} opacity={ease(f,16+i*14)}>
   <Stroke d={`M${x} ${y} L390 249`} p={ease(f,60+i*9)} color={GOLD} width={1.5}/>
   <circle cx={x} cy={y} r={48+Math.sin(f*.04+i)*4} fill="#000000" stroke={GOLD} strokeWidth={2}/>
   <Label x={x} y={y+9} size={25}>{['体验','成本','可制造'][i]}</Label>
  </g>)}
  <g opacity={ease(f,65)}>
   <circle cx={390+Math.sin(f*.045)*30*(1-resolve)} cy={249+Math.cos(f*.05)*22*(1-resolve)} r={10} fill={GOLD}/>
   <circle cx={390} cy={249} r={26+10*(1-resolve)} fill="none" stroke={GOLD} opacity={.35}/>
  </g>
  <g opacity={resolve} transform={`translate(0 ${20*(1-resolve)})`}>
   <rect x="239" y="409" width="302" height="60" rx="30" fill={GOLD}/>
   <Label x={390} y={448} color="#060705" size={25}>先把需求变成约束</Label>
   <Stroke d="M390 281 V397" p={resolve} width={2}/>
  </g>
 </svg>;
};
const FunctionDiagram = ({f}:{f:number})=>{
 const t=ease(f,70,65); const blocks=[{name:'装配',x:120,y:100,tx:138,ty:125},{name:'操作',x:320,y:135,tx:428,ty:125},{name:'连接',x:230,y:240,tx:138,ty:270},{name:'维护',x:410,y:220,tx:428,ty:270}];
 return <svg viewBox="0 0 780 500">
  <rect x="95" y="72" width="590" height="368" rx="38" fill="none" stroke="#4A4C44" strokeWidth="2" strokeDasharray="8 10"/>
  <Label x={650} y={53} anchor="end" color={DIM} size={22}>有限的内部空间</Label>
  {blocks.map((b,i)=>{const x=lerp(b.x,b.tx,t),y=lerp(b.y,b.ty,t); return <g key={i} opacity={ease(f,i*8)}>
   <rect x={x} y={y} width="210" height="113" rx="10" fill={t<.5?'#19170E':'#0D0F0A'} stroke={GOLD} strokeWidth={2}/>
   <Label x={x+105} y={y+66} size={30}>{b.name}</Label>
  </g>})}
  <Stroke d="M348 181 H428 M348 326 H428 M243 238 V270 M533 238 V270" p={ease(f,136,35)} width={3}/>
  <g opacity={ease(f,155)}><Dot x={388} y={181}/><Dot x={388} y={326}/><Label x={390} y={478} color={GOLD}>功能之间，必须留出接口</Label></g>
 </svg>;
};
const Structure = ({f}:{f:number})=>{
 const t=ease(f,65,65);const inset=lerp(0,22,t);const rib=ease(f,130,36);
 return <svg viewBox="0 0 780 500">
  <Stroke d="M130 113 H650" color="#3B3D36" p={ease(f,0)} width={1}/>
  <Stroke d="M130 366 H650" color="#3B3D36" p={ease(f,0)} width={1}/>
  <path d={`M170 115 L${170+inset} 365 H${610-inset} L610 115 H580 L${580-inset} 335 H${200+inset} L200 115 Z`} fill="#292411" stroke={GOLD} strokeWidth={3}/>
  <g opacity={rib}><path d={`M300 335 L${310-4*rib} ${335-90*rib} H${318+4*rib} L334 335 M454 335 L466 ${335-90*rib} H478 L488 335`} fill="#292411" stroke={GOLD} strokeWidth={2}/></g>
  <Stroke d="M390 265 V79 M375 96 L390 78 L405 96" p={ease(f,30)} width={3}/>
  <Label x={390} y={53} color={GOLD}>脱模方向</Label>
  <g opacity={ease(f,88)}>
   <Stroke d="M589 163 H690 V210" width={1.5}/><Label x={690} y={242} size={22}>拔模斜度</Label>
   <Stroke d="M207 293 H87 V326" width={1.5}/><Label x={88} y={358} size={22}>壁厚过渡</Label>
  </g>
  <g opacity={rib}><Stroke d="M317 267 L360 413" width={1.5}/><Label x={390} y={450} color={GOLD}>加强筋也要兼顾缩痕风险</Label></g>
  <Label x={390} y={492} color={DIM} size={18}>剖面示意 · 斜度与壁厚依材料和结构确定</Label>
 </svg>;
};
const Mold = ({f}:{f:number})=>{
 const close=ease(f,12,40),open=ease(f,155,40),gap=50*(1-close)+40*open; const flow=ease(f,66,57); const eject=ease(f,182,30);
 return <svg viewBox="0 0 780 500">
  <g transform={`translate(0 ${-gap})`}>
   <path d="M135 89 H645 V239 H548 V186 H232 V239 H135 Z" fill="#11130F" stroke="#787B70" strokeWidth={2}/>
   <Stroke d="M390 89 V164 H250 V204 M390 164 H530 V204" color={GOLD} width={9} p={flow}/>
   <Label x={179} y={145} size={21} color={DIM}>定模</Label>
  </g>
  <g transform={`translate(0 ${gap})`}>
   <path d="M135 251 H232 V290 H548 V251 H645 V360 H135 Z" fill="#11130F" stroke="#787B70" strokeWidth={2}/>
   <Stroke d={`M302 360 V${303-100*eject} M478 360 V${303-100*eject}`} color={GOLD} width={5} p={ease(f,150)} />
   <Label x={179} y={337} size={21} color={DIM}>动模</Label>
  </g>
  <g opacity={flow} transform={`translate(0 ${-eject*34})`}><path d="M241 208 V279 H539 V208" fill="none" stroke={GOLD} strokeWidth={13} pathLength={1} strokeDasharray={1} strokeDashoffset={1-flow}/></g>
  <Stroke d="M90 245 H690" color="#4A4C42" p={ease(f,5)} dash width={1}/>
  <Label x={688} y={230} anchor="end" size={19} color={DIM}>分型面</Label>
  <Label x={390} y={486} color={GOLD}>{f<150?'熔体要充满，气体要排出':'开模之后，还要顺利顶出'}</Label>
 </svg>;
};
const Trial = ({f}:{f:number})=>{
 const t=ease(f,40,110), marker=clamp((f-45)/125);const xx=145+marker*485;
 return <svg viewBox="0 0 780 500">
  <Stroke d="M123 65 V355 H670" p={ease(f,0)} color="#787B70" width={2}/>
  {[130,200,270].map(y=><Stroke key={y} d={`M123 ${y} H670`} color="#24271F" width={1}/>)}
  <Label x={124} y={43} anchor="start" size={21} color={DIM}>过程响应 / 示意</Label>
  <Label x={670} y={388} anchor="end" size={21} color={DIM}>一次次试模 →</Label>
  <rect x="125" y="166" width="544" height="66" fill={GOLD} opacity={.055}/>
  <Stroke d="M145 300 C185 300 190 95 250 108 S320 290 373 260 S423 155 470 173 S545 211 630 199" p={t} width={4}/>
  <circle cx={xx} cy={199} r={8} fill={GOLD} opacity={ease(f,160)}/>
  <g opacity={ease(f,90)}><Stroke d="M468 164 V99 H639" width={1.5}/><Label x={644} y={85} anchor="end" size={23}>寻找稳定工艺窗口</Label></g>
  {['短射','飞边','翘曲'].map((s,i)=><g key={s} opacity={ease(f,15+i*15)*(1-ease(f,130+i*15))}><Label x={230+i*160} y={430} size={26} color={GOLD}>{s}</Label></g>)}
  <g opacity={ease(f,166)}><Stroke d="M610 430 H170 M190 418 L170 430 L190 442" p={ease(f,166)} width={2}/><Label x={390} y={476} color={GOLD} size={25}>调工艺，也可能回改结构与模具</Label></g>
 </svg>;
};
const Production = ({f}:{f:number})=>{
 const p=ease(f,15,45), window=ease(f,80,40);
 return <svg viewBox="0 0 780 500">
  <Stroke d="M83 267 H697 M83 355 H697" color="#42453C" p={p} width={2}/>
  {[0,1,2,3,4,5].map(i=>{const x=75+((i*110+f*1.9)%660);return <g key={i} opacity={p*clamp((x-75)/35)*clamp((735-x)/35)} transform={`translate(${x} 310)`}><rect x="-30" y="-26" width="60" height="52" rx="9" fill="#17190F" stroke={x>330&&x<450?GOLD:'#777B6D'} strokeWidth={2}/><path d="M-15 0 H15" stroke={GOLD} strokeWidth={2}/></g>})}
  <g opacity={window}><path d="M337 235 V184 H443 V235 M337 379 V399 H443 V379" stroke={GOLD} fill="none" strokeWidth={3}/><Stroke d="M390 182 V106 H570" p={window} width={2}/><Label x={582} y={114} anchor="start" color={GOLD} size={24}>检验</Label></g>
  <Label x={390} y={53} color={WHITE} size={30}>合格一次 ≠ 批批稳定</Label>
  {['尺寸','外观','性能'].map((s,i)=><g key={s} opacity={ease(f,115+i*13)}><circle cx={215+i*175} cy={455} r={5} fill={GOLD}/><Label x={240+i*175} y={463} anchor="start" size={24}>{s}</Label></g>)}
  <Stroke d="M115 140 H290" p={ease(f,30)} color={DIM} width={1.5}/><Label x={115} y={121} anchor="start" color={DIM} size={22}>材料 · 工艺 · 检验标准</Label>
 </svg>;
};
const beats = [
 ['提出产品目标','三方约束展开','需求开始收敛','形成可验证要求'],
 ['功能进入空间','识别相互干涉','重新安排布局','建立装配接口'],
 ['查看结构剖面','沿脱模方向检查','加入拔模斜度','加强筋与壁厚协同'],
 ['两半模具合拢','熔体流经浇道','充填与冷却成型','开模并顶出制件'],
 ['观察试模缺陷','调整参数并验证','寻找稳定窗口','反馈结构与模具'],
 ['制件连续产出','建立检验环节','检查关键质量','持续控制批次波动'],
];
const descriptions = [
 {en:'DEFINE THE PROBLEM',title:['一个想法，','先做哪些取舍？'],key:'难点 01 / 需求取舍',line:'体验、成本、可制造性，要一起考虑。',foot:'把“想要什么”，变成可验证的产品要求。',visual:Concept},
 {en:'CONNECT THE FUNCTIONS',title:['功能越多，','越容易互相牵制。'],key:'难点 02 / 系统协同',line:'装得下，还要装得上、用得顺、修得到。',foot:'接口与装配空间，决定功能能否真正共存。',visual:FunctionDiagram},
 {en:'DESIGN FOR MOLDING',title:['画得出来，','还要成型、脱模。'],key:'难点 03 / 结构可制造性',line:'壁厚、拔模、加强筋，必须协同设计。',foot:'局部堆料容易缩痕；倒扣可能增加模具机构。',visual:Structure},
 {en:'ENGINEER THE TOOL',title:['一副模具，','不只是一个空腔。'],key:'难点 04 / 成型与顶出',line:'浇注、排气、冷却、顶出，环环相扣。',foot:'分型与进胶方案，会影响外观、成型和模具复杂度。',visual:Mold},
 {en:'ITERATE WITH EVIDENCE',title:['试模的结果，','会反推前面的设计。'],key:'难点 05 / 反馈迭代',line:'缺陷可能来自材料、工艺，也可能来自设计。',foot:'曲线仅表达收敛过程，不代表实测数据或固定次数。',visual:Trial},
 {en:'CONTROL THE VARIATION',title:['做出一个，','不等于稳定做出一批。'],key:'难点 06 / 量产一致性',line:'控制材料与工艺波动，持续检验关键质量。',foot:'确认样件与检验标准，才能让交付有据可依。',visual:Production},
];

const Chapter = ({index}:{index:number})=>{
 const f=useCurrentFrame(); const data=descriptions[index]; const Visual=data.visual;
 const enter=ease(f,0,24), exit=1-ease(f,222,18);
 return <AbsoluteFill style={{opacity:enter*exit,transform:`translateY(${(1-enter)*28-(1-exit)*18}px)`}}>
  <div className="chapter-kicker"><span>{String(index+1).padStart(2,'0')}</span><span>{stages[index]}</span><span className="en">{data.en}</span></div>
  <div className="headline"><Reveal text={data.title[0]} f={f} at={8}/><br/><Reveal text={data.title[1]} f={f} at={21} className="gold"/></div>
  <div className="beat" style={{opacity:ease(f%60,0,10),transform:`translateY(${(1-ease(f%60,0,12))*7}px)`}}><span>{String(Math.min(4,Math.floor(f/60)+1)).padStart(2,'0')} / 04</span>{beats[index][Math.min(3,Math.floor(f/60))]}</div>
  <div className="visual"><Visual f={f}/></div>
  <div className="takeaway" style={{opacity:ease(f,55,30),transform:`translateY(${(1-ease(f,55,30))*16}px)`}}>
   <div className="key">{data.key}</div><div className="body">{data.line}</div><div className="foot">{data.foot}</div>
  </div>
 </AbsoluteFill>;
};
const Intro=()=>{
 const f=useCurrentFrame();const out=1-ease(f,163,17);const count=Math.min(6,Math.floor(1+5*ease(f,35,65)));
 return <AbsoluteFill style={{opacity:out}}>
  <div className="intro-kicker"><Reveal text="从一个想法，到稳定交付" f={f} at={7}/></div>
  <div className="intro-title"><Reveal text="开发一款" f={f} at={10}/><br/><Reveal text="塑胶产品" f={f} at={23} className="gold"/><br/><Reveal text="到底有多难？" f={f} at={40}/></div>
  <svg className="intro-art" viewBox="0 0 780 460">
   <g opacity={ease(f,30)}><circle cx={390} cy={204} r={136} stroke="#34372C" fill="none" strokeWidth={1}/><circle cx={390} cy={204} r={136} stroke={GOLD} fill="none" strokeWidth={3} pathLength={1} strokeDasharray={1} strokeDashoffset={1-ease(f,30,90)} transform="rotate(-90 390 204)"/><Label x={390} y={238} size={109} color={GOLD}>{String(count).padStart(2,'0')}</Label><Label x={390} y={289} size={21} color={DIM}>个相互关联的阶段</Label></g>
   {stages.map((s,i)=>{const a=-Math.PI/2+i*Math.PI/3;const x=390+218*Math.cos(a),y=204+176*Math.sin(a);return <g key={s} opacity={ease(f,55+i*9)}><Dot x={390+136*Math.cos(a)} y={204+136*Math.sin(a)} r={5}/><Label x={x} y={y+8} size={23}>{s}</Label></g>})}
   <Label x={390} y={439} size={25} color={GOLD} opacity={ease(f,122)}>难的，是让每一步都能接上下一步。</Label>
  </svg>
 </AbsoluteFill>;
};
const Outro=()=>{
 const f=useCurrentFrame();
 return <AbsoluteFill style={{opacity:ease(f,0,20)}}>
  <div className="intro-kicker">从创意到交付 / THE BIG PICTURE</div>
  <div className="outro-title"><Reveal text="真正的难度" f={f} at={8}/><br/><Reveal text="藏在环环相扣里。" f={f} at={23} className="gold"/></div>
  <svg className="outro-art" viewBox="0 0 780 550">
   {stages.map((s,i)=>{const x=i%2===0?192:588,y=78+Math.floor(i/2)*162;return <g key={s} opacity={ease(f,20+i*8)}><circle cx={x} cy={y} r={45} fill="#17170C" stroke={GOLD} strokeWidth={2}/><Label x={x} y={y+10} color={GOLD} size={31}>{String(i+1).padStart(2,'0')}</Label><Label x={x} y={y+83} size={25}>{s}</Label></g>})}
   <Stroke d="M237 78 H543" p={ease(f,30,50)} width={2} color="#72765F"/>
   <Stroke d="M633 78 H680 V181 H192 V195" p={ease(f,38,40)} width={2} color="#72765F"/>
   <Stroke d="M237 240 H543 M633 240 H680 V343 H192 V357 M237 402 H543" p={ease(f,50,50)} width={2} color="#72765F"/>
   <Stroke d="M145 402 H76 V78 H133 M119 65 L133 78 L119 91" p={ease(f,83,45)} width={2}/>
   <Label x={390} y={535} color={GOLD} size={28} opacity={ease(f,103)}>向前推进，也为反馈留出回路。</Label>
  </svg>
  <div className="outro-end" style={{opacity:ease(f,130,25)}}>好产品，是系统协同的结果。</div>
 </AbsoluteFill>;
};
const Film=()=>{
 const f=useCurrentFrame();const current=f<180?-1:Math.min(5,Math.floor((f-180)/240));
 return <AbsoluteFill style={{backgroundColor:'#000000',color:WHITE,fontFamily:'MotionCJK, sans-serif'}}>
  <style>{`@font-face{font-family:MotionCJK;src:url('${staticFile('MotionCJK-Regular.otf')}') format('opentype');font-weight:100 900;font-display:block;}`}</style>
  <div key={`top-${f}`} className="topbar"><span className="brand"><i/>制造的逻辑</span><span>PLASTIC / ENGINEERING</span></div>
  <div className="edge-number">{String(Math.floor(f/30)).padStart(2,'0')} / 60</div>
  <Sequence durationInFrames={180}><Intro/></Sequence>
  {stages.map((_,i)=><Sequence key={i} from={180+i*240} durationInFrames={240}><Chapter index={i}/></Sequence>)}
  <Sequence from={1620} durationInFrames={180}><Outro/></Sequence>
  <div key={`rail-${f}`} className="timeline">{stages.map((s,i)=>{const progress=clamp((f-(180+i*240))/240);return <div className="timeline-item" key={s}><div className="track"><div style={{width:`${progress*100}%`}}/></div><span style={{color:current===i?GOLD:progress===1?'#C5C7BC':'#5E6256'}}>{s}</span></div>})}</div>
  <div key={`bottom-${f}`} className="bottom-line"><span>注塑产品开发 · 原理示意</span><span>IDEA → DELIVERY</span></div>
 </AbsoluteFill>;
};
export const Root=()=> <Composition id="PlasticJourney" component={Film} durationInFrames={1800} fps={30} width={900} height={1200}/>;
