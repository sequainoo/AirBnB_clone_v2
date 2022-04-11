#!/usr/bin/python3
'''starts a flask web application.'''
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    '''eturns Hello HBNB!.'''
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''Returns HBNB.'''
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    '''Return C followed by value of text: space replace underscore.'''
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text='is cool'):
    '''Handles /python/(<text>).'''
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    '''displays n is anumber only i it is an integer.'''
    return '{:d} is a number'.format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
