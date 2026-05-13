from datetime import datatime

class Call:
    
    def __init__(self, id: int, start_time, duration_sec: int, cost: float, from_device_id: int, to_device_id: int):
        self.id = id
        self.start_time = start_time
        self.duration_sec = duration_sec
        self.cost = cost
        self.from_device_id = from_device_id
        self.to_device_id = to_device_id
        

    def calculate_cost(self) -> float:
        pass

