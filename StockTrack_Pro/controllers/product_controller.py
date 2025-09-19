from models.product_model import ProductModel

class ProductController:
    def __init__(self):
        self.model = ProductModel()
    
    def get_all_products(self):
        return self.model.get_all_products()
    
    def get_product(self, product_id):
        return self.model.get_product(product_id)
    
    def add_product(self, product_id, product_name, description):
        return self.model.add_product(product_id, product_name, description)
    
    def update_product(self, product_id, product_name, description):
        return self.model.update_product(product_id, product_name, description)
    
    def delete_product(self, product_id):
        return self.model.delete_product(product_id)