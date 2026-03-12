"""
To achieve O(1) constant time for lookup and updates, we will have decouple data retrieval from order management.

I will be going for two data structures: Doubly Linked List & Hash Map

Why a Doubly Linked list?
It manages the order of usage. For example when an item is accessed or added, it moves to the head(MRU). When the cache exceeds capacity, we evict the node at the tail(LRU). Using a doubly linked list, it allows us to remove a node in O(1) time given its reference, as we can immediately access its previous and next neighbours.

Why a Hash Map?
It maps keys to the actual Node objects in our Doubly Linked List.
It allows us to jump directly to any node in the list for a 'get' or 'update' operation without traversing the entire list, ensuring O(1) time complexity.
"""

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self,capacity: int):
        self.capacity = capacity
        self.cache = {} # Mapping key to node object

        #adding dummy values (simulating boundary conditions)
        self.head = Node(0,0)
        self.tail = Node(0,0)

        self.head.next = self.tail
        self.tail.prev = self.head

    def remove(self,node): #Function to remove a node from a DLL.
        prevNode = node.prev
        nextNode = node.next
        prevNode.next = nextNode
        nextNode.prev = prevNode

    
    def add_to_head(self,node): #Function to add a node right after the head.
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key:int) -> int:
        if key in self.cache:
            node = self.cache[key]
            #Move accessed node to front (MRU)
            self.remove(node)
            newNode = Node(key, value)
            self.add_to_head(newNode)
            return node.value
        return -1


    def put(self, key: int, value: int):
        if key in self.cache:
            #Updating existing node value and move to front.
            self.remove(cache[key])
        newNode = Node(key,value)
        self.cache[key] = newNode
        self.add_to_head(newNode)

        if len(self.cache) > self.capacity:
            #Get rid of LRU node (the node right before dummy tail)
            lruNode = self.tail.prev
            self.remove(lruNode)
            del self.cache[lruNode.key]


"""
Why this achieves O(1)?
-> Hash Map lookup: to access self.cache[key] is O(1) on average.
 
-> Doubly Linked List: Re-linking four pointers (prev and next) is a fixed number of operations, regardless of how many items are in the cache, therefore O(1).
"""


