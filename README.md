# final_task_pazyko
Coffe For Me project

Launch project through the main.py module.

Accept the following commandline arguments:

 1.User name.
 2.When user role has been selected, user can select available actions or logout.
 3.User position. (1-Manager or 2-Salesman are available).
 4.Beverage type (1-CAPPUCHINO, 2-MOCCACHINO, 3-AMERICANO or 0 to continue order) . Available for salesmen position only.
 5.Additional beverage ingredients (1-CINNAMON, 2-SUGAR, 3-MILK or 0 to continue order). Available for salesmen position only.
 6.Get the beverage price (after order is served). Available for salesmen position only.
 7.Save the sale details in additional separate bill (file). Available for salesmen position only.
 8.Save the sales details for every salesman (in a database).
 9.Show the summary of all the sales records, in case the utility is started by manager.
 
See an example of such a summary below:

Seller name |  Number of sales |  Total Value ($)

John        |  13              |  340

Mary        |  3               |  124

Total:      |  16              |  464

Though the data can be submitted through commandline arguments, the script must provide additional interactive input.

Handle exceptions for incorrect/invalid arguments and entered values, both for commandline args and in interactive mode.

Some details and requirements may not be covered, use common sense for the program flow creation and document it properly in README.txt file.

