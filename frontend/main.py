from frontend.DashApp import Generate_Dash_App


if __name__ == "__main__":
    app = Generate_Dash_App()

    app.run(debug=True, port=8519)