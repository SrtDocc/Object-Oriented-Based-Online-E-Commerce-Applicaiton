from datetime import datetime


class User:
    def __init__(self, username, password):
        self.username = str(username)
        self.password = str(password)
        self.basket = Basket()


class InventoryProduct:
    def __init__(self, name, price, stock_amount):
        self.name = str(name)
        self.price = float(price)
        self.stock_amount = float(stock_amount)


class Basket:
    def __init__(self):
        self.contents = {}
        self.total_value = 0

    def displayContents(self, currentUser):
        if len(currentUser.basket.contents) == 0:
            print("Your basket is empty! \n Total amount is: 0$")
            Market().showMarketMenu(currentUser)
        num = 1

        for key, value in currentUser.basket.contents.items():
            print(str(num), ".", key, "price=", value[1], "$", "amount=", value[0])
            num += 1
        print("Total value is: ", currentUser.basket.total_value, "$")

        self.showBasketSub(currentUser)

    def showBasketSub(self, currentUser):
        sub_menu = [("Update amount", 1), ("Remove an item", 2), ("Go back to main menu", 3)]
        for word, number in sub_menu:
            print(str(number), ".", str(word))

        option = int(input("Please choose an option: "))
        while option > 4 or option <= 0:
            print("Please provide a valid option!")
            option = int(input("Please choose an option: "))

        if option == 1:
            self.updateItem(currentUser)

        elif option == 2:
            self.removeItem(currentUser)

        elif option == 3:
            Market().showMarketMenu(currentUser)

    def updateItem(self, currentUser):
        update_item = input("Please type the name of the item you want to update the amount: (Enter 0 for basket menu)")

        while update_item not in currentUser.basket.contents.keys():
            print("No such item in your basket!")
            update_item = input("Please select the item you want to update the amount: (Enter 0 for basket menu)")
            if update_item == str(0):
                self.showBasketSub(currentUser)

        update_amount = int(input("Please enter new amount: "))

        while update_amount <= 0 or update_amount > Market.Inventory[update_item][0] + 1:
            print("Invalid amount to update!")
            update_amount = int(input("Please enter new amount: "))

        currentUser.basket.total_value -= currentUser.basket.contents[update_item][1] * \
                                          currentUser.basket.contents[update_item][0]
        Market.productInventory[update_item][0] += currentUser.basket.contents[update_item][0]
        currentUser.basket.contents[update_item][0] = update_amount
        Market.productInventory[update_item][0] -= update_amount
        currentUser.basket.total_value += currentUser.basket.contents[update_item][1] * update_amount
        self.showBasketSub(currentUser)

    def removeItem(self, currentUser):
        removal = input("Please select the item to be removed: (Enter 0 for basket menu)")

        while removal not in currentUser.basket.contents.keys():
            print("No such item in your basket!")
            removal = input("Please select the item to be removed: (Enter 0 for basket menu)")
            if removal == str(0):
                self.showBasketSub(currentUser)

        reamount = currentUser.basket.contents[removal][0]
        Market.productInventory[removal][0] += reamount
        currentUser.basket.total_value -= reamount*currentUser.basket.contents[removal][1]
        del currentUser.basket.contents[removal]
        self.showBasketSub(currentUser)


class Market:
    Inventory = {'asparagus': [10, 5], 'broccoli': [15, 6], 'carrots': [18, 7], 'apples': [20, 5],
                 'banana': [10, 8], 'berries': [30, 3], 'eggs': [50, 2], 'mixed fruit juice': [0, 8],
                 'fish sticks': [25, 12], 'ice cream': [32, 6], 'apple juice': [40, 7], 'orange juice': [30, 8],
                 'grape juice': [10, 9]}

    productInventory = {}

    for product in Inventory:
        invObject = InventoryProduct(product, Inventory[product][1], Inventory[product][0])
        productInventory[product] = [invObject.stock_amount, invObject.price]

    def __init__(self):

        john = User('john', 'john12')
        alex = User('alex', '123')

        self.users = {'john': john, 'alex': alex}


    def showMarketMenu(self, currentUser):

        menu = [("Search for a product", 1), ("See Basket", 2), ("Check Out", 3), ("Logout", 4), ("Exit", 5)]
        for word, number in menu:
            print(str(number), ".", str(word))

        self.choice = int(input("Your choice: "))
        while self.choice > 5 or self.choice <= 0:
            print("Invalid menu number!")
            self.choice = int(input("Your choice: "))

        if self.choice == 1:
            self.search(currentUser)

        elif self.choice == 2:
            Basket().displayContents(currentUser)

        elif self.choice == 3:
            self.checkout(currentUser)

        elif self.choice == 4:
            print("Logging out...")
            starter.login()

        elif self.choice == 5:
            exit()

    def search(self, currentUser):

        search_term = input("What are you looking for? (Enter 0 for main menu)")
        if search_term == str(0):
            self.showMarketMenu(currentUser)

        tuple_inventory = Market.productInventory.items()
        itemCount = 0
        itemList = []
        num = 1

        for key, value in tuple_inventory:
            if search_term in key and value[0] > 0:
                itemCount += 1
                itemList.append(key)

        print("{} similar items found.".format(itemCount))

        if itemCount == 0:
            print("No item found! Please search for another term.")
            self.search(currentUser)

        for itm in itemList:
            print(str(num), ".", str(itm), " ", Market.productInventory[itm][1], "$")
            num += 1

        choice1 = int(input("Please select the item number to add the item to your basket (Enter 0 for main menu):"))
        if choice1 == 0:
            self.showMarketMenu(currentUser)

        while choice1 not in range(itemCount + 1):
            print("Invalid item number!")
            choice1 = int(
                input("Please select the item number to add the item to your basket (Enter 0 for main menu):"))
            if choice1 == 0:
                self.showMarketMenu(currentUser)

        print("Adding ", itemList[choice1 - 1], " to the basket!")

        self.amount = int(input("Please enter the amount of the product: "))

        product = itemList[choice1 - 1]

        while self.amount > Market.productInventory[product][0]:
            print("Sorry! The amount exceeds the limit, Please try again with smaller amount!(Enter 0 for main menu)")
            self.amount = int(input("Please enter the amount of the product: "))
            if self.amount == str(0):
                self.showMarketMenu(currentUser)

        invobject = InventoryProduct(product, Market.productInventory[product][1], Market.productInventory[product][0])

        if product in currentUser.basket.contents:
            currentUser.basket.contents[product][0] += self.amount
            Market.productInventory[product][0] -= self.amount
            currentUser.basket.total_value += self.amount * invobject.price
            self.showMarketMenu(currentUser)

        currentUser.basket.contents[product] = [self.amount, invobject.price]
        Market.productInventory[product][0] -= self.amount
        currentUser.basket.total_value += self.amount * invobject.price
        self.showMarketMenu(currentUser)

    def checkout(self, currentUser):
        print("Processing your receipt...\n******* Git Online Market ********\n************************************\n"
              "www.github.com\n------------------------------------")
        num = 1
        for key, value in currentUser.basket.contents.items():
            print(str(num), ".", key, "price=", value[1], "$", "amount=", value[0])
            num += 1
        print("Total value is: ", currentUser.basket.total_value, "$")
        print("------------------------------------")
        print(datetime.today())
        print("------------------------------------")
        print("Thank You for using Git Market!")
        self.showMarketMenu(currentUser)

    def login(self):
        print("******Welcome to the Git Online Market******\nPlease provide your credentials to login")
        self.logged_user = input("Username: ")
        self.logged_password = input("Password: ")

        while self.logged_user not in self.users or self.logged_password != self.users[self.logged_user].password:
            print("Your user name and/or password is not correct. Please try again!")
            self.logged_user = input("Username: ")
            self.logged_password = input("Password: ")

        print("Successfully logged in!")
        print(
            "Welcome, {}! Please choose one of the following options by entering the corresponding menu number.".format(
                self.logged_user))

        self.currentUser = self.users[self.logged_user]
        self.showMarketMenu(self.currentUser)


starter = Market()
starter.login()

