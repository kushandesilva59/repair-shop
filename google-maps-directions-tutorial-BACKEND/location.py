coordinates = [(7, 80), (7, 70)]

# Convert list of tuples to list of dictionaries
converted_coordinates = [{'lat': lat, 'lon': lon} for lat, lon in coordinates]

print(converted_coordinates)