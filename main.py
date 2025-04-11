import sqlite3


def create_connection():
    return sqlite3.connect("D:/Python Project/BDpart1/t1.db")


def print_all_products(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT p.id, p.name, p.price, c.name 
            FROM products p 
            JOIN categories c ON p.category_id = c.id
        """
    )
    products = cursor.fetchall()

    if not products:
        print("Нет товаров в базе данных.")
        return

    print("\nСписок всех товаров:")
    print("ID   Название            Цена      Категория")
    print("-" * 45)
    for product in products:
        print(f"{product[0]:<5} {product[1]:<20} {product[2]:<10} {product[3]:<10}")


def print_all_categories(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()

    if not categories:
        print("Нет категорий в базе данных.")
        return

    print("\nСписок категорий:")
    print("ID   Название  ")
    print("-" * 15)
    for category in categories:
        print(f"{category[0]:<5} {category[1]:<20}")


def add_product(conn):
    print("\nДобавление нового товара")

    if (name := input("Введите название товара: ")) == "":
        print("Вы должны были указать имя!")
        return

    if not (price := input("Введите цену товара: ")).isdigit():
        print("Цена должна быть положительным числом!")
        return

    price = int(price)

    print_all_categories(conn)
    try:
        category_id = int(input("Введите ID категории товара: "))
    except:
        print("ID категории должен быть числом!")
        return

    # Проверяем существование категории
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categories WHERE id = ?", (category_id,))
    if not cursor.fetchone():
        print("Категории с таким ID не существует!")
        return

    # Добавляем товар
    cursor.execute(
        "INSERT INTO products (name, price, category_id) VALUES (?, ?, ?)",
        (name, price, category_id),
    )
    conn.commit()
    print("Товар успешно добавлен!")


def add_category(conn):
    """Добавляет новую категорию"""
    print("\nДобавление новой категории")
    name = input("Введите название категории: ")

    if not name:
        print("Название категории не может быть пустым!")
        return

    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    print("Категория успешно добавлена!")


def delete_product(conn):
    """Удаляет товар по ID"""
    print("\nУдаление товара")
    print_all_products(conn)

    try:
        product_id = int(input("Введите ID товара для удаления: "))
    except:
        print("ID товара должен быть числом!")
        return

    cursor = conn.cursor()
    # Проверяем существование товара
    cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
    if not cursor.fetchone():
        print("Товара с таким ID не существует!")
        return

    # Удаляем товар
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    print("Товар успешно удален!")


def main():
    conn = create_connection()

    while True:
        print("\nМеню:")
        print("1. Вывести все товары")
        print("2. Вывести список категорий")
        print("3. Добавить товар")
        print("4. Добавить категорию")
        print("5. Удалить товар")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            print_all_products(conn)
        elif choice == "2":
            print_all_categories(conn)
        elif choice == "3":
            add_product(conn)
        elif choice == "4":
            add_category(conn)
        elif choice == "5":
            delete_product(conn)
        elif choice == "0":
            print("Выход из программы...")
            break
        else:
            print("Неверный ввод. Попробуйте еще раз.")

    conn.close()


if __name__ == "__main__":
    main()
