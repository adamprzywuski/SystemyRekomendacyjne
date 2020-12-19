# This is a sample Python script.
import partner_data_reader as p
import optmizer as op
import per_partner_simulator as pq



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    #pk=p.Partner_data_reader("C0F515F0A2D0A5D9F854008BA76EB537.csv")
    #print(pk.how_many_dates)
    #print(pk.next_day(1))
    #optimizer=op.optimizer("0A2CEC84A65760AD90AA751C1C3DD861.csv",12.5,2)
    #print(optimizer.excluded_products)
    pp=pq.per_partner_simulator("04A66CE7327C6E21493DA6F3B9AACC75.csv")
    pp.all_info_about_partner()
    #print("dog")
    #print(pp.test)






# See PyCharm help at https://www.jetbrains.com/help/pycharm/
