import psycopg2
from psycopg2 import IntegrityError
import os
from dotenv import *

load_dotenv()


def db_connect():
    database = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    return database


def db_check_user(chat_id: int) -> tuple | None:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM web_admin_users WHERE user_telegram = %s
    ''', (chat_id,))
    user = cursor.fetchone()
    database.close()
    return user


def db_register_user(chat_id: int, full_name: str) -> None:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO web_admin_users(user_telegram, user_name) VALUES (%s,%s)
    ''', (chat_id, full_name))
    database.commit()
    database.close()


def db_update_user(chat_id: int, phone: str) -> None:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    UPDATE web_admin_users SET user_phone = %s WHERE user_telegram = %s
    ''', (phone, chat_id))
    database.commit()
    database.close()


def db_create_user_cart(chat_id: int) -> None:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO web_admin_carts(user_id) VALUES
    (
        (SELECT id FROM web_admin_users WHERE user_telegram = %s)
    )
    ''', (chat_id,))

    database.commit()
    database.close()


def db_get_categories() -> list:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM web_admin_categories;
    ''')
    categories = cursor.fetchall()
    database.close()
    return categories


def db_get_products(category_id: int) -> list:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    SELECT id, product_name FROM web_admin_products WHERE product_category_id = %s
    ''', (category_id,))
    products = cursor.fetchall()
    database.close()
    return products


def db_get_product(product_id: int) -> tuple:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM web_admin_products WHERE id = %s
    ''', (product_id,))
    product = cursor.fetchone()
    database.close()
    return product


def db_get_user_cart(chat_id: int) -> tuple:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT web_admin_carts.id, web_admin_carts.total_price, web_admin_carts.total_products
    FROM web_admin_carts JOIN web_admin_users 
    ON web_admin_carts.user_id = web_admin_users.id
    WHERE user_telegram = %s;
    ''', (chat_id,))
    cart_id = cursor.fetchone()
    database.close()
    return cart_id


def db_update_to_cart(price: int, quantity: int, cart_id: int) -> None:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    UPDATE web_admin_carts SET total_price=%s, total_products=%s WHERE id = %s
    ''', (price, quantity, cart_id))
    database.commit()
    database.close()


def db_get_product_by_name(product_name: str) -> tuple:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_price, product_info, product_image
    FROM web_admin_products WHERE product_name = %s
    ''', (product_name,))
    product_info = cursor.fetchone()
    database.close()
    return product_info


def db_ins_or_upd_finally_cart(
        cart_id: int, product_name: str, total_products: int, total_price: int
) -> bool:
    database = db_connect()
    cursor = database.cursor()
    try:
        cursor.execute('''
        INSERT INTO web_admin_finally_carts (cart_id, product_name, product_quantity, final_price )
        VALUES (%s, %s, %s, %s)
        ''', (cart_id, product_name, total_products, total_price))
        return True
    except IntegrityError:
        cursor.execute('''
        UPDATE web_admin_finally_carts SET product_quantity = %s,  final_price = %s
        WHERE product_name = ? AND cart_id = %s
        ''', (total_products, total_price, product_name, cart_id))
        return False
    finally:
        database.commit()
        database.close()


def db_get_cart_products(chat_id: int, delete: bool = False) -> list:
    if delete:
        columns = '''
                  web_admin_finally_carts.id, 
                  web_admin_finally_carts.product_name
                  '''
    else:
        columns = '''
                  web_admin_finally_carts.product_name, 
                  web_admin_finally_carts.product_quantity, 
                  web_admin_finally_carts.final_price,
                  web_admin_finally_carts.cart_id
                  '''

    database = db_connect()
    cursor = database.cursor()
    cursor.execute(f'''
    SELECT {columns}
    FROM web_admin_finally_carts 
    JOIN web_admin_carts 
          ON web_admin_finally_carts.cart_id = web_admin_carts.id
    JOIN web_admin_users
          ON web_admin_carts.user_id = web_admin_users.id
    WHERE user_telegram = %s;
    ''', (chat_id,))
    products = cursor.fetchall()
    database.close()
    return products


def db_delete_product(finally_id: int) -> None:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM web_admin_finally_carts WHERE id = %s
    ''', (finally_id,))
    database.commit()
    database.close()


def db_get_final_price(chat_id: int) -> int | None:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
    SELECT sum(web_admin_finally_carts.final_price) 
    FROM web_admin_finally_carts 
    JOIN web_admin_carts 
        ON web_admin_carts.id = web_admin_finally_carts.cart_id
    JOIN web_admin_users 
        ON web_admin_users.id = web_admin_carts.user_id 
    WHERE web_admin_users.user_telegram = %s
    ''', (chat_id,))
    summary_price = cursor.fetchone()
    database.close()
    return summary_price[0]


def clear_finally_cart(cart_id: int) -> None:
    database = db_connect()
    cursor = database.cursor()
    cursor.execute('''
     DELETE FROM web_admin_finally_carts WHERE cart_id = %s
    ''', (cart_id,))
    database.commit()
    database.close()
