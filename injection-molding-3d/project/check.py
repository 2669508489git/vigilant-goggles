import os,runpy,sys,json
sys.argv.append('--setup');g=runpy.run_path(os.path.join(os.path.dirname(__file__),'build.py'));sc=g['sc']
def at(t):sc.frame_set(round(t*30)+1)
def near(a,b):return abs(a-b)<1e-5
at(0);spin0=g['screw'].rotation_euler.x
at(1);assert g['screw'].rotation_euler.x<spin0,'Right-handed flights must turn toward +X conveyance'
at(5);x0=g['screw'].location.x
at(9.9);xr=g['screw'].location.x
assert xr<x0-.6,'Plasticizing must retract screw'
at(10);rot=g['screw'].rotation_euler.x
at(13);assert near(g['screw'].location.x,0),'Injection must advance screw';assert near(g['screw'].rotation_euler.x,rot),'Injection is axial, not rotational'
for t in [10,13,16,20,21.9]:
 at(t)
 assert all((o.location-g['orig'][o.name]).length<1e-5 for o in g['moving']),'Mold must stay closed'
at(23.9);opening=g['moving'][0].location.x-g['orig'][g['moving'][0].name].x
assert near(opening,2.2)
assert near(g['pins'][0].location.x-g['orig'][g['pins'][0].name].x,opening),'No ejection before mold opens'
at(25.6);pinshift=g['pins'][0].location.x-g['orig'][g['pins'][0].name].x
assert pinshift<opening-.9,'Pins extend toward open mold space'
at(21.8);assert g['orange'].diffuse_color[0]<.1,'Solidification color'
at(26.9);assert g['parts'][0].location.x>3.3,'Ejected part must remain in the open mold gap, clear of the fixed insert'
at(28);assert all(not o.hide_render for o in g['parts']),'Hero product visible'
at(0);assert not g['screw'].hide_render,'Scrubbing backwards restores visibility'
report={'checks':'passed','resolution':[1080,1920],'fps':30,'frames':900,'duration':30,'mold_closed_during_injection':True,'screw_retracts_during_plasticizing':True,'screw_advances_without_rotation_during_injection':True,'ejection_after_opening':True,'ejected_part_clears_fixed_mold':True,'screw_handedness_and_rotation_consistent':True,'preview_notes':'Initial framing widened; front platen section removed to expose ejection; helical flight uses continuous radial fin.'}
open(g['ROOT']+'/mechanical_checks.json','w').write(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
