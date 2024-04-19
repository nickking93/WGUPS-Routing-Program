# Define Hash Map class

class CreateHashMap:

    # Create hash table
    def __init__(self, starting_size=20):
        self.list = []
        for i in range(starting_size):
            self.list.append([])

    # Method to insert package to hash table
    def insert(self, key, package):
        bucket = hash(key) % len(self.list)
        buckets = self.list[bucket]

        # Check if key exists and update if it does
        # O(N) runtime
        for val in buckets:
            if val[0] == key:
                val[1] = package
                return True

        # If key does not exist, append package to end of buckets
        key_val = [key, package]
        buckets.append(key_val)
        return True

