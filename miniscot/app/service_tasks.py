
def CustomerBuyingSimulation(parameters):
    print("CustomerBuyingSimulation: {}".format(parameters))
    return (1)

def DemandForecasting(parameters):
    print("DemandForecasting: {}".format(parameters))
    return (2)

def InventoryOrderingSimulation(parameters):
    print("InventoryOrderingSimulation: {}".format(parameters))
    return (3)

def ProfitCalculator(parameters):
    print("ProfitCalculator: {}".format(parameters))
    return (4)

TASKS = {'CustomerBuyingSimulation': CustomerBuyingSimulation, 'DemandForecasting': DemandForecasting, 'InventoryOrderingSimulation': InventoryOrderingSimulation, 'ProfitCalculator': ProfitCalculator}
