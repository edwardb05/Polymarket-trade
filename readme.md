
# Polymarket Arbritage bot

This is a proof of concept trading bot that is aiming to exploit inefficiencies in the polymarket 5Minute crypto markets.

## Theory

The theory behind this trading bot is that the BTC crypto market on polymarket is very volatile, especially in the 2 minutes before the time slot opens. E.G. for the "Bitcoin Up or Down - April 09, 9:50AM-9:55AM" market the trades at 9:48 AM will hit either side of 50 cents. As the market always resolves to $1 for the correct outcome, Up or Down, if we are able to fill both legs at $0.49 we can guarantee at 2% profit. If this is to occur every 5 minutes with $2.50 on up and $2.50 on down, it can make about $1.20 an hour. Not a signficant amount of money but enough for a POC. As well as this profit, by placing limit orders at $0.49 cents we are adding liquidity to the market book so benefit from polymarket's maker rebate program, wherein a percentage of the daily volume is returned to people who added liquidity to the order book.
## How it works

The software works by placing limit orders every 5 minutes for markets 25minutes in the future. These limit orders are for 5 shares at $0.49. Due to how Polymarket works it then checks to redeem any of the winning trades for the dollar they were realized to. 

## Ensuring this runs 24/7

As Polymarket is unlike normal markets, trades can be made 24/7 therefore to ensure the bot is making as much profit as possible it will be ran on a cloud PC. This will keep logs and alert if multiple trades are not placed. For this Oracle's Standard E2 Micro was used running Linux 9.


## Backtesting

To test the bot I gave it 25 dollars and monitored just under 1000 trades, I go into detail in the back testing about how it did and what issues it came into as well as improvenents that can be made to the model.



