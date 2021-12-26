from info import create_app

app = create_app('develop')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)