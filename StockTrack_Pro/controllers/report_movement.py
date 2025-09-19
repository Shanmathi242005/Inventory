from database import db

class ReportController:
    def get_inventory_report(self):
        conn = db.get_connection()
        report_data = conn.execute('''
            WITH incoming AS (
                SELECT product_id, to_location as location_id, SUM(quantity) as total_in
                FROM product_movements 
                WHERE to_location IS NOT NULL
                GROUP BY product_id, to_location
            ),
            outgoing AS (
                SELECT product_id, from_location as location_id, SUM(quantity) as total_out
                FROM product_movements 
                WHERE from_location IS NOT NULL
                GROUP BY product_id, from_location
            )
            SELECT 
                p.product_id,
                p.product_name,
                l.location_id,
                l.location_name,
                COALESCE(i.total_in, 0) - COALESCE(o.total_out, 0) as balance
            FROM products p
            CROSS JOIN locations l
            LEFT JOIN incoming i ON p.product_id = i.product_id AND l.location_id = i.location_id
            LEFT JOIN outgoing o ON p.product_id = o.product_id AND l.location_id = o.location_id
            WHERE COALESCE(i.total_in, 0) - COALESCE(o.total_out, 0) > 0
            ORDER BY p.product_name, l.location_name
        ''').fetchall()
        conn.close()
        return report_data
    
    def get_movement_history(self, product_id=None, location_id=None):
        conn = db.get_connection()
        
        query = '''
            SELECT pm.*, p.product_name, 
                   fl.location_name as from_location_name, 
                   tl.location_name as to_location_name
            FROM product_movements pm
            LEFT JOIN products p ON pm.product_id = p.product_id
            LEFT JOIN locations fl ON pm.from_location = fl.location_id
            LEFT JOIN locations tl ON pm.to_location = tl.location_id
            WHERE 1=1
        '''
        params = []
        
        if product_id:
            query += ' AND pm.product_id = ?'
            params.append(product_id)
        
        if location_id:
            query += ' AND (pm.from_location = ? OR pm.to_location = ?)'
            params.extend([location_id, location_id])
        
        query += ' ORDER BY pm.timestamp DESC'
        
        movements = conn.execute(query, params).fetchall()
        conn.close()
        return movements