TEA: Capstone Project - Education Planning Dashboard

To run the project please execute the following steps per Operating System: 


On Linux: Open Command Terminal
1. Command: install python3 
2. Navigate to project folder. 
3. Command: pip install -r requirements.text 
4. Command: python -m frontend.main
5. Open http://127.0.0.1:8519/


On Mac: Open Command Terminal
1. Command: brew install python3
2. Navigate to project folder. 
3. Command: pip3 install -r requirements.text 
4. Command: python3 -m frontend.main
5. Open http://127.0.0.1:8519/

On Windows: 
1. Install Python3 
--Open Command Terminal 
2. Navigate to project folder. 
3. Command: pip3 install -r requirements.text 
4. Command: python -m frontend.main
5. Open http://127.0.0.1:8519/


Architecture Descriptions: 

There are 3 Main Layers -- 

DataLayer: 
This folder holds modules that responsible for database operations. It can be use to launch an API with defined endpoints
with flexiable parameterization. 

ApplicationLayer: 
This folder helps segregate the logical flows that the dashboard will need to make to retrieve and present the 
data to the user. 
    Subfolders => 
    DataServiceAPI: Used to make API calls to the API served by the DataLayer 
    LogicalOperations: Holds the codes that encomposes the logical processing of the data.
        Modules => 
        OptionsUtilis.py: Used to on dashboard launch to get all dropdown selection options.
        DataUtilis.py: Used for data manipulation and pre-processing after getting through the DataServiceAPI folder.
        GraphUtilis.py: Graphical functions that generate interactive visualizations. 

