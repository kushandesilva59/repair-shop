
from math import cos, asin, sqrt
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import atexit
import socket
import requests
import geocoder

app = Flask(__name__)
CORS(app)

@app.route("/members")
def members():
    return {"Members": ["Member1", "Member2", "Member3"]}

@app.route("/location")
def location():
    coordinates = get_current_gps_coordinates()
    if coordinates is not None:
        latitude, longitude = coordinates
        print(f"Your current GPS coordinates are:")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        return {"Latitude": latitude, "Longitude": longitude}
    else:
        print("Unable to retrieve your GPS coordinates.")
        
        
        
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(hav))

def closest(data, v):
    return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))   




    
def get_current_gps_coordinates():
    g = geocoder.ip('me')#this function is used to find the current information using our IP Add
    if g.latlng is not None: #g.latlng tells if the coordiates are found or not
        return g.latlng
    else:
        return None
    
@app.route('/shop-locations')    
def get_all_locations():
    try:
        # Replace these placeholder values with your actual database credentials
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='repair_shop')

        cursor = conn.cursor()

        # Example: Retrieving all data from a 'users' table
        select_query = "SELECT * FROM shop_locations"

        # Execute the query
        cursor.execute(select_query)


        # Fetch all rows
        rows = cursor.fetchall()
    
        # check_user_exist(rows)

        # Print the retrieved data
        # for row in rows:
        #     print(row[1])
        
        return rows

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and connection
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/nearest-place')    
def get_nearest_location():
    locations = get_all_locations()
    print("this one")
    print(locations)
    converted_coordinates = [{'lat': item[1], 'lon': item[2]} for item in locations]

    print("after")
    print(converted_coordinates)
    
    nearest_place = closest(converted_coordinates,{"lat": 6.4353308, "lon": 80.0222144})
    
    print(nearest_place)
    
    return (nearest_place)
   
   
get_nearest_location()

    
@app.route('/register', methods=['POST'])    
def register_user():
    data = request.json
    
    # Process the data
    email = data.get('email')
    password = data.get('password')

    # Perform registration logic here
    # For example, you can print the received data
    print("Received email:", email)
    print("Received password:", password)
    
    last_user_id = get_last_value()
    print("Last value:", last_user_id)
    new_user_id = last_user_id+1
    print("New id---------->",new_user_id)
    
    data = {
    'id': new_user_id,
    'email': email,
    'password': password
    }

    insert_data_into_users(data)
    # Return a response
    return jsonify({'status': 1}), 200



    
@app.route('/login', methods=['POST'])
def receive_data():
    data_received = request.get_json()
    # Process the received data as needed
    print('Data received from frontend:', data_received)

    users = get_all_users()

    print(data_received['email'])

    user_exist = check_user_exist(users, data_received)
    
    print(user_exist)
    
    if(user_exist):
        response_data = {'status': 1}
    else:
       response_data = {'status': -1}
    return jsonify(response_data)



def get_last_user_id():
    try:
        # Replace these placeholder values with your actual database credentials
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='repair_shop')

        cursor = conn.cursor()

        # Example: Retrieving all data from a 'users' table
        select_query = "SELECT id FROM users ORDER BY id DESC LIMIT 1"

        # Execute the query
        cursor.execute(select_query)


        # Fetch all rows
        rows = cursor.fetchall()
    
        # check_user_exist(rows)

       
        print("LAst u id")
        print (rows)
        return rows
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and connection
        if conn.is_connected():
            cursor.close()
            conn.close()
    
def get_all_users():
    try:
        # Replace these placeholder values with your actual database credentials
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='repair_shop')

        cursor = conn.cursor()

        # Example: Retrieving all data from a 'users' table
        select_query = "SELECT * FROM users"

        # Execute the query
        cursor.execute(select_query)


        # Fetch all rows
        rows = cursor.fetchall()
    
        # check_user_exist(rows)

        # Print the retrieved data
        # for row in rows:
        #     print(row[1])

        return rows

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and connection
        if conn.is_connected():
            cursor.close()
            conn.close()


def check_user_exist(rows, user_credentiols):
        for row in rows:
            if(row[1] == user_credentiols['email']):
                return True

        return False

def insert_data_into_users(data):
    try:
    
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='repair_shop')
        if conn.is_connected():
            print("Connection success!..")

            cursor = conn.cursor()
         
            table_name = 'users'
            column_names = ('id', 'email', 'password') 
            values = tuple(data.get(column, 4) for column in column_names)
         
            insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['%s'] * len(column_names))})"

            cursor.execute(insert_query, values)
            conn.commit()

            print("Data inserted successfully!")
            cursor.close()
            conn.close()

    except mysql.connector.Error as e:
        print(f"Error: {e}")

def get_last_value():
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="repair_shop"
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    try:
        # Execute the SQL query to retrieve the last value from the column
        cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")

        # Fetch the result
        result = cursor.fetchone()

        if result:
            # Extract the last value from the result
            last_value = result[0]
           
        else:
            print("No rows returned.")
            
        return last_value

    except mysql.connector.Error as error:
        print("Error executing query:", error)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# Call the function to get the last value
get_last_value()

if __name__ == "__main__":
    print("Main running")
    # Establish MySQL connection when the script is executed
    # connection = establish_mysql_connection()
    # if connection:
    #     # Close the connection when the script terminates
    #     atexit.register(connection.close)
    app.run(debug=True)
    

