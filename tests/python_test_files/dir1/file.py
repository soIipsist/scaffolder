def blue(string):
    print('blue ', string)

def green(str):
    print('green', str)

def goodbye():
    print()

def hello_world():
    print('hello world')

def hello():
    print('hi')

def redd(string):
    print('red', string)

def define(string = None):
    if not string:
        raise ValueError("string was not defined")

    print('hello')

def define2(string = None):
    if not string:
        raise ValueError("string was not defined")
    
    print('hello')