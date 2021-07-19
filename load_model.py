import pandas as pd
import logging
import sqlalchemy
import os

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = sqlalchemy.create_engine('postgresql://postgres:postgres@localhost:5438/postgres')


def load_dataframes():
    customers = pd.read_csv(os.path.dirname(__file__)+'data_files/Customers.csv')
    transactions = pd.read_csv(os.path.dirname(__file__)+'data_files/Transactions.csv')
    distributors = pd.read_csv(os.path.dirname(__file__)+'data_files/Distributor.csv')
    # para reemplazar mayúsculas y espacios en los nombres de las columnas
    # a postgres no le gustan las mayúsculas
    customers.columns = [x.lower().strip().replace(" ", "_") for x in customers.columns]
    transactions.columns = [x.lower().strip().replace(" ", "_") for x in transactions.columns]
    distributors.columns = [x.lower().strip().replace(" ", "_") for x in distributors.columns]

    # insertar los dataframes de pandas en las tablas
    customers.to_sql("customers",
                     engine,
                     if_exists="append",
                     index=False,
                     dtype={'customer_id': sqlalchemy.types.NUMERIC,
                            'customer_category': sqlalchemy.types.String,
                            'affiliation_date': sqlalchemy.types.Date,
                            'conversion_date': sqlalchemy.types.Date})
    distributors.to_sql("distributors",
                        engine,
                        if_exists="append",
                        index=False,
                        dtype={'distributor_id': sqlalchemy.types.Integer,
                               'distributor_name': sqlalchemy.types.String,
                               'distribution_center_id': sqlalchemy.types.Integer,
                               'distribution_center_name': sqlalchemy.types.String})

    transactions.to_sql("transactions",
                        engine,
                        if_exists="append",
                        index=False,
                        dtype={'customer_id': sqlalchemy.types.Integer,
                               'distribution_cender_id': sqlalchemy.types.Integer,
                               'transaction_amount': sqlalchemy.types.Float,
                               'fee': sqlalchemy.types.Float,
                               'overdue_fee': sqlalchemy.types.Float,
                               'total': sqlalchemy.types.Float,
                               'transaction_date': sqlalchemy.types.DateTime})


if __name__ == '__main__':
    load_dataframes()
