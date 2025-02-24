import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import datetime
import smtplib


app = Flask(__name__)

# mongodb configuration
mongo_uri = os.environ.get("MONGO_URI")
mongodb_client = MongoClient(mongo_uri)
db = mongodb_client.get_database("flask_app_db")
user_registrations_collection = db.user_registrations


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user_data = user_registrations_collection.find_one({"email": email})
        if user_data:
            hashed_password = user_data["password"]
            if check_password_hash(hashed_password, password):
                return redirect(url_for("success", action="login"))
            else:
                error = "Invalid Password. Please try again."
        else:
            error = "User not found. Please register."

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        mobile = request.form["mobile"]
        email = request.form["email"]
        password = request.form["password"]
        address = request.form["address"]
        registration_number = request.form["registration_number"]

        hashed_password = generate_password_hash(password)

        registration_data = {
            "mobile": mobile,
            "email": email,
            "password": hashed_password,
            "address": address,
            "registration_number": registration_number,
        }

        user_registrations_collection.insert_one(registration_data)
        print("Registration data inserted into MongoDB")

        return redirect(url_for("success", action="register"))
    return render_template("register.html")


@app.route("/success", methods=["GET", "POST"])
def success():
    action = request.args.get("action")
    message = None
    user = None
    search_performed = False

    if request.method == "POST":
        search_reg_number = request.form["registration_number"]
        user = user_registrations_collection.find_one(
            {"registration_number": search_reg_number.upper()}
        )
        search_performed = True
    elif action == "login":
        message = "Logged in successfully"
    elif action == "register":
        message = "Registered successfully"
    else:
        return redirect(url_for("index"))

    return render_template(
        "success.html",
        message=message,
        action=action,
        user=user,
        search_performed=search_performed,
    )


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    error = None
    message = None
    if request.method == "POST":
        email = request.form["email"]
        user = user_registrations_collection.find_one({"email": email})
        if user:
            reset_token = secrets.token_urlsafe(16)
            token_expiry = datetime.datetime.now() + datetime.timedelta(hours=1)
            user_registrations_collection.update_one(
                {"email": email},
                {
                    "$set": {
                        "reset_token": reset_token,
                        "reset_token_expiry": token_expiry,
                    }
                },
            )
            print(f"Reset token stored for user with email {email}")

            reset_link = url_for("reset_password", token=reset_token, _external=True)

            # Send email using SMTP
            try:
                s = smtplib.SMTP("smtp.gmail.com", 587)
                s.starttls()
                s.login(
                    os.environ.get("MAIL_USERNAME"), os.environ.get("MAIL_PASSWORD")
                )
                email_message = f"Subject: Password Reset Request\n\nPlease click on the following link to reset your password: {reset_link}"
                s.sendmail(os.environ.get("MAIL_USERNAME"), email, email_message)
                s.quit()

                message = "Password reset link has been sent to your email address. Please check your email. If you don't see the email in your inbox, check your spam folder."
            except Exception as e:
                error = f"Error Sending email. Please try again later. Error details: {str(e)}"
                print(f"Error sending email: {str(e)}")

        else:
            error = "Email address not found. Please check your email or register."
    return render_template("forgot_password.html", error=error, message=message)


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    error = None
    message = None

    user = user_registrations_collection.find_one({"reset_token": token})
    if not user:
        error = "Invalid or expired reset token. Please try again."
        return render_template("reset_password.html", error=error)
    if user["reset_token_expiry"] < datetime.datetime.now():
        error = "Reset token has expired. Please request a new password reset."
        return render_template("reset_password.html", error=error)
    if request.method == "POST":
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            error = "Passwords do not match. Please try again."
            return render_template("reset_password.html", error=error)

        if len(password) < 6:
            error = "Password must be at least 6 characters long."
            return render_template("reset_password.html", error=error)
        hashed_password = generate_password_hash(password)
        user_registrations_collection.update_one(
            {"reset_token": token},
            {
                "$set": {"password": hashed_password},
                "$unset": {"reset_token": "", "reset_token_expiry": ""},
            },
        )

        print(f"Password reset successfully for user with email {user['email']}")
        message = "Password reset successfully! Please log in with your new password."
        return redirect(url_for("login", message=message))
    return render_template("reset_password.html", error=error)


# test mongodb connection
@app.route("/mongodb")
def mongodb_test():
    try:
        db.command("ping")
        return "MongoDB connection is successful"
    except Exception as e:
        return f"MongoDB connection failed: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
