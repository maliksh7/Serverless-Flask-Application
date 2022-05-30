def lambda_handler(event, context):
    
    """
        Creates the lambda function
        
        @param: event: describe what the event is and what it contains
        
        @param: context: describe what the context is and what it returns
        
        return: Hello World username(str)
        
    """
    
    return "Hello World {} {}!".format(event['first_name'], event['last_name'])