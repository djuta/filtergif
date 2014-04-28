from flask import Flask, render_template, request, abort
app = Flask(__name__)

import filtergif.views
