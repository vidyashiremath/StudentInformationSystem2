
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "student-management-demo-key"

# Temporary storage for demonstration
users = {}
students = []
next_student_id = 1


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter username and password.")
        elif username in users:
            flash("Username already exists.")
        else:
            users[username] = generate_password_hash(password)
            flash("Registration successful. Please log in.")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username in users and check_password_hash(
            users[username], password
        ):
            session["username"] = username
            return redirect(url_for("student_list"))

        flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


@app.route("/students", methods=["GET", "POST"])
def student_list():
    global next_student_id

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll_no = request.form.get("roll_no", "").strip()
        course = request.form.get("course", "").strip()

        if name and roll_no and course:
            students.append({
                "id": next_student_id,
                "name": name,
                "roll_no": roll_no,
                "course": course
            })
            next_student_id += 1
            flash("Student added successfully.")
        else:
            flash("Please fill in all student details.")

        return redirect(url_for("student_list"))

    return render_template("students.html", students=students)


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    if "username" not in session:
        return redirect(url_for("login"))

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            flash("Student deleted successfully.")
            break

    return redirect(url_for("student_list"))


if __name__ == "__main__":
    app.run(debug=True)
