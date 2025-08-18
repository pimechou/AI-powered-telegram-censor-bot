import json
import time

def spam(user_id, chat_id, rate):
    user = str(user_id)
    try:
        with open(f'groups/{chat_id}.json', 'r') as f:
            data = json.load(f)
    except:
        data = {}
    if user not in data:
        data[user] = []
    data[user].append(int(time.time()))
    if len(data[user]) > rate:
        data[user].pop(0)
    with open(f'groups/{chat_id}.json', 'w') as f:
        json.dump(data, f)
    if len(data[user]) < rate:
        return 0
    if data[user][-1] - data[user][0] < 60:
        return 1
    return 0
    