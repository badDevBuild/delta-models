export function formatMeasure(value) {
  return new Intl.NumberFormat('zh-CN', {maximumFractionDigits: 1}).format(value);
}

export function setModelWireframe(assembly, enabled) {
  if (!assembly) return;
  for (const part of assembly.parts.values()) {
    for (const {material} of part.materials) {
      if (!('wireframe' in material)) continue;
      material.wireframe = enabled;
      material.needsUpdate = true;
    }
  }
}
