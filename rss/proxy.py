"""Proxy for Redis sentinel."""
from redis.sentinel import Sentinel


class SentinelProxy:
    """Proxy for Redis sentinel."""

    def __init__(self, sentinel_host, master_name, socket_timeout=0.1):
        """Initialize Redis sentinel connection.

        :params: sentinel_host: (host, port)
        """
        self.sentinel = Sentinel(
            [sentinel_host], socket_timeout=socket_timeout)
        self.master = self.sentinel.master_for(master_name, socket_timeout=0.1)
        self.slave = self.sentinel.slave_for(master_name, socket_timeout=0.1)

    def __getattr__(self, name):
        """Get attribute from Redis master or slave."""
        if 'set' in name:
            target = self.master
        else:
            target = self.slave
        return getattr(target, name)
