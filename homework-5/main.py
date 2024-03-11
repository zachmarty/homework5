import json
from types import NoneType

import psycopg2

from config import config


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'my_new_db'

    params = config()
    conn = None

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")
                
                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")
                
                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")
                
                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY успешно добавлены")
                
                conn.commit()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params, db_name) -> None:
    con = psycopg2.connect(**params)
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('DROP DATABASE IF EXISTS ' + db_name + ';')
    cur.execute('CREATE DATABASE ' + db_name + ';')
    con.close() 
    cur.close()
    pass

def execute_sql_script(cur, script_file) -> None:
    cur.execute(open(script_file, 'r').read())



def create_suppliers_table(cur) -> None:
    cur.execute('DROP TABLE IF EXISTS suppliers;')
    cur.execute('CREATE TABLE suppliers(company_name varchar(40) not null unique, contact text not null, address text not null, phone varchar(20) not null, fax varchar(20), homepage varchar(100));')
    cur.execute('DROP TABLE IF EXISTS suppliers_products;')
    cur.execute('CREATE TABLE suppliers_products(company_name varchar(40) references suppliers (company_name), product_id int references products (product_id));')


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    counter = 0
    for supplier in suppliers:
        counter += 1
        name = supplier['company_name']
        cur.execute('insert into suppliers values (%s, %s, %s, %s, %s, %s)', (supplier['company_name'], supplier['contact'], supplier['address'], supplier['phone'], supplier['fax'], supplier['homepage']))


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    cur.execute('alter table products add supplier_company_name varchar(40) default null')
    data = get_suppliers_data(json_file)
    for supplier in data:
        name = supplier['company_name']
        for product in supplier['products']:
            try:
                cur.execute('update products set supplier_company_name = %s where product_name = %s', (name, product))
            except:
                pass
            


if __name__ == '__main__':
    main()
