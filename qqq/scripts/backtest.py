#!/usr/bin/env python3
"""
甜水日历 Mitha Pani：离线复现“精确度保证”（甜水窗口逐年回测）

用法：
    python scripts/backtest.py data/mitha-pani-data-YYYY-MM-DD.json

输入是网页底部“下载本页使用的数据（JSON）”导出的文件，里面有恒河哈丁桥的
GloFAS 逐日模拟流量。本脚本按网页里完全相同的方法重算：

1. 7 天滑动平均流量 q7（窗口内至少 5 天有值）；
2. 旱季常年中位流量 QL = 1991–2020 年 1–5 月 q7 的中位数；
3. 每个旱季（10 月 1 日到次年 6 月 30 日，共 273 天）第一次 q7 < QL 的日子 = 甜水窗口关闭日；
4. 相似年份法：挑出同一天来水（和两周前来水）最接近的 12 个历史旱季，按比例微调后推演；
   跌破日中位数与“同一天还没跌破的年份”的跌破日中位数各占一半（权重事先固定）；
5. 共形预测区间：用其余年份在同一提前量下的实际误差的 10% 和 90% 分位数；
6. 每个旱季轮流当考题（留一法），在跌破前 120、90、60、30、15 天发布预测。

只依赖 numpy。
"""
import json, math, sys, datetime as dt
import numpy as np

SEASON_LEN = 273
K_ANALOG = 12
BLEND_W = 0.5
LEADS = [120, 90, 60, 30, 15]


def quant(sorted_vals, q):
    n = len(sorted_vals)
    if n == 0:
        return None
    pos = (n - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


def load(path):
    d = json.load(open(path, encoding="utf-8"))
    dis = d["discharge"]
    start = dt.date.fromisoformat(dis["start"])
    q = [None if v is None else float(v) for v in dis["q"]]
    src = dis.get("src") or [1] * len(q)
    gen = d.get("generated", "")[:10]
    today = dt.date.fromisoformat(gen) if gen else start + dt.timedelta(len(q) - 1)
    hist_end = None
    for j in range(len(q) - 1, -1, -1):
        if src[j] in (1, 3) and q[j] is not None and start + dt.timedelta(j) <= today:
            hist_end = j
            break
    return start, q, hist_end


def q7_series(q):
    out = [None] * len(q)
    for j in range(len(q)):
        w = [v for v in q[max(0, j - 6): j + 1] if v is not None]
        if len(w) >= 5:
            out[j] = sum(w) / len(w)
    return out


def main(path):
    start, q, hist_end = load(path)
    q7 = q7_series(q)
    idx = lambda d: (d - start).days
    val = lambda d: q7[idx(d)] if 0 <= idx(d) < len(q7) and idx(d) <= hist_end else None

    jm = [val(dt.date(y, 1, 1) + dt.timedelta(i)) for y in range(1991, 2021) for i in range((dt.date(y, 5, 31) - dt.date(y, 1, 1)).days + 1)]
    jm = sorted(v for v in jm if v is not None)
    QL = quant(jm, 0.5)
    yrs = sorted({y for y in range(1991, 2021) if any(val(dt.date(y, 1, 1) + dt.timedelta(i)) is not None for i in range(151))})
    print(f"旱季常年中位流量 QL = {QL:.0f} 立方米/秒（1991–2020 年中有数据的 {yrs[0]}–{yrs[-1]} 年，1–5 月 7 天平均流量的中位数，样本 {len(jm)} 天）")

    end_date = start + dt.timedelta(hist_end)
    seasons = {}
    first_s = start.year + 1
    last_s = end_date.year + (1 if end_date.month >= 7 else 0)
    for S in range(first_s, last_s + 1):
        s0 = dt.date(S - 1, 10, 1)
        arr = np.full(SEASON_LEN, np.nan)
        miss = 0
        for k in range(SEASON_LEN):
            v = val(s0 + dt.timedelta(k))
            if v is None:
                miss += 1
            else:
                arr[k] = v
        cross = None
        below = np.where(arr < QL)[0]
        if len(below):
            cross = int(below[0])
        complete = miss < 15 and idx(s0 + dt.timedelta(SEASON_LEN - 1)) <= hist_end
        seasons[S] = dict(arr=arr, cross=cross, complete=complete)
    allS = [S for S in sorted(seasons) if seasons[S]["complete"]]
    print(f"完整旱季 {len(allS)} 个，其中跌破过中位流量的 {sum(1 for S in allS if seasons[S]['cross'] is not None)} 个")

    def analog(k, q_now, pool, q_prev):
        cand = []
        for z in pool:
            az = seasons[z]["arr"]
            base = az[k]
            if not (base > 0):
                continue
            d = abs(math.log(base / q_now))
            if q_prev is not None and q_prev > 0 and k >= 14 and az[k - 14] > 0:
                d += 0.5 * abs(math.log(az[k - 14] / q_prev))
            cand.append((d, z))
        if not cand:
            return None
        cand.sort(key=lambda t: t[0])  # 稳定排序，与网页一致
        use = [z for _, z in cand[:min(K_ANALOG, len(cand))]]
        hits = []
        for z in use:
            az = seasons[z]["arr"]
            thr = QL * az[k] / q_now
            seg = az[k + 1:]
            hit = np.where(seg < thr)[0]
            if len(hit):
                hits.append(k + 1 + int(hit[0]))
        hits.sort()
        return dict(hit_med=quant(hits, 0.5) if hits else None, p_cross=len(hits) / len(use))

    def cond_prior(k, pool):
        c = sorted(seasons[z]["cross"] for z in pool if seasons[z]["cross"] is not None and seasons[z]["cross"] > k)
        return quant(c, 0.5) if c else None

    def blended(k, q_now, pool, q_prev):
        m = analog(k, q_now, pool, q_prev)
        if m is None:
            return None
        prior = cond_prior(k, pool)
        if m["hit_med"] is None or prior is None:
            return dict(p=None, prior=prior)
        return dict(p=BLEND_W * m["hit_med"] + (1 - BLEND_W) * prior, prior=prior)

    rows = []
    for L in LEADS:
        err, naive, cov, n = [], [], 0, 0
        for y in allS:
            c = seasons[y]["cross"]
            if c is None:
                continue
            pool = [z for z in allS if z != y]
            ay = seasons[y]["arr"]
            k = c - L
            if k < 0 or not (ay[k] >= QL):
                continue
            r = blended(k, ay[k], pool, ay[k - 14] if k >= 14 else None)
            if r is None or r["p"] is None:
                continue
            res = []
            for z in pool:
                cz = seasons[z]["cross"]
                if cz is None:
                    continue
                kz = cz - L
                az = seasons[z]["arr"]
                if kz < 0 or not (az[kz] >= QL):
                    continue
                rz = blended(kz, az[kz], [u for u in pool if u != z], az[kz - 14] if kz >= 14 else None)
                if rz is not None and rz["p"] is not None:
                    res.append(rz["p"] - cz)
            if len(res) < 5:
                continue
            res.sort()
            lo, hi = r["p"] - quant(res, 0.9), r["p"] - quant(res, 0.1)
            err.append(r["p"] - c)
            naive.append(r["prior"] - c)
            n += 1
            if lo - 0.5 <= c <= hi + 0.5:
                cov += 1
        mae = sum(abs(e) for e in err) / n if n else float("nan")
        nmae = sum(abs(e) for e in naive) / n if n else float("nan")
        rows.append((L, n, mae, nmae, cov))
    print()
    print("| 提前量 | 旱季数 | 甜水日历平均误差（天） | 照往年经验（天） | 误差减少 | 八成区间命中 |")
    print("|---|---|---|---|---|---|")
    for L, n, mae, nmae, cov in rows:
        if n == 0:
            print(f"| {L} 天 | 0 | 无样本 | 无样本 | — | — |")
            continue
        gain = (1 - mae / nmae) * 100 if nmae else float("nan")
        print(f"| {L} 天 | {n} | {mae:.1f} | {nmae:.1f} | {gain:.0f}% | {cov}/{n}（{cov / n * 100:.0f}%） |")
    return rows


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
