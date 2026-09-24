"""Explicit PBR fallback for procedural walnut in owned miniature web exports.

Preserves geometry and binary buffers. Blender source keeps editable procedural grain.
"""
import json,struct,hashlib
from pathlib import Path

def apply_walnut_fallback(path):
    path=Path(path);raw=path.read_bytes()
    magic,version,total=struct.unpack_from('<4sII',raw,0)
    if magic!=b'glTF' or version!=2 or total!=len(raw):raise ValueError('Invalid GLB container')
    chunks=[];pos=12;changed=[]
    while pos<len(raw):
        length,kind=struct.unpack_from('<II',raw,pos);pos+=8
        data=raw[pos:pos+length];pos+=length
        if kind==0x4E4F534A:
            doc=json.loads(data)
            for material in doc.get('materials',[]):
                if 'Warm walnut artistic grain' in material.get('name',''):
                    pbr=material.setdefault('pbrMetallicRoughness',{})
                    pbr['baseColorFactor']=[.105,.032,.011,1]
                    pbr['metallicFactor']=0;pbr['roughnessFactor']=.53
                    changed.append(material['name'])
            data=json.dumps(doc,separators=(',',':'),ensure_ascii=False).encode();data+=b' '*((-len(data))%4)
        chunks.append(struct.pack('<II',len(data),kind)+data)
    if not changed:raise ValueError('Expected owned walnut material missing')
    payload=b''.join(chunks);path.write_bytes(struct.pack('<4sII',b'glTF',2,12+len(payload))+payload)
    return {'changed_materials':changed,'baseColorFactor':[.105,.032,.011,1],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

if __name__=='__main__':
    import sys
    print(json.dumps(apply_walnut_fallback(sys.argv[1]),ensure_ascii=False))
