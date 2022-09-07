# Hashmap Implementation
This project includes implementation of a hashmap using chaining and open addressing.


For the implementation using chaining for collision resolution, a dynamic array is used to store the hash table which holds singly linked lists. Chains of key / value pairs are stored in linked list nodes. For the implementation using open addressing, a dynamic array is used to store the hash table. Both implementations include the following methods:

put() - This method updates the key / value pair in the hash map. If the given key already exists in the hash map, its associated value must be replaced with the new value. If the given key is not in the hash map, a new key / value pair must be added.

empty_buckets() - This method returns the number of empty buckets in the hash table.

table_load() - This method returns the current hash table load factor.

clear() - This method clears the contents of the hash map. It does not change the underlying hash table capacity.

resize_table() - This method changes the capacity of the internal hash table. All existing key / value pairs must remain in the new hash map, and all hash table links must be rehashed. It first checks that new_capacity is not less than 1; if so, the method does nothing. If new_capacity is 1 or more, it checks if new_capacity is a prime number. If not, new_capacity is changed to the next highest prime number.

get() - This method returns the value associated with the given key. If the key is not in the hash map, the method returns None.

contains_key() - This method returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does not contain any keys.

remove() - This method removes the given key and its associated value from the hash map. If the key is not in the hash map, the method does nothing.

get_keys_and_values() - This method returns a dynamic array where each index contains a tuple of a key / value pair stored in the hash map.


Only the implementation using chaining for collision resolution contains the following method:

find_mode() - A standalone function outside of the HashMap class that receives a dynamic array. This function will return a tuple containing, in this order, a dynamic array comprising the mode value/s of the array, and an integer that represents the highest frequency. It is assumed that the input array will contain at least one element, and that all values stored in the array will be strings. 
