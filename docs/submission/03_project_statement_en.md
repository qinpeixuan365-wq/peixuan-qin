# Project statement (English)

Mitha Pani ("fresh water" in Bangla) helps smallholders in Shyamnagar, coastal southwest Bangladesh, decide when to sow Boro rice, which variety to grow and how much pond water to store before the rivers turn salty.

**Problem.** Upstream Ganges discharge is the main control of surface-water salinity along the Bangladesh coast (BWDB data from 86 stations, 1990–2019). Ordinary rice tolerates about 3 dS/m, while trials in Satkhira measured 8 to 16 dS/m. Early transplanting is the most effective adaptation, but farmers do not know how long fresh water will last. The 1996 Ganges Water Treaty, which governs dry-season sharing, expires on 12 December 2026.

**What the AI does.**

- **Fresh-water window.** It forecasts when Ganges flow at Hardinge Bridge will drop below its usual dry-season median. The forecast uses the 12 most similar of 29 dry seasons in GloFAS reanalysis since 1997, blended with conditional climatology. It gives a date, a conformal 80% interval and the chance that the flow drops at all, cross-checked against GloFAS's own 7-month ensemble.
- **Boro planner.** It works back from that date to sowing and transplanting dates for four BRRI varieties, flags salinity risk at flowering, and estimates the pond water needed after the window closes.
- **Pond budget.** A FAO-56 calculation sizes how much watermelon, sunflower, mung bean or Boro rice one pond can irrigate.
- **Weather and flood risks.** It flags heavy rain, heat and wind using Bangladesh Meteorological Department categories and the 51-member ECMWF ensemble.
- **Official observations.** It embeds the Flood Forecasting and Warning Centre's observed and 5-day forecast water levels. Hardinge Bridge levels corroborate the GloFAS recession, and coastal tide gauges within 10 cm of danger level trigger an embankment alert.
- **Interactive map.** A zoomable Sentinel-2 satellite map shows the river network and gauges; picking any field recomputes the local weather risks and pond budget.
- **Bangla outputs.** Bangla cards, SMS and mosque-loudspeaker scripts work from rule templates; an LLM can rewrite them, quoting only the numbers it is given.

**Validation.** In a leave-one-season-out backtest over 29 dry seasons (1998–2026), forecasts issued 15 days ahead missed by 2.3 days on average, against 4.5 days for climatology; at 30 and 60 days the errors were 4.1 and 3.7 days, against 5.2. The 80% intervals contained the actual date in 81–85% of seasons. The backtest reruns in the browser on every load, and `scripts/backtest.py` reproduces it offline. For the 2027 season the forecast issued on 19 October is 24 January (80% interval 19 January to 5 February); GloFAS's own ensemble median gives 29 January.

**Status.** A working single-file web app with live and replay modes, a guided tour and a planned 2027 Boro-season pilot. Demo: https://qinpeixuan365-wq.github.io/peixuan-qin/ . Code (MIT): https://github.com/qinpeixuan365-wq/peixuan-qin .
