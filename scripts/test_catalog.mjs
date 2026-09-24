import assert from 'node:assert/strict';
import {readFile,stat} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const publicRoot=path.join(root,'web/public');
const catalog=JSON.parse(await readFile(path.join(publicRoot,'catalog.json'),'utf8'));
let releaseAssets;
try{
  const manifest=JSON.parse(await readFile(path.join(root,'release-assets.json'),'utf8'));
  releaseAssets=new Map(manifest.assets.map(asset=>[asset.name,asset]));
}catch(error){if(error.code!=='ENOENT')throw error;}
let checkedDownloads=0;

for(const entry of catalog.models){
  const manifest=JSON.parse(await readFile(path.join(root,'assets',entry.id,'manifest.json'),'utf8'));
  assert.equal(entry.lengthMm,manifest.display_length_mm,`${entry.id}: displayed size matches the asset`);
  for(const [kind,relativeUrl] of Object.entries(entry.downloads||{})){
    if(!relativeUrl)continue;
    assert(relativeUrl.startsWith('/downloads/'),`${entry.id}: ${kind} is a local download`);
    const filename=path.resolve(publicRoot,relativeUrl.slice(1));
    assert(filename.startsWith(`${publicRoot}${path.sep}`),`${entry.id}: ${kind} stays under public assets`);
    try{
      assert((await stat(filename)).isFile(),`${entry.id}: ${kind} exists`);
    }catch(error){
      if(error.code!=='ENOENT')throw error;
      const asset=releaseAssets?.get(path.basename(filename));
      assert(asset&&asset.bytes>0&&/^[a-f0-9]{64}$/.test(asset.sha256),`${entry.id}: ${kind} is recorded in the release manifest`);
    }
    checkedDownloads++;
  }
}

assert.equal(catalog.models.length,67);
console.log(JSON.stringify({passed:true,models:catalog.models.length,checkedDownloads}));
