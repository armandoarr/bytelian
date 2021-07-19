-- create customers table
CREATE TABLE IF NOT EXISTS customers (
  customer_id serial NOT NULL,
  customer_category varchar(255),
  affiliation_date timestamp,
  conversion_date timestamp,
  PRIMARY KEY(customer_id)
);




-- create distributors table
CREATE TABLE IF NOT EXISTS distributors (
  distributor_id INT NOT NULL,
  distributor_name varchar(255) NOT NULL,
  distribution_center_id serial NOT NULL,
  distribution_center_name varchar(255),
  PRIMARY KEY(distribution_center_id)
);


CREATE TABLE IF NOT EXISTS transactions (
  customer_id serial NOT NULL,
  distribution_center_id INT NOT NULL,
  transaction_amount double precision,
  fee double precision,
  overdue_fee double precision,
  total double precision,
  transaction_date timestamp,
  FOREIGN KEY(distribution_center_id) REFERENCES distributors(distribution_center_id)
);
