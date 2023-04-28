from enum import Enum

class FoodType(str, Enum):
    WHEAT = "Wheat"
    MEAT = "Meat"
    VEGGIE = "Veggie"
    FRUIT = "Fruit"
    ALCOHOLIC_BEVERAGE = "Alcoholic Beverage"
    MILK = "Milk"
    CHEESE = "Cheese"
    BEANS = "Beans"
    NUTS = "Nuts"

    def __str__(self) -> str:
        return self.value


