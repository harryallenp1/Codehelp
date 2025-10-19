'''
This module calls the Generate_Dash_App function to create the Dash application. Once the application is created,
main will run the app on the specified port.
'''
from frontend.DashApp import Generate_Dash_App


if __name__ == "__main__":
    app = Generate_Dash_App()

    app.run(debug=True, port=8519)