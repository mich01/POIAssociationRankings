from routes.CrudActions import app
from routes.Analyze import app




if __name__ == '__main__':
    app.run(debug =True, port=5000)