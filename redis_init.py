import redis
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

print(config['server'])
print(config['port'])
print(config['password'])

class RedisClient(object):

    def __init__(self):
        self.pool = redis.ConnectionPool(host = config['server'], port = config['port'], password = config['password'])

    def getConnection(self):
        return redis.Redis(connection_pool = self.pool)

redis_client = RedisClient()

p = redis_client.getConnection().ping()
print(p)