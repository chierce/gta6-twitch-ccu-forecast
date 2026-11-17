# GTA VI Launch-Day Twitch CCU Forecast Engine

[![make.fun · gta6-twitch-ccu-forecast-01](https://make.fun/badge/gta6-twitch-ccu-forecast-01.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)
[![rank](https://make.fun/badge/gta6-twitch-ccu-forecast-01/chierce/gta6-twitch-ccu-forecast/rank.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)
[![reward](https://make.fun/badge/gta6-twitch-ccu-forecast-01/chierce/gta6-twitch-ccu-forecast/reward.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)

An empirical log-normal quantile forecasting engine for Grand Theft Auto VI launch-day Twitch concurrent viewership (CCU), built for [make.fun](https://make.fun/bounty/gta6-twitch-ccu-forecast-01).

## Methodology & Architecture

1. **Diurnal Log-Ratio Curve**: GTA VI unlocks rolling midnight by country (UK at 00:00 UTC, US East Coast at 05:00 UTC, US West Coast at 08:00 UTC). Rather than assuming static persistence, the model fits a robust log-ratio trajectory derived from historical AAA console launches.
2. **Proper Pinball Loss Quantiles**: Evaluates the exact pinball loss metric at quantiles $\tau \in \{0.05, 0.25, 0.50, 0.75, 0.95\}$ in log space:
   $$q_\tau(h) = p_1 \cdot r_h \cdot \exp(z_\tau \cdot s_h)$$
3. **Monotonicity & Robustness**: Enforces strict quantile ordering $q_{05} \le q_{25} \le q_{50} \le q_{75} \le q_{95}$ with adaptive dispersion bounds.

## License

[MIT](LICENSE)
