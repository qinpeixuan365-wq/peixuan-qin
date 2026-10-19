# 数据说明

网页运行时直接从公开接口取数，不需要这个文件夹里的任何文件。这里放的是：网页内嵌数据的可读版本、复现用的样例，以及每份数据的来源和许可。

## 网页运行时调用的公开数据

| 数据 | 用途 | 来源 | 许可 |
| --- | --- | --- | --- |
| ERA5 再分析逐日天气（1985 年至今） | 甜水账本的常年蒸散和降雨、长期变化 | ECMWF，经 Open-Meteo Historical Weather API | CC BY 4.0 |
| 16 天数值预报 | 14 天天气风险、今日农事卡 | Open-Meteo Forecast API | CC BY 4.0 |
| ECMWF IFS 0.25° 51 成员集合预报 | 大雨概率 | Open-Meteo Ensemble API | CC BY 4.0 |
| GloFAS v4 逐日河流流量（1984 年至今）和 7 个月季节集合预报 | 甜水窗口预测、精确度保证 | 哥白尼应急管理服务，经 Open-Meteo Flood API | CC BY 4.0 |
| 地形高程（哥白尼 90 米 DEM） | 地图点选位置的海拔 | Open-Meteo Elevation API | CC BY 4.0 |
| Sentinel-2 cloudless 2024 卫星影像 | 地图卫星底图（只在浏览器里加载，不存储） | EOX IT Services GmbH，https://s2maps.eu | CC BY-NC-SA 4.0，仅限非商业用途 |

## 这个文件夹里的文件

| 文件 | 内容 | 来源 |
| --- | --- | --- |
| `ffwc_snapshot_2026-10-19.csv` | 6 个水文站的实测和 5 天预报水位（米，平均海平面以上），以及危险水位和历史最高水位 | 孟加拉洪水预报预警中心（FFWC，隶属孟加拉水利发展局），http://old.ffwc.gov.bd/ffwc_charts/waterlevelfcast.php 和 waterlevelobs.php，2026 年 10 月 19 日抄录。FFWC 官方 API 需注册（api.support@bwdb.gov.bd），正式版接入后每天同步 |
| `boro_varieties.csv` | 博罗稻排期用的 4 个品种的生育期和耐盐性 | 孟加拉水稻研究所（BRRI）年度成果报告、PLOS ONE 2024、CGIAR、萨德基拉农业推广局 |
| `crop_kc_fao56.csv` | 甜水账本用的作物系数和生育期 | 联合国粮农组织 FAO-56（《作物蒸散量》）表 11、12，按当地播种期调整 |
| `risk_thresholds.csv` | 暴雨、高温、大风、连续无雨和潮水的风险分级 | 孟加拉气象局（BMD）分级、蒲福风级、FFWC 危险水位 |
| `basemap_natural_earth.geojson` | 地图底图：孟加拉国和印度国界、恒河三角洲河网（已裁剪、简化并分类） | Natural Earth 1:10m，公有领域；由 `scripts/build_basemap.py` 生成 |

## 复现用的完整数据

`mitha-pani-data-2026-10-19.json` 是 2026 年 10 月 19 日从网页导出的真实数据：恒河 GloFAS 逐日流量和 7 个月集合预报、逐日天气、FFWC 快照和回测结果。注意导出时天气取点是地图上选的位置（北纬 23.39°，东经 89.77°），回测只用流量，不受影响。


在网页底部点“下载本页使用的数据（JSON）”，会导出当天网页实际用到的全部天气和流量数据、GloFAS 季节预报、FFWC 快照和回测结果。把这个文件放进本文件夹，就可以用 `scripts/backtest.py` 离线复现“精确度保证”里的全部数字。

## 没有用、以及为什么

- 河道实测盐度：孟加拉水利发展局有 86 个站的长期记录，但数据属于孟加拉政府，目前不公开，只能申请。所以网页预测的是公开可得的上游驱动因子（恒河来水），试点时再用实测盐度标定。
- 卫星盐度反演：孟加拉沿海的研究显示，9 种卫星盐度指数和实测土壤电导率几乎不相关（R² 最高约 0.02，Land 2022），不足以准确判断盐度。
- GADM 行政边界：许可不允许再分发，所以底图只用公有领域的 Natural Earth。
- 人道主义数据交换（HDX）和孟加拉开放数据平台（data.gov.bd）：都查过，暂时没有公开的河道盐度时间序列。
