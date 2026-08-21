# Economic edge path-attribution addendum

Status: frozen after the first aggregate decomposition showed that differing
whole-share counts can dominate a paired P&L delta, and before computing the
direct-versus-path totals. Research-only.

For every common RSR1/RSR2 trade:

- `direct_exit_effect_on_rsr1_shares = RSR1 shares × (RSR2 exit fill − RSR1 exit fill)`.
- `capital_path_and_sizing_residual = observed RSR2 P&L − observed RSR1 P&L − direct_exit_effect_on_rsr1_shares`.

Both variants make one final exit order per trade, so the paired direct effect
does not add a commission difference. The direct effect isolates only a changed
exit fill on the original RSR1 shares. The residual includes later NAV, whole-
share sizing and compounding effects; it must not be described as a direct
benefit of the profit-lock exit itself.

Report aggregate direct effect, aggregate residual, their shares of total
overlay P&L improvement, and the number of trades with a nonzero direct effect.
No rule or threshold changes are permitted.
