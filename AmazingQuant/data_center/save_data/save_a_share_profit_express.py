# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/22
# @Author  : gao
# @File    : save_a_share_profit_express.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime

import pandas as pd
import numpy as np
from mongoengine.fields import ListField, FloatField, IntField, DateTimeField, StringField

from AmazingQuant.data_center.database_field.field_a_share_finance_data import AShareProfitExpress
from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.utils.transfer_field import get_collection_property_list


class SaveProfitExpress(object):
    def __init__(self, data_path):
        self.data_df = pd.read_csv(data_path, low_memory=False)
        self.collection_property_list = get_collection_property_list(AShareProfitExpress)

    def save_a_share_profit_express(self):
        database = 'stock_base_data'
        with MongoConnect(database):
            doc_list = []
            for index, row in self.data_df.iterrows():
                row_dict = dict(row)
                row_dict['security_code'] = row_dict['S_INFO_WINDCODE']
                row_dict.pop('OBJECT_ID')
                row_dict.pop('S_INFO_WINDCODE')

                doc = AShareProfitExpress()

                for key, value in row_dict.items():
                    if key.lower() in self.collection_property_list:
                        property_name = AShareProfitExpress.__dict__[key.lower()]
                        if isinstance(property_name, StringField):
                            setattr(doc, key.lower(), str(value))
                        elif isinstance(property_name, DateTimeField):
                            if np.isnan(value):
                                setattr(doc, key.lower(), None)
                            else:
                                setattr(doc, key.lower(), datetime.strptime(str(int(value)), "%Y%m%d"))
                        else:
                            setattr(doc, key.lower(), value)
                doc_list.append(doc)
                if len(doc_list) > 999:
                    AShareProfitExpress.objects.insert(doc_list)
                    doc_list = []
            else:
                AShareProfitExpress.objects.insert(doc_list)


if __name__ == '__main__':
    data_path = '../../../../data/finance/ASHAREPROFITEXPRESS.csv'
    save_cash_flow_obj = SaveProfitExpress(data_path)
    save_cash_flow_obj.save_a_share_profit_express()
