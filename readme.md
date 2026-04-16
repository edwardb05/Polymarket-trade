# Polymarket Arbitrage Bot

This is a proof-of-concept trading bot designed to exploit inefficiencies in Polymarket's 5-minute crypto markets.

## Theory

The idea behind this bot is that Polymarket's BTC markets can become very volatile, especially in the final minutes before a time slot opens. For example, in a market such as "Bitcoin Up or Down - April 09, 9:50AM-9:55AM", prices can briefly trade on either side of $0.50 around 9:48AM. Because the market ultimately resolves to $1 for the correct outcome, filling both legs at $0.49 creates a small edge of 2%.

If this opportunity occurs every 5 minutes with $2.50 allocated to both `UP` and `DOWN`, the strategy can produce a modest hourly return. While the absolute profit is small, it is enough to serve as a useful proof of concept. In addition, placing limit orders at $0.49 adds liquidity to the order book, which may also benefit from Polymarket's maker rebate program, where a portion of daily volume is returned to traders who add liquidity.

## How It Works

The bot places limit orders every 5 minutes for markets approximately 25 minutes in the future. Each order targets 5 shares at $0.49. Once both legs have been filled, the bot later attempts to redeem the resulting position after resolution.

## Running 24/7

Unlike traditional financial markets, Polymarket trades continuously, so the bot is intended to run 24/7. To keep it active and reduce downtime, it can be deployed on a cloud machine with logging and alerting in place if multiple trades fail to execute. For testing, Oracle's Standard E2 Micro instance running Linux 9 was used.

## Backtesting

To test the strategy, I funded the bot with $25 and monitored just under 1,000 trades. The backtesting section goes into more detail on its performance, the issues encountered, and the improvements that could be made to the model.

