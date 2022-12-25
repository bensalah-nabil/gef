import abc


class GefManager(metaclass=abc.ABCMeta):
    def reset_caches(self) -> None:
        """Reset the LRU-cached attributes"""
        for attr in dir(self):
            try:
                obj = getattr(self, attr)
                if not hasattr(obj, "cache_clear"):
                    continue
                obj.cache_clear()
            except: # we're reseting the cache here, we don't care if (or which) exception triggers
                continue
        return
