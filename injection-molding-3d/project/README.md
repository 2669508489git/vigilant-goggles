# 注塑成型全过程 · 瑞晨欣塑胶模具

交付规格：30 秒，1080×1920，30FPS，H.264 MP4。中文字幕，无配音，无音乐。

## 文件
- complete.mp4：动画、字幕、同步音效。
- silent.mp4：动画、字幕，无音频流。
- sound_effects.wav：30 秒立体声音效总轨，48kHz/16bit。
- motor / pellets / hydraulics / cooling_water / transitions.wav：同起点分轨。
- preview.mp4：检查用低分辨率、低采样率预览，不用于发布。
- project/injection.blend：可播放、可检查的三维场景。
- project/build.py：权威程序化模型、相机、工艺运动时间轴。
- project/finish.py：动态中文字幕、图形包装、音效生成与编码。
- project/bake.py：将脚本运动烘焙为 Blender 关键帧。

## 重建
需要 Blender 4.3+、FFmpeg 及 Python 3。安装 requirements.txt 后执行 `bash render.sh`。
`SCALE=25 STEP=10 FRAMES=/tmp/injection_preview/ blender -b -P build.py` 生成每十帧采样的270×480预览；对应编码帧率应为3。
最终渲染用 SCALE=100 STEP=1。音效合成使用固定随机种子，重复结果一致。
自定义输出根目录使用 OUT 环境变量；帧目录使用 FRAMES，必须以斜线结尾。

## 修改
- 六幕时长及文字：finish.py 中 chapters。主时间轴共900帧，需同步修改 build.py。
- 颜色、尺寸与零件：build.py 的材料和 cube/cyl/tube 构造。
- 运动：build.py 的 update；时间单位为秒，机器轴向为X，喷嘴位于X正方向。
- 注塑产品：电子外壳示意模型，包含边框和安装柱，可替换为实际CAD模型。
- 中文字体随项目附带 Noto Sans CJK，采用 SIL Open Font License 1.1。

## 工艺与表现范围
本片为程序化三维剖面科普示意，结构和行程经过简化，不作为制造图纸或工艺参数依据。
螺杆采用连续右旋螺旋叶片；在X轴正向为输送方向的坐标系下，塑化旋转角随时间减小，使螺旋推进方向指向喷嘴；塑化时旋转并随熔体积聚后退；注射时停止旋转并轴向前进。
0–22秒模具闭合；22–23.8秒动模后移；24.2秒起顶针向开模空间顶出，产品随动模先移动再脱离。
16–17秒短暂保压，17秒后冷却变色；可视化水路位于模具剖切侧，成型件与水路不相交。
料筒和模具使用开剖结构使内部可见，剖开的视窗不表示实际生产中模具敞开。
熔体使用几何增长、颗粒和流向示意，不含CFD/黏弹性求解；冷却为加速演示。
音效为程序合成的机械质感、颗粒、液压、流水和短电子提示，未使用实机录音。
总轨峰值约−12.4 dBFS，保留后期配音混音余量。
Blender 场景烘焙采样约10Hz并线性插值；交付视频则由原始脚本逐帧计算并以30FPS渲染。

## 补充编辑资料
subtitles.srt 提供六幕简体中文静态字幕文本；动态字效以 finish.py 为准。
sound_cues.csv 列出独立音轨的有效时间段，所有WAV均从0秒起对齐，便于直接叠放。
mechanical_checks.json、media_checks.json、audio_checks.json 记录交付检查。
