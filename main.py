# This is a sample Python script.
import partner_data_reader as p
import optmizer as op
import per_partner_simulator as pq



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    pk=p.Partner_data_reader("0B569D05041C6C038C28D92E9C3C2220.csv")
    print(pk.how_many_dates)
    #print(pk.next_day(1))
    #optimizer=op.optimizer("0A2CEC84A65760AD90AA751C1C3DD861.csv",12.5,2)
    #print(optimizer.excluded_products)
    pp=pq.per_partner_simulator("0A2CEC84A65760AD90AA751C1C3DD861.csv")
    pp.all_info_about_partner()
    #print("dog")
    #print(pp.test)






# See PyCharm help at https://www.jetbrains.com/help/pycharm/
