import json

# Read the JSON file
def delete_object(filename, key_to_delete):
    # Read the JSON file
    with open(filename, 'r') as file:
        data = json.load(file)
    
    # Delete the specified object
    if key_to_delete in data:
        del data[key_to_delete]
    
    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
filename = 'models/chocolate/models_data.json'

# Example JSON file contents (data.json):
# {
#     "user1": {
#         "name": "John",
#         "age": 30
#     },
#     "user2": {
#         "name": "Jane",
#         "age": 25
#     }
# }

# Delete an object with key "user1"
delete_object(filename, "vgg16")
