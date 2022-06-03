from pulp import *
import json



class LpObject:
    drinkMixer = LpProblem('drinkMixer', LpMinimize)
    lpJson = ''
    ingredientsList = []
    pricesList = []
    currentValues = []


    def solveForJson(self, jsonIn):
                self.lpJson = json.loads(jsonIn)
                self.setVariables()
                self.setPrices()
                self.setConstraints()
                self.drinkMixer.solve()
                for ingredient in self.ingredientsList:
                    print(ingredient.varValue)

    def setVariables(self):
        for ingredient in self.lpJson["ingredients"]:
             self.ingredientsList.append(LpVariable(ingredient["name"], lowBound = 0, cat = LpContinuous))


    def getProperties(self, which):
        self.currentValues.clear()
        for ingredient in self.lpJson["ingredients"]:
            self.currentValues.append(ingredient["properties"][which])


    def setPrices(self):
        self.getProperties("price")
        self.drinkMixer += LpAffineExpression([(self.ingredientsList[i], self.currentValues[i]) for i in range(len(self.ingredientsList))])


    def setConstraint(self, which):
        self.getProperties(which)
        for value in self.lpJson["values"]:
            if value["values"]["type"] == "l" and value["name"] == which:
                self.drinkMixer += LpConstraint(LpAffineExpression([(self.ingredientsList[i], self.currentValues[i]) for i in range(len(self.currentValues))]), sense = LpConstraintLE, rhs = value["values"]["value"])
            elif value["values"]["type"] == "g" and value["name"] == which:
                self.drinkMixer += LpConstraint(LpAffineExpression([(self.ingredientsList[i], self.currentValues[i]) for i in range(len(self.currentValues))]), sense = LpConstraintGE, rhs = value["values"]["value"])


    def setConstraints(self):
        self.drinkMixer += LpConstraint(LpAffineExpression([(self.ingredientsList[i], self.currentValues[i]) for i in range(len(self.currentValues))]), sense = LpConstraintEQ, rhs = 5)
        categories = ["calories", "fats", "carbohydrate", "proteins", "fiber", "alcohol"]
        for category in categories:
            self.setConstraint(category)
        print(self.drinkMixer)

    def getSolution(self):
        response = "{"
        for ingredient in self.ingredientsList:
            response += '\'{}\':{},'.format(ingredient.name, ingredient.varValue) #ingredient.name + "\':" + ingredient.varValue + ","
        response = response[:-1]
        response += "}"
        return response