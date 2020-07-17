import json
import logging
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from os import path
from utilities import getBulletList


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
        logging.info('File exists. Attempting to read. ')
        # If the file exists, get data from it
        with open(DATA_FILE) as f:
            return json.load(f)
    else:
        logging.info('No file exists - creating a new one.')
        # If file doesn't exist, return an empty LitterData
        return {'cleanings': [], 'period': 3}


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
parser.add_argument('cleaning_date', location="json")

# I'm not making a Cleaning class at the moment because
# I don't see a reason to get a specific date or edit it
# ...yet.


class CleaningHistory(Resource):
    def get(self):
        logging.info('CleaningHistory GET Request')
        logging.info(data)
        return data['cleanings']

    def post(self):
        logging.info('CleaningHistory POST Request')
        args = parser.parse_args()
        # Replace in-memory data history with the passed in value
        newCleaning = args['cleaning_date']
        data['cleanings'].append(newCleaning)
        saveNewData(data)
        logging.info(f'Added "{newCleaning}" to history.')
        return newCleaning, 201


##
# Actually setup the Api resource routing here
##
api.add_resource(CleaningHistory, '/litter/cleanings')


if __name__ == '__main__':
    app.run(debug=True)
