# test with memurai database, see https://www.memurai.com/
# for redis python clients, see https://redis.io/clients#python
# usage of package redis-py (package redis)
#   documentation https://redis-py.readthedocs.io/en/stable/
#   source and quick start: https://github.com/redis/redis-py

import redis
r=redis.Redis(host='localhost', port=6379, db=0)
success=r.set('foo', 'bar')
print("Success: {}".format(success))
bo=r.get('foo')
print('Content:')
print(bo)