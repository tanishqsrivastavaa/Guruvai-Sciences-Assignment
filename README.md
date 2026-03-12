# Guruvai Sciences Assignment

A Python implementation of two classic computer science problems: an LRU Cache and an Event Scheduler.

---

## Problem 1: LRU Cache (`cache.py`)

### Overview

Implements a **Least Recently Used (LRU) Cache** supporting two operations:

- `get(key)` — Returns the value for `key` if it exists (and marks it as recently used), otherwise returns `-1`.
- `put(key, value)` — Inserts or updates a key-value pair. If the cache is at capacity, the least recently used item is evicted first.

Both operations run in **O(1)** time complexity.

### Data Structure Choice

The implementation uses a **Hash Map + Doubly Linked List** combination:

- **Doubly Linked List** manages usage order. The head holds the Most Recently Used (MRU) item and the tail holds the Least Recently Used (LRU) item. Because each node holds references to both its previous and next neighbours, any node can be removed and re-inserted in O(1) — no traversal needed.
- **Hash Map** (`dict`) maps keys directly to their corresponding node objects in the list. This enables O(1) lookup, so `get` and `put` can jump straight to the right node without scanning the list.

Two sentinel (dummy) nodes act as permanent head and tail boundaries, eliminating edge-case checks when inserting or removing nodes at the ends of the list.

---

## Problem 2: Event Scheduler (`event_scheduler.py`)

### Overview

Implements an **EventScheduler** with two methods:

- `can_attend_all(events)` — Returns `True` if a single person can attend every event without any time overlap, `False` otherwise.
- `min_rooms_required(events)` — Returns the minimum number of meeting rooms needed to run all events simultaneously.

Input format: a list of `(start, end)` tuples, e.g. `[(9, 10), (10, 11), (11, 12)]`. Adjacent events (end time == start time) are **not** considered overlaps.

### Algorithmic Logic

**`can_attend_all`**: Events are sorted by start time. A single pass then checks each consecutive pair — if any event starts before the previous one has ended (`current_end > next_start`), a conflict exists and the function returns `False`.

**`min_rooms_required`**: This is a *peak concurrency* problem solved with a two-pointer sweep:
1. Start times and end times are each sorted independently into two lists.
2. Two pointers advance through these lists simultaneously. When the next start time is strictly less than the next end time, a new room is occupied (`rooms += 1`). Otherwise a room is freed (`rooms -= 1`, end pointer advances).
3. Because adjacent meetings are not overlaps, an end event at the same time as a start event is processed first (via the strict `<` comparison), freeing a room before allocating it.
4. The maximum value `rooms` reaches during the sweep is the answer.

---

## Final Discussion & Analysis

### Time & Space Complexity

| Function | Time | Space |
|---|---|---|
| `LRUCache.get` | O(1) average | O(1) |
| `LRUCache.put` | O(1) average | O(1) per entry; O(n) total for n items |
| `EventScheduler.can_attend_all` | O(n log n) — dominated by sort | O(1) extra |
| `EventScheduler.min_rooms_required` | O(n log n) — dominated by sort | O(n) for the two sorted arrays |

### Trade-offs: Hash Map + Doubly Linked List for LRU Cache

A hash map alone gives O(1) lookup but provides no ordering information, so identifying the LRU item would require an O(n) scan. An array or singly linked list can maintain order but cannot remove an arbitrary node in better than O(n). The doubly linked list solves this: given a direct pointer to a node (supplied by the hash map), relinking four pointers is all that is needed to move it to the head — constant time regardless of cache size. The combination therefore achieves O(1) for every operation without compromise.

### Future Proofing: Assigning Specific Room Numbers

To assign named rooms (e.g. "Room A", "Room B") to each event, the scheduler would need to track *which* room becomes free at each moment, not just *how many* rooms are free. A **min-heap** keyed on end times would work well: each heap entry stores `(end_time, room_name)`. When a new event starts, if the earliest-ending room is free (its end time ≤ new start time), pop it and reassign that room name to the new event; otherwise allocate a new room from a pool of available names and push the new event's end time alongside it. The return value would be a dict mapping each event to its assigned room.

### Concurrency: Making LRU Cache Thread-Safe

The current implementation is not thread-safe because a `get` or `put` call involves multiple non-atomic steps (hash map read/write plus several pointer re-links). Two threads executing concurrently could corrupt the linked list. To make it thread-safe:

- **Coarse-grained locking**: wrap every `get` and `put` call with a `threading.Lock` (or `RLock`). Simple and correct, but serialises all access.
- **Fine-grained locking**: use separate locks for the hash map and the linked list, allowing concurrent reads where possible — more complex but higher throughput under read-heavy workloads.
- **Reader-writer lock**: if reads (`get`) vastly outnumber writes (`put`), a reader-writer lock allows multiple concurrent readers while still serialising writers.

For a Python implementation, a `threading.Lock` acquired at the start of each public method and released on exit (using a `with` statement) is the idiomatic and safest starting point.

---

## Detailed Complexity & Design Notes

### 1. Time & Space Complexity Analysis

#### Problem 1: LRU Cache

| Function | Time Complexity | Space Complexity | Reasoning |
|---|---|---|---|
| `get(key)` | O(1) | O(1) | Hash map lookup and DLL pointer re-assignment are constant time. |
| `put(key, val)` | O(1) | O(1) | Adding/removing nodes in a DLL and map insertion are constant time. |
| Overall | O(1) | O(N) | We store N nodes in the map and the list, where N is the capacity. |

#### Problem 2: Event Scheduler

| Function | Time Complexity | Space Complexity | Reasoning |
|---|---|---|---|
| `can_attend_all` | O(N log N) | O(N) | Dominated by sorting. Python's Timsort uses O(N) space in the worst case. |
| `min_rooms_required` | O(N log N) | O(N) | Requires sorting two separate lists of size N. |

---

### 2. Trade-offs: The Hash Map + DLL Duo

The combination is used because it solves the **"Search vs. Update"** conflict:

- **Hash Map alone**: Provides O(1) access, but has no concept of order. To find the "least recently used" item, you'd have to search the whole map — O(N).
- **Linked List alone**: Maintains order perfectly. However, to find a specific key, you must traverse the list — O(N).
- **The Hybrid**: The Hash Map stores pointers to the List nodes. This gives us the speed of a map with the ordering of a list. The *Doubly* part of the list is essential; it allows a node to remove itself in O(1) because it knows its own neighbours.

---

### 3. Future Proofing: Assigning Room Names

To assign specific rooms (e.g. "Room A", "Room B"), replace the simple counter with a **Min-Heap (Priority Queue)** tracking occupied rooms by end time:

1. Store room names in a **"Free Rooms" pool**.
2. Use a **Min-Heap** to track currently occupied rooms, keyed by their end times.
3. For each new meeting:
   - **Check the Heap**: Has any room's end time passed? If yes, move that room name back to the Free Rooms pool.
   - **Assign a room** from the Free Rooms pool to the current meeting.
   - **Push** the meeting's end time and assigned room name back into the Heap.

---

### 4. Concurrency: Making it Thread-Safe

In a multi-threaded environment, the LRU Cache would suffer from **race conditions** — two threads trying to update the same pointers simultaneously.

**Required changes:**

- **Locks (Mutex)**: Wrap `get` and `put` logic in a `threading.Lock()`. This ensures only one thread can modify the pointers at a time.
- **Granular Locking**: For higher performance, use a **Read-Write Lock**. Multiple threads could read (`get`) concurrently, but only one could write (`put` or move a node).
- **Atomic Operations**: In some languages you might use atomic pointers, but in Python a standard `Lock` is the idiomatic approach for thread safety.
