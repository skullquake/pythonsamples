from flask import Blueprint
bp=Blueprint('plotly',__name__)
from app.plotly import routes
