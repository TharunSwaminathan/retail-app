from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import pandas as pd
import os


@app.route("/search", methods=["GET"])
def search():
    hshd_num = request.args.get("HSHD_NUM")
    # Query database for hshd_num
    query = f"SELECT * FROM Transactions3 WHERE HSHD_NUM = {hshd_num}"
    results = execute_query(query)  # Replace with actual database logic
    return render_template("search_results.html", results=results)
