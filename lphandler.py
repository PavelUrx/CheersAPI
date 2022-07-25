from pulp import *
import json


class LpObject:
    drinkMixer = LpProblem('drinkMixer', LpMinimize)
    lpJson = ''
    ingredientsList = []
    pricesList = []
    currentValues = []

    #Reseni soucasti LP problemu
    def solveForJson(self, jsonIn):
                self.drinkMixer = LpProblem('drinkMixer', LpMinimize)
                self.lpJson = json.loads(jsonIn)
                self.setVariables()
                self.setPrices()
                self.setConstraints()
                self.drinkMixer.solve()
                for ingredient in self.ingredientsList:
                    print(ingredient.varValue)

    #Nastavuje promenne problemu lp z dat z json
    def setVariables(self):
        for ingredient in self.lpJson["ingredients"]:
             self.ingredientsList.append(LpVariable(ingredient["name"], lowBound = 0, cat = LpContinuous))

    #Nastavuje vlastnosti vybranou vlastnost pro kazdou zvolenou ingredienci
    def getProperties(self, which):
        self.currentValues.clear()
        for ingredient in self.lpJson["ingredients"]:
            self.currentValues.append(ingredient["properties"][which])

    #Nastavuje cenovy vektor LP promennych
    def setPrices(self):
        self.getProperties("price")
        self.drinkMixer += LpAffineExpression([(self.ingredientsList[i], self.currentValues[i]) for i in range(len(self.ingredientsList))])

    #Pridava urcitou podminku do modelu LP
    def setConstraint(self, which):
        self.getProperties(which)
        for value in self.lpJson["values"]:
            if value["values"]["type"] == "l" and value["name"] == which:
                self.drinkMixer += LpConstraint(LpAffineExpression([(self.ingredientsList[i], self.currentValues[i]) for i in range(len(self.ingredientsList))]), sense = LpConstraintGE, rhs = value["values"]["value"])
            elif value["values"]["type"] == "g" and value["name"] == which:
                self.drinkMixer += LpConstraint(LpAffineExpression([(self.ingredientsList[i], self.currentValues[i]) for i in range(len(self.ingredientsList))]), sense = LpConstraintLE, rhs = value["values"]["value"])

    #Zpracovava vsechny podminky z jsonu
    def setConstraints(self):
        self.drinkMixer += LpConstraint(LpAffineExpression([(self.ingredientsList[i], self.currentValues[i]) for i in range(len(self.currentValues))]), sense = LpConstraintEQ, rhs = 1)
        categories = ["calories", "fats", "carbohydrate", "proteins", "fiber", "alcohol"]
        for category in categories:
            self.setConstraint(category)
        #print(self.drinkMixer)

    #vraci json soubor reseni a restartuje resitel problemu LP
    def getSolution(self):
        response = "{\"ingredients\": {"
        for ingredient in self.ingredientsList:
            response += '\"{}\":{},'.format(ingredient.name, ingredient.varValue)
        response = response[:-1]
        response += "}}"
        self.ingredientsList.clear()
        self.pricesList.clear()
        self.currentValues.clear()
        return response