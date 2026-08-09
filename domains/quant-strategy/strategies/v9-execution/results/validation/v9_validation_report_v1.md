# V9 Validation Report v1

- Generated: `2026-07-14 16:37:48.687885+00:00`
- Formal V9 weights unchanged.

## Experiment A: Panic-to-repair

```json
{
  "experiment": "A_panic_to_repair",
  "event_count": 175,
  "label_counts": {
    "normal": 3657,
    "post_drawdown_watch": 2582,
    "panic_to_repair": 175
  },
  "overlap_with_fear_stress_or_worse": 68,
  "forward_returns": {
    "1": {
      "n": 175,
      "spy_mean": -0.0005888944062986441,
      "qqq_mean": -0.0005131942706007113
    },
    "5": {
      "n": 175,
      "spy_mean": 0.0018330457636890137,
      "qqq_mean": 0.001517094717772935
    },
    "21": {
      "n": 175,
      "spy_mean": 0.01703402772413089,
      "qqq_mean": 0.02499452619097123
    },
    "63": {
      "n": 173,
      "spy_mean": 0.052757891134902646,
      "qqq_mean": 0.07677159865201655
    }
  },
  "authorizes_trade": false
}
```

## Experiment B: Slow vol overlay

```json
{
  "experiment": "B_slow_vol_overlay_126d",
  "sample_start": "2000-04-27",
  "sample_end": "2026-07-02",
  "by_cost": {
    "0.001": {
      "overlay_cagr": 0.0678505548363495,
      "baseline_cagr": 0.08332447994391501,
      "overlay_sharpe": 0.6078048271218772,
      "baseline_sharpe": 0.5137365136480627,
      "overlay_max_drawdown": -0.2998034776939337,
      "baseline_max_drawdown": -0.5518943663343292,
      "overlay_es5": -0.01811103509856156,
      "baseline_es5": -0.02887081632271272,
      "avg_scale": 0.7744987550213261,
      "turnover": 0.0029634532154359282
    },
    "0.002": {
      "overlay_cagr": 0.06705231525121413,
      "baseline_cagr": 0.08332447994391501,
      "overlay_sharpe": 0.6015311659375756,
      "baseline_sharpe": 0.5137365136480627,
      "overlay_max_drawdown": -0.30094081929778105,
      "baseline_max_drawdown": -0.5518943663343292,
      "overlay_es5": -0.01812273846925071,
      "baseline_es5": -0.02887081632271272,
      "avg_scale": 0.7744987550213261,
      "turnover": 0.0029634532154359282
    },
    "0.005": {
      "overlay_cagr": 0.06466101975731209,
      "baseline_cagr": 0.08332447994391501,
      "overlay_sharpe": 0.5827102951373103,
      "baseline_sharpe": 0.5137365136480627,
      "overlay_max_drawdown": -0.3043418450434985,
      "baseline_max_drawdown": -0.5518943663343292,
      "overlay_es5": -0.018157891588394235,
      "baseline_es5": -0.02887081632271272,
      "avg_scale": 0.7744987550213261,
      "turnover": 0.0029634532154359282
    }
  },
  "authorizes_trade": false,
  "note": "Inspected 2019-2025 is not a fresh OOS period for future parameter changes."
}
```

## Experiment C: WML comparator

```json
{
  "experiment": "C_wml_comparator",
  "authorizes_trade": false,
  "v9_is_not_wml": true,
  "event_count": 175,
  "status": "completed_with_wml_and_approx_legs",
  "wml_sample": {
    "start": "1926-11-03",
    "end": "2026-05-29",
    "n": 26152
  },
  "forward_returns": {
    "1": {
      "n": 175,
      "wml_mean": -0.002544571428571426,
      "spy_mean": -0.0005888944062986441,
      "qqq_mean": -0.0005131942706007113,
      "wml_skew_fullsample": -1.611151690735273
    },
    "5": {
      "n": 175,
      "wml_mean": -0.008354285714285689,
      "spy_mean": 0.0018330457636890137,
      "qqq_mean": 0.001517094717772935,
      "wml_skew_fullsample": -1.611151690735273
    },
    "21": {
      "n": 175,
      "wml_mean": -0.03219599999999994,
      "spy_mean": 0.01703402772413089,
      "qqq_mean": 0.02499452619097123,
      "wml_skew_fullsample": -1.611151690735273
    },
    "63": {
      "n": 173,
      "wml_mean": -0.04345664739884397,
      "spy_mean": 0.052757891134902646,
      "qqq_mean": 0.07677159865201655,
      "wml_skew_fullsample": -1.611151690735273
    }
  },
  "approx_legs_in_panic_to_repair": {
    "n": 135,
    "winner_leg_mean": 0.045984176189292555,
    "loser_leg_mean": 0.1844248505367185,
    "WML_approx_mean": -0.1384406743474259,
    "loser_outperforms_winner_share": 0.7111111111111111,
    "note": "Approx equal-weight decile legs from cached PIT/universe prices; not CRSP."
  }
}
```