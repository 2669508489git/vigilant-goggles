import bpy, math, random, os, sys
from mathutils import Vector
ROOT=os.path.abspath(os.getenv('OUT',os.path.join(os.path.dirname(__file__),'..')))
os.makedirs(ROOT,exist_ok=True)
os.makedirs(ROOT+'/project',exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene
sc.render.engine='BLENDER_WORKBENCH'; sc.render.resolution_x=1080; sc.render.resolution_y=1920; sc.render.resolution_percentage=int(os.getenv('SCALE','100')); sc.render.fps=30
sc.render.image_settings.file_format='PNG'; sc.render.film_transparent=False
sh=sc.display.shading; sh.light='STUDIO'; sh.studiolight_rotate_z=.4; sh.color_type='MATERIAL'; sh.show_shadows=True; sh.show_cavity=True; sh.cavity_type='BOTH'; sh.curvature_ridge_factor=1.4; sh.curvature_valley_factor=1.1; sh.show_specular_highlight=True; sh.background_type='WORLD'; sc.world.color=(.008,.016,.032)
sc.display.render_aa='5'
def mat(n,c):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); return m
metal=mat('Brushed steel',(.46,.56,.65)); dark=mat('Graphite',(.045,.075,.12)); blue=mat('Technology blue',(.025,.42,.9)); orange=mat('Molten polymer',(1,.17,.025)); water=mat('Cooling water',(.02,.7,1)); plastic=mat('Solid polymer',(.08,.14,.2)); white=mat('Fasteners',(.72,.8,.86))
def cube(n,p,s,m,bevel=.08):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p); o=bpy.context.object; o.name=n; o.dimensions=s; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m)
 if bevel: mod=o.modifiers.new('Machined edges','BEVEL'); mod.width=bevel; mod.segments=3; o.modifiers.new('Normals','WEIGHTED_NORMAL')
 return o
def cyl(n,p,r,l,m,axis='X'):
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=l,location=p); o=bpy.context.object;o.name=n
 if axis=='X':o.rotation_euler[1]=math.pi/2
 if axis=='Y':o.rotation_euler[0]=math.pi/2
 o.data.materials.append(m)
 for f in o.data.polygons:f.use_smooth=True
 return o
def tube(n,pts,r,m):
 c=bpy.data.curves.new(n,'CURVE'); c.dimensions='3D'; c.bevel_depth=r;c.bevel_resolution=3; p=c.splines.new('POLY');p.points.add(len(pts)-1)
 for a,b in zip(p.points,pts):a.co=(*b,1)
 o=bpy.data.objects.new(n,c);sc.collection.objects.link(o);o.data.materials.append(m);return o
# Base, drive and tie bars
cube('Machine foundation',(0,0,-1.7),(12,3.4,.9),dark)
for x in [-4,4]:cube('Foot',(x,0,-2.3),(1,2.6,.4),metal)
cube('Injection drive',(-5,0,0),(1.7,2,1.9),blue)
for y in [-1.05,1.05]:
 for z in [-.95,.95]:cyl('Clamping tie bar',(4.1,y,z),.105,5.7,white)
# rear half barrel shell open toward camera
verts=[];faces=[]
for x in [-4.3,1.25]:
 for j in range(33):
  a=math.pi*j/32; verts.append((x,.71*math.sin(a),.71*math.cos(a)))
for j in range(32):faces.append((j,j+1,j+34,j+33))
me=bpy.data.meshes.new('Section barrel');me.from_pydata(verts,[],faces);o=bpy.data.objects.new('Cutaway steel barrel',me);sc.collection.objects.link(o);o.data.materials.append(metal)
for x in [-3.7,-2.3,-.9,.65]:
 tube('Heater band',[(x,.78*math.sin(math.pi*j/32),.78*math.cos(math.pi*j/32)) for j in range(33)],.09,blue)
# screw true helical flight
screw=bpy.data.objects.new('Reciprocating screw',None);sc.collection.objects.link(screw)
o=cyl('Screw core',(-1.8,0,0),.31,5.1,metal);o.parent=screw
pts=[]
for i in range(1100):
 x=-4.25+5.15*i/1099;a=i/1099*math.pi*2*10;pts.append((x,.49*math.sin(a),.49*math.cos(a)))
vs=[];fs=[]
for i in range(1100):
 x=-4.25+5.15*i/1099;a=i/1099*math.pi*2*10
 for r in [.30,.60]:vs.append((x,r*math.sin(a),r*math.cos(a)))
 if i:fs.append((2*i-2,2*i-1,2*i+1,2*i))
me=bpy.data.meshes.new('Continuous helicoid flight');me.from_pydata(vs,[],fs);o=bpy.data.objects.new('Helical screw flight',me);sc.collection.objects.link(o);o.data.materials.append(white);o.parent=screw
mod=o.modifiers.new('Flight thickness','SOLIDIFY');mod.thickness=.055
# Hopper open cone
bpy.ops.mesh.primitive_cone_add(vertices=48,radius1=.3,radius2=.95,depth=1.4,end_fill_type='NOTHING',location=(-3.55,0,1.45));bpy.context.object.data.materials.append(metal)
cyl('Feed throat',(-3.55,0,.7),.25,.65,metal,'Z')
cyl('Nozzle',(1.5,0,0),.22,.7,metal)
# shot melt reservoir visible in front half
melt=cyl('Metered melt',(1,0,0),.57,.1,orange)
random.seed(8);pellets=[]
for i in range(85):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.095,location=(0,0,0));o=bpy.context.object;o.name='Feed pellet';o.data.materials.append(blue);pellets.append(o)
# fixed and moving mold, sectional upper/lower blocks
fixed=[];moving=[]
for group,x in [(fixed,2.5),(moving,4.1)]:
 for z in [-1.15,1.15]:group.append(cube('Sectioned mold insert',(x,0,z),(1.45,2.65,.8),metal))
 group.append(cube('Mold rear section',(x,.95,0),(1.45,.65,1.55),metal))
 for y in [-1.15,1.15]:
  for z in [-1.15,1.15]:group.append(cyl('Mold bolt',(x-.76,y,z),.13,.1,dark))
fixed.append(cube('Fixed platen',(1.9,.95,0),(.25,.65,3.3),dark))
moving.append(cube('Moving platen',(4.9,.95,0),(.35,.65,3.3),dark))
# cavity product: precision electronics housing, x thickness, yz plane
parts=[]
parts.append(cube('Housing base',(3.25,0,0),(.16,1.7,1.65),orange,.12))
for y in [-.79,.79]:parts.append(cube('Housing side rib',(3.42,y,0),(.32,.12,1.62),orange,.05))
for z in [-.77,.77]:parts.append(cube('Housing end rib',(3.42,0,z),(.32,1.6,.12),orange,.05))
for y in [-.55,.55]:
 for z in [-.52,.52]:parts.append(cyl('Assembly boss',(3.46,y,z),.115,.3,orange))
runner=tube('Sprue runner gate',[(1.75,-.12,0),(2.85,-.12,0),(3.2,-.12,0)],.12,orange)
# rational U circuits in mold lower section, section view foreground
cool=[]
for x in [2.35,4.25]:
 pts=[(x,-1.39,.8),(x,-1.39,.48),(x+.27,-1.39,.48),(x+.27,-1.39,-.55),(x,-1.39,-.55),(x,-1.39,-.8)]
 cool.append(tube('Cooling circuit',pts,.065,blue))
flow=tube('Viscous melt bed',[(-1.5,-.40,-.24),(1.15,-.40,-.24)],.20,orange)
tracers=[]
for i in range(12):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.06);o=bpy.context.object;o.data.materials.append(white);tracers.append(o)
drops=[]
for i in range(18):
 o=cyl('Water pulse',(0,0,0),.074,.13,water,'Z');drops.append(o)
pins=[]
for y in [-.5,.5]:
 for z in [-.45,.45]:pins.append(cyl('Ejector pin',(4.1,y,z),.055,1.0,white))
# floor grid
for i in range(-10,11):
 tube('Floor grid',[(i,-8,-2.55),(i,8,-2.55)],.009,blue)
 tube('Floor grid',[(-10,i,-2.55),(10,i,-2.55)],.009,blue)
bpy.ops.object.camera_add();cam=bpy.context.object;sc.camera=cam;cam.data.type='ORTHO';cam.data.lens=45

def ease(a):a=max(0,min(1,a));return a*a*(3-2*a)
def show(o,v):o.hide_render=not v
orig={o.name:o.location.copy() for o in moving+pins+parts+cool}
def update(scene):
 t=(scene.frame_current-1)/30
 for ob in scene.objects:ob.hide_render=False
 # camera smooth tracks assembly and then follows product
 if t<5:
  a=ease(t/5);target=Vector((-1.3-0.7*a,0,.2));pos=target+Vector((8-5*a,-17,10-3*a));scale=25-14*a
 elif t<10:target=Vector((-1.4,0,0));pos=target+Vector((2,-15,7));scale=10.6-.6*ease((t-5)/5)
 elif t<22:target=Vector((3.1,0,0));pos=target+Vector((12,-16,8));scale=10.8-.5*ease((t-10)/12)
 elif t<27:target=Vector((3.1,0,0));pos=target+Vector((12,-16,8));scale=12
 else:target=Vector((1.7,0,.1));pos=target+Vector((15,-10,8));scale=7.5
 cam.location=pos;cam.rotation_euler=(target-pos).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
 retreat=.65*ease((t-5)/5) if t<10 else .65*(1-ease((t-10)/3))
 screw.location.x=-retreat;screw.rotation_euler.x=80-t*4 if t<10 else 40
 for i,o in enumerate(pellets):
  show(o,t<10);q=(t*.52+i*.137)%1
  if i<38:o.location=(-3.55+.55*math.sin(i*9)*(1-q),.4*math.cos(i*7)*(1-q),2.8-2.8*q)
  else:
   x=-4.1+5*((t*.15+i*.027)%1);a=i*2.4+t*4;o.location=(x,.48*math.sin(a),.48*math.cos(a));o.data.materials[0]=blue if x<-1.5 else orange
 show(flow,5<t<10);flow.scale.x=max(.01,ease((t-5)/4))
 for i,o in enumerate(tracers):
  show(o,10<t<15);q=(t*.7+i/12)%1;o.location=(1.8+1.5*q,-.27,0)
 fill=ease((t-10)/4.5)
 show(melt,5<t<15);melt.location.x=.95-retreat/2;melt.scale.z=max(.01,retreat*8*(1-fill))
 opening=2.2*ease((t-22)/1.8);eject=.95*ease((t-24.2)/1.3)
 for o in moving:o.location=orig[o.name]+Vector((opening,0,0));show(o,t<27)
 for o in fixed:show(o,t<27)
 for o in pins:o.location=orig[o.name]+Vector((opening-eject,0,0));show(o,22<t<27)
 for o in parts:
  show(o,t>=10)
  o.location=orig[o.name].copy();o.rotation_euler=(0,0,0);o.scale=(1,max(.005,fill),1)
  if t>=22:o.location.x+=opening-eject
  if t>=26:o.location.z-=.40*ease((t-26)/.5)
  if t>=27:
   v=orig[o.name]-Vector((3.3,0,0));ang=-(t-27)*.25
   from mathutils import Matrix
   rot=Matrix.Rotation(ang,4,'Z');o.location=Vector((1.7,0,.1))+rot@v;o.rotation_euler.z=ang;o.scale=(1,1,1)
  c=ease((t-17)/4.5);o.color=(1,1,1,1)
  # unique interpolated material shared across housing
 color=tuple((1-c)*a+c*b for a,b in zip((1,.17,.025),(.08,.14,.2)))
 orange.diffuse_color=(*color,1)
 show(runner,10<t<22);runner.scale.x=max(.001,fill)
 for j,o in enumerate(cool):show(o,16<t<22)
 for i,o in enumerate(drops):
  show(o,16.7<t<22);q=(t*.7+i/9)%1;x=2.35 if i<9 else 4.25;o.location=(x+.27,-1.39,.48-1.03*q)
 # remove machine on hero shot
 for o in scene.objects:
  if t>=27 and o.type in ['MESH','CURVE'] and o not in parts:o.hide_render=True
bpy.app.handlers.frame_change_pre.append(update)
sc.frame_start=int(os.getenv('START','1'));sc.frame_end=int(os.getenv('END','900'));sc.frame_step=int(os.getenv('STEP','1'));sc.render.filepath=os.getenv('FRAMES',ROOT+'/frames/')
if not os.getenv('SKIP_SAVE'):bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/project/injection.blend')
if '--setup' in sys.argv:pass
elif '--test' in sys.argv:
 sc.frame_set(int(os.getenv('TEST_FRAME','360')));sc.render.filepath=ROOT+'/test.png';bpy.ops.render.render(write_still=True)
else:bpy.ops.render.render(animation=True)
