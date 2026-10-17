# 开发一款塑胶产品，到底有多难？

Remotion + React + TypeScript 原生矢量动画。900 × 1200（3:4），30 fps，1800 帧，60 秒。纯黑、金黄、白色；无人物、图片、3D 或音频。

## 使用

```bash
npm ci
npm run dev
npm run typecheck
npm run test:render  # 先输出前 300 帧 / 10 秒
npm run render      # 再输出完整 1800 帧 / 60 秒
```

渲染命令启用 SwANGLE 软件图形后端，并逐帧刷新固定界面文字，避免长序列中浏览器缓存造成的漏绘。

此环境 Chromium 路径为 `/usr/bin/chromium`。其他机器请把 package.json 渲染命令中的 `--browser-executable` 改为本机浏览器路径，或移除这个参数并使用 Remotion 的浏览器安装流程。需要 Node.js 18+。安装命令请在项目根目录执行。

- `out/test-10s.mp4`：10 秒测试片。
- `out/plastic-product-60s.mp4`：完整无声成片，H.264 / 4:2:0 / CRF 16。
- `src/Root.tsx`：全部分镜、文字、SVG 图形和帧驱动动画。
- `src/style.css`：版式、颜色和字体样式。
- `public/MotionCJK-Regular.otf`：随项目打包的简体中文字体子集；许可证见同目录文件。
- `STORYBOARD.md`：时间轴、节拍和知识边界。

所有动画由帧号确定，可精确跳帧复现，不依赖 CSS animation、随机数、网络或音频。`--muted` 明确禁用音轨。`out` 与 `node_modules` 已忽略，不提交大型生成文件。

## 修改方式

`descriptions` 定义各阶段标题和结论，`beats` 定义每 2 秒一个的动作提示。`Concept` / `FunctionDiagram` / `Structure` / `Mold` / `Trial` / `Production` 是六个独立可编辑 SVG 场景。`Root` 中设置尺寸、帧率和总帧数。

字体子集已覆盖现有全部文案。增加新汉字时，需使用完整的 Noto Sans CJK SC 字体，或重新生成子集，避免依赖系统字体补字。当前字体来自 Noto Sans CJK，采用 SIL Open Font License；子集使用新的字体文件名。

项目在独立云任务的现有检出目录中开发，无需创建额外 Git worktree。

## 浏览器下载成片

交付文件位于 [`delivery/`](delivery/README.md)。在 GitHub 中打开 MP4 或源码 ZIP 文件页面，点击右上角 **Download raw file** 下载。
