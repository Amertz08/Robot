from factory import create_app
import os

app = create_app(os.getenv('CONFIG_LVL') or 'default')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
