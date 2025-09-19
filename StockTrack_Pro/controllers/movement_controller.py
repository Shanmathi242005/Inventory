from models.movement_model import MovementModel

class MovementController:
    def __init__(self):
        self.model = MovementModel()
    
    def get_all_movements(self):
        return self.model.get_all_movements()
    
    def get_movement(self, movement_id):
        return self.model.get_movement(movement_id)
    
    def add_movement(self, movement_id, from_location, to_location, product_id, quantity, notes):
        return self.model.add_movement(movement_id, from_location, to_location, product_id, quantity, notes)
    
    def update_movement(self, movement_id, from_location, to_location, product_id, quantity, notes):
        return self.model.update_movement(movement_id, from_location, to_location, product_id, quantity, notes)
    
    def delete_movement(self, movement_id):
        return self.model.delete_movement(movement_id)