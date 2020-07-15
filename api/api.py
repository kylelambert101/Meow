from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import json
import logging
from utilities import getBulletList
from os import path


# Base Variables
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FILE = "api.log"
DATA_FILE = "api.json"

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s - (%(levelname)s) - %(message)s',
    datefmt=DATE_FORMAT)


# class LitterData:
#     DEFAULT = {'history': [], 'period': 3}

#     def __init__(self, jsonData):
#         # List of previous litter cleaning  events
#         self.history = jsonData['history']
#         # Number of days expected between cleanings
#         self.frequency = jsonData['period']


def loadData():
    if path.exists(DATA_FILE):
        # If the file exists, get data from it
        with open(DATA_FILE) as f:
            return json.load(f)
    else:
        # If file doesn't exist, return an empty LitterData
        return {'history': [], 'period': 3}


def saveNewData(newData):
    json.dump(newData, open(DATA_FILE, 'w'))


logging.info(f'Attempting to load data from {DATA_FILE}')
# Load data
try:
    data = loadData()
    logging.info("Data successfully loaded")
except json.decoder.JSONDecodeError as e:
    logging.error(f'Error loading JSON data: {e}')
    exit(1)

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('history', location="json")

# API Classes


# History
# shows a list of litter cleaning dates and lets you POST to add new cleanings
class History(Resource):
    def get(self):
        logging.info('History GET Request')
        return data['history']

    # TODO
    # right now my post just overwrites the whole history
    # Probably better to accept a post of a date and add it
    # to the history list.
    def post(self):
        logging.info('History POST Request')
        args = parser.parse_args()
        print(args)
        print(args['history'])
        # Replace in-memory data history with the passed in value
        newData = data
        try:
            newData['history'] = json.loads(args['history'])
        except json.decoder.JSONDecodeError as e:
            logging.error(e)
        saveNewData(newData)
        logging.info(f'Updated data history to \n{newData["history"]}')
        return newData['history'], 201


##
# Actually setup the Api resource routing here
##
api.add_resource(History, '/litter')


if __name__ == '__main__':
    app.run(debug=True)
