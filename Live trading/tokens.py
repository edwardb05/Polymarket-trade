from py_clob_client.clob_types import OrderArgs
from py_clob_client.order_builder.constants import BUY

#Place limit order for token using provided client
def buy_token(client, token_id, price=0.49, size=5):
    try:
        response = client.create_and_post_order(
            OrderArgs(
                token_id=token_id,
                price=price,
                size=size,
                side=BUY,
            ),
            options=None
        )
        print(f"Order placed for token {token_id}. Order ID: {response.get('orderID')}, Status: {response.get('status')}")
        return True
    except Exception as e:
        print(f"[Buy Error] Failed to place order for token {token_id}: {e}")
        return False

#Try to redeem tokens on chain
def redeem_tokens(redeem_clients, condition_id, amounts):
    for redeem_client in redeem_clients:
        try:
            redeem_client.redeem_position(condition_id, amounts=amounts, neg_risk=False)
            print(f"Redeemed positions for condition {condition_id}")
            return True
        except Exception as e:
            print(f"[Redeem Error] {e}")

    print("All redeem clients failed")
    return False
