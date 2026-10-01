class order():
    def __init__(self, id, s, p, quant):
        self.OrderID = id
        self.CreateTime = None  ## int; will be generated in main
        self.Side = s
        self.Price = p
        self.Quantity = quant

class execution():
    def __init__(self, id, p, quant, sellid, buyid):
        self.ExecutionID = id
        self.Price = p
        self.Quantity = quant
        self.SellOrderID = sellid
        self.BuyOrderID = buyid


### main ###

buyBook = []
sellBook = []
time = 0
execs = 1

def trade(order):
    global buyBook, sellBook, time, execs
    order.CreateTime = time
    currentExec = []

    if order.Side == "Buy":
        buyBook.append(order)
        buyBook = sorted(buyBook, key=lambda order: (-order.Price, order.CreateTime))
    else:
        sellBook.append(order)
        sellBook = sorted(sellBook, key=lambda order: (order.Price, order.CreateTime))

    for buyOrder in buyBook:
        for sellOrder in sellBook:
            if buyOrder.Price >= sellOrder.Price and buyOrder.Quantity > 0 and sellOrder.Quantity > 0:
                if buyOrder.Quantity >= sellOrder.Quantity:
                    quant = sellOrder.Quantity
                    buyOrder.Quantity -= sellOrder.Quantity
                    sellOrder.Quantity = 0
                else:
                    quant = buyOrder.Quantity
                    sellOrder.Quantity -= buyOrder.Quantity
                    buyOrder.Quantity = 0
                currentExec.append(execution(execs, sellOrder.Price, quant, sellOrder.OrderID, buyOrder.OrderID))
                print("Execution #", execs, "!! ID:", currentExec[-1].ExecutionID, "Price: $", currentExec[-1].Price, "Quantity:", currentExec[-1].Quantity, "Buy ID:", currentExec[-1].BuyOrderID, "Sell ID:", currentExec[-1].SellOrderID)
                execs += 1

    print("BUY BOOK:")
    for i in buyBook:
        if i.Quantity > 0:
            print(i.OrderID, "$", i.Price, i.Quantity)
    print("SELL BOOK:")
    for i in sellBook:
        if i.Quantity > 0:
            print(i.OrderID, "$", i.Price, i.Quantity)
    print()

    execSet = set()
    execSet.update(currentExec)
    
    time += 1
    if not execSet:
        return None
    return(execSet)

trade(order("Buy-1", "Buy", 9.99, 300))
trade(order("Buy-2", "Buy", 10.00, 200))
trade(order("Sell-1", "Sell", 10.01, 300))
trade(order("Sell-2", "Sell", 10.00, 100))
trade(order("Sell-3", "Sell", 9.99, 200))
trade(order("Sell-4", "Sell", 10.00, 200))
trade(order("Buy-3", "Buy", 10.00, 300))
trade(order("Sell-5", "Sell", 10.01, 500))
trade(order("Buy-4", "Buy", 10.01, 200))
trade(order("Buy-5", "Buy", 10.01, 300))
