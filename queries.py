from postgres_db import connect, postgres_to_pd, params

conn = connect(params)


# En algunos queries el número de resultados está limitado debido al tamaño de la muestra.
# Sin embargo, para tratar con esto en un caso real podría agregarse paginación
def get_dataframe(metric):
    if metric == "monto_colocado":
        columns = ["transaction_date", "monto_colocado"]
        query = """SELECT distinct(date(transaction_date)) AS transaction_date,
        SUM(transaction_amount) OVER(PARTITION BY date(transaction_date))
        AS monto_colocado
        FROM transactions ORDER BY monto_colocado desc;"""

    elif metric == "numero_transacciones":
        columns = ["count"]
        query = """SELECT COUNT(*) FROM transactions;"""

    elif metric == "transacciones_por_cliente":
        columns = ["customer_id", "total_transaction", "customer_category"]
        query = """CREATE TEMP TABLE temp_customer_transactions AS
            SELECT distinct(customer_id), SUM(transaction_amount)
            OVER(PARTITION BY customer_id) AS total_transaction
            FROM transactions
            GROUP BY customer_id, transaction_amount
            ORDER BY total_transaction desc;

            SELECT t.customer_id, total_transaction, customer_category
            FROM temp_customer_transactions t
            JOIN customers c
            ON t.customer_id = c.customer_id
            ORDER BY total_transaction desc LIMIT 25;
            """

    elif metric == "cargos_por_retraso":
        columns = ["customer_id", "total_overdue_fee"]
        query = """SELECT distinct(customer_id),
                SUM(overdue_fee) OVER(PARTITION BY customer_id)
                AS total_overdue_fee
                FROM transactions
                GROUP BY customer_id, overdue_fee
                ORDER BY total_overdue_fee desc LIMIT 25;"""
    elif metric == "transacciones_por_distribuidor":
        columns = ["distributor_name", "distribution_center_name", "total_transaction"]
        query = """CREATE TEMP TABLE temp_distributors_transactions AS
        SELECT distinct(distribution_center_id), SUM(transaction_amount)
        OVER(PARTITION BY distribution_center_id) AS total_transaction
        FROM transactions
        GROUP BY distribution_center_id, transaction_amount;

        SELECT distributor_name, distribution_center_name, total_transaction
        FROM distributors d
        JOIN temp_distributors_transactions t
        ON d.distribution_center_id = t.distribution_center_id
        ORDER by total_transaction desc;"""
    df = postgres_to_pd(conn, query, columns)
    return df
