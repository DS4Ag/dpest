import dpest.wheat.utils as utils

def test_uplantgro_runs():
    # Just verify that the function runs without raising an error
    utils.uplantgro(
        './DSSAT48_data/Wheat/PlantGro.OUT',
        '164.0 KG N/HA IRRIG',
        ['LAID', 'CWAD', 'T#AD']
    )