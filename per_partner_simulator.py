import optmizer as op
import partner_data_reader as p

class per_partner_simulator():
    def __init__(self,partner_id):
        self.partner_id=partner_id
        self.k=p.Partner_data_reader(self.partner_id)

        self.how_many_days=self.k.how_many_dates


    def all_info_about_partner(self):
        i=0
        list=[]
        for i in range(0,self.how_many_days):
            list.append(self._getting_sales_on_click_per_day(i))
        print(list)







    def _getting_sales_on_click_per_day(self,i):
        date_in_day = self.k.next_day(i)
        sales_amount_in_euro=0
        numbers_of_clicks=0
        for rows in date_in_day.itertuples(index=True):
            sale=getattr(rows, "Sale")
            money=getattr(rows,"SalesAmountInEuro")
            if (sale!=-1):
                numbers_of_clicks=numbers_of_clicks+1
            if(money!=-1):
                sales_amount_in_euro=sales_amount_in_euro+money
        return sales_amount_in_euro*0.12/numbers_of_clicks


