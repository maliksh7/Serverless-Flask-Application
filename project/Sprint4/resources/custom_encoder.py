import json
from decimal import Decimal


""" Custom Json Encoder Class """

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        
                
                
        """ 
        
            Description: Decoded the given object to float
            
            @param: self: scope(constructor)
            
            @param: obj (Decimal): object to be decoded to float,
      
            return: it returns the object in float            
        
        """
        
        #check if the object is instance of Decimal
        if isinstance(obj, Decimal):
            
            # return float version of that decimal
            return float(obj)
        
        # else return the object as it is, default value
        return json.JSONEncoder.default(self, obj)