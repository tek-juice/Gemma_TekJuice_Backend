from models.apikey import ApiKey

def validate_api_key(api_key_value):
    if not api_key_value:
        return None
    
    key = ApiKey.query.filter_by(
        key = api_key_value,
        is_acive = True
    ). first()

    return key

