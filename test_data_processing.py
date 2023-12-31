from data_processing import lamber93_to_gps, process_chunk, operator_mapping
import pandas as pd

from math import isclose

def test_lamber93_to_gps():
    x, y = 102980, 6847973
    expected_long, expected_lat = -5.088856, 48.456575
    long, lat = lamber93_to_gps(x, y)
    assert isclose(long, expected_long, abs_tol=1e-5)
    assert isclose(lat, expected_lat, abs_tol=1e-5)

def test_process_chunk():
    data = pd.DataFrame({
        'x': [102980],
        'y': [6847973],
        '2G': [1],
        '3G': [1],
        '4G': [0]
    })
    processed = process_chunk(data, 1)
    assert 'Longitude' in processed
    assert 'Latitude' in processed

def test_operator_mapping():
    data = pd.DataFrame({'Operateur': [20801, 20810]})
    data['Operateur'] = data['Operateur'].map(operator_mapping)
    assert all(data['Operateur'].isin(['Orange', 'SFR']))
