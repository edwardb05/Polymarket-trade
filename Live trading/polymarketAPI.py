import os
import time

from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from polymarket_apis.clients.web3_client import PolymarketGaslessWeb3Client
from polymarket_apis.types.clob_types import ApiCreds

from markets import get_unixtime_300, get_market_token_ids
from tokens import buy_token, redeem_tokens

load_dotenv()

#SET POLYMARKET HOST AND CHAIN ID
HOST = "https://clob.polymarket.com"
CHAIN_ID = 137  # Polygon mainnet

#SET ORDER, NEEDS TO STAY LOW FOR LIQUIDITY
ORDER_PRICE = 0.49
ORDER_SIZE = 5
REDEEM_BUFFER_SECONDS = 15

#ENSURE ENV IS FU=ILLED
def require_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


#Initialize clients (Multiple for rotation)
def build_api_creds(index):
    return ApiCreds(
        key=require_env(f"BUILDER_API_KEY{index}"),
        secret=require_env(f"BUILDER_SECRET{index}"),
        passphrase=require_env(f"BUILDER_PASSPHRASE{index}"),
    )

def initialize_clients():
    private_key = require_env("PRIVATE_KEY")
    funder = require_env("FUNDER")

    redeem_clients = [
        PolymarketGaslessWeb3Client(
            private_key=private_key,
            signature_type=1,
            builder_creds=build_api_creds(index),
        )
        for index in (1, 2, 3)
    ]

    temp_client = ClobClient(HOST, key=private_key, chain_id=CHAIN_ID)
    api_creds = temp_client.create_or_derive_api_creds()
    client = ClobClient(
        HOST,
        key=private_key,
        chain_id=CHAIN_ID,
        creds=api_creds,
        signature_type=1,
        funder=funder,
    )
    return client, redeem_clients


#Buy both UP and DOWN tokens for the given market, return True if both buys succeed
def try_buy_market(client, token_id_up, token_id_down):
    bought_up = buy_token(client, token_id_up, price=ORDER_PRICE, size=ORDER_SIZE)
    bought_down = buy_token(client, token_id_down, price=ORDER_PRICE, size=ORDER_SIZE)
    return bought_up and bought_down

#Try to redeem tokens
def process_redemptions(redeem_clients, pending_redemptions):
    now = int(time.time())
    remaining = []

    for redemption in pending_redemptions:
        if now < redemption["redeem_after"]:
            remaining.append(redemption)
            continue

        redeemed = redeem_tokens(
            redeem_clients,
            redemption["condition_id"],
            amounts=[ORDER_SIZE, ORDER_SIZE],
        )
        if not redeemed:
            remaining.append(redemption)

    return remaining


def main():
    client, redeem_clients = initialize_clients()
    old_unixtime_300 = None
    pending_redemptions = []

    while True:
        pending_redemptions = process_redemptions(redeem_clients, pending_redemptions)
        unixtime_300 = get_unixtime_300(5)
        if unixtime_300 == old_unixtime_300:
            time.sleep(10)  # Wait 10 seconds before checking again
            continue

        token_id_up, token_id_down, condition_id = get_market_token_ids(unixtime_300)
        if token_id_up and token_id_down and condition_id:
            print(f"Token ID for UP: {token_id_up}, DOWN: {token_id_down}")
            bought_both = try_buy_market(client, token_id_up, token_id_down)
            if bought_both:
                pending_redemptions.append(
                    {
                        "condition_id": condition_id,
                        "redeem_after": unixtime_300 + REDEEM_BUFFER_SECONDS,
                    }
                )
            else:
                print(f"Skipping redemption scheduling for {condition_id} because one or more buys failed")
        else:
            print(f"Skipping market at {unixtime_300} due to missing data")

        old_unixtime_300 = unixtime_300
        print("Waiting for next interval...")
        time.sleep(10)


if __name__ == "__main__":
    main()
