import pandas as pd
import partner_data_splitter as p


class partner_data_reader():
    def __init__(self, partner_id):
        self.partner_id = partner_id
        self.dataOfPartner=self._data()
        self.how_many_dates=self.how_many()

    def _data(self):
        path = r'C:\Users\AdamPrzywuski\PycharmProjects\Systemy\partners_id_datasets\\'
        partner_id_dataset = pd.read_csv(path + self.partner_id, sep="\t", header=0,
                                         nrows=None)
        grouped_dataset = partner_id_dataset.groupby("date")

        return grouped_dataset

    def how_many(self):
        i=0
        for date, df_group_for_date in self.dataOfPartner:
            i=i+1
        return i

    def next_day(self, which_day):
        i = 0

        for date, df_group_for_date in self.dataOfPartner:
            if i == which_day:
                return df_group_for_date

            i = i + 1

        #print("The next day don't exist. The numbers of day are " + str(i))
