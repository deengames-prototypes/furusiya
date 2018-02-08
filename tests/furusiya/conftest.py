import pytest
import model.config as prod_config
import os

# Has to be done before other imports
path = os.path.join('furusiya', 'config.json')       
with open(path, 'rt') as f:
    raw_json = f.read()

prod_config.load(raw_json)

@pytest.fixture(scope='session', autouse=True)
def config(request):
    return prod_config