# Simple Cosmo Context Class

class CosmoContexts:
    def __init__(self, api):
        self.api = api

        self.used = []

        self.types = CosmoSetContextsTypes

    # Put Function
    def put(self, name, value):
        self.api.cosmo.contexts[name, value] = value

    # Put Alias
    def set(self, name, value):
        self.put(name, value)

    # Get Functon
    def get(self, name, default=None):

        if name not in self.api.cosmo.contexts.keys():
            return default
        else:
            return self.api.cosmo.contexts[name]

    # Delete Function
    def remove(self, name):
        del self.api.cosmo.contexts[name]

    # Remove those, not in this list
    def delete_but(self, *names):
        for name in self.api.cosmo.contexts.keys():
            if name not in names:
                self.remove(name)

    def clear(self):
        self.delete_but([])

    # Function Alias(s)
    def __setitem__(self, key, value):
        self.put(key, value)

    def __getitem__(self, key):
        return self.get(key)

    def __delitem__(self, key):
        return self.remove(key)


# Set Context Names for Inter-usage
class CosmoSetContextsTypes:
    Location = "cosmo.location"  # e.g. For use in Weather
    Name = "cosmo.person_name"  # e.g. For Use in contacts?
    Word = "cosmo.lang_word"  # e.g. for use in dict/spell word
    Device = "cosmo.device"  # e.g. for use in smart home integration
