# DELTA MODELS 模型收藏馆

中文 Three.js 网页，按需展示 config/models.json 清单中的模型。各批次共用同一收藏馆，支持名称搜索和类别筛选。页面读取 `public/catalog.json`，不连接远程账户或托管服务。

## 本机启动

需要 Node.js 22.12+（或 Vite 8 支持的更新版本）。在此目录执行：

```sh
npm ci
npm run dev
```

打开 `http://127.0.0.1:5174/`。网址 `?model=awm` 可直接打开 AWM；`?category=突击步枪` 可按类别筛选。开发服务器只绑定本机回环地址。

```sh
npm run build
npm run preview
npm test
```

`build` 输出到 `dist/`，包含 67 个网页展示模型与缩略图。完整打印、切片和 Blender 文件存放在 GitHub Release，生产环境的下载链接由 `.env.production` 指向发布包。`preview` 地址为 `http://127.0.0.1:4174/`。`npm test` 直接解析真实 GLB，并调用网页同一套组件和加载模块；发布版使用 `release-assets.json` 核对下载文件索引。Node 测试不能替代 WebGL 视觉检查。

## 文件接口

- `public/catalog.json`：目录和逐款交付状态。
- `public/models/<id>.glb`：按需加载的三维文件。
- `public/previews/<id>.png`：六卡目录缩略图。
- `public/downloads/<id>-print.zip`：打印文件包。
- `public/downloads/<id>-sliced.zip`：通过当前输入文件校验的 P1S / 0.4 mm / PLA 原生切片工程（就绪时显示）。
- `public/downloads/<id>.blend`：可编辑母版。

`id` 及批次由项目根目录 `config/models.json` 统一定义。GLB 顶级逻辑组件使用 `part_<id>` 节点，节点 extras 映射为 Three.js `userData`：

```json
{
  "label": "前端装饰件",
  "description": "用于展示外观的实心组件。",
  "default_visible": true,
  "variant": {"group": "barrel", "value": "short"},
  "explode_direction": [-1.05, 0.07, 0]
}
```

`variant` 为可选字段。同组变体互斥；`default_visible: false` 且无互斥组的组件显示为可选附件开关。M7 旧版 `barrel_short / barrel_long / optic / foregrip` 兼容识别。`explode_direction` 为可选展示偏移，单位是最长边归一为 3 后的显示坐标，未提供时按语义名称或组件几何位置推算。此信息只描述艺术展示，不描述机械结构。

```json
{
  "schemaVersion": 1,
  "updatedAt": "2026-09-22",
  "models": [{
    "id": "m7",
    "name": "M7",
    "category": "战斗步枪",
    "description": "外观装饰模型。",
    "lengthMm": 300,
    "model": "/models/m7.glb",
    "preview": "/previews/m7.png",
    "downloads": {"print": "/downloads/m7-print.zip", "blend": "/downloads/m7.blend"},
    "status": {
      "geometry": {"state": "passed", "label": "网格验证通过", "detail": "说明验证范围。"},
      "slicing": {"state": "pending", "label": "未切片"},
      "physical": {"state": "pending", "label": "未实机打印"},
      "rights": {"state": "passed", "label": "发布者声明已取得非商业分享授权"}
    }
  }]
}
```

只有 `id / name` 是必要内容；模型和缩略图路径按约定补齐。下载链接必须显式提供；某个下载尚未准备好时，缺省该字段，或传 `downloads.print: null` / `downloads.blend: null`，对应链接会禁用。状态可用 `passed / pending / failed`；页面不会把缺失记录推断成通过。

## 代码模块

- `src/assembly.js`：识别逻辑组件、材质独立选中高亮、默认外观范围归一、变体/拆装/隐藏/单独查看、几何资源释放。
- `src/model-loader.js`：流式下载进度、请求取消、快速切换竞态处理，释放过期解析结果。
- `src/main.js`：目录和控件、灯光与相机、真实射线点击选件、错误恢复。
- `src/style.css`：桌面与移动端布局，不依赖远程字体。

每次切换释放上一模型的几何、材质与纹理，过期请求不能覆盖当前选中展品。颜色直接使用导出材质，不统一压黑木质或绿色外观。打印几何、切片检查、实机打印、发布权利分别显示。

## 参考文档

- [Three.js GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html)
- [Three.js OrbitControls](https://threejs.org/docs/pages/OrbitControls.html)
- [Three.js Material.dispose](https://threejs.org/docs/pages/Material.html#dispose)
- [Three.js BufferGeometry.dispose](https://threejs.org/docs/pages/BufferGeometry.html#dispose)

许可范围见仓库根目录：代码为 MIT，模型与缩略图等资产为仅限非商业使用的 CC BY-NC 4.0。游戏名称与商标不在这些许可证覆盖范围内。
