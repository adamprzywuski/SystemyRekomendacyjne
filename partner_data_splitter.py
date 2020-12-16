import pandas as pd
import time
from datetime import datetime
import os


dtypes = {"Sale": 'int64', "SalesAmountInEuro": 'float64', "time_delay_for_conversion": 'int64',
          "click_timestamp": 'int64',
          "nb_clicks_1week": 'int64', "product_price": 'float64', "product_age_group": 'object',
          "device_type": 'object',
          "audience_id": 'object', "product_gender": 'object', "product_brand": 'object',
          "product_category(1-7)": 'object',
          "product_id": 'object', "product_title": 'object', "partner_id": 'object', "user_id": 'object'}

name = ["Sale", "SalesAmountInEuro", "time_delay_for_conversion", "click_timestamp", "nb_clicks_1week", "product_price",
        "product_age_group", "device_type", "audience_id", "product_gender", "product_brand", "product_category1","product_category2","product_category3",
        "product_category4","product_category5","product_category6","product_category7",
        "product_country", "product_id", "product_title", "partner_id", "user_id"]
partners_selected_for_test_parameter_for_Mr_Riegel_20201103 = ["C0F515F0A2D0A5D9F854008BA76EB537",
                                                               "E3DDEB04F8AFF944B11943BB57D2F620",
                                                               "E68029E9BCE099A60571AF757CBB6A08"]



def loading_dataset():
    raw_dataset_df = pd.read_csv("CriteoSearchData", sep="\t", names=name, header=None)
    print(raw_dataset_df.dtypes)

    print(raw_dataset_df.head(10))
    return raw_dataset_df






def df_groups_for_partners_testing():
    start = time.time()
    print("hello")

    df_groups_for_partners = loading_dataset().groupby("partner_id")
    print(df_groups_for_partners.head(3))
    for partner_id, df_group_for_partner in df_groups_for_partners:
        if partner_id in partners_selected_for_test_parameter_for_Mr_Riegel_20201103:
            test_parameter_for_Mr_Riegel_20201103 = df_group_for_partner.shape[0]
            # print(df_group_for_partner.head(3))
            print("test_parameter_for_Mr_Riegel_20201103 for partner_id " + partner_id + " : ",
                  test_parameter_for_Mr_Riegel_20201103)
    end = time.time()
    print(end - start)


def df_groups_for_partners():
    #time to run on full dataset 1889.835s
    start=time.time()
    df_groups_for_partners = loading_dataset().groupby("partner_id")
    for partner_id, df_group_for_partner in df_groups_for_partners:
        # if partner_id in all_partners_id:
        #test_parameter_for_Mr_Riegel_20201103 = df_group_for_partner.shape[0]
        # print("test_parameter_for_Mr_Riegel_20201103 for partner_id " + partner_id + " : ",
        #     test_parameter_for_Mr_Riegel_20201103)
        temp_df = pd.DataFrame(df_group_for_partner)
        #print(temp_df['click_timestamp'])
        temp_df['date'] = temp_df['click_timestamp'].apply(lambda x: str(pd.to_datetime(int(x), unit='s').date()))
        temp_df.sort_values(by=['date'],inplace=True)
        path=r'C:\Users\AdamPrzywuski\PycharmProjects\pythonProject\partners_id_datasets\\'
        temp_df.to_csv(path+partner_id+'.csv',sep="\t")

    end = time.time()
    print(end - start)






if __name__ == '__main__':
    print("dog")
    df_groups_for_partners()
