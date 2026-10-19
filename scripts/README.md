# 脚本说明

| 脚本 | 作用 | 依赖 |
| --- | --- | --- |
| `backtest.py` | 用网页导出的数据离线复现“精确度保证”：约 40 个旱季逐年回测，提前 120、90、60、30、15 天的平均误差、照往年经验的误差和八成区间命中率 | numpy |
| `build_basemap.py` | 从 Natural Earth 原始数据生成地图底图（裁剪、简化、给河段分类） | shapely |

```bash
pip install -r scripts/requirements.txt
python scripts/backtest.py data/mitha-pani-data-2026-10-19.json
python scripts/build_basemap.py
```

`backtest.py` 与网页里的 JavaScript 实现逐行对应（同样的 7 天滑动平均、同样的 12 个相似年份、同样固定的 50/50 权重、同样的共形区间），对同一份数据两边算出的数字完全一致。
