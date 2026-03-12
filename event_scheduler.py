"""
Logic and Approach:

1.can_attend_all(events):
To determine if one person can attend every meeting, we first sort the events by their start times. This will allow us to process the day in a chronological order. We then iterate through the sorted list and compare the end time of the current meeting with the start time of the next. If any meeting starts before the previous one ends, an overlap will occur.
We will return false if current_end > next_start because of the constraints given in the question.

2.min_rooms_required(events):
This is a 'peak load' problem where we need to find the maximum number of meetings happening at any single point in time.
-> Chronological approach: we will separate the start times and end times into two sorted lists. We thne use two pointers to move through time. Every time we encounter a 'start' event, it means a room is now occupied which leads to the counter increasing. Every time we encounter an 'end' event, it means a room has now been freed, thus counter decreasing.

-> Global Maximum: the minimum rooms required is simply the highest value our conter reaches during this process, because the prompt says adjacenet meetings dont overlap, if a meeting ends at 10 and another starts at 10, we treat the 'end' first to free up the room before the next one starts.
"""



class EventScheduler:
    def can_attend_all(self, events: list[tuple]) -> bool:
        if not events:
            return True

        events.sort(key=lambda x: x[0]) #sorting chronologically by start time
        for i in range(len(events) - 1): #if current meeting ends AFTER the next one starts, it's an overlap
            
            if events[i][1] > events[i+1][0]:
                return False
        return True

    def min_rooms_required(self, events: list[tuple]) -> int:
        if not events:
            return 0
        #separating and sorting all start and end points
        starts = sorted([e[0] for e in events])
        ends = sorted([e[1] for e in events])
        
        rooms = 0
        max_rooms = 0
        s_ptr = 0
        e_ptr = 0
        
        while s_ptr < len(events): #if a meeting starts before the earliest meeting ends, we need a new room
            if starts[s_ptr] < ends[e_ptr]:
                rooms += 1
                s_ptr += 1
            else: #a meeting ended (or ended exactly when the next starts), free a room
                rooms -= 1
                e_ptr += 1

            max_rooms = max(max_rooms, rooms) 
        return max_rooms


