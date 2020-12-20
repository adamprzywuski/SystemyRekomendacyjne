import numpy as np
import partner_data_reader as p
import random
import pandas as pd


class bank_of_one_dim_UCBs_optimizer:
    def __init__(self, partner_id):
        self.UCB_factors_for_products = None
        self.partner_id = partner_id
        # self.avg_click_cost = avg_click_cost
        # self.NPM = NPM
        self.day_by_day_many_partners_data_of_not_exclude_products = []
        self.products_seen_so_far = []
        self.per_product_NPG = {}

        self.producsts = set()
        self.UCB_beta = 2.5
        pk = p.partner_data_reader(self.partner_id)
        # self.get_UCB_factors_for_products(pk.next_day(1), self.NPM)

    def get_UCB_factors_for_products(self, new_per_product_NPG_factors_statistics, NPM):
        UCB_factors_for_products = {}
        for product_id in new_per_product_NPG_factors_statistics:
            if product_id not in self.per_product_NPG and product_id != "-1":
                self.per_product_NPG[product_id] = []
            if (product_id != "-1"):
                temp_total_Sales = new_per_product_NPG_factors_statistics[product_id]["total_Sales"]
                temp_number_of_clicks = new_per_product_NPG_factors_statistics[product_id]["number_of_clicks"]
                temp_clicks_cost = temp_number_of_clicks * self.avg_click_cost
                temp_profit_gain = temp_total_Sales * self.NPM
                temp_clicks_NPG = temp_profit_gain = temp_clicks_cost
                self.per_product_NPG[product_id].append(temp_clicks_NPG)
            for product_id in self.per_product_NPG:
                if product_id not in UCB_factors_for_products:
                    UCB_factors_for_products[product_id] = {}
                UCB_factors_for_products[product_id]["mean"] = np.mean(self.per_product_NPG[product_id])
                UCB_factors_for_products[product_id]["std"] = np.std(self.per_product_NPG[product_id])
        self.UCB_factors_for_products = UCB_factors_for_products


class optimizer:
    def __init__(self, partner_id):
        self.partner_id = partner_id
        # self.avg_click_cost = avg_click_cost
        # self.NPM = NPM
        pk = p.partner_data_reader(self.partner_id)
        self.UCB_beta = 2.5
        #self.bank_of_one_dim_UCBs_optimizer = bank_of_one_dim_UCBs_optimizer(self.partner_id)



    def get_excluded_products_pseudorandomly(self, date):
        dummy_list_of_potentially_excluded_products = list(date)

        dummy_list_of_potentially_excluded_products.sort()

        #print(len(dummy_list_of_potentially_excluded_products))
        dummy_how_many_products = round(len(dummy_list_of_potentially_excluded_products) / 20)
        #print(dummy_how_many_products)

        random.seed(12)
        excluded_products = random.sample(dummy_list_of_potentially_excluded_products, dummy_how_many_products)
        return excluded_products
