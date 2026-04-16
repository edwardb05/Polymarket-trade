import json
import time
import requests


def get_unixtime_300(future):
    #Calculate the next 5-minute interval timestamp, adjusted by 'future' intervals
    unix_time = int(time.time())
    unixtime_300 = unix_time - (unix_time % 300) + 300 * future 
    return unixtime_300

#Get the token ids of upcoming market
def get_market_token_ids(unixtime_300):
    
    slug = f"btc-updown-5m-{unixtime_300}"
    url = "https://gamma-api.polymarket.com/markets"
    params = {"slug": slug}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError(f"No market found for slug: {slug}")
        market = data[0]
        condition_id = market["conditionId"]
        token_ids = json.loads(market["clobTokenIds"])
        
        token_id_up = token_ids[0]
        token_id_down = token_ids[1]
        return token_id_up, token_id_down, condition_id
    except requests.RequestException as e:
        print(f"[Network Error] Failed to fetch market: {e}")
        return None, None, None
    except ValueError as e:
        print(f"[Value Error] {e}")
        return None, None, None
    except Exception as e:
        print(f"[Unexpected Error] {e}")
        return None, None, None

