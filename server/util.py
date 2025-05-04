import json
import pickle
import numpy as np

locations = None
data_columns = None
model = None

# getting locations
def get_location_names () :
    return locations 

# gettinv estimated price
def get_estimated_price (location ,sqft, bath , bhk ) : 
         
    try : 
        loc_index = data_columns.index (location.lower())    
    except : 
        loc_index = -1
         
    x = np.zeros (len(data_columns)) 
    x[0] = sqft 
    x[1] = bath 
    x[2] = bhk 
    
    if loc_index >= 0 : 
        x[loc_index] = 1
    
    return round(model.predict([x])[0], 2)

# load saved artifacts
def load_saved_artifacts () : 
    print("loading artficts......")
    
    global locations
    global data_columns
    global model

    with open ("server/artifacts/columns.json", "r") as file : 
       data_columns =  json.load(file)["data_columns"]
       locations = data_columns[3:]

    with open("server/artifacts/real_state_price_prediction.pickle", "rb") as file : 
       model =  pickle.load(file)
    print("Artifacts Loaded Done")
         
    
# main class 
if __name__ == "__main__" : 
    load_saved_artifacts ()
    print(get_location_names())
    print(get_estimated_price('1st phase jp nagar', 1000, 3,3))
    print(get_estimated_price('1st phase jp nagar', 1000, 2,2))