from app import create_app
from flasgger import Swagger

app = create_app()

# Инициализация Swagger для документации
swagger = Swagger(app, template_file='../swagger.yml')

if __name__ == '__main__':
    app.run(debug=True,port=5000)
