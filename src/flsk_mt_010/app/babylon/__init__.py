from flask import Blueprint
bp=Blueprint('babylon',__name__)
from app.babylon import routes
