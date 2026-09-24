import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const publicRoot=path.join(root,'web/public');
const catalog=JSON.parse(await readFile(path.join(publicRoot,'catalog.json'),'utf8'));
const data=JSON.parse(await readFile(path.join(publicRoot,'game-guides.json'),'utf8'));
const expectedIds=new Set(catalog.models.map(model=>model.id));
const actualIds=new Set();
const isText=value=>typeof value==='string'&&value.trim().length>0;

assert.equal(data.schemaVersion,2,'supported game guide schema');
assert(Array.isArray(data.guides),'game guides are a list');
for(const guide of data.guides){
  assert(expectedIds.has(guide.modelId),`${guide.modelId}: present in catalog`);
  assert(!actualIds.has(guide.modelId),`${guide.modelId}: one guide per model`);
  actualIds.add(guide.modelId);
  for(const field of ['region','mode','reviewedAt','strength','tactics','basis']){
    assert(isText(guide[field]),`${guide.modelId}: ${field} has content`);
  }
  for(const field of ['advice','note']){
    assert(isText(guide.ammo?.[field]),`${guide.modelId}: ammo.${field} has content`);
  }
  assert(guide.strength.length<=100,`${guide.modelId}: strength fits the short card`);
  assert(guide.tactics.length<=100,`${guide.modelId}: tactics fits the short card`);
  assert(guide.ammo.advice.length<=110,`${guide.modelId}: ammo advice fits the short card`);
  assert(Array.isArray(guide.sources)&&guide.sources.length>0,`${guide.modelId}: has a source`);
  for(const source of guide.sources){
    assert(isText(source.title),`${guide.modelId}: source has a title`);
    assert.equal(new URL(source.url).protocol,'https:',`${guide.modelId}: source uses HTTPS`);
  }
}
assert.deepEqual(actualIds,expectedIds,'every catalog model has a game guide');
console.log(JSON.stringify({passed:true,guides:actualIds.size,sourced:actualIds.size}));
