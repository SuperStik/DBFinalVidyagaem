#imports
from helper import helper
from db_operations import db_operations

db_ops = db_operations()

#main method
query = "SELECT * FROM video_game"
result = db_ops.select_query(query)
helper.pretty_print(result)

db_ops.destructor()