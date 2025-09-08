import pandas as pd

IMAGE_PATH = 'assets/FLOORPLAN.svg'

events_data_path = 'data/event_data.csv'
event_data = pd.read_csv(events_data_path)

MAP_POSITIONS_PATH = 'data/POSITIONS.JSON'
MAP_POSITIONS = pd.read_json(MAP_POSITIONS_PATH)

MAP_LOCATIONS_PATH = 'data/LOCATIONS.JSON'
MAP_LOCATIONS = pd.read_json(MAP_LOCATIONS_PATH)
