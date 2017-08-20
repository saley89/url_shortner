import redis
from flask import g


def get_cached_redis_store():
    db = getattr(g, 'redis_db', None)
    if db is None:
        db = g.redis_db = get_redis_store()
    return db


def get_redis_store():
    conn_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    return redis.Redis(connection_pool=conn_pool)