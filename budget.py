class Category:

    def __init__(self, name) -> None:
        """
        """
        self.name = name
        self.ledger = []
        self.balance = 0


    def deposit(self, amount, description = ""):
        """
        """
        self.ledger.append({"amount": amount, "description": description})
        self.balance += amount


    def withdraw(self, amount, description = ""):
        """
        """
        if amount <= self.balance:
            self.ledger.append({"amount": -1 * amount, "description": description})
            self.balance -= amount
            return True
        else:
            return False


    def get_balance_calc(self):
        """Calculates balance from the ledger instead of using self.balance attribute.

        This method can substitute get_balance or can be called in get_balance
        if the dynamic calculation of the balance is preferred.
        """
        balance = 0
        for record in self.ledger:
            balance += record["amount"]
        return balance


    def get_balance(self):
        """
        """
        return self.balance


    def transfer(self, amount, dest_category):
        """
        """
        if self.withdraw(amount, f"Transfer to {dest_category.name}"):
            dest_category.deposit(amount, f"Transfer from {self.name}")
            return True
        else:
            return False


    def check_funds(self, amount):
        """
        """
        return True if amount <= self.balance else False


    def __str__(self) -> str:
        """
        """
        line_length = 30    # max length of the line
        
        # title
        margin = (line_length - len(self.name)) // 2
        title =  margin * '*' + self.name + (line_length - len(self.name) - margin) * '*'
        print_out = title + "\n"

        # ledger
        for record in self.ledger:
            desc = record["description"] if len(record["description"]) <= 23 else record["description"][0:23]
            amount = f"{record['amount']:.2f}"
            space = (line_length - len(desc) - len(amount)) * ' '
            line = desc + space + amount
            print_out += line + "\n"
        
        # Total
        print_out += f"Total: {self.balance}"
        
        return print_out
            

    def spent(self):
        """Return sum of spendings itn the category presented as non negative number
        """
        spendings = [record['amount']for record in self.ledger if record['amount'] < 0]
        return sum(spendings) * -1


    def is_in_total_percentage(self, total_spendings, percentage):
        """Check percentage of the total_spendings

        Parameters
        ----------
            total_spendings : number
                total spendings from all categories
            percentage: number
                the percentage that the category should be checked against

        Return True if the category spendings in relation to the given spendings
        is greater or equal of the given percentage.
        """
        if total_spendings is None or total_spendings == 0: return None
        spent_percentage_of_total = int((self.spent() / total_spendings) * 100)
        return True if spent_percentage_of_total >= percentage else False
    

    def print_char_in_spent_chart(self, line_type, line_index = None, total_spendings = None):
        """Print a char in the spent_chart

        Parameters
        ----------
            line_type : str in ["P","N"]
                P - percentage
                N - name
                S - separation
            line_index : number
                index of the line depending on the line_type
                    100 - 0 for P 
                    0 - max name length for N
            total_spendings : num
                required for line_type == P
        """
        if line_type == "P":
            return " o " if self.is_in_total_percentage(total_spendings, line_index) else "   "
        elif line_type == "N":
            return f" {self.name[line_index]} " if len(self.name) >= line_index + 1 else "   "
        elif line_type == "S":
            return "---"
        else:
            return ""
        


        
    




    




def create_spend_chart(categories):
    """
    """
    line_index_percentage = [p for p in range(100,-1,-10)]
    max_name_length = max([len(category.name) for category in categories])
    line_index_name = [i for i in range(0,max_name_length)]
    total_spendings = sum([category.spent() for category in categories])

    print_out = ""
    
    # print percentage part
    print_out = "Percentage spent by category\n"
    for line_index in line_index_percentage:
        line = f"{line_index:3}|"
        for category in categories:
            line += category.print_char_in_spent_chart("P", line_index, total_spendings)
        print_out += line + " \n"
    
    # print separation
    line = "    "
    for category in categories:
        line += category.print_char_in_spent_chart("S")
    print_out += line + "-\n"
    
    # print names
    for line_index in line_index_name:
        line = "    "
        for category in categories:
            line += category.print_char_in_spent_chart("N", line_index)
        print_out += line + " \n"
    
    return print_out.strip("\n")
