from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Database connection function
def get_db_connection():
    server = 'myretailserver.database.windows.net'  # Replace with your Azure SQL server name
    database = 'RetailDataDB'                      # Replace with your database name
    username = 'retailserver1'                     # Replace with your username
    password = 'Retail@123'                        # Replace with your password
    driver = '{ODBC Driver 18 for SQL Server}'     # Ensure ODBC Driver is installed

    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    return conn

# Route: Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username, password, and email exist in the database
        query = """
        SELECT COUNT(*)
        FROM Users
        WHERE username = ? AND password = ? AND email = ?
        """
        cursor.execute(query, (username, password, email))
        result = cursor.fetchone()[0]
        conn.close()

        if result > 0:  # Username, password, and email match
            return redirect(url_for("search"))
        else:
            flash("Invalid credentials. Please create an account or recover your password.")
            return redirect(url_for("create_account"))  # Redirect to create account page

    return render_template("login.html")

# Route: Create Account Page
@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert new user into the database
        query = """
        INSERT INTO Users (username, password, email)
        VALUES (?, ?, ?)
        """
        try:
            cursor.execute(query, (username, password, email))
            conn.commit()
            flash("Account created successfully. Please log in.")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error creating account: {str(e)}")
        finally:
            conn.close()

    return render_template("create_account.html")

# Route: Forgot Password Page
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the email exists in the database
        query = """
        SELECT username
        FROM Users
        WHERE email = ?
        """
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        conn.close()

        if result:
            username = result[0]
            flash(f"Password recovery email sent to {email}.")
        else:
            flash("Email not found. Please create an account.")
            return redirect(url_for("create_account"))

    return render_template("forgot_password.html")



# Route: Search Page
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        hshd_num = request.form["hshd_num"]  # Get the household number from the form input
        conn = get_db_connection()
        cursor = conn.cursor()

        # SQL Query to retrieve data
        query = """
        SELECT 
            h.HSHD_NUM,
            t.BASKET_NUM,
            t.PURCHASE_,
            t.PRODUCT_NUM,
            p.DEPARTMENT,
            p.COMMODITY,
            t.SPEND,
            t.UNITS,
            t.STORE_R,
            t.WEEK_NUM,
            t.YEAR,
            h.L,
            h.AGE_RANGE,
            h.MARITAL,
            h.INCOME_RANGE,
            h.HOMEOWNER,
            h.HSHD_COMPOSITION,
            h.HH_SIZE,
            h.CHILDREN
        FROM 
            Households5 h
        JOIN 
            Transactions3 t ON h.HSHD_NUM = t.HSHD_NUM
        JOIN 
            Products p ON t.PRODUCT_NUM = p.PRODUCT_NUM
        WHERE 
            h.HSHD_NUM = ?
        ORDER BY 
            t.BASKET_NUM, t.PURCHASE_, t.PRODUCT_NUM
        """
        
        cursor.execute(query, (hshd_num,))
        results = cursor.fetchall()
        conn.close()

        return render_template("search_results.html", results=results)

    return render_template("search.html")

# Route: Upload Page
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        files = request.files  # This contains all uploaded files
        for file_key in files:  # file_key is the key in request.files (e.g., "transactions_file")
            file = files[file_key]  # Retrieve the actual file object
            if file.filename != "":
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(file_path)
                data = pd.read_csv(file_path)  # Read the file into a DataFrame
                conn = get_db_connection()
                
                # Dynamic table name based on file_key
                table_name = file_key.split("_")[0].capitalize()  # Extracts "Transactions", "Households", "Products"
                data.to_sql(table_name, conn, if_exists="replace", index=False)  # Writes to SQL table
                conn.close()
        flash("Files uploaded and database updated successfully!")
        return redirect(url_for("upload"))
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
