"""
BookStore Microservice - Sample Data Seeder
Run this script after all services are up: python seed_data.py
"""
import requests
import time
import sys

CUSTOMER_URL = "http://localhost:8001"
BOOK_URL = "http://localhost:8002"
CART_URL = "http://localhost:8003"
STAFF_URL = "http://localhost:8004"
MANAGER_URL = "http://localhost:8005"
CATALOG_URL = "http://localhost:8006"
ORDER_URL = "http://localhost:8007"
SHIP_URL = "http://localhost:8008"
PAY_URL = "http://localhost:8009"
REVIEW_URL = "http://localhost:8010"
RECOMMEND_URL = "http://localhost:8011"


def post(url, data):
    try:
        r = requests.post(url, json=data, timeout=10)
        if r.status_code in (200, 201):
            print(f"  [OK] {url} -> {r.json().get('id', '')}")
            return r.json()
        else:
            print(f"  [FAIL] {url} -> {r.status_code}: {r.text[:100]}")
            return None
    except Exception as e:
        print(f"  [ERROR] {url} -> {e}")
        return None


def wait_for_services():
    print("Waiting for services to be ready...")
    services = [
        ("customer-service", f"{CUSTOMER_URL}/customers/"),
        ("book-service", f"{BOOK_URL}/books/"),
        ("cart-service", f"{CART_URL}/carts/1/"),
        ("staff-service", f"{STAFF_URL}/staffs/"),
        ("manager-service", f"{MANAGER_URL}/managers/"),
        ("catalog-service", f"{CATALOG_URL}/catalogs/"),
        ("order-service", f"{ORDER_URL}/orders/"),
        ("review-service", f"{REVIEW_URL}/reviews/"),
        ("recommender-service", f"{RECOMMEND_URL}/recommendations/"),
    ]
    for name, url in services:
        for attempt in range(10):
            try:
                requests.get(url, timeout=3)
                print(f"  {name}: ready")
                break
            except Exception:
                if attempt == 9:
                    print(f"  {name}: NOT READY (skipping)")
                time.sleep(2)


def seed():
    print("\n" + "=" * 50)
    print("  BookStore Sample Data Seeder")
    print("=" * 50)

    wait_for_services()

    # ── Catalogs ──
    print("\n--- Creating Catalogs ---")
    catalogs = [
        {"name": "Fiction", "description": "Novels, short stories, and literary fiction"},
        {"name": "Science & Technology", "description": "Computer science, physics, mathematics"},
        {"name": "History", "description": "World history, biographies, and historical events"},
        {"name": "Business", "description": "Management, entrepreneurship, and economics"},
        {"name": "Self-Help", "description": "Personal development and motivation"},
    ]
    for c in catalogs:
        post(f"{CATALOG_URL}/catalogs/", c)

    # ── Books ──
    print("\n--- Creating Books ---")
    # catalog_id: 1=Fiction, 2=Science & Technology, 3=History, 4=Business, 5=Self-Help
    books_data = [
        {"title": "Moby Dick", "author": "Herman Melville", "price": "13.99", "stock": 20, "catalog_id": 1},
{"title": "War and Peace", "author": "Leo Tolstoy", "price": "19.99", "stock": 18, "catalog_id": 1},
{"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "price": "14.99", "stock": 25, "catalog_id": 1},
{"title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky", "price": "16.99", "stock": 22, "catalog_id": 1},
{"title": "Anna Karenina", "author": "Leo Tolstoy", "price": "15.99", "stock": 24, "catalog_id": 1},
{"title": "Jane Eyre", "author": "Charlotte Bronte", "price": "12.99", "stock": 30, "catalog_id": 1},
{"title": "Wuthering Heights", "author": "Emily Bronte", "price": "11.99", "stock": 28, "catalog_id": 1},
{"title": "Dracula", "author": "Bram Stoker", "price": "13.49", "stock": 27, "catalog_id": 1},
{"title": "Frankenstein", "author": "Mary Shelley", "price": "12.49", "stock": 29, "catalog_id": 1},
{"title": "The Odyssey", "author": "Homer", "price": "14.49", "stock": 26, "catalog_id": 1},

{"title": "Refactoring", "author": "Martin Fowler", "price": "47.99", "stock": 15, "catalog_id": 2},
{"title": "Code Complete", "author": "Steve McConnell", "price": "54.99", "stock": 12, "catalog_id": 2},
{"title": "You Don't Know JS", "author": "Kyle Simpson", "price": "29.99", "stock": 25, "catalog_id": 2},
{"title": "Eloquent JavaScript", "author": "Marijn Haverbeke", "price": "27.99", "stock": 20, "catalog_id": 2},
{"title": "Head First Design Patterns", "author": "Eric Freeman", "price": "44.99", "stock": 18, "catalog_id": 2},
{"title": "Cracking the Coding Interview", "author": "Gayle Laakmann McDowell", "price": "39.99", "stock": 22, "catalog_id": 2},
{"title": "The Clean Coder", "author": "Robert C. Martin", "price": "34.99", "stock": 19, "catalog_id": 2},
{"title": "Deep Learning", "author": "Ian Goodfellow", "price": "72.99", "stock": 10, "catalog_id": 2},
{"title": "Hands-On Machine Learning", "author": "Aurelien Geron", "price": "49.99", "stock": 17, "catalog_id": 2},
{"title": "Database System Concepts", "author": "Silberschatz, Korth, Sudarshan", "price": "79.99", "stock": 14, "catalog_id": 2},

{"title": "The Diary of a Young Girl", "author": "Anne Frank", "price": "13.99", "stock": 35, "catalog_id": 3},
{"title": "Long Walk to Freedom", "author": "Nelson Mandela", "price": "18.99", "stock": 20, "catalog_id": 3},
{"title": "Steve Jobs", "author": "Walter Isaacson", "price": "21.99", "stock": 25, "catalog_id": 3},
{"title": "Becoming", "author": "Michelle Obama", "price": "19.99", "stock": 28, "catalog_id": 3},
{"title": "Educated", "author": "Tara Westover", "price": "17.99", "stock": 30, "catalog_id": 3},
{"title": "The Immortal Life of Henrietta Lacks", "author": "Rebecca Skloot", "price": "16.99", "stock": 22, "catalog_id": 3},
{"title": "Into the Wild", "author": "Jon Krakauer", "price": "15.99", "stock": 24, "catalog_id": 3},
{"title": "Unbroken", "author": "Laura Hillenbrand", "price": "18.49", "stock": 21, "catalog_id": 3},
{"title": "Outliers", "author": "Malcolm Gladwell", "price": "16.49", "stock": 40, "catalog_id": 3},
{"title": "Blink", "author": "Malcolm Gladwell", "price": "15.49", "stock": 38, "catalog_id": 3},

{"title": "Start with Why", "author": "Simon Sinek", "price": "17.99", "stock": 34, "catalog_id": 4},
{"title": "The $100 Startup", "author": "Chris Guillebeau", "price": "16.99", "stock": 29, "catalog_id": 4},
{"title": "Rework", "author": "Jason Fried", "price": "18.99", "stock": 26, "catalog_id": 4},
{"title": "Crushing It!", "author": "Gary Vaynerchuk", "price": "19.49", "stock": 23, "catalog_id": 4},
{"title": "Measure What Matters", "author": "John Doerr", "price": "20.99", "stock": 21, "catalog_id": 4},
{"title": "The E-Myth Revisited", "author": "Michael E. Gerber", "price": "17.49", "stock": 27, "catalog_id": 4},
{"title": "Blue Ocean Strategy", "author": "W. Chan Kim", "price": "22.49", "stock": 19, "catalog_id": 4},
{"title": "Hooked", "author": "Nir Eyal", "price": "18.49", "stock": 28, "catalog_id": 4},
{"title": "Made to Stick", "author": "Chip Heath", "price": "17.99", "stock": 30, "catalog_id": 4},
{"title": "Drive", "author": "Daniel Pink", "price": "16.99", "stock": 32, "catalog_id": 4},

{"title": "Can't Hurt Me", "author": "David Goggins", "price": "19.99", "stock": 45, "catalog_id": 5},
{"title": "Deep Work", "author": "Cal Newport", "price": "17.99", "stock": 40, "catalog_id": 5},
{"title": "Digital Minimalism", "author": "Cal Newport", "price": "16.99", "stock": 35, "catalog_id": 5},
{"title": "The Subtle Art of Not Giving a F*ck", "author": "Mark Manson", "price": "18.99", "stock": 50, "catalog_id": 5},
{"title": "12 Rules for Life", "author": "Jordan Peterson", "price": "19.49", "stock": 33, "catalog_id": 5},
{"title": "The Mountain Is You", "author": "Brianna Wiest", "price": "15.99", "stock": 37, "catalog_id": 5},
{"title": "Awaken the Giant Within", "author": "Tony Robbins", "price": "20.99", "stock": 29, "catalog_id": 5},
{"title": "Unlimited Power", "author": "Tony Robbins", "price": "18.49", "stock": 27, "catalog_id": 5},
{"title": "Make Your Bed", "author": "William H. McRaven", "price": "14.49", "stock": 42, "catalog_id": 5},
{"title": "Grit", "author": "Angela Duckworth", "price": "16.49", "stock": 36, "catalog_id": 5},
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": "12.99", "stock": 50, "catalog_id": 1},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "price": "14.99", "stock": 35, "catalog_id": 1},
        {"title": "1984", "author": "George Orwell", "price": "11.99", "stock": 60, "catalog_id": 1},
        {"title": "Pride and Prejudice", "author": "Jane Austen", "price": "9.99", "stock": 40, "catalog_id": 1},
        {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "price": "13.50", "stock": 25, "catalog_id": 1},
        {"title": "The Alchemist", "author": "Paulo Coelho", "price": "12.49", "stock": 38, "catalog_id": 1},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "price": "15.99", "stock": 32, "catalog_id": 1},
        {"title": "Dune", "author": "Frank Herbert", "price": "18.99", "stock": 28, "catalog_id": 1},
        {"title": "The Road", "author": "Cormac McCarthy", "price": "14.99", "stock": 22, "catalog_id": 1},
        {"title": "Brave New World", "author": "Aldous Huxley", "price": "13.99", "stock": 30, "catalog_id": 1},
        {"title": "Clean Code", "author": "Robert C. Martin", "price": "39.99", "stock": 20, "catalog_id": 2},
        {"title": "Design Patterns", "author": "Gang of Four", "price": "49.99", "stock": 15, "catalog_id": 2},
        {"title": "Python Crash Course", "author": "Eric Matthes", "price": "35.99", "stock": 30, "catalog_id": 2},
        {"title": "Microservices Patterns", "author": "Chris Richardson", "price": "44.99", "stock": 18, "catalog_id": 2},
        {"title": "The Pragmatic Programmer", "author": "David Thomas", "price": "42.99", "stock": 22, "catalog_id": 2},
        {"title": "Introduction to Algorithms", "author": "Cormen, Leiserson, Rivest, Stein", "price": "89.99", "stock": 12, "catalog_id": 2},
        {"title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell & Peter Norvig", "price": "79.99", "stock": 14, "catalog_id": 2},
        {"title": "The Innovators", "author": "Walter Isaacson", "price": "17.99", "stock": 25, "catalog_id": 2},
        {"title": "Sapiens", "author": "Yuval Noah Harari", "price": "16.99", "stock": 45, "catalog_id": 3},
        {"title": "Guns, Germs, and Steel", "author": "Jared Diamond", "price": "18.99", "stock": 26, "catalog_id": 3},
        {"title": "The Silk Roads", "author": "Peter Frankopan", "price": "19.99", "stock": 20, "catalog_id": 3},
        {"title": "Team of Rivals", "author": "Doris Kearns Goodwin", "price": "21.99", "stock": 18, "catalog_id": 3},
        {"title": "The Wright Brothers", "author": "David McCullough", "price": "17.50", "stock": 22, "catalog_id": 3},
        {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "price": "15.99", "stock": 28, "catalog_id": 5},
        {"title": "Atomic Habits", "author": "James Clear", "price": "18.99", "stock": 55, "catalog_id": 5},
        {"title": "The Power of Habit", "author": "Charles Duhigg", "price": "16.99", "stock": 40, "catalog_id": 5},
        {"title": "Mindset", "author": "Carol S. Dweck", "price": "14.99", "stock": 37, "catalog_id": 5},
        {"title": "The 7 Habits of Highly Effective People", "author": "Stephen R. Covey", "price": "19.99", "stock": 32, "catalog_id": 5},
        {"title": "The Lean Startup", "author": "Eric Ries", "price": "22.99", "stock": 33, "catalog_id": 4},
        {"title": "Rich Dad Poor Dad", "author": "Robert Kiyosaki", "price": "14.99", "stock": 42, "catalog_id": 4},
        {"title": "Zero to One", "author": "Peter Thiel", "price": "18.99", "stock": 28, "catalog_id": 4},
        {"title": "Good to Great", "author": "Jim Collins", "price": "21.99", "stock": 24, "catalog_id": 4},
        {"title": "The Hard Thing About Hard Things", "author": "Ben Horowitz", "price": "19.99", "stock": 30, "catalog_id": 4},
    ]

    manga_cover_pool = [
        "https://m.media-amazon.com/images/I/81YOuOGFCJL._UF1000,1000_QL80_.jpg",
        "https://dummyimage.com/360x520/1f2937/ffffff&text=Naruto+Volume+1",
        "https://dummyimage.com/360x520/7c2d12/ffffff&text=Dragon+Ball+Volume+1",
        "https://dummyimage.com/360x520/0f766e/ffffff&text=Detective+Conan+Volume+1",
        "https://dummyimage.com/360x520/1d4ed8/ffffff&text=Bleach+Volume+1",
        "https://dummyimage.com/360x520/991b1b/ffffff&text=Attack+on+Titan+Volume+1",
        "https://dummyimage.com/360x520/7e22ce/ffffff&text=Demon+Slayer+Volume+1",
        "https://dummyimage.com/360x520/334155/ffffff&text=Jujutsu+Kaisen+Volume+1",
    ]

    for idx, b in enumerate(books_data):
        b["picture_url"] = manga_cover_pool[idx % len(manga_cover_pool)]

    books = []
    for b in books_data:
        result = post(f"{BOOK_URL}/books/", b)
        if result:
            books.append(result)

    # ── Customers (auto-creates carts) ──
    print("\n--- Creating Customers (+ auto cart) ---")
    customers_data = [
        {"name": "Nguyen Van An", "email": "an.nguyen@email.com", "password": "123456"},
        {"name": "Tran Thi Binh", "email": "binh.tran@email.com", "password": "123456"},
        {"name": "Le Hoang Cuong", "email": "cuong.le@email.com", "password": "123456"},
        {"name": "Pham Minh Duc", "email": "duc.pham@email.com", "password": "123456"},
        {"name": "Vo Thanh Em", "email": "em.vo@email.com", "password": "123456"},
        {"name": "Hoang Thi Phuong", "email": "phuong.hoang@email.com", "password": "123456"},
        {"name": "Dang Quoc Gia", "email": "gia.dang@email.com", "password": "123456"},
        {"name": "Bui Van Hung", "email": "hung.bui@email.com", "password": "123456"},
    ]
    customers = []
    for c in customers_data:
        result = post(f"{CUSTOMER_URL}/customers/", c)
        if result:
            customers.append(result)

    # ── Staff ──
    print("\n--- Creating Staff ---")
    staff_data = [
        {"name": "Nguyen Thi Lan", "email": "lan.nguyen@bookstore.com", "position": "Librarian", "password": "123456"},
        {"name": "Tran Van Minh", "email": "minh.tran@bookstore.com", "position": "Cashier", "password": "123456"},
        {"name": "Le Thi Ngoc", "email": "ngoc.le@bookstore.com", "position": "Inventory Manager", "password": "123456"},
        {"name": "Pham Quoc Bao", "email": "bao.pham@bookstore.com", "position": "Sales Associate", "password": "123456"},
        {"name": "Vo Hoang Nam", "email": "nam.vo@bookstore.com", "position": "IT Support", "password": "123456"},
    ]
    for s in staff_data:
        post(f"{STAFF_URL}/staffs/", s)

    # ── Managers ──
    print("\n--- Creating Managers ---")
    managers_data = [
        {"name": "Dr. Tran Dinh Que", "email": "que.tran@bookstore.com", "department": "Operations"},
        {"name": "Nguyen Thanh Son", "email": "son.nguyen@bookstore.com", "department": "Sales"},
        {"name": "Le Minh Tuan", "email": "tuan.le@bookstore.com", "department": "Technology"},
    ]
    for m in managers_data:
        post(f"{MANAGER_URL}/managers/", m)

    # ── Add Cart Items ──
    print("\n--- Adding Items to Carts ---")
    if books and customers:
        cart_items = [
            {"cart": 1, "book_id": 1, "quantity": 2},
            {"cart": 1, "book_id": 6, "quantity": 1},
            {"cart": 1, "book_id": 13, "quantity": 1},
            {"cart": 2, "book_id": 3, "quantity": 1},
            {"cart": 2, "book_id": 9, "quantity": 1},
            {"cart": 3, "book_id": 8, "quantity": 2},
            {"cart": 3, "book_id": 10, "quantity": 1},
            {"cart": 4, "book_id": 11, "quantity": 1},
            {"cart": 4, "book_id": 12, "quantity": 1},
            {"cart": 5, "book_id": 14, "quantity": 3},
        ]
        for item in cart_items:
            post(f"{CART_URL}/cart-items/", item)

    # ── Orders (auto-creates payments and shipments) ──
    print("\n--- Creating Orders (+ auto payment & shipment) ---")
    orders_data = [
        {
            "customer_id": 1,
            "items": [
                {"book_id": 1, "quantity": 1, "price": "12.99"},
                {"book_id": 6, "quantity": 1, "price": "39.99"},
            ],
            "payment_method": "credit_card",
            "shipping_address": "123 Le Loi, District 1, Ho Chi Minh City",
        },
        {
            "customer_id": 2,
            "items": [
                {"book_id": 3, "quantity": 2, "price": "11.99"},
                {"book_id": 13, "quantity": 1, "price": "18.99"},
            ],
            "payment_method": "bank_transfer",
            "shipping_address": "456 Tran Hung Dao, Hoan Kiem, Hanoi",
        },
        {
            "customer_id": 3,
            "items": [
                {"book_id": 8, "quantity": 1, "price": "35.99"},
                {"book_id": 9, "quantity": 1, "price": "44.99"},
                {"book_id": 10, "quantity": 1, "price": "42.99"},
            ],
            "payment_method": "credit_card",
            "shipping_address": "789 Nguyen Hue, Hai Chau, Da Nang",
        },
        {
            "customer_id": 4,
            "items": [
                {"book_id": 11, "quantity": 1, "price": "16.99"},
            ],
            "payment_method": "cash",
            "shipping_address": "321 Hung Vuong, Ninh Kieu, Can Tho",
        },
        {
            "customer_id": 1,
            "items": [
                {"book_id": 14, "quantity": 1, "price": "22.99"},
                {"book_id": 15, "quantity": 1, "price": "14.99"},
            ],
            "payment_method": "debit_card",
            "shipping_address": "123 Le Loi, District 1, Ho Chi Minh City",
        },
        {
            "customer_id": 5,
            "items": [
                {"book_id": 2, "quantity": 1, "price": "14.99"},
                {"book_id": 4, "quantity": 1, "price": "9.99"},
                {"book_id": 5, "quantity": 1, "price": "13.50"},
            ],
            "payment_method": "credit_card",
            "shipping_address": "55 Phan Chu Trinh, Hue City",
        },
    ]
    for o in orders_data:
        post(f"{ORDER_URL}/orders/", o)

    # ── Reviews ──
    print("\n--- Creating Reviews ---")
    reviews_data = [
        {"customer_id": 1, "book_id": 1, "rating": 5, "comment": "A masterpiece of American literature. Fitzgerald's prose is beautiful."},
        {"customer_id": 1, "book_id": 6, "rating": 5, "comment": "Essential reading for every developer. Changed how I write code."},
        {"customer_id": 2, "book_id": 3, "rating": 4, "comment": "Chilling and prophetic. More relevant today than ever."},
        {"customer_id": 2, "book_id": 13, "rating": 5, "comment": "Practical advice that actually works. Highly recommend!"},
        {"customer_id": 3, "book_id": 8, "rating": 4, "comment": "Great for beginners. Clear explanations and good projects."},
        {"customer_id": 3, "book_id": 9, "rating": 5, "comment": "The definitive guide to microservices architecture. A must-read."},
        {"customer_id": 3, "book_id": 10, "rating": 4, "comment": "Timeless advice for software developers. Still very relevant."},
        {"customer_id": 4, "book_id": 11, "rating": 5, "comment": "Fascinating journey through human history. Couldn't put it down."},
        {"customer_id": 5, "book_id": 2, "rating": 5, "comment": "A powerful story about justice and compassion. Truly moving."},
        {"customer_id": 5, "book_id": 4, "rating": 4, "comment": "Witty and charming. Austen at her finest."},
        {"customer_id": 6, "book_id": 12, "rating": 4, "comment": "Eye-opening insights into how we think and make decisions."},
        {"customer_id": 6, "book_id": 14, "rating": 3, "comment": "Some good ideas but a bit repetitive in parts."},
        {"customer_id": 7, "book_id": 7, "rating": 5, "comment": "Classic software engineering reference. Every pattern is well explained."},
        {"customer_id": 7, "book_id": 15, "rating": 4, "comment": "Simple financial advice that everyone should hear early in life."},
        {"customer_id": 8, "book_id": 5, "rating": 3, "comment": "Interesting character study but not for everyone."},
    ]
    for r in reviews_data:
        post(f"{REVIEW_URL}/reviews/", r)

    # ── Recommendations ──
    print("\n--- Creating Recommendations ---")
    recommendations_data = [
        {"customer_id": 1, "book_id": 9, "score": 95.5, "reason": "Based on your interest in Clean Code"},
        {"customer_id": 1, "book_id": 10, "score": 88.0, "reason": "Popular among developers who read Clean Code"},
        {"customer_id": 1, "book_id": 7, "score": 82.3, "reason": "Complements your software engineering reading"},
        {"customer_id": 2, "book_id": 11, "score": 91.0, "reason": "Readers who liked 1984 also enjoyed Sapiens"},
        {"customer_id": 2, "book_id": 12, "score": 85.5, "reason": "Popular in the non-fiction category"},
        {"customer_id": 3, "book_id": 6, "score": 93.2, "reason": "Essential companion to your programming books"},
        {"customer_id": 3, "book_id": 7, "score": 89.7, "reason": "Next level software design patterns"},
        {"customer_id": 4, "book_id": 12, "score": 87.0, "reason": "Similar to Sapiens in scope and depth"},
        {"customer_id": 4, "book_id": 13, "score": 79.5, "reason": "Trending book in self-improvement"},
        {"customer_id": 5, "book_id": 1, "score": 90.0, "reason": "Classic literature matching your taste"},
        {"customer_id": 5, "book_id": 3, "score": 86.8, "reason": "Readers of To Kill a Mockingbird also loved 1984"},
        {"customer_id": 6, "book_id": 13, "score": 88.5, "reason": "Highly rated in behavior & psychology"},
        {"customer_id": 7, "book_id": 9, "score": 94.0, "reason": "Perfect for your software architecture interests"},
        {"customer_id": 8, "book_id": 1, "score": 75.0, "reason": "Top classic fiction recommendation"},
        {"customer_id": 8, "book_id": 2, "score": 82.0, "reason": "Award-winning literature you might enjoy"},
    ]
    for rec in recommendations_data:
        post(f"{RECOMMEND_URL}/recommendations/", rec)

    print("\n" + "=" * 50)
    print("  Seeding complete!")
    print("=" * 50)
    print("\nSummary:")
    print(f"  Catalogs:        5")
    print(f"  Books:           15")
    print(f"  Customers:       8  (+ 8 carts auto-created)")
    print(f"  Staff:           5")
    print(f"  Managers:        3")
    print(f"  Cart Items:      10")
    print(f"  Orders:          6  (+ 6 payments & 6 shipments auto-created)")
    print(f"  Reviews:         15")
    print(f"  Recommendations: 15")
    print(f"\nCustomer Portal:  http://localhost:8000/")
    print(f"Admin Dashboard:  http://localhost:8000/dashboard/")
    print(f"\nAll demo accounts use password: 123456")
    print(f"Customer login example: an.nguyen@email.com / 123456")
    print(f"Staff login example:    lan.nguyen@bookstore.com / 123456")


if __name__ == "__main__":
    seed()
