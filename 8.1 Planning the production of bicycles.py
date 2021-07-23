from pyomo.environ import *

# 0. Dataa
MONTHS = list(range(1, 13))
CNORM = 32
COVER = 40
CSTOCK = 5
ISTOCK = 2000
CAP = 30000
DEM = {1:30000, 2:15000, 3:15000, 4:25000, 5:33000, 6:40000, 7:45000, 8:45000, 9:26000, 10:14000, 11:25000, 12:30000}
# 1. Create a model
model = ConcreteModel()

# 2. Instantiate the model
# 2.1 declare decision variables
model.pnorm = Var(MONTHS, within=NonNegativeIntegers)
model.pover = Var(MONTHS, within=NonNegativeIntegers)
model.store = Var(MONTHS, within=NonNegativeIntegers)
# 2.2 declare objective function
model.cost = Objective(expr=sum([model.pnorm[i]*CNORM + model.pover[i]*COVER + model.store[i]*CSTOCK for i in MONTHS]), sense = minimize)
# 2.3 declare constraints
def conCapNorm_rule(model,i):
    return model.pnorm[i] <= CAP
model.conCapNorm = Constraint(MONTHS, rule=conCapNorm_rule)


def conCapOver_rule(model,i):
    return model.pover[i] <= 0.5*CAP
model.conCapOver = Constraint(MONTHS, rule=conCapOver_rule)


def storeEq_rule(model,i):
    if i == 1:
        return model.pnorm[i]+model.pover[i]+ISTOCK==DEM[i]+model.store[i]
    else:
        return model.pnorm[i]+model.pover[i]+model.store[i-1]==DEM[i]+model.store[i]

model.storeEq = Constraint(MONTHS,rule=storeEq_rule)

# 3. Apply solver
opt = SolverFactory('cplex')
result = opt.solve(model)

# 4. Print results
model.pnorm.pprint()
model.pover.pprint()
model.store.pprint()
print(model.cost())
result.write()

