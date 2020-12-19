import partner_data_reader as p
import optmizer as opp
import json


class per_partner_simulator():
    def __init__(self, partner_id):
        self.partner_id = partner_id
        self.k = p.partner_data_reader(self.partner_id)
        self.productsToExclude = set()
        self.productsSeenSoFar = set()
        self.productsActuallyExcluded = set()
        self.day = ""
        self.group_info_about_days = []
        self.json_score = {"days": self.group_info_about_days}
        self.sales_amount_in_euro = 0
        self.numbers_of_clicks = 0
        self.per_partner_averge_click_cost = 0
        self.how_many_days = self.k.how_many_dates

    def getting_value_of_averge_click_cost(self):
        for i in range(0, self.how_many_days):
            self._getting_sales_on_click_per_day(i)
        self.per_partner_averge_click_cost = (self.sales_amount_in_euro * 0.12) / self.numbers_of_clicks
        print("For the partnerId= " + self.partner_id + "\n the number of click was " + str(self.numbers_of_clicks)
              + "\n and the all sales_amount was " + str(self.sales_amount_in_euro) +
              "\n That means the CPM was " + str(self.per_partner_averge_click_cost))

    def all_info_about_partner(self):

        # print(self.how_many_days)

        for i in range(0, self.how_many_days):
            self._getting_sales_and_click(i)
        with open("log.json", "w") as outfile:
            json.dump(self.json_score, outfile)


    def _getting_sales_and_click(self,i):
        date_in_day = self.k.next_day(i)
        for rows in date_in_day.itertuples(index=True):

            # getting data from single days
            sale = getattr(rows, "Sale")
            money = getattr(rows, "SalesAmountInEuro")
            if sale != -1:
                self.numbers_of_clicks = self.numbers_of_clicks + 1
            if money != -1:
                self.sales_amount_in_euro = self.sales_amount_in_euro + money

    def _getting_sales_on_click_per_day(self, i):
        date_in_day = self.k.next_day(i)
        self.day = date_in_day.iloc[1]["date"]
        # here i should json data
        self._saving_to_json()
        for rows in date_in_day.itertuples(index=True):

            # getting data from single days
            sale = getattr(rows, "Sale")
            money = getattr(rows, "SalesAmountInEuro")

            self.productsSeenSoFar.add(getattr(rows, "product_id"))
            if sale != -1:
                self.numbers_of_clicks = self.numbers_of_clicks + 1
            if money != -1:
                self.sales_amount_in_euro = self.sales_amount_in_euro + money
        # getting the new excluded day

        self.productsActuallyExcluded = self.productsSeenSoFar.intersection(self.productsToExclude)
        self.productsSeenSoFar - self.productsActuallyExcluded
        self.go_to_optimizer(self.productsSeenSoFar)

    def go_to_optimizer(self, list_):
        op = opp.optimizer(self.partner_id)
        self.productsToExclude = op.get_excluded_products_pseudorandomly(list_)

    def _saving_to_json(self):
        self.group_info_about_days.append(
            {
                "day": self.day,
                "productsToExclude": sorted(self.productsToExclude),
                "productsSeenSoFar": sorted(self.productsSeenSoFar),
                "productsActuallyExcluded": sorted(self.productsActuallyExcluded)
            }
        )
