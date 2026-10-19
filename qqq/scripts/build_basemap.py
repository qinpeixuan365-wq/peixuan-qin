#!/usr/bin/env python3
"""
甜水日历 Mitha Pani：从 Natural Earth 原始数据生成地图底图

用法：
    pip install shapely
    python scripts/build_basemap.py            # 输出 data/basemap_natural_earth.geojson

数据：Natural Earth 1:10m 国界（admin_0_countries）和河流中心线（rivers_lake_centerlines），公有领域。
Natural Earth 里的 “Ganges” 要素包含恒河三角洲的几条主要支流，本脚本按起止点把它们分成：
  major  恒河主河道（含博多河）和贾木纳河
  gorai  戈拉伊河—马杜马蒂河（西南地区淡水的主通道）
  sw     西南沿海感潮河网（流向孙德尔本斯）
  minor  其他（印度境内的胡格利河等）
网页里的静态地图另外用墨卡托投影（第 9 级）把这些坐标换算成了 SVG 坐标，方法见 project() 函数。
"""
import json, math, os, urllib.request
from shapely.geometry import shape, box

NE = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'
FILES = ['ne_10m_admin_0_countries.geojson', 'ne_10m_rivers_lake_centerlines.geojson']
BB = box(87.6, 21.2, 90.9, 24.9)
CACHE = os.path.join(os.path.dirname(__file__), '.ne_cache')


def fetch(name):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        print('下载', name); urllib.request.urlretrieve(NE + name, p)
    return json.load(open(p, encoding='utf-8'))


def polys(g):
    if g.is_empty: return []
    if g.geom_type == 'Polygon': return [g]
    return [p for p in getattr(g, 'geoms', []) if p.geom_type == 'Polygon']


def project(lon, lat, z=9, x0=None, y0=None, f=1.0):
    """墨卡托投影（网络地图通用，EPSG:3857）下的像素坐标，用于和卫星瓦片对齐"""
    world = 256 * 2 ** z
    x = (lon + 180) / 360 * world
    r = math.radians(lat)
    y = (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * world
    return ((x - (x0 or 0)) * f, (y - (y0 or 0)) * f)


def main():
    R = lambda c: [round(c[0], 4), round(c[1], 4)]
    feats = []
    for f in fetch(FILES[0])['features']:
        nm = f['properties'].get('ADMIN')
        if nm not in ('Bangladesh', 'India'): continue
        g = shape(f['geometry']).intersection(BB).simplify(0.002, preserve_topology=True)
        coords = [[[R(q) for q in p.exterior.coords]] + [[R(q) for q in i.coords] for i in p.interiors] for p in polys(g)]
        feats.append({'type': 'Feature', 'properties': {'name': nm, 'layer': 'country'}, 'geometry': {'type': 'MultiPolygon', 'coordinates': coords}})
    for f in fetch(FILES[1])['features']:
        nm = f['properties'].get('name')
        if nm not in ('Ganges', 'Brahmaputra'): continue
        gg = shape(f['geometry']).intersection(BB)
        parts = [gg] if gg.geom_type == 'LineString' else list(getattr(gg, 'geoms', []))
        for p in parts:
            if len(p.coords) < 3: continue
            st = (round(p.coords[0][0], 2), round(p.coords[0][1], 2)); en = (round(p.coords[-1][0], 2), round(p.coords[-1][1], 2))
            ys = [q[1] for q in p.coords]
            k = 'minor'
            if nm == 'Brahmaputra': k = 'major'
            elif en == (89.09, 23.98) and min(ys) >= 23.97: k = 'major'
            elif (st, en) == ((89.09, 23.98), (89.75, 23.85)): k = 'major'
            elif (st, en) == ((89.09, 23.98), (90.01, 22.49)): k = 'gorai'
            elif (st, en) in [((89.29, 22.6), (89.35, 21.97)), ((89.48, 22.3), (89.29, 22.6)), ((88.41, 22.95), (89.06, 22.13))] or en == (89.29, 22.6): k = 'sw'
            feats.append({'type': 'Feature', 'properties': {'layer': 'river', 'class': k}, 'geometry': {'type': 'LineString', 'coordinates': [R(q) for q in p.simplify(0.0015).coords]}})
    out = os.path.join(os.path.dirname(__file__), '..', 'data', 'basemap_natural_earth.geojson')
    json.dump({'type': 'FeatureCollection', 'name': 'mitha_pani_basemap', 'features': feats}, open(out, 'w'), separators=(',', ':'))
    print('写出', os.path.normpath(out), len(feats), '个要素')


if __name__ == '__main__':
    main()
