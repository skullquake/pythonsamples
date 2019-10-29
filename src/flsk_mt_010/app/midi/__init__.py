from flask import Blueprint
bp=Blueprint('midi',__name__)
from app.midi import routes
