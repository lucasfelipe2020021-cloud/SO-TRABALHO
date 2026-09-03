from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Criar banco
def criar_banco():
    conn = sqlite3.connect("empresa.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cargo TEXT,
            salario REAL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect("empresa.db")
    c = conn.cursor()
    c.execute("SELECT * FROM funcionarios")
    funcionarios = c.fetchall()
    conn.close()
    return render_template("index.html", funcionarios=funcionarios)

@app.route("/add", methods=["POST"])
def add():
    nome = request.form["nome"]
    cargo = request.form["cargo"]
    salario = request.form["salario"]

    conn = sqlite3.connect("empresa.db")
    c = conn.cursor()
    c.execute("INSERT INTO funcionarios (nome, cargo, salario) VALUES (?, ?, ?)",
              (nome, cargo, salario))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("empresa.db")
    c = conn.cursor()
    c.execute("DELETE FROM funcionarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)