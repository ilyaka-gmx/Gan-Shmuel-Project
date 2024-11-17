from sql.billing_sql import Providers

def create_provider(data):
    name = data.get('name')
    if not name:
        return {"error": "Name is required"}, 400

    try:
        new_provider = Providers.create(name=name)
        return {"id": new_provider.id, "name": new_provider.name}
    except Exception as e:
        return {"error": f"Failed to create provider: {str(e)}"}, 500
