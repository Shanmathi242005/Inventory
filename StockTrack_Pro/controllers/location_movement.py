from models.location_model import LocationModel

class LocationController:
    def __init__(self):
        self.model = LocationModel()
    
    def get_all_locations(self):
        return self.model.get_all_locations()
    
    def get_location(self, location_id):
        return self.model.get_location(location_id)
    
    def add_location(self, location_id, location_name, address, capacity):
        return self.model.add_location(location_id, location_name, address, capacity)
    
    def update_location(self, location_id, location_name, address, capacity):
        return self.model.update_location(location_id, location_name, address, capacity)
    
    def delete_location(self, location_id):
        return self.model.delete_location(location_id)