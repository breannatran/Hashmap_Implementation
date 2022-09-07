# Author: Breanna Tran
# GitHub username: breannatran
# Due Date: 8/9/2022
# Description: Implement the HashMap class with separate chaining collision resolution


from supplemental_data_structures import (DynamicArray, LinkedList, hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        """
        hash = self._hash_function(key)         # Get the hash value from the hash function
        index = hash % self._capacity           # Calculate index by using the mod operator

        # Check if the linked list at the index of dynamic array contains the key
        matching_node = self._buckets[index].contains(key)

        if matching_node:
            matching_node.value = value  # Reassign value of node to new value
        else:
            self._buckets[index].insert(key, value)  # Add node to linked list
            self._size += 1

        pass

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        empty_count = 0  # Define variable to keep count of empty buckets
        for index in range(0, self._capacity):
            if self._buckets[index].length() == 0:  # Check if the bucket is empty (length of 0)
                empty_count += 1  # if empty, increment empty_count by one

        return empty_count

        pass

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        load_factor = float(self._size / self._capacity)
        return load_factor

        pass

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        for index in range(0, self._capacity):  # Iterate through all buckets
            self._buckets[index] = LinkedList()  # Each bucket is overwritten to be an empty LinkedList

        self._size = 0

        pass

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All existing key / value pairs
        must remain in the new hash map, and all hash table links must be rehashed.
        First check that new_capacity is not less than 1; if so, the method does nothing.
        If new_capacity is 1 or more, make sure it is a prime number. If not, change it to the next
        highest prime number. You may use the methods _is_prime() and _next_prime() from the
        skeleton code.
        """

        if new_capacity >= 1:  # Check if new_capacity is 1 or more
            if self._is_prime(new_capacity) is False:  # Check if new_capacity is not prime
                new_capacity = self._next_prime(new_capacity)  # Recalculate new_capacity from _next_prime()

            new_array = DynamicArray()  # Create new DynamicArray for hash map
            for array_index in range(0, new_capacity):
                new_array.append(LinkedList())

            for index in range(0, self._capacity):  # Iterate through existing DynamicArray
                for node in self._buckets[index]:
                    hash = self._hash_function(node.key)  # Get the hash value from the hash function
                    index = hash % new_capacity  # Calculate index by using the mod operator

                    new_array[index].insert(node.key, node.value)  # Add node to linked list

            self._buckets = new_array
            self._capacity = new_capacity

        pass

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        hash = self._hash_function(key)  # Get the hash value from the hash function
        index = hash % self._capacity  # Calculate index by using the mod operator

        # Check if the linked list at the index of dynamic array contains the key
        matching_node = self._buckets[index].contains(key)

        if matching_node:
            return matching_node.value  # Return value associated with the given key
        else:
            return None

        pass

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.
        """
        hash = self._hash_function(key)  # Get the hash value from the hash function
        index = hash % self._capacity  # Calculate index by using the mod operator

        # Check if the linked list at the index of dynamic array contains the key
        matching_node = self._buckets[index].contains(key)

        if matching_node:
            return True  # Return True if key is in the hash map
        else:
            return False  # Return False if key is not in the hash map

        pass

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing (no exception needs to be raised).
        """
        hash = self._hash_function(key)  # Get the hash value from the hash function
        index = hash % self._capacity  # Calculate index by using the mod operator

        removal = self._buckets[index].remove(key)  # Remove first node in LinkedList with matching key
        if removal is True:
            self._size -= 1

        pass

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key / value pair
        stored in the hash map. The order of the keys in the dynamic array does not matter.
        """
        keys_values_array = DynamicArray()

        for index in range(0, self._capacity):  # Iterate through existing DynamicArray
            for node in self._buckets[index]:
                keys_values_array.append((node.key, node.value))

        return keys_values_array

        pass

    def get_buckets(self) -> DynamicArray:
        """
        Return size of map
        """
        return self._buckets


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Write a standalone function outside of the HashMap class that receives a dynamic array
    (that is not guaranteed to be sorted). This function will return a tuple containing, in this
    order, a dynamic array comprising the mode (most occurring) value/s of the array, and an
    integer that represents the highest frequency (how many times they appear).
    """
    map = HashMap()
    mode_count = 1
    mode_array = DynamicArray()

    for index in range(0, da.length()):
        node = map.get_buckets()[1].contains(da[index])

        if node:
            node.value += 1
            if node.value > mode_count:
                mode_count = node.value
        else:
            map.get_buckets()[1].insert(da[index], 1)

    for item in map.get_buckets()[1]:
        if item.value == mode_count:
            mode_array.append(item.key)

    mode_tuple = (mode_array, mode_count)

    return mode_tuple

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
