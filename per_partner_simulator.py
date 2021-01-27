import partner_data_reader as p
import optmizer as opp
import json
import matplotlib.pyplot as plt


class per_partner_simulator():
    def __init__(self, partner_id):
        self.partner_id = partner_id
        self.k = p.partner_data_reader(self.partner_id)
        self.productsToExclude = set()
        self.productsSeenSoFarNextDay = set()
        self.productsSeenSoFar=set()
        self.productsActuallyExcluded = set()
        self.day = ""
        self.group_info_about_days = []
        self.json_score = {"days_of_A.Przywuski": self.group_info_about_days}
        self.sales_amount_in_euro = 0
        self.numbers_of_clicks = 0
        self.per_partner_averge_click_cost = 0
        self.how_many_days = self.k.how_many_dates
        self.list_of_profit_net=[]
        self.list_of_accumulated=[]

    def getting_value_of_averge_click_cost(self):
        for i in range(0, self.how_many_days):
            self._getting_sales_and_click(i)
        self.per_partner_averge_click_cost = (self.sales_amount_in_euro * 0.12) / self.numbers_of_clicks
        print("For the partnerId = " + self.partner_id + "\nthe number of click was " + str(self.numbers_of_clicks)
              + "\nand the all sales_amount was " + str(self.sales_amount_in_euro) +
              "\nThat means the ACC was " + str(self.per_partner_averge_click_cost))

    def all_info_about_partner(self):

        # print(self.how_many_days)
        self._first_time()
        for i in range(1, self.how_many_days):
            self._getting_sales_on_click_per_day(i)
        path = r'C:\Users\AdamPrzywuski\PycharmProjects\Systemy\logs\\'
        with open(path+"log_"+self.partner_id+".json", "w") as outfile:
            json.dump(self.json_score, outfile)
        self._displaying_graph()
        self._displaying_accumulated_graph()
        self._displaying_accumulated_graph_ratio()


    def _getting_sales_and_click(self,i):
        date_in_day = self.k.next_day(i)
        for rows in date_in_day.itertuples(index=True):
            # getting data from single days
            sale = getattr(rows, "Sale")
            money = getattr(rows, "SalesAmountInEuro")
            if sale != -1:
                self.numbers_of_clicks = self.numbers_of_clicks + 1
            if money > 0:
                self.sales_amount_in_euro = self.sales_amount_in_euro + money

    def _getting_sales_on_click_per_day(self, i):
        date_in_day = self.k.next_day(i)
        self.day = date_in_day.iloc[0]["date"]
        # here i should json data
        full_day=set()
        for rows in date_in_day.itertuples(index=True):
            # getting data from single days

            full_day.add(getattr(rows, "product_id"))
            #self.productsSeenSoFarNextDay.add(getattr(rows, "product_id"))

        # getting the new excluded day

        self.productsActuallyExcluded = full_day.intersection(self.productsToExclude)
        self._getting_daily_per_excluded(date_in_day)
        #self.productsSeenSoFar - self.productsActuallyExcluded
        self._saving_to_json()
        self.productsSeenSoFarNextDay=self.productsSeenSoFarNextDay.union(full_day)
        self.go_to_optimizer(self.productsSeenSoFarNextDay)

    def _first_time(self):
        date_in_day = self.k.next_day(0)
        self.day = date_in_day.iloc[1]["date"]
        # here i should json data
        self._saving_to_json()
        full_day=set()
        for rows in date_in_day.itertuples(index=True):

            # getting data from single days
            sale = getattr(rows, "Sale")
            money = getattr(rows, "SalesAmountInEuro")

            self.productsSeenSoFarNextDay.add(getattr(rows, "product_id"))
        # getting the new excluded day

        self.productsActuallyExcluded = self.productsSeenSoFarNextDay.intersection(self.productsToExclude)
        self.productsSeenSoFar=self.productsSeenSoFarNextDay

        self.go_to_optimizer(self.productsSeenSoFarNextDay)

    def go_to_optimizer(self, list_):
        op = opp.optimizer(self.partner_id)
        self.productsToExclude = op.get_excluded_products_pseudorandomly(list_)

    def _saving_to_json(self):
        self.group_info_about_days.append(
            {
                "day": self.day,
                "productsToExclude": sorted(self.productsToExclude),
                "productsSeenSoFar": sorted(self.productsSeenSoFarNextDay),
                "productsActuallyExcluded": sorted(self.productsActuallyExcluded)
            }
        )

    def _getting_daily_per_excluded(self,date_in_day):
        daily_per_excluded_product_total_number_of_clicks=0
        daily_per_excluded_product_total_salesAmountInEuro=0
        for excluded_products in self.productsActuallyExcluded:
            for rows in date_in_day.itertuples(index=True):
                if(excluded_products==getattr(rows, "product_id")):
                    sale = getattr(rows, "Sale")
                    money = getattr(rows, "SalesAmountInEuro")

                    #self.productsSeenSoFarNextDay.add(getattr(rows, "product_id"))
                    if sale != -1:
                        daily_per_excluded_product_total_number_of_clicks = daily_per_excluded_product_total_number_of_clicks + 1
                    if money != -1:
                        daily_per_excluded_product_total_salesAmountInEuro = daily_per_excluded_product_total_salesAmountInEuro + money

        daily_per_excluded_product_net_profit_gain=daily_per_excluded_product_total_number_of_clicks * self.per_partner_averge_click_cost -daily_per_excluded_product_total_salesAmountInEuro * 0.22
        print("The profit day of "+self.day+" was "+ str(daily_per_excluded_product_net_profit_gain))
        self.list_of_profit_net.append(daily_per_excluded_product_net_profit_gain)

    def _displaying_graph(self):
        plt.plot(self.list_of_profit_net,label=self.partner_id)
        plt.title(self.partner_id)
        plt.ylabel("Euro")
        plt.xlabel("Day")
        plt.savefig("graphs\\"+self.partner_id+".pdf")
        plt.close()

    def _displaying_accumulated_graph(self):

        for n in range(len(self.list_of_profit_net)):
            i=0
            for k in range(n):
                i=i+self.list_of_profit_net[k]
            self.list_of_accumulated.append(i)
        plt.ylabel("Accumulated profit gain")
        plt.xlabel("Day")
        plt.plot(self.list_of_accumulated, label=self.partner_id+"_accumulated")
        plt.title(self.partner_id+" Accumulated graph")
        plt.savefig("graphs_accumulated\\"+self.partner_id+".pdf")
        plt.close()

    def _displaying_accumulated_graph_ratio(self):

        list=[]
        for n in range(len(self.list_of_profit_net)):
            if self.list_of_accumulated[n]!=0:
                list.append((self.list_of_profit_net[n]/self.list_of_accumulated[n]))
            else:
                list.append(0)
        plt.ylabel("Accumulated profit gain ratio")
        plt.xlabel("Day")
        plt.plot(list, label=self.partner_id+"_accumulated_ratio")
        plt.title(self.partner_id+" Accumulated graph")
        plt.savefig("graphs_accumulated_ratio\\"+self.partner_id+".pdf")




