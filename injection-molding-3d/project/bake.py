"""Bake procedural animation into a normally playable Blender file."""
import sys,runpy,os,json
from mathutils import Vector
sys.argv.append('--setup')
g=runpy.run_path(os.path.join(os.path.dirname(__file__),'build.py'))
bpy=g['bpy'];sc=g['sc'];update=g['update']
animated=g['pellets']+g['parts']+g['moving']+g['pins']+g['drops']+g['tracers']+[g[k] for k in ['cam','screw','melt','runner','flow']]
# Render visibility is discrete. Geometry motion uses linear interpolated samples.
vis={};samples=sorted(set(range(1,901,3))|{150,151,300,301,480,481,660,661,810,811,900})
for f in samples:
 sc.frame_set(f);update(sc)
 for ob in sc.objects:
  v=ob.hide_render
  if vis.get(ob.name)!=v:ob.keyframe_insert('hide_render',frame=f);vis[ob.name]=v
 for ob in animated:
  for prop in ['location','rotation_euler','scale']:ob.keyframe_insert(prop,frame=f)
 g['cam'].data.keyframe_insert('ortho_scale',frame=f)
 g['orange'].keyframe_insert('diffuse_color',frame=f)
for ob in animated:
 if ob.animation_data and ob.animation_data.action:
  for fc in ob.animation_data.action.fcurves:
   for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path=='hide_render' else 'LINEAR'
bpy.app.handlers.frame_change_pre.clear();sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=g['ROOT']+'/project/injection.blend')
print('Baked',len(samples),'samples',len(animated),'objects')
