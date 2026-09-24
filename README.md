# Delta Models · 游戏外观模型收藏馆

独立制作的三维外观模型收藏馆，使用 Three.js 展示 67 款非功能性缩比装饰模型。网页支持旋转、缩放、三角网格、外观组件拆装及可选配件切换。

本项目与《三角洲行动》游戏的运营方没有隶属或背书关系。游戏名称、商标和原始画面属于各自权利人。模型按视觉参考重新建造，不包含游戏原始网格、真实内部机构或可用武器接口。模型尚未完成实机打印验证。

## 使用许可

- 网站、建模脚本、配置及测试代码： [MIT](LICENSE)。
- GLB、PNG 预览图、Blender 母版、打印包和切片包等模型资产： [CC BY-NC 4.0](LICENSE-MODELS)。允许署名后下载、修改和再分发，**仅限非商业用途**；修改后再分发须标注改动。

非商业限制意味着模型资产不是符合开放源代码定义的“开源”资产。MIT 仅适用于代码，不覆盖模型、游戏商标或第三方权利。本仓库发布者表示已取得上述非商业分享授权；仓库未附独立的授权证明。

## 文件在哪里

- `web/public/models/`：67 款供网页展示的 GLB 模型。
- `web/public/previews/`：目录缩略图。
- `scripts/`、`config/`：建模、资源整理和验证代码。
- [model-pack-v1 发布包](https://github.com/badDevBuild/delta-models/releases/tag/model-pack-v1)：每款打印文件、P1S 切片工程和 Blender 可编辑母版，共 201 个下载文件。
- `release-assets.json`：发布包文件名、大小与 SHA-256，供下载后核对。

为让代码仓库易于克隆，约 4.5 GB 的完整打印与母版文件放在 GitHub Release，不重复提交进 Git 历史。网页生产构建会把下载链接指向该发布包；本地开发时可把这些文件放在 `web/public/downloads/`，沿用本地路径。

## 本地运行

需要 Node.js 22.12 或更新版本：

```sh
cd web
npm ci
npm run dev
```

打开 `http://127.0.0.1:5174/`。运行 `npm test` 检查模型目录与文件索引，`npm run build` 生成静态站点。

## Cloudflare Pages

连接本仓库后，将 Root directory 设为 `web`，Build command 设为 `npm run build`，Build output directory 设为 `dist`。项目是纯静态网页，不需要 Pages Functions。`web/.env.production` 规定下载文件的 GitHub Release 地址。

发布前应先确认 GitHub Release 的 201 个资产完整可访问，再部署网页；否则下载按钮会指向尚不存在的文件。
