# Author: Breanna Tran
# GitHub username: breannatran
# Due Date: 8/9/2022
# Description: Implement the HashMap class with open addressing collision resolution


from supplemental_data_structures import (DynamicArray, HashEntry, hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key / value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the given key is
        not in the hash map, a new key / value pair must be added.

        For this hash map implementation, the table must be resized to double its current
        capacity when this method is called and the current load factor of the table is
        greater than or equal to 0.5.
        """

        if self.table_load() >= 0.5:
            self.resize_table(2 * self._capacity)

        hash = self._hash_function(key)  # Get the hash value from the hash function
        index = hash % self._capacity  # Calculate index by using the mod operator

        new_entry = HashEntry(key, value)

        # Check if the index of dynamic array
        if self._buckets[index]:  # Case where index is not available
            if self._buckets[index].key == key:  # Case where key is already in hash map at index
                self._buckets[index].value = value
                if self._buckets[index].is_tombstone is True:
                    self._buckets[index].is_tombstone = False
                    self._size += 1

            else:
                j = 1
                new_index = index + j ** 2  # Quadratic probing
                new_index = new_index % self._capacity

                while j < self._capacity:
                    if self._buckets[new_index] and self._buckets[new_index].is_tombstone is not True:
                        # Case where new_index is not available
                        if self._buckets[new_index].key == key:  # Case where key is already in hash map at new_index
                            self._buckets[new_index].value = value
                            if self._buckets[new_index].is_tombstone is True:
                                self._buckets[new_index].is_tombstone = False
                                self._size += 1
                            break
                        else:
                            j += 1
                            new_index = index + j ** 2  # Quadratic probing
                            new_index = new_index % self._capacity
                    else:  # Case where new_index is available
                        self._buckets[new_index] = new_entry
                        self._size += 1
                        break
        else:  # Case where index is available
            self._buckets[index] = new_entry
            self._size += 1

        pass

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        load_factor = float(self._size / self._capacity)
        return load_factor

        pass

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        empty_count = 0  # Define variable to keep count of empty buckets
        for index in range(0, self._capacity):
            if self._buckets[index] is None or self._buckets[index].is_tombstone is True:
                # Check if the bucket is empty at index
                empty_count += 1  # if empty, increment empty_count by one

        return empty_count

        pass

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All existing key / value pairs
        must remain in the new hash map, and all hash table links must be rehashed.
        First check that new_capacity is not less than the current number of elements in the hash
        map; if so, the method does nothing.
        If new_capacity is valid, make sure it is a prime number; if not, change it to the next
        highest prime number. You may use the methods _is_prime() and _next_prime() from the
        skeleton code.
        """
        initial_capacity = self._capacity
        initial_array = self._buckets

        if new_capacity < self._size:
            return
        else:
            if self._is_prime(new_capacity) is False:  # Check if new_capacity is not prime
                new_capacity = self._next_prime(new_capacity)  # Recalculate new_capacity from _next_prime()
            self._capacity = new_capacity

            new_array = DynamicArray()  # Create new DynamicArray for hash map
            for array_index in range(0, new_capacity):
                new_array.append(None)
            self._buckets = new_array
            self._size = 0

            for index in range(0, initial_capacity):  # Iterate through existing DynamicArray
                if initial_array[index] is not None:
                    self.put(initial_array[index].key, initial_array[index].value)

        pass

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        if self._size == 0:  # Case where hashmap is empty
            return
        else:
            for index in range(0, self._capacity):  # Check for key
                if self._buckets[index] is not None and self._buckets[index].key == key and \
                        self._buckets[index].is_tombstone is False:  # Key is a match
                    return self._buckets[index].value
        return None

        pass

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.
        """
        if self._size == 0:  # Case where hashmap is empty
            return False
        else:
            for index in range(0, self._capacity):  # Check for key
                if self._buckets[index] is not None and self._buckets[index].key == key and \
                        self._buckets[index].is_tombstone is False:  # Key is a match
                    return True
        return False

        pass

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing (no exception needs to be raised).
        """
        if self._size == 0:  # Case where hashmap is empty
            return
        else:
            for index in range(0, self._capacity):  # Check for key
                if self._buckets[index] is not None and self._buckets[index].key == key and \
                        self._buckets[index].is_tombstone is False:  # Key is a match
                    self._buckets[index].is_tombstone = True
                    self._size -= 1  # Decrement self._size by 1
                    return

        pass

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        for index in range(0, self._capacity):  # Iterate through all buckets
            self._buckets[index] = None  # Each bucket is overwritten to be None

        self._size = 0

        pass

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key / value pair
        stored in the hash map. The order of the keys in the dynamic array does not matter.
        """
        keys_values_array = DynamicArray()

        for index in range(0, self._capacity):  # Iterate through existing DynamicArray
            if self._buckets[index] is not None and self._buckets[index].is_tombstone is False:
                # Check for key/value pairs that aren't tombstones
                add_tuple = (self._buckets[index].key, self._buckets[index].value)
                keys_values_array.append(add_tuple)

        return keys_values_array

        pass


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
