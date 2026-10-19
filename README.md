# 甜水日历 Mitha Pani（মিঠা পানি）：孟加拉沿海农户的盐水与洪水助手

AI4Climate 全球青年气候解决方案挑战赛 2026 参赛作品
赛道 03：孟加拉沿海复合盐碱与洪水风险区的气候智慧农业

- 在线演示：https://qinpeixuan365-wq.github.io/peixuan-qin/ （打开后点右上角“3 分钟导览”）
- 代码、数据和技术报告：https://github.com/qinpeixuan365-wq/peixuan-qin
- 演示视频：（提交时替换成你的视频链接）

## 一句话

甜水日历预测恒河上游来水今年何时跌破“旱季常年中位流量”，倒推博罗稻（旱季稻）的落谷和插秧日期，算清自家池塘的水够种什么，再用孟加拉语的农事卡、短信和清真寺喇叭广播稿把建议送到农户手里。

## 要解决的问题

萨德基拉县 Shyamnagar 紧邻孙德尔本斯。旱季的淡水主要靠恒河上游来水顶住海水；孟加拉水利发展局 86 个站 1990 到 2019 年的实测表明，沿海地表水盐度的变化主要由流入三角洲的河流流量控制（Haq 等，2024）。

普通水稻的耐盐上限约 3 dS/m，萨德基拉的田间试验里盐度可达 8 到 16 dS/m。土壤资源发展研究所（SRDI）的调查显示，1973 到 2009 年 Shyamnagar 等地的土壤盐度几乎翻倍，从 2.8–18.5 dS/m 升到 4.0–42.8 dS/m。研究表明提早插秧是应对盐害最有效的办法，但农户不知道今年的甜水能用到哪天。

规定旱季分水的 1996 年《恒河分水条约》将于 2026 年 12 月 12 日到期，2027 年旱季的上游来水比以往更难预料。

## 功能

- **今日农事卡**：中文、英文、孟加拉语都有规则模板，不依赖网络 AI；可以用 AI 重写、语音播报、生成 WhatsApp 图片，还有孟加拉语短信和清真寺喇叭广播稿（附中文对照）。
- **河网地图**：用 Natural Earth 的真实国界、海岸线和恒河三角洲河网，讲清甜水从哪来、咸水从哪进。从哈丁桥到戈拉伊河口，再到西南感潮河网和 Shyamnagar；水文站按 FFWC 当天数据着色，点击任一站点，右侧会讲它和农户决策的关系。地图基于 Leaflet，可以随意缩放、拖动，默认显示 Sentinel-2 无云卫星影像，放大能看清虾塘和田块；点右侧条目会自动飞到对应地点。在地图上任意点一下或拖动“田”字图钉，可以查看那里离哈丁桥多远、最近的潮位站和海拔，并一键按这个位置重新计算天气、风险和甜水账本（链接里会带上位置，方便分享）。影像或地图组件加载失败时，自动退回静态示意地图。
- **甜水窗口**：预测跌破日、八成区间和“今年会不会跌破”的概率，同时显示 GloFAS 7 个月集合预报做独立对照，画在孟加拉历旱季尺上。
- **博罗稻排期**：由甜水窗口倒推 BRRI dhan67、97、99 和 dhan28 的插秧、开花、收获日期，给出盐害风险和窗口关闭后需要的池塘水量。
- **甜水账本**：按 FAO-56 方法，算出一池甜水能浇多少西瓜、向日葵、绿豆或博罗稻。
- **FFWC 官方水位**：放入孟加拉洪水预报预警中心发布的哈丁桥、戈拉伊河口和沿海潮位站的实测与 5 天预报。实测水位用来印证 GloFAS 的退水趋势；潮位离危险水位 10 厘米以内时，今日卡片会提醒检查堤坝和闸门。
- **14 天天气风险**：按孟加拉气象局分级判断，叠加 ECMWF 51 成员的大雨概率。
- **精确度保证**：1997 年以来 29 个完整旱季的逐年回测，网页打开时现场重算；`scripts/backtest.py` 用导出的数据离线复现，结果与网页逐项一致（见下方“检验结果”）。
- **长期变化与历史回放**：包括最近一季、最早告急、最枯一季，以及气旋 Aila、Amphan、Remal 来临前。
- **落地计划、问答和数据导出**：落地计划是 2027 年博罗季试点；问答支持三种语言，AI 连不上时由规则引擎回答；可下载本页使用的全部数据（JSON）。

## 方法

**数据**
- 天气：ERA5（1985 年至今）、16 天预报、ECMWF IFS 0.25° 集合预报，均经 Open-Meteo 获取。
- 流量：GloFAS v4 河流流量（接口从 1984 年起提供；哈丁桥附近这个格点 1997 年起才有完整数据），加 7 个月季节集合预报。网页会在哈丁桥周围的 GloFAS 网格中自动找出雨季流量最大的格点，即恒河主河道。
- 官方水位：孟加拉洪水预报预警中心（FFWC，隶属孟加拉水利发展局）的实测和 5 天预报水位，目前为 2026 年 10 月 19 日发布的快照（来源：old.ffwc.gov.bd）。FFWC 官方 API 需注册（api.support@bwdb.gov.bd），正式版接入后每天同步。
- 另查阅了人道主义数据交换（HDX）和孟加拉开放数据平台（data.gov.bd）：前者以行政区划和灾害影响数据为主，后者的 FFWC 条目指向同一网站，暂无公开的河道盐度时间序列。

**甜水窗口**
- **阈值**：旱季常年中位流量，即 1991–2020 年 1–5 月 7 天平均流量的中位数。
- **定义**：每个旱季（10 月 1 日至次年 6 月 30 日）第一次跌破这条线的日子。整季不跌破的年份作为一种结果计入概率。
- **预测**：用相似年份法。挑出同一天来水和两周前来水最接近今年的 12 个历史旱季，按今年流量微调后推演；跌破比例即跌破概率。跌破日中位数与“同一天尚未跌破的年份”的跌破日中位数各占一半合成，权重和年份数都事先固定。区间由历年同一时间点的实际误差确定（共形预测）。
- **检验**：每个旱季轮流当考题，在跌破前 120、90、60、30、15 天发布预测，与“照往年经验”比较。

**博罗稻排期**
- 生育期取 BRRI 公布值：dhan67 约 145 天，dhan97 约 152 天，dhan99 约 154 天，dhan28 约 145 天。
- 插秧 = 落谷 + 秧龄；开花约在收获前 30 天，生殖期约 35 天。
- 来水跌破后，咸水上溯到田间按 50 天估计：按 GloFAS 的典型跌破日（1 月中下旬）倒推，这能让推荐插秧期落在 BRRI 试验产量最高的 12 月中下旬；试点时用实测盐度标定。不耐盐的 dhan28 按窗口关闭日从严判断。
- 咸水上溯以后的灌溉按全部改用池塘水估算（FAO-56，另加每天 3 毫米渗漏）。

**大模型**
- 默认 DeepSeek，也可用智谱等兼容 OpenAI 格式的接口；不可用时走 Pollinations 免费体验通道，再不行用规则模板。
- 大模型只负责翻译、短信、广播稿和问答，提示词限定只能引用给定数据。

**实现**：单个 HTML 文件，原生 JavaScript 加 SVG 和 Canvas；只有交互地图按需加载开源的 Leaflet 1.9.4（BSD-2，cdnjs，备用 jsDelivr），加载不了就用内置的静态地图。海拔来自 Open-Meteo 地形接口（哥白尼 90 米地形数据）。

## 检验结果（2026 年 10 月 19 日真实数据）

恒河哈丁桥附近 GloFAS 格点（北纬 23.92°，东经 89.18°），1997 年以来 29 个完整旱季，其中 26 个跌破过旱季常年中位流量（约 1930 立方米/秒）。每个旱季轮流当考题，只用其余年份的经验发布预测：

| 发布时间 | 甜水日历平均误差 | 照往年经验 | 误差减少 | 八成区间命中 |
| --- | --- | --- | --- | --- |
| 提前 90 天 | 5.0 天 | 5.1 天 | 2% | 21/25（84%） |
| 提前 60 天 | 3.7 天 | 5.2 天 | 29% | 21/26（81%） |
| 提前 30 天 | 4.1 天 | 5.2 天 | 22% | 22/26（85%） |
| 提前 15 天 | 2.3 天 | 4.5 天 | 48% | 22/26（85%） |

跌破日每年都在 1 月 13 日到 2 月 5 日之间（标准差约 6 天），所以照往年经验本身就不差；模型的优势越临近越明显。提前 120 天没有样本，因为那时还没进入旱季。

2027 年旱季的预测（10 月 19 日发布）：1 月 24 日前后跌破，八成把握在 1 月 19 日到 2 月 5 日之间，跌破概率 92%；GloFAS 7 个月集合预报的中位线为 1 月 29 日。由此倒推，BRRI dhan67 最晚 11 月 20 日落谷、12 月 30 日插秧。回放上一季：2025 年 12 月 1 日发布的预测为 1 月 25 日（1 月 22 日到 2 月 4 日），实际为 1 月 30 日。

官方实测对照：FFWC 实测哈丁桥水位 10 月 13 日到 19 日下降 0.97 米，同期 GloFAS 模拟流量下降 29%，方向一致。

复现：`python scripts/backtest.py data/mitha-pani-data-2026-10-19.json`

## 使用边界

- GloFAS 是模拟流量，不是实测。哈丁桥来水只是咸淡水的上游控制因素之一，潮汐、圩田闸门、当地降雨和虾塘取水同样重要。
- 咸水上溯缓冲期（50 天）是估计值，需要用孟加拉水利发展局（BWDB）的实测盐度标定。
- 模型只依据历年流量规律，无法预见条约或上游调度的变化；这里只描述流量统计，不评价两国的水资源安排。
- 卫星影像用来看清河网、虾塘、稻田和红树林的真实分布，不用于判断盐度。孟加拉沿海的研究显示，卫星盐度指数和实测土壤电导率几乎不相关（R² 最高约 0.02，Land 2022），所以盐度要靠实测。
- 本工具只做辅助决策，不替代孟加拉气象局（BMD）警报和备灾计划（CPP）的撤离通知。品种选择请咨询当地农技员（SAAO）。
- 页面不收集个人信息，AI Key 只保存在用户浏览器里。

## 主要依据

- Haq et al. (2024). What drives changes in surface water salinity in coastal Bangladesh? Frontiers in Water.
- Adapting to salinity in coastal rice farming (2025). npj Climate Action.
- Options for increasing Boro rice production in the saline coastal zone of Bangladesh (2021). Field Crops Research.
- Developing climate-resilient rice varieties (BRRI dhan97 and BRRI dhan99) (2024). PLOS ONE.
- BRRI Research Achievements 2014–15 和 2020–21（BRRI dhan67、dhan99 的生育期，插秧期试验）。
- Open-Meteo Flood API（GloFAS v4）；The Business Standard 关于《恒河分水条约》的报道。
- 孟加拉洪水预报预警中心（FFWC）实测和预报水位表；SRDI 研究人员（2023）的孟加拉沿海土壤盐度管理综述。

## English summary

Mitha Pani ("fresh water") helps smallholders in Shyamnagar, coastal southwest Bangladesh, plan the dry season.

- **Fresh-water window.** It forecasts when Ganges flow at Hardinge Bridge will drop below its usual dry-season median, which is when salt water starts pushing up the southwest rivers. The forecast comes from the 12 most similar historical seasons in GloFAS reanalysis since 1997, blended with conditional climatology, with conformal intervals and a probability that the flow drops at all. A leave-one-season-out backtest over 29 dry seasons (1998–2026) reruns in the browser: 15 days ahead the mean error is 2.3 days against 4.5 days for climatology, and the 80% intervals contain the actual date in 81–85% of seasons.
- **Boro planner.** From that date it works back to sowing and transplanting dates for four BRRI varieties and estimates the pond water needed after the window closes.
- **Pond budget.** It sizes how much watermelon, sunflower, mung bean or Boro rice one pond can irrigate, using FAO-56.
- **Bangla outputs.** Rule-based Bangla cards, SMS and mosque-loudspeaker scripts work without AI; an LLM can rewrite them.

## 许可与说明

- 代码：MIT License
- 数据：Open-Meteo.com（CC BY 4.0），含 ECMWF ERA5、IFS 集合预报和哥白尼 GloFAS；底图：Natural Earth（公有领域）；卫星影像：Sentinel-2 cloudless 2024 by EOX IT Services GmbH（https://s2maps.eu，含经处理的哥白尼 Sentinel 数据，CC BY-NC-SA 4.0，仅限非商业用途，商业化时需更换影像源）；官方水位：孟加拉洪水预报预警中心（FFWC）
- 开发过程中使用了 AI 编程助手（Claude）辅助编写代码、做数据分析和撰写文档。

## 仓库结构

| 路径 | 内容 |
| --- | --- |
| `index.html` | 网页本身，单个文件，打开即用 |
| `REPORT.md` | 技术报告：问题、数据、方法、精确度保证、局限和落地计划 |
| `data/` | 2026 年 10 月 19 日导出的真实数据、FFWC 官方水位快照、品种和作物系数表、风险阈值、地图底图，以及每份数据的来源和许可 |
| `scripts/` | `backtest.py` 离线复现精确度保证；`build_basemap.py` 从 Natural Earth 生成地图底图 |
| `docs/submission/` | 报名表文字、英文说明、视频脚本、社区帖和答辩准备 |
| `docs/screenshots/` | 网页截图 |

