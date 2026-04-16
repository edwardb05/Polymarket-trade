# Testing

Because Polymarket does not provide especially convenient access for this workflow, I initially funded the bot with a small amount of capital and recorded its live trades. I then used this Python script to measure how many hedges completed successfully and to visualise when failures were clustered over time.

## Performance Summary

| Metric | Count |
|---------------------|------:|
| Total markets | 491 |
| Successful hedges | 370 |
| Failed hedges | 121 |

These results show that the hedge completion rate was not high enough for the strategy to be reliably scalable. For the model to work consistently, successful hedges would likely need to account for well over 98% of trades, whereas the observed rate here was closer to 78%. Despite that, the realised PnL over the period was still positive at roughly $2.

In hindsight, some of the trades classified as "failed hedges" were still profitable because only one side filled, and that side happened to be the one that later resolved to $1. This suggests that while hedge completion was inconsistent, the strategy could still occasionally benefit from directional exposure. More broadly, the results reflect the limitations of the Polymarket API and order book during volatile periods.

## Timings of Failed Trades

![Performance Chart](hedgesVtime.png)

The chart shows that failed hedges were not evenly distributed over time. Instead, they appeared in clusters, with the most notable spike occurring on 26 March. Looking at Bitcoin's price action on that day, it fell by roughly 3.5%, which helps explain the behaviour: in strongly directional conditions, the `DOWN` token often never traded below $0.50, so both sides of the hedge could not be filled.

## Improvements

Reviewing these results suggests several ways the strategy could be improved. For the bot to work reliably, there needs to be sufficient order-book volume and relatively balanced short-term price action; otherwise, one leg is unlikely to fill.

One possible improvement would be to add a simple market regime filter based on recent Bitcoin price movement. For example, if Bitcoin has moved strongly in one direction over the previous two 5-minute intervals, the bot could avoid entering the next market, where the probability of completing both legs may be lower.
