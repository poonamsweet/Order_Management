3# from flask import Flask, render_template, request
import flask
import json
import datetime
from datetime import date, timedelta, timezone
import os
from sqlalchemy import distinct
from flask import jsonify, request, send_file
from sqlalchemy import exists, select
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt, \
    unset_jwt_cookies

from flask_cors import CORS
from dateutil.relativedelta import relativedelta

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased
from datetime import time
#import logging
from sqlalchemy import DECIMAL

from werkzeug.utils import secure_filename

import boto3
import botocore
import os
from flask_jwt_extended import jwt_required, get_jwt_identity

from send_mail import send

from botocore.exceptions import NoCredentialsError
from io import BytesIO
from sqlalchemy import or_ , func, and_, extract, case
from flask import request, jsonify
import urllib.parse

app = flask.Flask(__name__)

#CORS(app, origins="http://13.235.94.214:3000/")

CORS(app,  resources={r"/*": {"origins": ['http://13.202.119.149:3000','http://localhost:3000','https://ordermanagementapp.in', 'https://api.ordermanagementapp.in', 'https://www.ordermanagementapp.in']}})
#cors = CORS(app, resources={r"/gettutoruser/*": {"origins": "http://localhost:3000"}})

app.config["JWT_SECRET_KEY"] = ""  # Change this!
#app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)  # Token expires in 30 days


jwt = JWTManager(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = 'prateek.tutorshive@gmail.com'

app.config['CORS_HEADERS'] = 'Content-Type'





#MySQL configurations
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}/{}".format(
#      os.getenv("RDS_USERNAME"),
#      os.getenv("RDS_PASSWORD"),
#      os.getenv("RDS_HOSTNAME"),
#      os.getenv("RDS_DB_NAME"),
#  )
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from sqlalchemy import create_engine


#password = 'admin@123'
#password = 'password'

# Assuming your SQLAlchemy configuration is in app.config
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://new_user:{password}@localhost:3306/ordermodule'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/ordermodule'

# this db seeting for aws deployement
username = 'myuser'
password = 'passsword'
hostname = 'localhost'
dbname = 'ordermodule'

# # URL-encode the username and password
# username_encoded = urllib.parse.quote(username)
# password_encoded = urllib.parse.quote(password)

# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username_encoded}:{password_encoded}@{hostname}/{dbname}'
password = 'admin@123'

# this db setting for local
#app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{password}@localhost:3306/ordermodule'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passsword@localhost:3306/ordermodule'



# this db setting for local
#app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{password}@localhost:3306/ordermodule'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/ordermodule'

#this is local db setting
# # URL-encode the username and password
# password = 'Tutorshive@123'
# username = 'admin'
# hostname = 'localhost'
# username_encoded = urllib.parse.quote(username)
# password_encoded = urllib.parse.quote(password)
# password = password_encoded


# dbname = 'dump20241022'



# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://admin:{password}@localhost:3306/{dbname}'


# app.app_context().push()
db = SQLAlchemy(app)

""" logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
"""


class EmployeesForm(db.Model):
    __tablename__ = 'employeesform'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    blood_group = db.Column(db.String(5))
    marital_status = db.Column(db.String(20))
    aadhaar_number = db.Column(db.String(12))
    aadhaar_image_url = db.Column(db.String(255))
    pan_number = db.Column(db.String(10))
    dob = db.Column(db.Date)
    pan_image_url = db.Column(db.String(255))
    degree = db.Column(db.String(100))
    degree_image_url = db.Column(db.String(255))
    appointment_letter_url = db.Column(db.String(255))
    department = db.Column(db.String(50))
    degree_image_url = db.Column(db.String(255))
    official_email = db.Column(db.String(50))
    personal_email = db.Column(db.String(50))
    reporting_manager_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))

    passbook_cheque_url = db.Column(db.String(255))
    employment_type = db.Column(db.String(50))
    salary_annual = db.Column(DECIMAL(12, 2), nullable=False)
    salary_monthly = db.Column(DECIMAL(12, 2), nullable=False)
    religion = db.Column(db.String(50))
    work_mode = db.Column(db.String(20))
    emergency_contact_name = db.Column(db.String(50))
    emergency_contact_relationship = db.Column(db.String(50))
    emergency_contact_number = db.Column(db.String(50))
    emergency_contact_blood_group = db.Column(db.String(5))
    present_address_line1 = db.Column(db.String(255))
    present_address_line2 = db.Column(db.String(255))
    present_city = db.Column(db.String(100))
    present_state = db.Column(db.String(100))
    present_country = db.Column(db.String(100))
    present_postal_code = db.Column(db.String(20))
    permanent_address_line1 = db.Column(db.String(255))
    permanent_address_line2 = db.Column(db.String(255))
    permanent_city = db.Column(db.String(100))
    permanent_state = db.Column(db.String(100))
    permanent_country = db.Column(db.String(100))
    permanent_postal_code = db.Column(db.String(20))
    employees = db.relationship('Employees', foreign_keys=[reporting_manager_id], backref=db.backref('employees_foreign_key'))

    
class Users(db.Model):
    users_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    contact = db.Column(db.String(25))
    joiningDate = db.Column(db.Date)
    type = db.Column(db.String(50))


class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_name = db.Column(db.String(100))
    client_contact = db.Column(db.String(25))
    client_email = db.Column(db.String(50))
    client_status = db.Column(db.String(100))
    university = db.Column(db.String(100))
    business_name = db.Column(db.String(100))
    student_login = db.Column(db.String(100))
    student_password = db.Column(db.String(100))


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.users_id'))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(50))
    contact = db.Column(db.String(25))
    address = db.Column(db.String(255))
    dob = db.Column(db.Date)
    status = db.Column(db.String(50))
    roles = db.Column(db.String(50))
    designation = db.Column(db.String(100))

    users = db.relationship('Users', backref=db.backref('employees_foreign_key'))

class Orders(db.Model):
    __tablename__ = 'orders'
    orders_id = db.Column(db.String(50), primary_key=True)
    task_subject = db.Column(db.String(100))
    expert_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    status = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    order_budget = db.Column(db.Float)
    currency = db.Column(db.String(15))
    expert_currency = db.Column(db.String(15))
    qc_expert_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    otm_id = db.Column(db.Integer, db.ForeignKey('users.users_id'))
    description = db.Column(db.String(200))
    word_count = db.Column(db.Integer)
    expert_price = db.Column(db.Integer)
    assigned_expert = db.Column(db.Integer)
    task_date = db.Column(db.Date)
    expert_deadline = db.Column(db.Date)
    assigned_expert_deadline = db.Column(db.Date)

    client = db.relationship('Client', backref=db.backref('orders'))
    expert = db.relationship('Employees', foreign_keys=[expert_id], backref=db.backref('orders_as_expert'))
    qc_expert = db.relationship('Employees', foreign_keys=[qc_expert_id], backref=db.backref('orders_as_qc_expert'))
    otm = db.relationship('Users', backref=db.backref('orders'))
    comments = db.Column(db.String(100)) 
    operation_status = db.Column(db.String(100))
    team_lead_status = db.Column(db.String(100))




class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.users_id'))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    status = db.Column(db.String(100))
    working_hours = db.Column(db.Integer)
    users = db.relationship('Users', backref=db.backref('attendance_foreign_key'))


class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_number = db.Column(db.String(50))
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    total_amount = db.Column(db.Float)
    discount = db.Column(db.Integer)
    invoice_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    total = db.Column(db.Float)
    #orders_id = db.Column(db.String(30))
    tax_rate = db.Column(db.Integer)
    tax_type = db.Column(db.String(45))
    currency = db.Column(db.String(45))
    discountType = db.Column(db.String(45))
    sub_tax = db.Column(db.String(20))
    dis_percent = db.Column(db.Float)
    paid_amount = db.Column(db.Float)
    payment_date = db.Column(db.Date)
    tax_amount = db.Column(db.Float)
    payment_method = db.Column(db.String(50))
    client = db.relationship('Client', backref=db.backref('invoice'))
   

class InvoiceOrders(db.Model):
    __tablename__ = 'invoice_orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_number = db.Column(db.String(50))
    item = db.Column(db.String(45))
    amount = db.Column(db.Float)
    orders_id = db.Column(db.String(50))
    tax_rate = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    item_total = db.Column(db.Float)
    vat = db.Column(db.Float)
    cgst = db.Column(db.Float)
    sgst = db.Column(db.Float)
    igst = db.Column(db.Float)


# class FreelancerInvoice(db.Model):
#     __tablename__ = 'freelancerinvoice'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     invoice_number = db.Column(db.String(50))
#     freelancer_id =  db.Column(db.String(45))
#     amount = db.Column(db.Float)
#     total = db.Column(db.Float)
#     invoice_date = db.Column(db.Date)
#     due_date = db.Column(db.Date)
#     orders_id = db.Column(db.Integer)
#     currency = db.Column(db.String(45))
#     paid_amount = db.Column(db.Float)
#     payment_date = db.Column(db.Date)
#     payment_method = db.Column(db.String(50))
    
class Attachments(db.Model):
    __tablename__ = 'attachments'
    attachment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name =  db.Column(db.String(150))
    invoice_number = db.Column(db.String(50))

class AssignedOrders(db.Model):
    __tablename__ = 'assigned_orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orders_id = db.Column(db.String(50))
    expert_id = db.Column(db.Integer)
    assigned_date = db.Column(db.Date)
    deadline = db.Column(db.Date)
    no_of_words = db.Column(db.String(50))
    remarks = db.Column(db.String(200))
    status = db.Column(db.String(100))
    assigned_expert = db.Column(db.Integer)
    assigned_expert_deadline = db.Column(db.Date)
    incentive = db.Column(db.Float, nullable=True)  # New column for incentive with nullable=True
    qc_expert = db.Column(db.Integer)
    comments = db.Column(db.String(100))
    comment_for_tl = db.Column(db.String(100))
    is_admin_assigned_by = db.Column(db.String(100))
    teammember_comment = db.Column(db.String(100))
    team_deadline1 = db.Column(db.Date)
    team_deadline2 = db.Column(db.Date)
    team_deadline3 = db.Column(db.Date)
    team_deadline4 = db.Column(db.Date)
    team_deadline5 = db.Column(db.Date)
    team_deadline6 = db.Column(db.Date)
    assigned_expert_deadline1 = db.Column(db.Date)
    assigned_expert_deadline2 = db.Column(db.Date)
    assigned_expert_deadline3 = db.Column(db.Date)
    assigned_expert_deadline4 = db.Column(db.Date)
    assigned_expert_deadline5 = db.Column(db.Date)
    assigned_expert_deadline6 = db.Column(db.Date)
    no_of_word1 = db.Column(db.String(50))
    no_of_word2 = db.Column(db.String(50))
    no_of_word3 = db.Column(db.String(50))
    no_of_word4 = db.Column(db.String(50))
    no_of_word5 = db.Column(db.String(50))
    no_of_word6 = db.Column(db.String(50))
    expert_no_of_words = db.Column(db.String(50))
    expert_no_of_word1 = db.Column(db.String(50))
    expert_no_of_word2 = db.Column(db.String(50))
    expert_no_of_word3 = db.Column(db.String(50))
    expert_no_of_word4 = db.Column(db.String(50))
    expert_no_of_word5 = db.Column(db.String(50))
    expert_no_of_word6 = db.Column(db.String(50))
    deadline_for_operation = db.Column(db.Date)
    operation_member_comment = db.Column(db.String(100))
    is_admin_assigned_by_operation = db.Column(db.String(100))

    
    
class Urgentdeadlines(db.Model):
    from datetime import datetime

    __tablename__ = 'urgentdeadlines'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orders_id = db.Column(db.String(50))
    expert_id = db.Column(db.Integer)
    urgent_deadline = db.Column(db.Date, nullable=True)
    urgent_deadline_comment = db.Column(db.String(50), nullable=True)
    is_status = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'orders_id': self.orders_id,
            'expert_id': self.expert_id,
            'urgent_deadline': self.urgent_deadline.strftime('%Y-%m-%d'),  # Format date as a string
            'urgent_deadline_comment': self.urgent_deadline_comment,
            'is_status': self.is_status
        }


class Highprioritydeadlines(db.Model):
    from datetime import datetime

    __tablename__ = 'highprioritydeadlines'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orders_id = db.Column(db.String(50))
    expert_id = db.Column(db.Integer)
    high_priority_deadline = db.Column(db.Date, nullable=True)
    high_priority_comment = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_status = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'orders_id': self.orders_id,
            'expert_id': self.expert_id,
            'high_priority_deadline': self.high_priority_deadline.strftime('%Y-%m-%d'),  # Format date as a string
            'high_priority_comment': self.high_priority_comment,
            'is_status': self.is_status
        }

   
class Meetingdeadlines(db.Model):
    from datetime import datetime

    __tablename__ = 'meetingdeadlines'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orders_id = db.Column(db.String(50))
    expert_id = db.Column(db.Integer)
    meeting_sche_deadline = db.Column(db.Date, nullable=True)
    meeting_sche_comment = db.Column(db.String(200), nullable=True)
    meeting_sche_time = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)    
    is_status = db.Column(db.Boolean, default=False, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'orders_id': self.orders_id,
            'expert_id': self.expert_id,               
            'meeting_sche_deadline': self.meeting_sche_deadline.strftime('%Y-%m-%d'),  # Format date as a string
            'meeting_sche_comment': self.meeting_sche_comment,
            'meeting_sche_time': self.meeting_sche_time,
            'is_status': self.is_status
        }

# -------------------LOG in Module Route start -------------------__

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.datetime.now(timezone.utc)
        target_timestamp = datetime.datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
                print(response)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

def format_invoice_date(invoice_date_str):
    from datetime import datetime

    if invoice_date_str:
        # Convert from ISO 8601 (2024-12-05T08:38:06.000Z) to MySQL DATETIME format
        try:
            date_obj = datetime.strptime(invoice_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            return date_obj.strftime("%Y-%m-%d %H:%M:%S")  # Return as MySQL compatible format
        except ValueError:
            return None  # Return None if the date format is invalid
    return None  # Return None if the date is None or empty

@app.route('/total_admin_count/', methods=['POST'])
@jwt_required()
def totalorderscount(): 
    from datetime import datetime
    now = datetime.now()

    current_user = get_jwt_identity()

    if not current_user:
        return jsonify({"message": "User email not found in token"}), 400

    # Retrieve the user's ID based on the email
    user = Users.query.filter_by(email=current_user).first()
    if user:
         current_expert_id = user.users_id
         current_user_type = user.type
    else:
        # Handle the case where the user is not found
        raise Exception("User not found")
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    selected_month = request.form['month']
    selected_year = request.form['year']

    # Assume `selected_month` is the month selected by the user (1-12), None if no selection
    selected_month = int(selected_month)  # Convert to integer if needed
    selected_year = int(selected_year)  # Convert to integer if needed

    # Subquery to get unique orders based on deadline or assigned_expert_deadline
    if current_expert_id == 1 or current_user_type == "admin":  # Check if admin
        print("admin")
        assigned_orders_subquery = (
            AssignedOrders.query
                .filter(
                    func.extract('year', func.coalesce(AssignedOrders.deadline, AssignedOrders.assigned_expert_deadline)) == selected_year,
                    func.extract('month', func.coalesce(AssignedOrders.deadline, AssignedOrders.assigned_expert_deadline)) == selected_month
                )
                .with_entities(func.distinct(AssignedOrders.orders_id).label('orders_id'))  # Ensure unique orders_id
        ).subquery()
        assigned_orders_count = (
                Orders.query
                    .join(assigned_orders_subquery, Orders.orders_id == assigned_orders_subquery.c.orders_id)  # Join on unique orders_id
                    .with_entities(
                        func.count(func.distinct(Orders.orders_id)).label('total_orders'),
                        func.sum(case((Orders.status == 'assigned', 1), else_=0)).label('assigned_orders_count'),
                        func.sum(case((Orders.status == 'qc', 1), else_=0)).label('qc_orders_count'),
                        func.sum(case((Orders.status == 'rework', 1), else_=0)).label('rework_count'),
                        func.sum(case((Orders.status == 'fail', 1), else_=0)).label('failed_count'),
                        func.sum(case((Orders.status == 'pass', 1), else_=0)).label('completed_count'),
                    )
                    .one_or_none()  # Ensure you only get one result or None
            )
    else:  # For experts
        assigned_orders_subquery = (
            AssignedOrders.query
                .filter(
                    AssignedOrders.expert_id == current_expert_id,  # Filter by expert ID
                    func.extract('year', func.coalesce(AssignedOrders.deadline, AssignedOrders.assigned_expert_deadline)) == selected_year,
                    func.extract('month', func.coalesce(AssignedOrders.deadline, AssignedOrders.assigned_expert_deadline)) == selected_month
                )
                .with_entities(func.distinct(AssignedOrders.orders_id).label('orders_id'))  # Ensure unique orders_id
        ).subquery()

        # Query Orders using the subquery
        assigned_orders_count = (
                Orders.query
                    .join(assigned_orders_subquery, Orders.orders_id == assigned_orders_subquery.c.orders_id)  # Join on unique orders_id
                    .with_entities(
                        func.count(func.distinct(Orders.orders_id)).label('total_orders'),
                        func.sum(case((Orders.status == 'assigned', 1), else_=0)).label('assigned_orders_count'),
                        func.sum(case((Orders.status == 'qc', 1), else_=0)).label('qc_orders_count'),
                        func.sum(case((Orders.status == 'rework', 1), else_=0)).label('rework_count'),
                        func.sum(case((Orders.status == 'fail', 1), else_=0)).label('failed_count'),
                        func.sum(case((Orders.status == 'pass', 1), else_=0)).label('completed_count'),
                    )
                    .one_or_none()  # Ensure you only get one result or None
            )
    new_orders_count = (
            Orders.query
                .filter(
                    Orders.status == 'new order',  # Only count new orders
                    func.extract('year', Orders.start_date) == selected_year,
                    func.extract('month', Orders.start_date) == selected_month
                )
                .count()
        )
    if assigned_orders_count:
        total_orders = assigned_orders_count.total_orders
        assigned_orders = assigned_orders_count.assigned_orders_count
        qc_orders = assigned_orders_count.qc_orders_count
        rework_orders = assigned_orders_count.rework_count
        failed_orders = assigned_orders_count.failed_count
        completed_orders = assigned_orders_count.completed_count
        new_orders_count = new_orders_count
        return jsonify({"Orders": total_orders, "assigned_order_count":assigned_orders,"completed_count":completed_orders,
                        "qc_orders":qc_orders,"rework_orders":rework_orders,"failed_orders":failed_orders,
                        "new_order_count":new_orders_count}), 200
    else:
        total_orders = new_order_count = assigned_orders = qc_orders = rework_orders = failed_orders = 0
        return jsonify({"message": "No orders found for the specified month and year.","total_orders":total_orders}), 404

    
@app.route('/urgent_deadline', methods=['POST'])
@jwt_required()
def urgentDeadlines():
    current_user = get_jwt_identity()
    urgdeadline = request.form['urgent_deadline']
    urgcmt = request.form['urgent_deadline_comment']
    order_id = request.form['orders_id']
    #expert_id = request.form['expert_id']
    

    existing_order = AssignedOrders.query.filter_by(orders_id=order_id).first()
    order = Urgentdeadlines.query.filter_by(orders_id=order_id).first()
    if order:
        return jsonify({"message": "Order  is already in urgent deadline "}), 400
   
    if not existing_order:
        # If the email already exists, return a message indicating that the email is not unique
        return jsonify({'message': 'order not  exists in db'}), 400

    # If the email is unique, proceed to add the user to the database
    current_user = get_jwt_identity()

    if not current_user:
        return jsonify({"message": "User email not found in token"}), 400

    # Retrieve the user's ID based on the email
    user = Users.query.filter_by(email=current_user).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    expert_id = user.users_id

    all_deadline = Urgentdeadlines(orders_id=order_id,
                                 expert_id=expert_id,
                                 urgent_deadline=urgdeadline, 
                                 urgent_deadline_comment=urgcmt,
                                )
    db.session.add(all_deadline)
    db.session.commit()

    return jsonify({'message': 'Deadline updated Successful'}), 200


@app.route('/urgent_deadline_done/<orderId>', methods=['POST'])
@jwt_required()
def urgent_deadline_done(orderId):
    order = Urgentdeadlines.query.filter_by(orders_id=orderId).first()
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order completed successfully"}), 200
    else:
        return jsonify({"message": "Order not found"}), 200
    
    
@app.route('/list_urgdeadline/', methods=['POST'])
@jwt_required()
def list_urgent_deadline(): 
    current_user = get_jwt_identity()

    if not current_user:
        return jsonify({"message": "User email not found in token"}), 400

    # Retrieve the user's ID based on the email
    user = Users.query.filter_by(email=current_user).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    expert_id = user.users_id

    # Query the Urgentdeadlines table to get deadlines for the logged-in expert
    deadlines = Urgentdeadlines.query.filter_by(expert_id=expert_id).all()

    if deadlines:
        # Serialize the deadlines into a list of dictionaries
        deadlines_list = [deadline.to_dict() for deadline in deadlines]
        return jsonify({"deadlines": deadlines_list}), 200
    else:
        return jsonify({"message": "No deadlines found"}), 404

    
@app.route('/high_priority_deadline', methods=['POST'])
@jwt_required()
def highpriorityDeadlines():
    high_pri_deadline = request.form['high_priority_deadline']

    high_priority_comment = request.form['high_priority_comment']
    order_id = request.form['orders_id']
    #expert_id = request.form['expert_id']
    order = Highprioritydeadlines.query.filter_by(orders_id=order_id).first()
    if order:
        return jsonify({"message": "Order  is already in high priority deadline list "}), 400

    existing_order = AssignedOrders.query.filter_by(orders_id=order_id).first()
    current_user = get_jwt_identity()

    if not current_user:
        return jsonify({"message": "User email not found in token"}), 400

    # Retrieve the user's ID based on the email
    user = Users.query.filter_by(email=current_user).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    expert_id = user.users_id
    if not existing_order:
        # If the email already exists, return a message indicating that the email is not unique
        return jsonify({'message': 'order not  exists in db'}), 400

    # If the email is unique, proceed to add the user to the database
     
    all_deadline = Highprioritydeadlines(orders_id=order_id,
                                 expert_id=expert_id,
                                 high_priority_deadline=high_pri_deadline,
                                 high_priority_comment=high_priority_comment,
                                )
   
            
    db.session.add(all_deadline)
    db.session.commit()

    return jsonify({'message': 'Deadline updated Successful'}), 200


@app.route('/list_high_priority_deadline/', methods=['POST'])
@jwt_required()
def list_high_priority_deadline(): 
    current_user = get_jwt_identity()

    if not current_user:
        return jsonify({"message": "User email not found in token"}), 400

    # Retrieve the user's ID based on the email
    user = Users.query.filter_by(email=current_user).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    expert_id = user.users_id

    # Query the Urgentdeadlines table to get deadlines for the logged-in expert
    deadlines = Highprioritydeadlines.query.filter_by(expert_id=expert_id).all()

    if deadlines:
        # Serialize the deadlines into a list of dictionaries
        deadlines_list = [deadline.to_dict() for deadline in deadlines]
        return jsonify({"deadlines": deadlines_list}), 200
    else:
        return jsonify({"message": "No deadlines found"}), 404


@app.route('/high_priority_deadline_done/<orderId>', methods=['POST'])
@jwt_required()
def high_priority_deadline_done(orderId):
    order = Highprioritydeadlines.query.filter_by(orders_id=orderId).first()
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order completed successfully"}), 200
    else:
        return jsonify({"message": "Order not found"}), 200
    
 
 
 
@app.route('/meetingdeadline', methods=['POST'])
@jwt_required()
def meetingDeadlines():
    meeting_sche_deadline = request.form['meeting_sche_deadline']
    meeting_sche_comment = request.form['meeting_sche_comment']
    meeting_sche_time = request.form['meeting_sche_time']
    order_id = request.form['orders_id']
    #expert_id = request.form['expert_id']
    order = Meetingdeadlines.query.filter_by(orders_id=order_id).first()
    if order:
        return jsonify({"message": "Order  is already in meeting  deadline list "}), 400

    existing_order = AssignedOrders.query.filter_by(orders_id=order_id).first()
    current_user = get_jwt_identity()

    if not current_user:
        return jsonify({"message": "User email not found in token"}), 400

    # Retrieve the user's ID based on the email
    user = Users.query.filter_by(email=current_user).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    expert_id = user.users_id
    if not existing_order:
        # If the email already exists, return a message indicating that the email is not unique
        return jsonify({'message': 'order not  exists in db'}), 400

    # If the email is unique, proceed to add the user to the database
     
    all_deadline = Meetingdeadlines(orders_id=order_id, expert_id=expert_id, meeting_sche_deadline=meeting_sche_deadline,
                                 meeting_sche_comment=meeting_sche_comment,
                                 meeting_sche_time=meeting_sche_time,
                                 )  
            
    db.session.add(all_deadline)
    db.session.commit()
    
    return jsonify({'message': 'Deadline updated Successful'}), 200

@app.route('/list_meetingdeadline/', methods=['POST'])
@jwt_required()
def list_meetingdeadline(): 
    current_user = get_jwt_identity()

    if not current_user:
        return jsonify({"message": "User email not found in token"}), 400

    # Retrieve the user's ID based on the email
    user = Users.query.filter_by(email=current_user).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    expert_id = user.users_id

    # Query the Urgentdeadlines table to get deadlines for the logged-in expert
    deadlines = Meetingdeadlines.query.filter_by(expert_id=expert_id).all()

    if deadlines:
        # Serialize the deadlines into a list of dictionaries
        deadlines_list = [deadline.to_dict() for deadline in deadlines]
        return jsonify({"deadlines": deadlines_list}), 200
    else:
        return jsonify({"message": "No deadlines found"}), 404



@app.route('/meetingdeadline_done/<orderId>', methods=['POST'])
@jwt_required()
def meetingdeadline_done(orderId):
    order = Meetingdeadlines.query.filter_by(orders_id=orderId).first()
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order completed successfully"}), 200
    else:
        return jsonify({"message": "Order not found"}), 200



@app.route('/addUser', methods=['POST'])
def addUser():
    fname = request.form['firstName']
    lname = request.form['lastName']
    email = request.form['email']
    password = request.form['password']
    contact = request.form['contact']
    user_role = request.form['role']
    user_type = request.form['user_type']

    today = date.today()

    # Check if the email already exists in the database
    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        # If the email already exists, return a message indicating that the email is not unique
        return jsonify({'message': 'Email already exists'}), 400

    # If the email is unique, proceed to add the user to the database
    new_user = Users(
        firstname=fname,
        lastname=lname,
        email=email,
        password=password,
        contact=contact,
        joiningDate=today,
        type=user_role
    )

    db.session.add(new_user)
    db.session.commit()
    print(user_role)

    user_id = new_user.users_id
    print(user_id)

    new_expert = Employees(
        employee_id=user_id,
        firstname=fname,
        lastname=lname,
        email=email,
        # expert_address=address,
        contact=contact,
        # dob=today,
        roles=user_role,
        status=user_type,
    )
    db.session.add(new_expert)
    db.session.commit()

    return jsonify({'message': 'Registered Successful'}), 200

@app.route('/addclient', methods=['POST'])
@jwt_required()
def addclient():
    Client_name = request.form['Client_name']
    Client_contact = request.form['Client_contact']
    Client_email = request.form['Client_email']
    Client_status = request.form['Client_status']

    existing_user = Client.query.filter_by(client_email=Client_email).first()
    if existing_user:
        # If the email already exists, return a message indicating that the email is not unique
        return jsonify({'message': f'Client already exists with name {Client_name} and email {Client_email}'}), 400

    if Client_status == "student":
        University = request.form['University']
        Student_login = request.form['Student_login']
        Student_password = request.form['Student_password']
        client = Client(
            client_name=Client_name,
            client_contact=Client_contact,
            client_email=Client_email,
            client_status=Client_status,
            university=University,
            student_login=Student_login,
            student_password=Student_password
        )
    else:
        business_name = request.form['Business_name']
        client = Client(
            client_name=Client_name,
            client_contact=Client_contact,
            client_email=Client_email,
            client_status=Client_status,
            business_name=business_name
        )
    db.session.add(client)
    db.session.commit()

    return jsonify({'message': 'Client Added Successfully'}), 200

@app.route('/delete_users/<userId>', methods = ['POST'])
@jwt_required()
def deleteUsers(userId):
    existing_user = Employees.query.filter_by(employee_id=userId).first()
    if existing_user:
        # Delete from Employees table
        db.session.delete(existing_user)
        db.session.commit()

        user_table = Users.query.filter_by(users_id = userId).first()
        # Delete from User table
        db.session.delete(user_table)
        db.session.commit()
        return jsonify({'message': 'User removed'}), 200
    else:
        return jsonify({'message': 'User does not exists'}), 200

@app.route('/delete_clients/<userId>', methods = ['POST'])
@jwt_required()
def deleteClients(userId):
    existing_user = Client.query.filter_by(client_id=userId).first()
    if existing_user:
        # Delete from Employees table
        db.session.delete(existing_user)
        db.session.commit()

        return jsonify({'message': 'Client removed'}), 200
    else:
        return jsonify({'message': 'Client does not exists'}), 200


@app.route('/delete_invoice/<invoice_num>', methods = ['POST'])
@jwt_required()
def deleteInvocie(invoice_num):
    print(invoice_num)
    existing_user = Invoice.query.filter_by(invoice_number=invoice_num).delete()
    if existing_user:
        InvoiceOrders.query.filter_by(invoice_number=invoice_num).delete()
        db.session.commit()
        
        print(invoice_num)
        if delete_pdf_from_s3(invoice_num) == "success":
            return jsonify({'message': 'Invoice removed'}), 200
        else:
            return jsonify({'message': 'Error removing invoice from s3'}), 400
    else:
        return jsonify({'message': 'Invoice does not exists'}), 200
    
def delete_pdf_from_s3(invoiceNumber):
    try:
        # Create an S3 client
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

        # Generate the filename based on the invoice number
        filename = f"{invoiceNumber}.pdf"

        # Delete the file from S3
        s3.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=filename)

        return "success"
    except Exception as e:
        return str(e)


@app.route('/delete_attachment', methods = ['POST'])
@jwt_required()
def deleteAttachments():
    attachment_name = request.form['attachment']
    attach = Attachments.query.filter_by(name=attachment_name).first()
    if attach:
        # Delete from Employees table
        db.session.delete(attach)
        db.session.commit()
        if delete_attachment_s3(attachment_name) == "success":
            return jsonify({'message': 'Attachment removed'}), 200
        else:
            return jsonify({'message': 'Error removing Attachment from s3'}), 400
    else:
        return jsonify({'message': 'Attachment does not exists'}), 200
    
def delete_attachment_s3(name):
    try:
        # Create an S3 client
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

        # Generate the filename based on the invoice number
        filename = f"{name}"

        # Delete the file from S3
        s3.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=filename)

        return "success"
    except Exception as e:
        return str(e)


@app.route('/start_work/<userId>', methods=['POST'])
@jwt_required()
def startWork(userId):
    date = request.form['date']
    start_time = request.form['start_time']
    parsed_time = time.fromisoformat(start_time)
    print(date)
    print(parsed_time)
    new_date = datetime.datetime.strptime(date, "%d/%m/%Y")
    # new_start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")

    add_attendance = Attendance(
        employee_id=userId,
        date=new_date,
        start_time=parsed_time,
    )
    db.session.add(add_attendance)
    db.session.commit()

    return jsonify({'message': 'You have sucessfully logged in.'}), 200


@app.route('/end_work/<userId>', methods=['POST'])
@jwt_required()
def endWork(userId):
    end_time = request.form['end_time']
    working_hours = request.form['working_hours']

    # new_end_time = datetime.datetime.strptime(end_time, "%d/%m/%Y")
    update = Attendance.query.filter_by(employee_id=userId).first()

    if update:
        update.end_time = end_time
        update.working_hours = working_hours
        db.session.commit()

    return jsonify({'message': f'You have worked ${working_hours} hours.'}), 200


@app.route('/getAttendance', methods=['GET'])
@jwt_required()
def getAttendance():
    attendance = Attendance.query.all()
    data = []
    for emp in attendance:
        user = Users.query.filter_by(users_id=emp.employee_id).first()
        if emp.end_time != None:
            endTime = emp.end_time.strftime('%H:%M:%S')
        else:
            endTime = None
        client_data = {
            'id': emp.id,
            'first_name': user.firstname,
            'last_name': user.lastname,
            'email': user.email,
            'date': emp.date.strftime('%Y-%m-%d'),
            'start_time': emp.start_time.strftime('%H:%M:%S'),
            'end_time': endTime,
            'status': emp.status,
            'working_hours': emp.working_hours,
        }
        data.append(client_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/getEmployeeAttendance/<employee_id>', methods=['GET'])
@jwt_required()
def getEmployeeAttendance(employee_id):
    attendance = Attendance.query.filter_by(employee_id=employee_id).all()
    data = []
    for emp in attendance:
        client_data = {
            'date': emp.date.strftime('%Y-%m-%d'),
            'working_hours': emp.working_hours,
        }
        data.append(client_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/login', methods=['POST'])
def test():
    email = flask.request.form['email']
    password = flask.request.form['password']

    user = Users.query.filter_by(email=email, password=password).first()

    if user:
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token, type=user.type, userId=user.users_id)
    else:
        return jsonify({'message': 'Invalid email or password', 'code': '400'}), 400


@app.route('/', methods=['GET'])
def home():
    return "Welcome to order management backend"


# -------------------LOG in Module Route End  -------------------__

# ------------------- Add Tuters data  Module Route start -------------------__

@app.route('/getClient', methods=['GET'])
@jwt_required()
def getClient():
    clients = Client.query.all()
    data = []
    for client in clients:
        client_data = {
            'id': client.client_id,
            'Client_name': client.client_name,
            'Client_contact': client.client_contact,
            'Client_email': client.client_email,
            'Client_status': client.client_status,
            'University': client.university,
            'Business_name': client.business_name,
            'Student_login': client.student_login,
            'Student_password': client.student_password
        }
        data.append(client_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response


# def listit(t):
#    return list(map(listit, t)) if isinstance(t, (list, tuple)) else t


# ------------------- Add Tuters data  Module Route End -------------------__

# ------------------- Add OTM Mamber data  Module Route start -------------------__

@app.route('/otm', methods=['POST'])
@jwt_required()
def otm():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    password = request.form['password']
    email = request.form['email']
    contact = request.form['contact']
    joiningDate = request.form['joiningDate']
    joining_date_conv = datetime.datetime.strptime(joiningDate, "%Y-%m-%d")
    Level = request.form['Level']
    user_type = request.form['type']

    user = Users(
        firstname=firstname,
        lastname=lastname,
        password=password,
        email=email,
        contact=contact,
        joiningDate=joining_date_conv,
        Level=Level,
        type=user_type
    )

    db.session.add(user)
    db.session.commit()

    users = Users.query.all()
    data = [user.serialize() for user in users]

    if data:
        response = jsonify(data)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        return "Incorrect"


# ------------------- Add OTM Mamber  data  Module Route End -------------------__

# ------------------- Add Task data  Module Route start -------------------__
# add comment  
@app.route('/orders/<order_id>/comments', methods=['POST'])
@jwt_required()
def add_or_update_comments(order_id):
    try:
        new_comment = request.form['comments']
        
        existing_order = Orders.query.filter_by(orders_id=order_id).first()
        
        if existing_order:
            # If the order exists, update the comments
            existing_order.comments = new_comment
            db.session.commit()
            return jsonify({'message': 'Order comments updated successfully'}), 200
        else:
            return jsonify({'message': 'Order ID not found'}), 404
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    
@app.route('/orders/<order_id>/commentsfortl', methods=['POST'])
@jwt_required()
def add_or_update_commentfortl(order_id):
    try:
        new_comment = request.form['comment_for_tl']
        
        existing_order = AssignedOrders.query.filter_by(orders_id=order_id).first()
        
        if existing_order:
            # If the order exists, update the comments
            existing_order.comment_for_tl = new_comment
            db.session.commit()
            return jsonify({'message': 'Order comment for tl updated successfully'}), 200
        else:
            return jsonify({'message': 'Order ID not found'}), 404
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

@app.route('/addtask', methods=['POST'])
@jwt_required()
def addtask():
    from datetime import datetime, timezone, timedelta

    ist = timezone(timedelta(hours=5, minutes=30))  # Adjust timezone offset as needed

    # Fetch data from the request
    order_id = request.form['order_id']
    Task_Subject = request.form['Task_Subject']
    client_id = request.form['client_id']
    Status = request.form['Status']
    Start_date = request.form['Start_date']
    End_date = request.form['End_date']
    Description = request.form['Description']
    Word_count = request.form['Word_count']
    comments = request.form['Comments']
    invoice_dates = []
    no_of_words = []
    # Parse and convert start and end dates to IST timezone
    parsed_start_date = datetime.strptime(Start_date, "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone.utc)
    Start_date_conv = parsed_start_date.astimezone(ist).strftime("%Y-%m-%d")

    parsed_end_date = datetime.strptime(End_date, "%Y-%m-%d")
    End_date_conv = parsed_end_date.astimezone(ist).strftime("%Y-%m-%d")

    # Set current task date
    task_date = datetime.now().strftime("%Y-%m-%d")

    # Check if Word_count is empty, default to 0
    Word_count = 0 if Word_count == "" else int(Word_count)

    # Check if the order ID already exists
    existing_order = Orders.query.filter_by(orders_id=order_id).first()
    if existing_order:
        return jsonify({'message': 'Order id already exists'}), 400

    # Create the order entry in the Orders table
    order = Orders(
        orders_id=order_id,
        task_subject=Task_Subject,
        client_id=client_id,
        status=Status,
        start_date=Start_date_conv,
        end_date=End_date_conv,
        description=Description,
        word_count=Word_count,
        task_date=task_date,
    )

    db.session.add(order)
    db.session.commit()

    # Handle additional data passed in JSON format
    data = request.form.get('data')  # deadline, word count
    if data:
        try:
            parsed_data = json.loads(data)
            expert_id = request.form['expert_id']
            # Check if parsed_data is a list or a dictionary
            if isinstance(parsed_data, list):
                data_array = parsed_data
            elif isinstance(parsed_data, dict):
                data_array = parsed_data.get('task', [])
            else:
                return jsonify({'message': 'Invalid data format'}), 400

            # Delete existing assigned orders for this order_id
            existing_assigned_orders = AssignedOrders.query.filter_by(orders_id=order_id).all()
            for order_instance in existing_assigned_orders:
                db.session.delete(order_instance)
                print("Deleting:", order_instance)
            db.session.commit()
            invoice_dates = []
            no_of_words = []
            if isinstance(data_array, list):
                for item in data_array:
                    if isinstance(item, dict):
                        # Collect invoice dates and no_of_words
                        invoice_dates.append(format_invoice_date(item.get('invoiceDate')))
                        no_of_words.append(item.get('wordCount', 0))  # Default to 0 if not present
                    # Extract values with safe checks
                    invoice_date_1 = invoice_dates[0] if len(invoice_dates) > 0 else None
                    invoice_date_2 = invoice_dates[1] if len(invoice_dates) > 1 else None
                    invoice_date_3 = invoice_dates[2] if len(invoice_dates) > 2 else None
                    invoice_date_4 = invoice_dates[3] if len(invoice_dates) > 3 else None
                    invoice_date_5 = invoice_dates[4] if len(invoice_dates) > 4 else None
                    invoice_date_6 = invoice_dates[5] if len(invoice_dates) > 5 else None

                    no_of_words_1 = no_of_words[0] if len(no_of_words) > 0 else None
                    no_of_words_2 = no_of_words[1] if len(no_of_words) > 1 else None
                    no_of_words_3 = no_of_words[2] if len(no_of_words) > 2 else None
                    no_of_words_4 = no_of_words[3] if len(no_of_words) > 3 else None
                    no_of_words_5 = no_of_words[4] if len(no_of_words) > 4 else None
                    no_of_words_6 = no_of_words[5] if len(no_of_words) > 4 else None    
                    expert_no_of_words = no_of_words[0] if len(no_of_words) > 0 else None
                    expert_no_of_word1 = no_of_words[1] if len(no_of_words) > 1 else None
                    expert_no_of_word2 = no_of_words[2] if len(no_of_words) > 2 else None
                    expert_no_of_word3 = no_of_words[3] if len(no_of_words) > 3 else None
                    expert_no_of_word4 = no_of_words[4] if len(no_of_words) > 4 else None
                    expert_no_of_word5 = no_of_words[5] if len(no_of_words) > 4 else None                
                # task_data = data_item if isinstance(data_item, dict) else {}                    
                # invoice_date = task_data.get('invoiceDate')
                # word_count = task_data.get('wordCount', 0)        
                # end_date_conv = invoice_date.split('T')[0] if invoice_date else None
                expert_role = Employees.query.filter_by(employee_id=expert_id).first()
                if expert_role:
                    role = expert_role.roles
                else:
                    role = None  
                if role == "lead": 
                    new_assigned_order = AssignedOrders(
                        orders_id=order_id,
                        expert_id=expert_id,
                        assigned_date=task_date,
                        deadline=invoice_date_1,
                        team_deadline1=invoice_date_2,
                        team_deadline2=invoice_date_3,
                        team_deadline3=invoice_date_4,
                        team_deadline4=invoice_date_5,
                        team_deadline5=invoice_date_6,
                        no_of_words=no_of_words_1,
                        no_of_word1=no_of_words_2,
                        no_of_word2=no_of_words_3,
                        no_of_word3=no_of_words_4,
                        no_of_word4=no_of_words_5,
                        is_admin_assigned_by=False,
                        comments=comments,
                    )
                else:
                    print("elsdeee")
                    new_assigned_order = AssignedOrders(
                        orders_id=order_id,
                        expert_id=expert_id,
                        assigned_date=task_date,
                        assigned_expert_deadline=invoice_date_1,
                        expert_no_of_words=expert_no_of_words,
                        expert_no_of_word1=no_of_words_2,
                        expert_no_of_word2=expert_no_of_word1,
                        expert_no_of_word3=expert_no_of_word2,
                        expert_no_of_word4=expert_no_of_word3,
                        expert_no_of_word5=expert_no_of_word4,
                        expert_no_of_word6=expert_no_of_word5,
                        teammember_comment=comments,
                        assigned_expert_deadline1=invoice_date_2,
                        assigned_expert_deadline2=invoice_date_3,
                        assigned_expert_deadline3=invoice_date_4,
                        assigned_expert_deadline4=invoice_date_5,
                        assigned_expert_deadline5=invoice_date_6,
                    )
                         
                db.session.add(new_assigned_order)
            
            db.session.commit()
            return jsonify({'message': 'Order and assignments added successfully'}), 200
        except json.JSONDecodeError:
            return jsonify({'message': 'Invalid JSON data provided'}), 400
    else:
        return jsonify({'message': 'Order added successfully, no additional data provided'}), 200
    # ------------------- Add Client data  Module Route start -------------------__



@app.route('/updateClient/<clientId>', methods=['POST'])
@jwt_required()
def updateClient(clientId):
    print(clientId)
    client = Client.query.filter_by(client_id=clientId).one()

    name = request.form['Client_name']
    Client_status = request.form['Client_status']
    Client_contact = request.form['Client_contact']
    Client_email = request.form['Client_email']

    client.client_name = name
    client.client_contact = Client_contact
    client.client_email = Client_email
    if Client_status == "student":
        University = request.form['University']
        password = request.form['Student_password']
        client.university = University
        client.student_password = password
    else:
        business_name = request.form['Business_name']
        client.business_name = business_name
    db.session.add(client)
    db.session.commit()

    return jsonify({'message': 'Client Updated Successfully'}), 200


# ------------------- Add Client data  Module Route End -------------------__


# ------------------- Add Budget data  Module Route start -------------------__


# @app.route('/Budget', methods=['POST'])
# @jwt_required()
# def getBudget():
#     Client_name = request.form['Client_name']
#     Package_price = float(request.form['Package_price'])
#     Amount_Paid = float(request.form['Amount_Paid'])
#     Pending_amount = float(request.form['Pending_amount'])
#     Mode_of_payment = request.form['Mode_of_payment']
#     Status = request.form['Status']

#     client = Client.query.filter_by(client_name=Client_name).first()
#     if not client:
#         return jsonify(message='Client not found'), 404

#     budget = Budget(
#         client_id=client.client_id,
#         package_price=Package_price,
#         amount_paid=Amount_Paid,
#         pending_amount=Pending_amount,
#         mode_of_payment=Mode_of_payment,
#         status=Status
#     )

#     db.session.add(budget)
#     db.session.commit()

#     return jsonify(message='Budget added successfully')


# ------------------- Fatch OTM Mamber data For data table Module Route End -------------------__

# ------------------- Fatch Tutors(Expert) data For data table Module Route start -------------------__


@app.route('/getUsers', methods=['GET', 'POST'])
@jwt_required()
def getUsers():
    status = request.form['type']
    experts = Employees.query.filter_by(roles=status).all()
    data = []
    if experts:
        for expert in experts:
            expert_data = {
                'id': expert.employee_id,
                'firstname': expert.firstname,
                'lastname': expert.lastname,
                'contact': expert.contact,
                'email': expert.email,
                'address': expert.address,
                'designation': expert.designation
            }
            # Check if expert.dob is not None before formatting it
            if expert.dob:
                expert_data['DOB'] = expert.dob.strftime('%Y-%m-%d')
            else:
                expert_data['DOB'] = None  # or any other default value

            data.append(expert_data)

    response = flask.Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    response.set_data(json.dumps(data))
    return response


@app.route('/getExpertById/<expertId>', methods=['GET', 'POST'])
@jwt_required()
def getexpertById(expertId):
    experts = Employees.query.filter_by(employee_id=expertId).first()

    data = []
    if experts is not None:
        users = Users.query.filter_by(users_id=experts.employee_id).first()
        expert_data = {
            'id': experts.employee_id,
            'firstname': experts.firstname,
            'lastname': experts.lastname,
            'contact': experts.contact,
            'email': experts.email,
            'address': experts.address,
            'password': users.password,
            'designation': experts.designation
        }
        # Check if expert.dob is not None before formatting it
        if experts.dob:
            expert_data['DOB'] = experts.dob.strftime('%Y-%m-%d')
        else:
            expert_data['DOB'] = None  # or any other default value
        data.append(expert_data)

    response = flask.Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    response.set_data(json.dumps(data))
    return response


@app.route('/updateUsersDetails/<employeeId>', methods=['POST'])
def updateUsersDetails(employeeId):
    email = request.form['email']
    address = request.form['address']
    contact = request.form['contact']
    # expert_status = request.form['status']
    get_dob = flask.request.form['dob']
    password = flask.request.form['password']
    designation = flask.request.form['designation']

    if get_dob != "null":
        dob = datetime.datetime.strptime(get_dob, "%Y-%m-%d")
    else:
        dob = None
    # Check if the email already exists in the database
    employee = Employees.query.filter_by(employee_id=employeeId).first()

    # If the email is unique, proceed to add the user to the database
    if employee:
        users = Users.query.filter_by(users_id=employee.employee_id).first()
        users.password = password
        employee.email = email,
        employee.address = address,
        employee.contact = contact,
        employee.dob = dob,
        employee.designation = designation
        # employee.status=expert_status

        db.session.commit()

    return jsonify({'message': 'Updated Successfully'}), 200


@app.route('/getexpert', methods=['POST'])
@jwt_required()
def getexpert():
    type = request.form['user_type']
    if type == "permanent":
        experts = Employees.query.filter_by(status=type, roles = "expert").all()
    else:
        experts = Employees.query.filter_by(status=type).all()

    print(type)

    data = []
    for expert in experts:
        expert_data = {
            'id': expert.employee_id,
            'firstname': expert.firstname,
            'lastname': expert.lastname,
            'contact': expert.contact,
            'email': expert.email,
            'address': expert.address,
            'designation': expert.designation
        }
        data.append(expert_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/getExpertToAssign', methods=['POST'])
@jwt_required()
def getExpertToAssign():
    
    type = request.form['user_type']
    if type == "lead":
        experts = Employees.query.filter_by(status="permanent", roles = "lead").all()
    elif type == "permanent":
        experts = Employees.query.filter_by(status="permanent", roles = "expert").all()
    
    elif type == "operationMember":
        experts = Employees.query.filter_by(status="permanent", roles = "operationMember").all()
    else:
        experts = Employees.query.filter_by(status=type).all()
    
    print(type)

    data = []
    for expert in experts:
        expert_data = {
            'id': expert.employee_id,
            'firstname': expert.firstname,
            'lastname': expert.lastname,
            'contact': expert.contact,
            'email': expert.email,
            'address': expert.address,
            'designation': expert.designation
        }
        data.append(expert_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response
#assign to Qc expert
@app.route('/getQCExpertToAssign', methods=['POST'])
@jwt_required()
def getQCExpertToAssign():
    
    type = request.form['user_type']
    if type == "lead":
        experts = Employees.query.filter_by(status="permanent", roles = "lead").all()
    elif type == "permanent":
        experts = Employees.query.filter_by(status="permanent", roles = "expert").all()
    else:
        experts = Employees.query.filter_by(status=type).all()
    
    print(type)

    data = []
    for expert in experts:
        expert_data = {
            'id': expert.employee_id,
            'firstname': expert.firstname,
            'lastname': expert.lastname,
            'contact': expert.contact,
            'email': expert.email,
            'address': expert.address,
            'designation': expert.designation
        }
        data.append(expert_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/getclientdata', methods=['GET', 'POST'])
@jwt_required()
def getclient():
    clients = Client.query.all()

    data = []
    for client in clients:
        client_data = {
            'id': client.client_id,
            'Client_name': client.client_name,
            'Client_contact': client.client_contact,
            'Client_email': client.client_email,
            'Client_status': client.client_status,
            'University': client.university,
            'Business_name': client.business_name,
            'Student_login': client.student_login,
            'Student_password': client.student_password
        }
        data.append(client_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/getstudentclientdata', methods=['GET', 'POST'])
@jwt_required()
def getstudentclient():
    student_clients = Client.query.filter_by(client_status='student').all()

    data = []
    for student_client in student_clients:
        
        # invoice_data = Orders.query.filter_by(client_id=student_client.client_id).first()
        # if invoice_data is not None:
        #     invoice = True
        # else:
        #     invoice = False

        order_has_invoice = exists().where(InvoiceOrders.orders_id == Orders.orders_id)
        orders_without_invoice = Orders.query.filter(Orders.client_id == student_client.client_id)\
                                             .filter(~order_has_invoice)\
                                             .all()
        invoice = bool(orders_without_invoice)

        student_client_data = {
            'id': student_client.client_id,
            'name': student_client.client_name,
            'contact': student_client.client_contact,
            'email': student_client.client_email,
            'status': student_client.client_status,
            'university': student_client.university,
            'business_name': student_client.business_name,
            'login': student_client.student_login,
            'password': student_client.student_password,
            'invoice': invoice

        }
        data.append(student_client_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/getvendoreclientdata', methods=['GET', 'POST'])
@jwt_required()
def getvendoreclient():
    vendor_clients = Client.query.filter_by(client_status='vendor').all()

    data = []
    for vendor_client in vendor_clients:
        order_has_invoice = exists().where(InvoiceOrders.orders_id == Orders.orders_id)
        orders_without_invoice = Orders.query.filter(Orders.client_id == vendor_client.client_id)\
                                             .filter(~order_has_invoice)\
                                             .all()
        invoice = bool(orders_without_invoice)

        vendor_client_data = {
            'id': vendor_client.client_id,
            'name': vendor_client.client_name,
            'contact': vendor_client.client_contact,
            'email': vendor_client.client_email,
            'status': vendor_client.client_status,
            'university': vendor_client.university,
            'business_name': vendor_client.business_name,
            'login': vendor_client.student_login,
            'password': vendor_client.student_password,
            # 'budget': budget,
            'invoice': invoice
        }
        data.append(vendor_client_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response


# ------------------- Fatch  student client  data For data table Module Route End -------------------__

# ------------------- Fatch Client name data For Budget form Module Route start -------------------__


""" @app.route('/getclientnamedata', methods=['GET', 'POST'])
@jwt_required()
def getclientname():
    student_clients = Client.query.filter_by(client_status='student').all()

    data = []
    for student_client in student_clients:
        data.append(student_client.client_name)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response
 """


# ------------------- Fatch Task data For data table Module Route start -------------------__


@app.route('/getordersdata', methods=['GET'])
@jwt_required()
def getordersdata():
    # Get the current date
    today = datetime.datetime.now().date()

    # Filter orders based on end_date and status
    order_data = Orders.query.filter(Orders.end_date <= today, Orders.status != 'pass').all()

    data = []
    for order in order_data:
        # Get expert name by expert_id
        expert = Employees.query.filter_by(employee_id = order.expert_id).first()
        expert_name = expert.firstname if expert else None
        print("=====", expert_name)
        
        client = Client.query.filter_by(client_id = order.client_id).first()
        client_name = client.client_name if client else None
        
        order_dict = {
            'id': order.orders_id,
            'subject': order.task_subject,
            'expert': expert_name,
            'client': client_name,
            'order_status': order.status,
            'order_start_date': order.start_date,
            'order_end_date': order.end_date,
            'task_date': order.task_date,
            'order_price': order.order_budget,
        }
        data.append(order_dict)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/getinvoicesdata', methods=['GET'])
@jwt_required()
def get_unpaid_invoices():
    # Get the current date
    today = datetime.datetime.now().date()

    # Filter invoices based on unpaid status and due date passed
    unpaid_invoices = Invoice.query.filter(
        (Invoice.paid_amount == None) | (Invoice.paid_amount < Invoice.total),
        Invoice.due_date < today
    ).all()

    print("unpaid", unpaid_invoices)
    data = []
    for invoice in unpaid_invoices:
        client = Client.query.get(invoice.client_id)
        client_name = client.client_name if client else None
        
        formatted_due_date = invoice.due_date.strftime('%Y-%m-%d')
        formatted_invoice_date = invoice.invoice_date.strftime('%Y-%m-%d')
        
        invoice_dict = {
            'id': invoice.id,
            'invoice_number': invoice.invoice_number,
            'client': client_name,
            'invoice_date': formatted_invoice_date,
            'due_date': formatted_due_date,
            'total_amount': invoice.total_amount,
            'paid_amount': invoice.paid_amount,
            'currency': invoice.currency
        }
        data.append(invoice_dict)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/getOrdersStatus', methods=['POST'])
@jwt_required()
def getOrdersStatus():
    status = request.form['status']
    print(status)
    orders = Orders.query.filter_by(status=status).all()
    # orders = Orders.query.get(status)
    print(orders)
    data = []
    if orders:
        for order in orders:
            order_data = {
                'id': order.orders_id,
                'subject': order.task_subject,
                'expert_id': order.expert_id,
                'client_id': order.client_id,
                'order_status': order.status,
                'order_start_date': order.start_date,
                'order_end_date': order.end_date,

                'qc_expert_id': order.qc_expert_id,
                'otm_id': order.otm_id,
                'description': order.description,

                'word_count': order.word_count,
                'expert_price': order.expert_price,

            }
            data.append(order_data)

    else:
        data.append({'Error': 'No orders found'})

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/update_order/<orders_id>/<int:expert_id>', methods=['PUT'])
@jwt_required()
def update_order(orders_id, expert_id):
    # Extract the fields from the request
    data = request.json

    deadline_info = data.get('deadline')  # Assuming deadline info is provided as a list of dicts with 'id', 'deadline' and 'word_count'
    comments = data.get('comments')
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")
    task_date = formatted_date
    # Check if deadline_info is a list of dictionaries
    if not isinstance(deadline_info, list) or not all(isinstance(d, dict) for d in deadline_info):
        response = jsonify({'error': 'Invalid format for deadlines. Expected a list of dictionaries with "id", "deadline", and "word_count".'})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = 'application/json'
        return response, 400
    
    # Extract word counts and deadlines
    word_of_count_list = []
    deadlines = []
    ids = []
    for info in deadline_info:
        try:
            deadline = datetime.datetime.strptime(info['deadline'], '%Y-%m-%d')
            word_of_count_list.append(info['word_count'])
            deadlines.append(deadline)
            ids.append(info['id'])
        except ValueError as e:
            response = jsonify({'error': f'Invalid deadline format: {info["deadline"]}. Expected format: YYYY-MM-DD'})
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Content-Type'] = 'application/json'
            return response, 400
    
    for i in range(len(deadline_info)):
        assigned_order = AssignedOrders.query.filter_by(orders_id=orders_id, expert_id=expert_id, id=ids[i]).first()
        if assigned_order:
            # Update the existing order
            assigned_order.no_of_words = word_of_count_list[i]
            assigned_order.deadline = deadlines[i]
            assigned_order.comments = comments if comments is not None else assigned_order.comments
        else:
            # Add a new order
            new_order = AssignedOrders(
                orders_id=orders_id,
                expert_id=expert_id,
                no_of_words=word_of_count_list[i],
                deadline=deadlines[i],
                comments=comments,
                assigned_date=task_date
            )
            db.session.add(new_order)

    db.session.commit()

    response = jsonify({
        'message': 'Orders updated successfully',
        'orders': [{
            'id': info['id'],
            'deadline': deadlines[i].strftime('%d-%m-%Y') if deadlines[i] else None,
            'word_count': word_of_count_list[i]
        } for i, info in enumerate(deadline_info)],
        'comments': comments if comments is not None else assigned_order.comments,
        'expert_id': expert_id,
        'orders_id': orders_id
    })
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response, 200

# start from here

@app.route('/adminassignedby', methods=['POST'])
@jwt_required()
def adminassignedbyorders():
    current_user = get_jwt_identity()
    user = Users.query.filter_by(email=current_user).first()
    if user:
        current_expert_id = user.users_id
        role = user.type
    else:
        # Handle the case where the user is not found
        raise Exception("User not found")
    # Extract pagination parameters from request
    status = request.form['status']
    page = int(request.args.get('page', 1))  # Default to page 1
    per_page = int(request.args.get('per_page', 45))  # Default to 10 items per page
    status = request.form['status']
    search_term = request.form.get('search', None)
    orders = Orders.query.filter_by(status=status)

    assigned_new_orders_query = (Orders.query
                    .join(AssignedOrders, Orders.orders_id == AssignedOrders.orders_id)
                    .filter(Orders.status == status)
                    .filter(or_(
                        AssignedOrders.expert_id == current_expert_id,
                        AssignedOrders.qc_expert == current_expert_id,
                        AssignedOrders.assigned_expert == current_expert_id
                    ))
                    .distinct()
                    # .filter(
                    #     AssignedOrders.is_admin_assigned_by == 0,
                    #     AssignedOrders.is_admin_assigned_by.isnot(None)
                    # )
                )
    
    if role == 'lead':
        # For team lead, use the is_admin_assigned_by filter
        assigned_new_orders_query = assigned_new_orders_query.filter(
            AssignedOrders.is_admin_assigned_by == 0,
            AssignedOrders.is_admin_assigned_by.isnot(None)
        )
    elif role == 'operationMember':
        # For operation member, use the is_admin_assigned_by_operation filter
        assigned_new_orders_query = assigned_new_orders_query.filter(
            AssignedOrders.is_admin_assigned_by_operation == 0,
            AssignedOrders.is_admin_assigned_by_operation.isnot(None)
        )
    
    
    order_status = Orders.query.filter_by(orders_id=search_term).first()
    search_status = order_status.status if order_status else None
    if role == 'lead':
        orders = (db.session.query(Orders)
                    .join(AssignedOrders, Orders.orders_id == AssignedOrders.orders_id)
                    .filter(Orders.status == status)
                    .filter(
                        and_(
                            or_(
                                AssignedOrders.expert_id == current_expert_id,
                                AssignedOrders.assigned_expert == current_expert_id,
                                AssignedOrders.qc_expert == current_expert_id
                            ),
                            AssignedOrders.is_admin_assigned_by == 0,
                            AssignedOrders.is_admin_assigned_by.isnot(None)
                        )
                    ))
    elif role == "operationMember":
        orders = (db.session.query(Orders)
                    .join(AssignedOrders, Orders.orders_id == AssignedOrders.orders_id)
                    .filter(Orders.status == status)
                    .filter(
                        and_(
                            or_(
                                AssignedOrders.expert_id == current_expert_id,
                                AssignedOrders.assigned_expert == current_expert_id,
                                AssignedOrders.qc_expert == current_expert_id
                            ),
                            AssignedOrders.is_admin_assigned_by_operation == 0,
                            AssignedOrders.is_admin_assigned_by_operation.isnot(None)
                        )
                    ))
            


    # Apply search term if provided
    if search_term:
        assigned_new_orders_query = (orders
            .outerjoin(Employees, AssignedOrders.expert_id == Employees.employee_id)
            .filter(or_(
                Orders.orders_id.ilike(f"%{search_term}%"),
                Orders.description.ilike(f"%{search_term}%"),
                Orders.task_subject.ilike(f"%{search_term}%"),
                Employees.firstname.ilike(f"%{search_term}%")
            ),
                AssignedOrders.is_admin_assigned_by == 0
                )
        )
    # Pagination
    
    assigned_new_orders_count = assigned_new_orders_query.with_entities(func.count(Orders.orders_id.distinct())).scalar()

    # Apply pagination
    assigned_new_orders_paginated = (assigned_new_orders_query.offset((page - 1) * per_page).limit(per_page).all())

    # Use the paginated result
    orders = assigned_new_orders_paginated
    data = [] 
    if orders:
        for order in orders:
            client_data = Client.query.filter_by(client_id=order.client_id).first()

            if client_data is not None:
                client_name = client_data.client_name
            else:
                client_name = ""

            assigned_orders = AssignedOrders.query.filter_by(orders_id=order.orders_id).first()
            assigned_expert = None
            qc_assigned_expert = None
            expert_id = None
            qc_expert_id = None
            expert_roles = None

            #for experts_ids in assigned_orders:
            if assigned_orders is not None:
                print("not none", assigned_orders)
                expert_id = assigned_orders.expert_id
                expert_name_assigned = Employees.query.filter_by(employee_id=expert_id).first()    
                expert_roles = expert_name_assigned.roles if expert_name_assigned else None


                if expert_name_assigned is not None:
                    assigned_expert = expert_name_assigned.firstname
                else:
                    assigned_expert = None          
             
            if role == "lead":
                assigned_order = AssignedOrders.query.filter(
                                and_(
                                    AssignedOrders.orders_id == order.orders_id,
                                    AssignedOrders.is_admin_assigned_by == 0,
                                    AssignedOrders.is_admin_assigned_by.isnot(None)
                                )
                            ).order_by(AssignedOrders.id.desc()).first()
            else:
                assigned_order = AssignedOrders.query.filter(
                                and_(
                                    AssignedOrders.orders_id == order.orders_id,
                                    AssignedOrders.is_admin_assigned_by_operation == 0,
                                    AssignedOrders.is_admin_assigned_by_operation.isnot(None)
                                )
                            ).order_by(AssignedOrders.id.desc()).first()
                    
            #assigned_order = AssignedOrders.query.filter_by(orders_id=order.orders_id, is_admin_assigned_by=0).order_by(AssignedOrders.id.desc()).first()
            new_assigned_order = (db.session.query(AssignedOrders)
                                .join(Employees, AssignedOrders.expert_id == Employees.id)
                                .filter(AssignedOrders.orders_id == order.orders_id)
                                .filter(AssignedOrders.deadline.isnot(None))
                                .order_by(AssignedOrders.id.desc())
                                .first())
            if assigned_order is not None:
                expert_type = Employees.query.filter_by(employee_id=assigned_order.expert_id).first()
                if expert_type is not None:
                    expert_role = expert_type.roles
                    # Your existing code to handle expert_type
                else:
                    expert_role = ''   
                    # Handle the case where expert_type is None
            else:
                # Handle the case where assigned_order is None
                expert_role = None
                expert_type = None  # or handle it according to your application's needs
                
            expert_deadlines = AssignedOrders.query.filter_by(orders_id=order.orders_id).order_by(AssignedOrders.id.desc()).all()
            
            orders_with_deadline_only = AssignedOrders.query.filter_by(orders_id=order.orders_id) \
            .filter(or_(AssignedOrders.assigned_expert_deadline == None, 
                func.trim(AssignedOrders.assigned_expert_deadline) == '')) 


            #expert_word_from_admin = [assigned_orders.no_of_words for assigned_orders in expert_deadlines if assigned_orders.no_of_words is not None]
            expert_deadline_from_admin = [assigned_orders.deadline for assigned_orders in expert_deadlines if assigned_orders.deadline is not None]
            expert_word_count = [assigned_order.no_of_words for assigned_order in expert_deadlines if assigned_order.assigned_expert_deadline is not None and assigned_order.no_of_words is not None]
            #deadlines = [assigned_order.assigned_expert_deadline for assigned_order in expert_deadlines if assigned_order.assigned_expert_deadline is not None]
            subject=order.task_subject
            order_deadline = None
            assigned_expert_id = None
            assigned_expert_deadline = None
            assigned_expert_name = None
            #order_deadline = [order.deadline for order in orders_with_deadline_only]
            if assigned_order:   
                assigned_expert_id = assigned_order.assigned_expert
                comments = assigned_order.comments
                qc_expert_id = assigned_order.qc_expert
                qc_expert_name_assigned = Employees.query.filter_by(employee_id=qc_expert_id).first()            

                if qc_expert_name_assigned is not None:
                    qc_assigned_expert = qc_expert_name_assigned.firstname
                
                if assigned_expert_id is not None:
                    expert_name_assigned = Employees.query.filter_by(employee_id=assigned_expert_id).first()
                    if expert_name_assigned:
                        assigned_expert_name = expert_name_assigned.firstname
                    else:
                        assigned_expert_name = None
                     
                    assigned_expert_deadline = assigned_order.assigned_expert_deadline
            else:
                comments = None        
            for qc_order in orders_with_deadline_only:
                if not order.qc_expert:
                    qc_expert_id = qc_order.qc_expert
                    break  # Stop at the first occurrence of an order with empty qc_expert_id  
            order_create_deadline = order.end_date
            order_deadline = new_assigned_order.deadline if new_assigned_order else None
            
            is_admin_assigned_by = assigned_order.is_admin_assigned_by if assigned_order else None
            is_admin_assigned_by_operation = assigned_order.is_admin_assigned_by_operation if assigned_order else None 
            comment_for_opt = order.comments 
            comment_for_tl = assigned_orders.comment_for_tl if assigned_orders else None
            comment_forteam_member = assigned_order.teammember_comment if assigned_order else None
            incentive = assigned_orders.incentive if assigned_orders else None
            remark = assigned_orders.remarks if assigned_orders else None
            assigned_expert_deadline = assigned_order.assigned_expert_deadline  if assigned_order else None
            deadline_for_operation = assigned_order.deadline_for_operation if assigned_order else None 

            order_data = {
                'id': order.orders_id,
                'subject': order.task_subject,
                'expertId': expert_id,
                'expert_id': assigned_expert,
                'expert_type': expert_roles, 
                'client_id': client_name,
                'order_status': order.status,
                'order_start_date': order.start_date,
                'order_end_date': order_deadline,
                'description': order.description,
                'comments': comments,
                'word_count': order.word_count,
                'expert_price': order.expert_price,
                'budget': order.order_budget,
                'currency': order.currency,
                'expert_currency': order.expert_currency,
                'expert_end_date': order.expert_deadline,
                'assigned_expert': assigned_expert_name,
                'assigned_expert_id': assigned_expert_id,
                'assigned_expert_deadline': assigned_expert_deadline,
                'order_create_deadline': order_create_deadline,  
                'qc_expert': qc_assigned_expert,   
                "qc_expert_id": qc_expert_id,
                "comment_for_opt": comment_for_opt,
                "comment_for_tl": comment_for_tl,
                "incentive": incentive,
                "is_admin_assigned_by": is_admin_assigned_by,
                "remark": remark, 
                "comment_forteam_member": comment_forteam_member,
                "deadline_for_operation": deadline_for_operation,
                "is_admin_assigned_by_operation": is_admin_assigned_by_operation,
                "operation_status": order.operation_status if assigned_orders else None,
                "team_lead_status": order.team_lead_status if assigned_orders else None
           
                       
            } 
            if expert_deadlines:
                deadline_objects = []
                for deadline in expert_deadlines:
                    deadline_data = {
                        'id': deadline.id,
                        'expert_deadline': deadline.assigned_expert_deadline,
                        'expert_word_count': deadline.no_of_words
                    }
                    deadline_objects.append(deadline_data)
                order_data['deadlines_with_word_count'] = deadline_objects
            data.append(order_data)
            
    else:  

        data.append({'Error': 'No orders found', "Status": f"Order in {search_status} tab."})

    from datetime import datetime, date


    deadline_data = []
    for order in data:
        # Use .get() to safely extract the values from the order dictionary
        order_end_date = order.get('order_end_date', None)
        assigned_expert_deadline = order.get('assigned_expert_deadline', None)
        expert_type = order.get('expert_type', None)  # Extract expert_type

        # Normalize order_end_date
        if order_end_date is None or order_end_date == datetime(9999, 12, 31):
            order_end_date = None  # Treat None or placeholder as None
        elif isinstance(order_end_date, datetime):
            pass  # Already a datetime object
        elif isinstance(order_end_date, date):  # If it's a date, convert to datetime
            order_end_date = datetime.combine(order_end_date, datetime.min.time())
        else:
            raise ValueError(f"Unexpected type for order_end_date: {type(order_end_date)}")

        # Normalize assigned_expert_deadline
        if assigned_expert_deadline is None or assigned_expert_deadline == datetime(9999, 12, 31):
            assigned_expert_deadline = None  # Treat None or placeholder as None
        elif isinstance(assigned_expert_deadline, datetime):
            pass  # Already a datetime object
        elif isinstance(assigned_expert_deadline, date):  # If it's a date, convert to datetime
            assigned_expert_deadline = datetime.combine(assigned_expert_deadline, datetime.min.time())
        else:
            raise ValueError(f"Unexpected type for assigned_expert_deadline: {type(assigned_expert_deadline)}")

        # Add to the list for sorting
        deadline_data.append((order_end_date, assigned_expert_deadline, expert_type, order))

    # Sorting logic
    def sorting_key(x):
        order_end_date, assigned_expert_deadline, expert_type, order = x
        
        # Check if the role is 'operationMember'
        if role == 'operationMember':
            # For operationMember, treat both deadlines as far-future datetime
            return datetime(9999, 12, 31)
        
        # For other roles (like 'lead'), sort by the earliest of the two dates
        if role == 'lead':
            # Return the 'order_end_date' if it is available, otherwise 'assigned_expert_deadline'
            return order_end_date if order_end_date else assigned_expert_deadline or datetime(9999, 12, 31)

        # Return the minimum of the two deadlines if it's not a 'lead'
        return min(filter(lambda d: d is not None, (order_end_date, assigned_expert_deadline)), default=datetime(9999, 12, 31))

    # Sort deadline_data with the new sorting key
    deadline_data.sort(key=sorting_key)

    # Prepare the final sorted data
    sorted_data = [entry[3] for entry in deadline_data]
    assigned_new_orders_count = len(sorted_data)
    pagination_info = {
        'page': page,
        'per_page': per_page,
        'total_orders': assigned_new_orders_count,
        'total_pages': (assigned_new_orders_count + per_page - 1) // per_page  # Ceiling division
    }

    # Create response with pagination info
    response = jsonify({
        'pagination': pagination_info,
        'orders': sorted_data
    })

    # response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/assignedoperation', methods=['POST'])
@jwt_required()
def assignedbyopeartion():
    current_user = get_jwt_identity()
    user = Users.query.filter_by(email=current_user).first()
    if user:
        current_expert_id = user.users_id
    else:
        # Handle the case where the user is not found
        raise Exception("User not found")
    # Extract pagination parameters from request
    status = request.form['status']
    page = int(request.args.get('page', 1))  # Default to page 1
    per_page = int(request.args.get('per_page', 45))  # Default to 10 items per page
    status = request.form['status']
    search_term = request.form.get('search', None)
    orders = Orders.query.filter_by(status=status)

    assigned_new_orders_query = (Orders.query
                    .join(AssignedOrders, Orders.orders_id == AssignedOrders.orders_id)
                    .filter(Orders.status == status)
                    .filter(or_(
                        AssignedOrders.expert_id == current_expert_id,
                        AssignedOrders.qc_expert == current_expert_id,
                        AssignedOrders.assigned_expert == current_expert_id
                    ))
                    .distinct()
                    .filter(
                        AssignedOrders.is_admin_assigned_by_operation == 0,
                        AssignedOrders.is_admin_assigned_by_operation.isnot(None)
                    )
                )
   
    
    order_status = Orders.query.filter_by(orders_id=search_term).first()
    search_status = order_status.status if order_status else None
    orders = (db.session.query(Orders)
                .join(AssignedOrders, Orders.orders_id == AssignedOrders.orders_id)
                .filter(Orders.status == status)
                .filter(
                    and_(
                        or_(
                            AssignedOrders.expert_id == current_expert_id,
                            AssignedOrders.assigned_expert == current_expert_id,
                            AssignedOrders.qc_expert == current_expert_id
                        ),
                        AssignedOrders.is_admin_assigned_by_operation == 0,
                        AssignedOrders.is_admin_assigned_by_operation.isnot(None)
                    )
                )
)


    # Apply search term if provided
    if search_term:
        assigned_new_orders_query = (orders
            .outerjoin(Employees, AssignedOrders.expert_id == Employees.employee_id)
            .filter(or_(
                Orders.orders_id.ilike(f"%{search_term}%"),
                Orders.description.ilike(f"%{search_term}%"),
                Orders.task_subject.ilike(f"%{search_term}%"),
                Employees.firstname.ilike(f"%{search_term}%")
            ),
                AssignedOrders.is_admin_assigned_by_operation == 0
                )
        )
    # Pagination
    
    assigned_new_orders_count = assigned_new_orders_query.with_entities(func.count(Orders.orders_id.distinct())).scalar()

    # Apply pagination
    assigned_new_orders_paginated = (assigned_new_orders_query.offset((page - 1) * per_page).limit(per_page).all())

    # Use the paginated result
    orders = assigned_new_orders_paginated
    data = [] 
    if orders:
        for order in orders:
            client_data = Client.query.filter_by(client_id=order.client_id).first()

            if client_data is not None:
                client_name = client_data.client_name
            else:
                client_name = ""

            assigned_orders = AssignedOrders.query.filter_by(orders_id=order.orders_id).first()
            assigned_expert = None
            qc_assigned_expert = None
            expert_id = None
            qc_expert_id = None
            expert_roles = None

            #for experts_ids in assigned_orders:
            if assigned_orders is not None:
                print("not none", assigned_orders)
                expert_id = assigned_orders.expert_id
                expert_name_assigned = Employees.query.filter_by(employee_id=expert_id).first()    
                expert_roles = expert_name_assigned.roles if expert_name_assigned else None


                if expert_name_assigned is not None:
                    assigned_expert = expert_name_assigned.firstname
                else:
                    assigned_expert = None          
            
           
           
          
            
            assigned_order = AssignedOrders.query.filter(
                            and_(
                                AssignedOrders.orders_id == order.orders_id,
                                AssignedOrders.is_admin_assigned_by_operation == 0,
                                AssignedOrders.is_admin_assigned_by_operation.isnot(None)
                            )
                        ).order_by(AssignedOrders.id.desc()).first()
            #assigned_order = AssignedOrders.query.filter_by(orders_id=order.orders_id, is_admin_assigned_by=0).order_by(AssignedOrders.id.desc()).first()
            new_assigned_order = (db.session.query(AssignedOrders)
                                .join(Employees, AssignedOrders.expert_id == Employees.id)
                                .filter(AssignedOrders.orders_id == order.orders_id)
                                .filter(AssignedOrders.deadline.isnot(None))
                                .order_by(AssignedOrders.id.desc())
                                .first())
            if assigned_order is not None:
                expert_type = Employees.query.filter_by(employee_id=assigned_order.expert_id).first()
                if expert_type is not None:
                    expert_role = expert_type.roles
                    # Your existing code to handle expert_type
                else:
                    expert_role = ''   
                    # Handle the case where expert_type is None
            else:
                # Handle the case where assigned_order is None
                expert_role = None
                expert_type = None  # or handle it according to your application's needs
                
            expert_deadlines = AssignedOrders.query.filter_by(orders_id=order.orders_id).order_by(AssignedOrders.id.desc()).all()
            
            orders_with_deadline_only = AssignedOrders.query.filter_by(orders_id=order.orders_id) \
            .filter(or_(AssignedOrders.assigned_expert_deadline == None, 
                func.trim(AssignedOrders.assigned_expert_deadline) == '')) 


            #expert_word_from_admin = [assigned_orders.no_of_words for assigned_orders in expert_deadlines if assigned_orders.no_of_words is not None]
            expert_deadline_from_admin = [assigned_orders.deadline for assigned_orders in expert_deadlines if assigned_orders.deadline is not None]
            expert_word_count = [assigned_order.no_of_words for assigned_order in expert_deadlines if assigned_order.assigned_expert_deadline is not None and assigned_order.no_of_words is not None]
            #deadlines = [assigned_order.assigned_expert_deadline for assigned_order in expert_deadlines if assigned_order.assigned_expert_deadline is not None]
            subject=order.task_subject
            order_deadline = None
            assigned_expert_id = None
            assigned_expert_deadline = None
            assigned_expert_name = None
            #order_deadline = [order.deadline for order in orders_with_deadline_only]
            if assigned_order:   
                assigned_expert_id = assigned_order.assigned_expert
                comments = assigned_order.comments
                qc_expert_id = assigned_order.qc_expert
                qc_expert_name_assigned = Employees.query.filter_by(employee_id=qc_expert_id).first()            

                if qc_expert_name_assigned is not None:
                    qc_assigned_expert = qc_expert_name_assigned.firstname
                
                if assigned_expert_id is not None:
                    expert_name_assigned = Employees.query.filter_by(employee_id=assigned_expert_id).first()
                    if expert_name_assigned:
                        assigned_expert_name = expert_name_assigned.firstname
                    else:
                        assigned_expert_name = None
                     
                    assigned_expert_deadline = assigned_order.assigned_expert_deadline
            else:
                comments = None        
            for qc_order in orders_with_deadline_only:
                if not order.qc_expert:
                    qc_expert_id = qc_order.qc_expert
                    break  # Stop at the first occurrence of an order with empty qc_expert_id  
            order_create_deadline = order.end_date
            order_deadline = new_assigned_order.deadline if new_assigned_order else None
            
            is_admin_assigned_by_operation = assigned_order.is_admin_assigned_by_operation if assigned_order else None
            comment_for_opt = order.comments 
            comment_for_tl = assigned_orders.comment_for_tl if assigned_orders else None
            comment_forteam_member = assigned_order.teammember_comment if assigned_order else None
            incentive = assigned_orders.incentive if assigned_orders else None
            remark = assigned_orders.remarks if assigned_orders else None
            assigned_expert_deadline = assigned_order.assigned_expert_deadline  if assigned_order else None

            order_data = {
                'id': order.orders_id,
                'subject': order.task_subject,
                'expertId': expert_id,
                'expert_id': assigned_expert,
                'expert_type': expert_roles, 
                'client_id': client_name,
                'order_status': order.status,
                'order_start_date': order.start_date,
                'order_end_date': order_deadline,
                'description': order.description,
                'comments': comments,
                'word_count': order.word_count,
                'expert_price': order.expert_price,
                'budget': order.order_budget,
                'currency': order.currency,
                'expert_currency': order.expert_currency,
                'expert_end_date': order.expert_deadline,
                'assigned_expert': assigned_expert_name,
                'assigned_expert_id': assigned_expert_id,
                'assigned_expert_deadline': assigned_expert_deadline,
                'order_create_deadline': order_create_deadline,  
                'qc_expert': qc_assigned_expert,   
                "qc_expert_id": qc_expert_id,
                "comment_for_opt": comment_for_opt,
                "comment_for_tl": comment_for_tl,
                "incentive": incentive,
                "is_admin_assigned_by_operation": is_admin_assigned_by_operation,
                "remark": remark, 
                "comment_forteam_member": comment_forteam_member

                       
            } 
            if expert_deadlines:
                deadline_objects = []
                for deadline in expert_deadlines:
                    deadline_data = {
                        'id': deadline.id,
                        'expert_deadline': deadline.assigned_expert_deadline,
                        'expert_word_count': deadline.no_of_words
                    }
                    deadline_objects.append(deadline_data)
                order_data['deadlines_with_word_count'] = deadline_objects
            data.append(order_data)
            
    else:  

        data.append({'Error': 'No orders found', "Status": f"Order in {search_status} tab."})

    from datetime import datetime, date
    deadline_data = []
    for order in data:
        # Extract deadlines
        order_end_date = order['order_end_date']
        assigned_expert_deadline = order['assigned_expert_deadline']
        expert_type = order['expert_type']  # Extract expert_type


        # Normalize order_end_date
        if order_end_date is None or order_end_date == datetime(9999, 12, 31):
            order_end_date = None  # Treat None or placeholder as None
        elif isinstance(order_end_date, datetime):
            pass  # Already a datetime object
        elif isinstance(order_end_date, date):  # If it's a date, convert to datetime
            order_end_date = datetime.combine(order_end_date, datetime.min.time())
        else:
            raise ValueError(f"Unexpected type for order_end_date: {type(order_end_date)}")

        # Normalize assigned_expert_deadline
        if assigned_expert_deadline is None or assigned_expert_deadline == datetime(9999, 12, 31):
            assigned_expert_deadline = None  # Treat None or placeholder as None
        elif isinstance(assigned_expert_deadline, datetime):
            pass  # Already a datetime object
        elif isinstance(assigned_expert_deadline, date):  # If it's a date, convert to datetime
            assigned_expert_deadline = datetime.combine(assigned_expert_deadline, datetime.min.time())
        else:
            raise ValueError(f"Unexpected type for assigned_expert_deadline: {type(assigned_expert_deadline)}")

        # Add to the list for sorting
        deadline_data.append((order_end_date, assigned_expert_deadline, expert_type, order))

    # Sort based on the logic provided
    deadline_data.sort(key=lambda x: (
        x[0] if x[2] == 'lead' else min(filter(lambda d: d is not None, (x[0], x[1])), default=datetime.max)  # Get the minimum of the two dates
    ))

    # Prepare the final sorted data
    sorted_data = [entry[3] for entry in deadline_data]
    assigned_new_orders_count = len(sorted_data)
    pagination_info = {
        'page': page,
        'per_page': per_page,
        'total_orders': assigned_new_orders_count,
        'total_pages': (assigned_new_orders_count + per_page - 1) // per_page  # Ceiling division
    }
    
    # Create response with pagination info
    response = jsonify({
        'pagination': pagination_info,
        'orders': sorted_data
    })
    
    # response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response




@app.route('/dashboard_attention_orders', methods=['POST'])
@jwt_required()
def dashboardAttentionOrders():
    current_user = get_jwt_identity()
    from datetime import datetime

    today = datetime.today().date()
    user = Users.query.filter_by(email=current_user).first()
    if user:
         current_expert_id = user.users_id
    else:
        # Handle the case where the user is not found
        raise Exception("User not found")

    current_month_start = today.replace(day=1)
    current_month_end = (current_month_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    is_admin = current_expert_id = 1

    # Base query for orders
    if is_admin:
        assigned_new_orders_query = (
            db.session.query(Orders)
            .join(AssignedOrders, Orders.orders_id == AssignedOrders.orders_id)
            .filter(
                AssignedOrders.deadline == today,      # Only today's deadlines
                Orders.status == "assigned"            # Status in Orders table
            )
            .limit(4)  # Limit to 4 results
        )
    else:
        assigned_new_orders_query = (
            db.session.query(Orders)
            .join(AssignedOrders, Orders.orders_id == AssignedOrders.orders_id)
            .filter(
                AssignedOrders.deadline == today,      # Only today's deadlines
                Orders.status == "assigned",           # Status in Orders table
                or_(
                    AssignedOrders.expert_id == current_expert_id,
                    AssignedOrders.qc_expert == current_expert_id,
                    AssignedOrders.assigned_expert == current_expert_id
                )
            )
            .limit(4)  # Limit to 4 results
        )

    # Use select_from and specify the join explicitly
    
    orders = assigned_new_orders_query.all()


    data = []
    if orders:
        for order in orders:
            client_data = Client.query.filter_by(client_id=order.client_id).first()

            if client_data is not None:
                client_name = client_data.client_name
            else:
                client_name = ""

            assigned_orders = AssignedOrders.query.filter_by(orders_id=order.orders_id).first()
            assigned_expert = None
            qc_assigned_expert = None
            expert_id = None
            qc_expert_id = None
            expert_roles = None

            #for experts_ids in assigned_orders:
            if assigned_orders is not None:
                print("not none", assigned_orders)
                expert_id = assigned_orders.expert_id
                expert_name_assigned = Employees.query.filter_by(employee_id=expert_id).first()    
                expert_roles = expert_name_assigned.roles if expert_name_assigned else None


                if expert_name_assigned is not None:
                    assigned_expert = expert_name_assigned.firstname
                else:
                    assigned_expert = None
                    
           
            assigned_order = AssignedOrders.query.filter_by(orders_id=order.orders_id, deadline=today).order_by(AssignedOrders.id.desc()).first()
            new_assigned_order = (db.session.query(AssignedOrders)
                        .outerjoin(Employees, AssignedOrders.expert_id == Employees.id)
                        .filter(AssignedOrders.orders_id == order.orders_id)
                        .filter(AssignedOrders.deadline.isnot(None))
                        .order_by(AssignedOrders.id.desc())
                        .first())
            if assigned_order is not None:
                expert_type = Employees.query.filter_by(employee_id=assigned_order.expert_id).first()
                if expert_type is not None:
                    expert_role = expert_type.roles
                    # Your existing code to handle expert_type
                else:
                    expert_role = ''   
                    # Handle the case where expert_type is None
            else:
                # Handle the case where assigned_order is None
                expert_role = None
                expert_type = None  # or handle it according to your application's needs
                
            expert_deadlines = AssignedOrders.query.filter_by(orders_id=order.orders_id).order_by(AssignedOrders.id.desc()).all()
            
            orders_with_deadline_only = AssignedOrders.query.filter_by(orders_id=order.orders_id) \
            .filter(or_(AssignedOrders.assigned_expert_deadline == None, 
                func.trim(AssignedOrders.assigned_expert_deadline) == '')) 


            #expert_word_from_admin = [assigned_orders.no_of_words for assigned_orders in expert_deadlines if assigned_orders.no_of_words is not None]
            expert_deadline_from_admin = [assigned_orders.deadline for assigned_orders in expert_deadlines if assigned_orders.deadline is not None]
            expert_word_count = [assigned_order.no_of_words for assigned_order in expert_deadlines if assigned_order.assigned_expert_deadline is not None and assigned_order.no_of_words is not None]
            #deadlines = [assigned_order.assigned_expert_deadline for assigned_order in expert_deadlines if assigned_order.assigned_expert_deadline is not None]
            subject=order.task_subject
            order_deadline = None
            assigned_expert_id = None
            assigned_expert_deadline = None
            assigned_expert_name = None
            #order_deadline = [order.deadline for order in orders_with_deadline_only]
            if assigned_order:   
                assigned_expert_id = assigned_order.assigned_expert
                comments = assigned_order.comments
                qc_expert_id = assigned_order.qc_expert
                qc_expert_name_assigned = Employees.query.filter_by(employee_id=qc_expert_id).first()            

                if qc_expert_name_assigned is not None:
                    qc_assigned_expert = qc_expert_name_assigned.firstname
                
                print("==qc====", qc_expert_id, qc_assigned_expert)
                print("assigned orders", assigned_order)
                print("assigned expert", assigned_expert_id, )
                if assigned_expert_id is not None:
                    expert_name_assigned = Employees.query.filter_by(employee_id=assigned_expert_id).first()
                    if expert_name_assigned:
                        assigned_expert_name = expert_name_assigned.firstname
                    else:
                        assigned_expert_name = None
                     
                    assigned_expert_deadline = assigned_order.assigned_expert_deadline
            else:
                comments = None        
            for qc_order in orders_with_deadline_only:
                if not order.qc_expert:
                    qc_expert_id = qc_order.qc_expert
                    break  # Stop at the first occurrence of an order with empty qc_expert_id  
            order_create_deadline = order.end_date
            order_deadline = new_assigned_order.deadline if new_assigned_order else None
            
            is_admin_assigned_by = assigned_order.is_admin_assigned_by if assigned_order else None
            comment_for_opt = order.comments 
            comment_for_tl = assigned_orders.comment_for_tl if assigned_orders else None
            comment_forteam_member = assigned_order.teammember_comment if assigned_order else None
            incentive = assigned_orders.incentive if assigned_orders else None
            remark = assigned_orders.remarks if assigned_orders else None
            assigned_expert_deadline = assigned_order.assigned_expert_deadline if assigned_order else None

            order_data = {
                'id': order.orders_id,
                'subject': order.task_subject,
                'expertId': expert_id,
                'expert_id': assigned_expert,
                'expert_type': expert_roles, 
                'client_id': client_name,
                'order_status': order.status,
                'order_start_date': order.start_date,
                'order_end_date': order_deadline,
                'description': order.description,
                'comments': comments,
                'word_count': order.word_count,
                'expert_price': order.expert_price,
                'budget': order.order_budget,
                'currency': order.currency,
                'expert_currency': order.expert_currency,
                'expert_end_date': order.expert_deadline,
                'assigned_expert': assigned_expert_name,
                'assigned_expert_id': assigned_expert_id,
                'assigned_expert_deadline': assigned_expert_deadline,
                'order_create_deadline': order_create_deadline,  
                'qc_expert': qc_assigned_expert,   
                "qc_expert_id": qc_expert_id,
                "comment_for_opt": comment_for_opt,
                "comment_for_tl": comment_for_tl,
                "incentive": incentive,
                "is_admin_assigned_by": is_admin_assigned_by,
                "remark": remark, 
                "comment_forteam_member": comment_forteam_member


                       
            } 
            data.append(order_data)
            
    else:     

        data.append({'Error': 'No orders found'})

    
    # Create response with pagination info
    response = jsonify({
        'orders': data
    })
    
    # response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/getOrdersBySubjectAndStatus', methods=['POST'])
@jwt_required()
def getOrdersBySubjectAndStatus():
    from datetime import datetime, date  
 
    current_user = get_jwt_identity()
    print("curren", current_user)
    user = Users.query.filter_by(email=current_user).first()
    if user:
         current_expert_id = user.users_id
         role = user.type
    else:
        # Handle the case where the user is not found
        raise Exception("User not found")

    # Extract pagination parameters from request
    page = int(request.args.get('page', 1))  # Default to page 1
    per_page = int(request.args.get('per_page', 45))  # Default to 10 items per page
    status = request.form['status']
    search_term = request.form.get('search', None)
    orders = Orders.query.filter_by(status=status)
    order_status = Orders.query.filter_by(orders_id=search_term).first()
    search_status = order_status.status if order_status else None
    is_admin = current_expert_id == 1

    # Construct the base query
    query = Orders.query.filter(Orders.status == status)
    if current_expert_id == 1:
        # If admin, include all records
        assigned_new_orders_query = query.distinct().order_by(Orders.end_date)
    else:
        # If not admin, include only records where current_expert_id matches any of the fields
        # assigned_new_orders_query = (
        #     db.session.query(Orders)
        #     .join(AssignedOrders, AssignedOrders.orders_id == Orders.orders_id)  # Join condition
        #     .filter(
        #         or_(
        #             AssignedOrders.expert_id == current_expert_id,
        #             AssignedOrders.qc_expert == current_expert_id,
        #             AssignedOrders.assigned_expert == current_expert_id
        #         ),
        #         Orders.status == status,
             
        #     )
        # )
        if role == "operationMember":
            print("role", role)
            assigned_new_orders_query = (db.session.query(Orders)
                        .join(AssignedOrders, AssignedOrders.orders_id == Orders.orders_id)  # Join condition
                        .filter(Orders.status == status)
                        .filter(or_(
                            AssignedOrders.expert_id == current_expert_id,
                            AssignedOrders.qc_expert == current_expert_id,
                            AssignedOrders.assigned_expert == current_expert_id
                        ))
                        .distinct()
                        .filter(
                            AssignedOrders.is_admin_assigned_by_operation.is_(None)  # Ensure is_admin_assigned_by is NULL

        )
                    )
        else:   
                assigned_new_orders_query = (db.session.query(Orders)
                                .join(AssignedOrders, AssignedOrders.orders_id == Orders.orders_id)  # Join condition
                                .filter(Orders.status == status)
                                .filter(or_(
                                    AssignedOrders.expert_id == current_expert_id,
                                    AssignedOrders.qc_expert == current_expert_id,
                                    AssignedOrders.assigned_expert == current_expert_id
                                ))
                                .distinct()
                                .filter(
                                    AssignedOrders.is_admin_assigned_by.is_(None)  # Ensure is_admin_assigned_by is NULL

                )
                            )
    
    # Joining AssignedOrders and Employees
    # assigned_new_orders_query = (assigned_new_orders_query
    #     .outerjoin(AssignedOrders, Orders.orders_id == AssignedOrders.orders_id)
    #     .outerjoin(Employees, AssignedOrders.expert_id == Employees.employee_id)
    # )    
        
    if search_term:
        if user.users_id == 1 or user.users_id == "admin":
            assigned_new_orders_query = (orders
                            .outerjoin(AssignedOrders, Orders.orders_id == AssignedOrders.orders_id)
                            .outerjoin(Employees, AssignedOrders.expert_id == Employees.employee_id)
                            .filter(or_(
                                Orders.orders_id.ilike(f"%{search_term}%"),
                                Orders.description.ilike(f"%{search_term}%"),
                                Orders.task_subject.ilike(f"%{search_term}%"),
                                Employees.firstname.ilike(f"%{search_term}%")
                            ))
                    )
            
        else:
                
            assigned_new_orders_query = (
                        orders
                        .outerjoin(AssignedOrders, Orders.orders_id == AssignedOrders.orders_id)
                        .outerjoin(Employees, AssignedOrders.expert_id == Employees.employee_id)
                        .filter(
                            or_(
                                Orders.orders_id.ilike(f"%{search_term}%"),
                                Orders.description.ilike(f"%{search_term}%"),
                                Orders.task_subject.ilike(f"%{search_term}%"),
                                Employees.firstname.ilike(f"%{search_term}%")
                            ),
                            or_(
                                AssignedOrders.expert_id == current_expert_id,
                                AssignedOrders.qc_expert == current_expert_id,
                                AssignedOrders.assigned_expert == current_expert_id
                            ),
                            # New condition to check if is_admin_assigned_by and is_admin_assigned_by_operation are None
                            AssignedOrders.is_admin_assigned_by == None,
                            AssignedOrders.is_admin_assigned_by_operation == None
                        )
                    )
               
    assigned_new_orders_count = assigned_new_orders_query.count()
    assigned_orders_paginated = assigned_new_orders_query.offset((page - 1) * per_page).limit(per_page).all()

    orders = assigned_orders_paginated
    data = []
    if orders:
        for order in orders:
            client_data = Client.query.filter_by(client_id=order.client_id).first()

            if client_data is not None:
                client_name = client_data.client_name
            else:
                client_name = ""

            assigned_orders = AssignedOrders.query.filter_by(orders_id=order.orders_id).first()
            assigned_expert = None
            qc_assigned_expert = None
            expert_id = None
            qc_expert_id = None
            expert_roles = None

            #for experts_ids in assigned_orders:
            if assigned_orders is not None:
                print("not none", assigned_orders)
                expert_id = assigned_orders.expert_id
                print("expert_ihhhhd", expert_id)
                expert_name_assigned = Employees.query.filter_by(employee_id=expert_id).first()    
                expert_roles = expert_name_assigned.roles if expert_name_assigned else None


                if expert_name_assigned is not None:
                    assigned_expert = expert_name_assigned.firstname
                else:
                    assigned_expert = None
                    
           
            assigned_order = AssignedOrders.query.filter_by(orders_id=order.orders_id).order_by(AssignedOrders.id).first()
            assigned_experts = (db.session.query(AssignedOrders)
                            .outerjoin(Employees, AssignedOrders.expert_id == Employees.id)
                            .filter(AssignedOrders.orders_id == order.orders_id)
                            .order_by(AssignedOrders.id)
                            .first())
                    
           
            if assigned_order is not None:
                expert_type = Employees.query.filter_by(employee_id=assigned_order.expert_id).first()
                if expert_type is not None:
                    expert_role = expert_type.roles
                    # Your existing code to handle expert_type
                else:
                    expert_role = ''   
                    # Handle the case where expert_type is None
            else:
                # Handle the case where assigned_order is None
                expert_role = None
                expert_type = None  # or handle it according to your application's needs
                
            expert_deadlines = AssignedOrders.query.filter_by(orders_id=order.orders_id).order_by(AssignedOrders.id.desc()).all()
            
            orders_with_deadline_only = AssignedOrders.query.filter_by(orders_id=order.orders_id) \
            .filter(or_(AssignedOrders.assigned_expert_deadline == None, 
                func.trim(AssignedOrders.assigned_expert_deadline) == '')) 


            #expert_word_from_admin = [assigned_orders.no_of_words for assigned_orders in expert_deadlines if assigned_orders.no_of_words is not None]
            expert_deadline_from_admin = [assigned_orders.deadline for assigned_orders in expert_deadlines if assigned_orders.deadline is not None]
            expert_word_count = [assigned_order.no_of_words for assigned_order in expert_deadlines if assigned_order.assigned_expert_deadline is not None and assigned_order.no_of_words is not None]
            #deadlines = [assigned_order.assigned_expert_deadline for assigned_order in expert_deadlines if assigned_order.assigned_expert_deadline is not None]
            subject=order.task_subject
            order_deadline = None
            assigned_expert_id = None
            assigned_expert_deadline = None
            assigned_expert_name = None
            #order_deadline = [order.deadline for order in orders_with_deadline_only]
            if assigned_order:   
                assigned_expert_id = assigned_order.assigned_expert if assigned_order else None
                comments = assigned_order.comments
                qc_expert_id = assigned_order.qc_expert
                qc_expert_name_assigned = Employees.query.filter_by(employee_id=qc_expert_id).first()            

                if qc_expert_name_assigned is not None:
                    qc_assigned_expert = qc_expert_name_assigned.firstname
                
                print("==qc====", qc_expert_id, qc_assigned_expert)
                print("assigned orders", assigned_order)
                print("assigned expert", assigned_expert_id )
                if assigned_expert_id is not None:
                    expert_name_assigned = Employees.query.filter_by(employee_id=assigned_expert_id).first()
                    print("--expert_name_assigned.firstname--", expert_name_assigned.firstname)
                    if expert_name_assigned:
                        assigned_expert_name = expert_name_assigned.firstname
                    else:
                        assigned_expert_name = None
                     
                    assigned_expert_deadline = assigned_order.assigned_expert_deadline
            else:
                comments = None        
            for qc_order in orders_with_deadline_only:
                if not order.qc_expert:
                    qc_expert_id = qc_order.qc_expert
                    break  # Stop at the first occurrence of an order with empty qc_expert_id  
            order_create_deadline = order.end_date
            order_deadline = assigned_order.deadline if assigned_order else None
            
            is_admin_assigned_by = assigned_order.is_admin_assigned_by if assigned_order else None
            is_admin_assigned_by_operation = assigned_order.is_admin_assigned_by_operation if assigned_order else None

            comment_for_opt = order.comments 
            comment_for_tl = assigned_orders.comment_for_tl if assigned_orders else None
            comment_forteam_member = assigned_order.teammember_comment if assigned_order else None
            incentive = assigned_orders.incentive if assigned_orders else None
            remark = assigned_orders.remarks if assigned_orders else None
            assigned_expert_deadline = assigned_order.assigned_expert_deadline if assigned_order else None
            operation_member_comment = assigned_order.operation_member_comment if assigned_order else None
            deadline_for_operation = assigned_order.deadline_for_operation if assigned_order else None

                   
            order_data = {
                'id': order.orders_id,
                'subject': order.task_subject,
                'operation_status': order.operation_status,
                'lead_status': order.team_lead_status,
                'expertId': expert_id,
                'expert_id': assigned_expert,
                'expert_type': expert_roles, 
                'client_id': client_name,
                'order_status': order.status,
                'order_start_date': order.start_date,
                'order_end_date': order_deadline,
                'description': order.description,
                'comments': comments,
                'word_count': order.word_count,
                'expert_price': order.expert_price,
                'budget': order.order_budget,
                'currency': order.currency,
                'expert_currency': order.expert_currency,
                'expert_end_date': order.expert_deadline,
                'assigned_expert': assigned_expert_name,
                'assigned_expert_id': assigned_expert_id,
                'assigned_expert_deadline': assigned_expert_deadline,
                'order_create_deadline': order_create_deadline,  
                'qc_expert': qc_assigned_expert,   
                "qc_expert_id": qc_expert_id,
                "comment_for_opt": comment_for_opt,
                "comment_for_tl": comment_for_tl,
                "incentive": incentive,
                "is_admin_assigned_by": is_admin_assigned_by,
                "remark": remark, 
                "comment_forteam_member": comment_forteam_member,
                "operation_member_comment": operation_member_comment,
                "deadline_for_operation": deadline_for_operation,
                "is_admin_assigned_by_operation": is_admin_assigned_by_operation


                       
            } 
            if expert_deadlines:
                deadline_objects = []
                for deadline in expert_deadlines:
                    deadline_data = {
                        'id': deadline.id,
                        'expert_deadline': deadline.assigned_expert_deadline,
                        'expert_word_count': deadline.no_of_words
                    }
                    deadline_objects.append(deadline_data)
                order_data['deadlines_with_word_count'] = deadline_objects
            data.append(order_data)
            
    else:     

        data.append({'Error': 'No orders found', "Status": f"Order in {search_status} tab . "})

    print(data)# Construct pagination info
    from datetime import datetime, date

    deadline_data = []

    for order in data:
        order_end_date = None
        assigned_expert_deadline = None
        expert_type = None

        # Attempt to extract deadlines and expert type
        try:
            order_end_date = order.get('order_end_date', None)
            assigned_expert_deadline = order.get('assigned_expert_deadline', None)
            expert_type = order.get('expert_type', None)
        except Exception as e:
            print(f"Error extracting data from order: {order}, error: {e}")

        # Normalize order_end_date
        if order_end_date is None or order_end_date == datetime(9999, 12, 31):
            order_end_date = None
        elif isinstance(order_end_date, datetime):
            pass
        elif isinstance(order_end_date, date):
            order_end_date = datetime.combine(order_end_date, datetime.min.time())
        elif isinstance(order_end_date, str):
            try:
                order_end_date = datetime.strptime(order_end_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print(f"Could not parse order_end_date string: {order_end_date}")
                order_end_date = None
        else:
            raise ValueError(f"Unexpected type for order_end_date: {type(order_end_date)}")

        # Normalize assigned_expert_deadline
        if assigned_expert_deadline is None or assigned_expert_deadline == datetime(9999, 12, 31):
            assigned_expert_deadline = None
        elif isinstance(assigned_expert_deadline, datetime):
            pass
        elif isinstance(assigned_expert_deadline, date):
            assigned_expert_deadline = datetime.combine(assigned_expert_deadline, datetime.min.time())
        elif isinstance(assigned_expert_deadline, str):
            try:
                assigned_expert_deadline = datetime.strptime(assigned_expert_deadline, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print(f"Could not parse assigned_expert_deadline string: {assigned_expert_deadline}")
                assigned_expert_deadline = None
        else:
            raise ValueError(f"Unexpected type for assigned_expert_deadline: {type(assigned_expert_deadline)}")

        # Add to the list for sorting
        deadline_data.append((order_end_date, assigned_expert_deadline, expert_type, order))

    # Helper function to handle None values during sorting
    def sort_key(entry):
        order_end_date, assigned_expert_deadline, expert_type, _ = entry
        # Use assigned_expert_deadline for experts; otherwise, use order_end_date
        date_to_compare = assigned_expert_deadline if expert_type == 'expert' else order_end_date
        # Return a tuple where None is treated as a large future date
        return (date_to_compare if date_to_compare is not None else datetime.max,)

    # Sort based on the logic provided
    deadline_data.sort(key=sort_key)

    # Prepare the final sorted data
    sorted_data = [entry[3] for entry in deadline_data]
        # Print the sorted data
    # page_size = per_page   # Example page size
    # page_number = page  # Example page number (1-based index)

    # start_index = (page_number - 1) * page_size
    # end_index = start_index + page_size
    # paginated_data = sorted_data[start_index:end_index]

    for order in sorted_data:
                print(order)

    # Update the pagination count
    pagination_info = {
        'page': page,
        'per_page': per_page,
        'total_orders': assigned_new_orders_count,
        'total_pages': (assigned_new_orders_count + per_page - 1) // per_page,
        'previous_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < (assigned_new_orders_count + per_page - 1) // per_page else None
    }


    # Create response with pagination info
    response = jsonify({
        'pagination': pagination_info,
        'orders': sorted_data    
    })
    
    # response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response

# ------------------- Delete OTM Mamber data  from data table Module Route start -------------------__


@app.route('/deleteotm/<userId>', methods=['DELETE'])
@jwt_required()
def deleteUser(userId):
    user = Users.query.get_or_404(userId)
    db.session.delete(user)
    db.session.commit()

    response = flask.Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.set_data('Deleted!')
    return response


# ------------------- Delete OTM Mamber data  from data table Module Route End -------------------__

# ------------------- Delete Tutors(expert) data  from data table Module Route start -------------------__


# @app.route('/deleteexpert/<userId>', methods=['DELETE'])
# @jwt_required()
# def deleteexpertUser(userId):
#     print(userId)
#     expert = Expert.query.get_or_404(userId)
#     db.session.delete(expert)
#     db.session.commit()

#     response = flask.Response()
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.set_data('Deleted!')
#     return response


# ------------------- Delete Tutors(expert) data  from data table Module Route End -------------------__

# ------------------- Delete client data  from data table Module Route start -------------------__


@app.route('/deleteclient/<userId>', methods=['DELETE', "OPTIONS"])
@jwt_required()
def deleteclientUser(userId):
    client = Client.query.get_or_404(userId)
    db.session.delete(client)
    db.session.commit()

    response = flask.Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.set_data('Deleted!')
    return response

# -------------------Fatch OTM mamber Id for update  data in data table Module Route start -------------------__


@app.route('/getotmuser/<userId>', methods=['GET'])
@jwt_required()
def getotmuserUser(userId):
    user = Users.query.get_or_404(userId)
    data = []
    user_data = {
        'id': user.users_id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        'contact': user.contact,
        'joiningDate': user.joiningDate.strftime('%Y-%m-%d'),
        'Level': user.Level,
    }
    data.append(user_data)
    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response


# -------------------Fatch OTM mamber Id for update  data in data table Module Route End -------------------__

# -------------------Update OTM mamber  data in data table Module Route start -------------------__


@app.route('/updateotm/<userId>', methods=['POST'])
@jwt_required()
def updateotm(userId):
    user = Users.query.get_or_404(userId)

    user.firstname = flask.request.form['firstname']
    user.lastname = flask.request.form['lastname']
    user.password = flask.request.form['password']
    user.email = flask.request.form['email']
    user.contact = flask.request.form['contact']
    user.joiningDate = datetime.datetime.strptime(flask.request.form['joiningDate'], "%Y-%m-%d")
    user.Level = flask.request.form['Level']
    user.type = flask.request.form['type']

    db.session.commit()

    response = flask.Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    jsondata = json.dumps(user, default=datetime_handler)

    response.set_data(json.dumps(jsondata))

    return response


@app.route('/getOrdersByClientId/<clientId>', methods=['GET'])
@jwt_required()
def getOrdersByClientId(clientId):
    orders = Orders.query.filter_by(client_id=clientId).all()

    data = []
    for order in orders:
        order_data = {
            'order_id': order.orders_id,
            'task': order.task_subject,
            'order_budget': order.order_budget,
            'client_id': order.client_id,
            # 'amount_paid': budget.amount_paid,
            'currency': order.currency
        }
        data.append(order_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response


# -------------------Fatch client Id for view budget  data in data table Module Route End -------------------__
@app.route('/getStudentOrderHistory/<clientId>', methods=['GET'])
@jwt_required()
def getStudentOrderHistory(clientId):
    orders = Orders.query.filter_by(client_id=clientId).all()

    data = []
    for order in orders:
        invoice_alias = aliased(InvoiceOrders)

        # Check if the order_id is not in the Invoice table
        order_not_in_invoice = (
            db.session.query(exists().where(
                invoice_alias.orders_id == order.orders_id
            )).scalar() is False
        )
        print("order not in invoice",order_not_in_invoice)
        # Create a dictionary with the required data from the budget object
        if order_not_in_invoice:
            budget_data = {
                'id': order.orders_id,
                'task': order.task_subject,
                'order_budget': order.order_budget,
                'client_id': order.client_id,
                'currency': order.currency
            }
            data.append(budget_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/getVendorOrderHistory/<clientId>', methods=['POST'])
@jwt_required()
def getVendorOrderHistory(clientId):
    get_start_date = flask.request.form.get('start_date')
    get_end_date = flask.request.form.get('end_date')
    print(get_start_date)
    # Convert the start_date and end_date to datetime objects (you may need to adjust the format)
    start_date = datetime.datetime.strptime(get_start_date, '%m/%d/%Y').date()
    end_date = datetime.datetime.strptime(get_end_date, '%m/%d/%Y').date()
    print("cov start date", start_date)
    # Query orders within the specified date range for the given client
    orders = Orders.query.filter(
        Orders.client_id == clientId,
        Orders.task_date >= start_date,
        Orders.task_date <= end_date
    ).all()

    data = []
    for order in orders:
        # Create a dictionary with the required data from the budget object
       
        budget_data = {
            'id': order.orders_id,
            'task': order.task_subject,
            'order_budget': order.order_budget,
            'client_id': order.client_id,
            'currency': order.currency
        }
        data.append(budget_data)
    if data:
        return jsonify({'data': data}), 200
    else:
        return jsonify({'message': 'No orders Found'}), 404


# @app.route('/updateOrderAmount', methods=['POST'])
# @jwt_required()
# def updateOrderAmount():
#     try:
#         paid_amount = flask.request.form['paid_amount']
#         orderId = flask.request.form['order_id']
#         print(paid_amount)
#         print(orderId)
#         order_budget = Budget.query.filter_by(order_id=orderId).first()

#         if order_budget:
#             order_budget.amount_paid = paid_amount
#             print(order_budget.amount_paid)
#             db.session.add(order_budget)
#             db.session.commit()
#             return jsonify({'message': 'Amount Updated Successfully'}), 200
#         else:
#             return jsonify({'message': 'Order not found'}), 404
#     except Exception as e:
#         # Handle any exceptions that might occur during the process
#         print(f'Error: {str(e)}')
#         db.session.rollback()  # Rollback the transaction in case of an error
#         return jsonify({'message': 'An error occurred'}), 500


# -------------------Fatch client Id for update  data in data table Module Route start -------------------__


@app.route('/getClientFromClientId/<clientId>', methods=['GET'])
@jwt_required()
def getClientFromOrderId(clientId):
    client = Client.query.filter_by(client_id=clientId).first()
    data = []
    if client:
        client_data = {
            'id': client.client_id,
            'name': client.client_name,
            'contact': client.client_contact,
            'email': client.client_email,
            'status': client.client_status,
            'university': client.university,
            'business_name': client.business_name,

        }
    else:
        client_data = {}

    data.append(client_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/getclient/<userId>', methods=['GET'])
@jwt_required()
def getclientID(userId):
    client = Client.query.get(userId)
    data = []
    if client:
        client_data = {
            'id': client.client_id,
            'name': client.client_name,
            'contact': client.client_contact,
            'email': client.client_email,
            'status': client.client_status,
            'university': client.university,
            'business_name': client.business_name,
            'login': client.student_login,
            'password': client.student_password
        }
    else:
        client_data = {}

    data.append(client_data)

    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'

    return response


# -------------------Fatch client Id for update  data in data table Module Route End -------------------__

# -------------------Update client  data in data table Module Route start -------------------__


@app.route('/updateclient/<userId>', methods=['POST'])
@jwt_required()
def updateclient(userId):
    client = Client.query.get(userId)

    if client:
        client.client_name = flask.request.form['Client_name']
        client.client_contact = flask.request.form['Client_contact']
        client.client_email = flask.request.form['Client_email']
        client.client_status = flask.request.form['Client_status']
        client.university = flask.request.form['University']
        client.business_name = flask.request.form['Business_name']
        client.student_login = flask.request.form['Student_login']
        client.student_password = flask.request.form['Student_password']

        db.session.commit()
        response_data = {
            'status': 'success',
            'message': 'Client updated successfully'
        }
    else:
        response_data = {
            'status': 'error',
            'message': 'Client not found'
        }

    response = flask.Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    response.set_data(json.dumps(response_data))

    return response


# -------------------Update client data in data table Module Route End -------------------__

# -------------------Fatch budget Id for update  data in data table Module Route start -------------------__


# @app.route('/getbudget/<userId>', methods=['GET'])
# @jwt_required()
# def getbudget(userId):
#     budget = Budget.query.get(userId)
#     if budget:
#         budget_data = {
#             'id': budget.budget_id,
#             'client_id': budget.client_id,
#             'package_price': budget.package_price,
#             'amount_paid': budget.amount_paid,
#             'pending_amount': budget.pending_amount,
#             'mode_of_payment': budget.mode_of_payment,
#             'status': budget.status,
#         }

#         json_data = json.dumps(budget_data)

#         respp = flask.Response()
#         respp.headers['Access-Control-Allow-Origin'] = '*'
#         respp.headers['Content-Type'] = 'application/json'
#         respp.set_data(json_data)

#         return respp
#     else:
#         # Handle the case when the budget is not found
#         respp = flask.Response()
#         respp.headers['Access-Control-Allow-Origin'] = '*'
#         respp.set_data('Budget not found')

#         return respp


# -------------------Fatch budget Id for update  data in data table Module Route End -------------------__

# -------------------Update budget data in data table Module Route start -------------------__


# @app.route('/updatebudget/<userId>', methods=['POST'])
# @jwt_required()
# def updatebudget(userId):
#     Client_name = flask.request.form['Client_name']
#     Package_price = flask.request.form['Package_price']
#     Amount_Paid = flask.request.form['Amount_Paid']
#     Pending_amount = flask.request.form['Pending_amount']
#     Mode_of_payment = flask.request.form['Mode_of_payment']
#     Status = flask.request.form['Status']
#     print(Client_name)
#     # Query the client_id based on the Client_name
#     client = Client.query.filter_by(client_name=Client_name).first()
#     if not client:
#         return 'Client not found'

#     # Update the budget
#     budget = Budget.query.filter_by(budget_id=userId).first()
#     if budget:
#         budget.client_id = client.client_id
#         budget.package_price = Package_price
#         budget.amount_Paid = Amount_Paid
#         budget.pending_amount = Pending_amount
#         budget.mode_of_payment = Mode_of_payment
#         budget.status = Status
#         db.session.commit()
#         return 'Budget updated successfully'
#     else:
#         return 'Budget not found'


# -------------------Update budget data in data table Module Route End -------------------__

# -------------------Fatch task Id for update  data in data table Module Route start -------------------__

@app.route('/updateStatusWithId/<orderId>', methods=['POST'])
@jwt_required()
def updateStatusWithId(orderId):
    print("insdi this")
    current_user = get_jwt_identity()
    print("currenddddddddd", current_user)
    user = Users.query.filter_by(email=current_user).first()
    if user:
         current_expert_id = user.users_id
         operation_user_role = user.type
    else:
        # Handle the case where the user is not found
        raise Exception("User not found")
    # try:
    updateCondition = flask.request.form['updateCondition']
    print("====updateCondition====", updateCondition)  
    ist = timezone(timedelta(hours=5, minutes=30))
    status = None
    new_status = None  # Initialize new_status here
    print(updateCondition)   
    if updateCondition == "expert":       
        if 'status' in flask.request.form:
            data = flask.request.form['data'] #deadline, word count
            data_dict = json.loads(data)  # Parse the JSON string into a Python object

            if isinstance(data_dict, list):
                data_array = data_dict
            elif isinstance(data_dict, dict):
                data_array = data_dict.get('task', [])
            else:
                data_array = []
                
            status = flask.request.form['status']
            operation_member_name = flask.request.form['operation_member_name']  
            operation_member_comment = flask.request.form['operation_member_comment']  
            deadline_for_operation = flask.request.form['deadline_for_operation']  

                
            expert_id = flask.request.form['expert_id']
            comments = flask.request.form['comments']               
            user_roles = flask.request.form['roles']
        else:
            data = flask.request.form['data'] #deadline, word count
            data_dict = json.loads(data)
            if isinstance(data_dict, list):
                data_array = data_dict
            elif isinstance(data_dict, dict):
                data_array = data_dict.get('task', [])
            else:
                data_array = []
            expert_id = flask.request.form['expert_id']
            comments = flask.request.form['comments']
            user_roles = flask.request.form['roles']
    elif updateCondition == "qc_expert":
        qc_expert_id=flask.request.form['qc_expert_id']
        user_roles = flask.request.form['roles']
    elif updateCondition == "order_deadline":
        new_order_deadline = flask.request.form['order_deadline']
        
    elif updateCondition == "expert_deadline":
        new_expert_deadline = flask.request.form['expert_deadline']
        print("new_expert_deadline", new_expert_deadline)
    
    elif updateCondition == "operationMember":
        operationMember = flask.request.form['operationMember']
    
    elif updateCondition == "assigned_expert_deadline":
        new_assigned_expert_deadline = flask.request.form['assigned_expert_deadline']
    
    elif updateCondition == "task_subject":
        task_subject = flask.request.form['task_subject'] 
    else:
        print("else status ", flask.request.form['status'])
        new_status = flask.request.form['status']
    
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")
    task_date = formatted_date


    order = Orders.query.filter_by(orders_id=orderId).first()
    assign_expert = AssignedOrders.query.filter_by(orders_id=order.orders_id).order_by(AssignedOrders.id).first()
    expert_deadline_order = AssignedOrders.query.filter_by(orders_id=order.orders_id).order_by(AssignedOrders.id).first()
    #expert_update_order = (db.session.query(AssignedOrders)
                                # .join(Employees, AssignedOrders.expert_id == Employees.id)
                                # .filter(AssignedOrders.orders_id == order.orders_id)
                                # .filter(AssignedOrders.deadline.isnot(None))
                                # .order_by(AssignedOrders.id.desc())
                                # .first())
  
    expert_update_order = (db.session.query(AssignedOrders)
                            .outerjoin(Employees, AssignedOrders.expert_id == Employees.id)
                            .filter(AssignedOrders.orders_id == order.orders_id)
                            .filter(AssignedOrders.deadline.isnot(None))
                            .order_by(AssignedOrders.id)
                            .first())                        
    expertid = assign_expert.expert_id if assign_expert else None 
    invoice_dates = []
    no_of_words = []
   
                    
    if order is not None:      
        if updateCondition == "expert":
            expert_role = Employees.query.filter_by(employee_id=flask.request.form['expert_id']).first()
            if expert_role:
                role = expert_role.roles
            else:
                role = None   
            if status == 'assigned' and user_roles == 'admin':
                if isinstance(data_array, list):
                        for item in data_array:
                            if isinstance(item, dict):
                                # Collect invoice dates and no_of_words
                                invoice_dates.append(format_invoice_date(item.get('invoiceDate')))
                                no_of_words.append(item.get('wordCount', 0))  # Default to 0 if not present
                        # Extract values with safe checks
                        invoice_date_1 = invoice_dates[0] if len(invoice_dates) > 0 else None
                        invoice_date_2 = invoice_dates[1] if len(invoice_dates) > 1 else None
                        invoice_date_3 = invoice_dates[2] if len(invoice_dates) > 2 else None
                        invoice_date_4 = invoice_dates[3] if len(invoice_dates) > 3 else None
                        invoice_date_5 = invoice_dates[4] if len(invoice_dates) > 4 else None
                        invoice_date_6 = invoice_dates[5] if len(invoice_dates) > 5 else None

                        no_of_words_1 = no_of_words[0] if len(no_of_words) > 0 else None
                        no_of_words_2 = no_of_words[1] if len(no_of_words) > 1 else None
                        no_of_words_3 = no_of_words[2] if len(no_of_words) > 2 else None
                        no_of_words_4 = no_of_words[3] if len(no_of_words) > 3 else None
                        no_of_words_5 = no_of_words[4] if len(no_of_words) > 4 else None  
                        no_of_words_6 = no_of_words[5] if len(no_of_words) > 5 else None  
                       
                if role == "lead":
                        if expertid:
                            assign_expert.team_deadline1 = invoice_dates[0] if len(invoice_dates) > 0 else None
                        new_assigned_order = AssignedOrders(
                                orders_id=orderId,
                                expert_id=expert_id,
                                assigned_date=task_date,
                                deadline=invoice_date_1,
                                no_of_words=no_of_words_1,
                                no_of_word1=no_of_words_2,
                                no_of_word2=no_of_words_3,
                                no_of_word3=no_of_words_4,
                                no_of_word4=no_of_words_5,
                                comments=comments,
                                is_admin_assigned_by=False,
                                team_deadline1=invoice_date_2,
                                team_deadline2=invoice_date_3,
                                team_deadline3=invoice_date_4,
                                team_deadline4=invoice_date_5,
                                team_deadline5=invoice_date_6
                
                            )
                
                elif role=="operationMember":
                    print("===testing check====")
                    new_assigned_order = AssignedOrders(
                        orders_id=orderId,
                        expert_id=operation_member_name,
                        assigned_date=task_date,
                        operation_member_comment=operation_member_comment,
                        is_admin_assigned_by_operation=False,
                        deadline_for_operation=deadline_for_operation,
                        
                    )
                else:
                        expert_no_of_words_1 = no_of_words[0] if len(no_of_words) > 0 else None
                        expert_no_of_words_2 = no_of_words[1] if len(no_of_words) > 1 else None
                        expert_no_of_words_3 = no_of_words[2] if len(no_of_words) > 2 else None
                        expert_no_of_words_4 = no_of_words[3] if len(no_of_words) > 3 else None
                        expert_no_of_words_5 = no_of_words[4] if len(no_of_words) > 4 else None  
                        expert_no_of_words_6 = no_of_words[5] if len(no_of_words) > 5 else None  

                        if expertid:
                            assign_expert.assigned_expert_deadline = invoice_date_1

                        new_assigned_order = AssignedOrders(
                        orders_id = orderId,
                        expert_id = expert_id,
                        assigned_date = task_date,
                        expert_no_of_words=expert_no_of_words_1, 
                        expert_no_of_word1=expert_no_of_words_2,
                        expert_no_of_word2=expert_no_of_words_3,
                        expert_no_of_word3=expert_no_of_words_4,
                        expert_no_of_word4=expert_no_of_words_5,
                        expert_no_of_word5=expert_no_of_words_6,

                        teammember_comment=comments,
                        assigned_expert_deadline=invoice_date_1,
                        assigned_expert_deadline1=invoice_date_2,
                        assigned_expert_deadline2=invoice_date_3,
                        assigned_expert_deadline3=invoice_date_4,
                        assigned_expert_deadline4=invoice_date_5,
                        assigned_expert_deadline5=invoice_date_6   
                    )
                db.session.add(new_assigned_order)
            
                if role == "operationMember":
                    order.status = status
                    order.operation_status = status   
                else:
                    order.status = status
                    order.team_lead_status = status      
                
                db.session.commit()
                                        
            else:
                operation_member_name = flask.request.form['operation_member_name']  
                operation_member_comment = flask.request.form['operation_member_comment']  
                deadline_for_operation = flask.request.form['deadline_for_operation']  
                if user_roles == 'admin':
                    is_order_assigned =  AssignedOrders.query.filter_by(orders_id=orderId).first()
                    if is_order_assigned is not None:        
                        update_order = AssignedOrders.query.filter(AssignedOrders.orders_id == orderId).all()
                        print("update_order",update_order )
                        # for order_instance in update_order:
                        #     db.session.delete(order_instance)
                        #     print("deleting", order_instance)
                        # db.session.commit()
                        
                        # for items in data_array:
                        #     print("items", items)
                        #     invoice_date = items.get('invoiceDate')
                        #     end_date_conv = invoice_date.split('T')[0]
                        if isinstance(data_array, list):
                            for item in data_array:
                                if isinstance(item, dict): 
                                    invoice_dates.append(format_invoice_date(item.get('invoiceDate')))
                                    no_of_words.append(item.get('wordCount', 0))  # Default to 0 if not present
                            invoice_date_1 = invoice_dates[0] if len(invoice_dates) > 0 else None
                            invoice_date_2 = invoice_dates[1] if len(invoice_dates) > 1 else None
                            invoice_date_3 = invoice_dates[2] if len(invoice_dates) > 2 else None
                            invoice_date_4 = invoice_dates[3] if len(invoice_dates) > 3 else None
                            invoice_date_5 = invoice_dates[4] if len(invoice_dates) > 4 else None
                            invoice_date_6 = invoice_dates[5] if len(invoice_dates) > 5 else None


                            no_of_words_1 = no_of_words[0] if len(no_of_words) > 0 else None
                            no_of_words_2 = no_of_words[1] if len(no_of_words) > 1 else None
                            no_of_words_3 = no_of_words[2] if len(no_of_words) > 2 else None
                            no_of_words_4 = no_of_words[3] if len(no_of_words) > 3 else None
                            no_of_words_5 = no_of_words[4] if len(no_of_words) > 4 else None  
                            
                            expert_no_of_words_1 = no_of_words[0] if len(no_of_words) > 0 else None
                            expert_no_of_words_2 = no_of_words[1] if len(no_of_words) > 1 else None
                            expert_no_of_words_3 = no_of_words[2] if len(no_of_words) > 2 else None
                            expert_no_of_words_4 = no_of_words[3] if len(no_of_words) > 3 else None
                            expert_no_of_words_5 = no_of_words[4] if len(no_of_words) > 4 else None  
                            expert_no_of_words_6 = no_of_words[5] if len(no_of_words) > 5 else None 
                                    
                            if role == "expert":
                                new_assigned_order = AssignedOrders(
                                    orders_id=orderId,
                                    expert_id=expert_id,
                                    assigned_date=task_date,
                                    expert_no_of_words=expert_no_of_words_1,
                                    expert_no_of_word1=expert_no_of_words_2,
                                    expert_no_of_word2=expert_no_of_words_3,
                                    expert_no_of_word3=expert_no_of_words_4,
                                    expert_no_of_word4=expert_no_of_words_5,
                                    expert_no_of_word5=expert_no_of_words_6,

                                    teammember_comment=comments,
                                    is_admin_assigned_by=False,
                                    assigned_expert_deadline=invoice_date_1,
                                    assigned_expert_deadline1=invoice_date_2,
                                    assigned_expert_deadline2=invoice_date_3,
                                    assigned_expert_deadline3=invoice_date_4,
                                    assigned_expert_deadline4=invoice_date_5,
                                    assigned_expert_deadline5=invoice_date_6   
                                    )   
                            elif role=="operationMember":
                                    new_assigned_order = AssignedOrders(
                                        orders_id=orderId,
                                        expert_id=operation_member_name,
                                        assigned_date=task_date,
                                        operation_member_comment=operation_member_comment,
                                        is_admin_assigned_by_operation=False,
                                        deadline_for_operation=deadline_for_operation,
                                        
                                    )                               
                            else:
                                print("role2======", role)
                                new_assigned_order = AssignedOrders(
                                        orders_id=orderId,
                                        expert_id=expert_id,
                                        assigned_date=task_date,
                                        deadline=invoice_date_1,
                                        no_of_words=no_of_words_1,
                                        no_of_word1=no_of_words_2,
                                        no_of_word2=no_of_words_3,
                                        no_of_word3=no_of_words_4,
                                        no_of_word4=no_of_words_5,
                                        comments=comments,
                                        is_admin_assigned_by=False,
                                        team_deadline1=invoice_date_2,
                                        team_deadline2=invoice_date_3,
                                        team_deadline3=invoice_date_4,
                                        team_deadline4=invoice_date_5,
                                        team_deadline5=invoice_date_6
                                    )
                            db.session.add(new_assigned_order)
                        db.session.commit()
                elif user_roles == 'lead':
                    print("====leadddd")
                    is_order_assigned =  AssignedOrders.query.filter_by(orders_id=orderId).first()
                    if is_order_assigned is not None:        
                        update_order = AssignedOrders.query.filter(AssignedOrders.orders_id == orderId).all()
                        if isinstance(data_array, list):
                            for item in data_array:
                                if isinstance(item, dict):
                                    # Collect invoice dates and no_of_words
                                    invoice_dates.append(format_invoice_date(item.get('invoiceDate')))
                                    no_of_words.append(item.get('wordCount', 0))  # Default to 0 if not present
                            # Extract values with safe checks
                            invoice_date_1 = invoice_dates[0] if len(invoice_dates) > 0 else None
                            invoice_date_2 = invoice_dates[1] if len(invoice_dates) > 1 else None
                            invoice_date_3 = invoice_dates[2] if len(invoice_dates) > 2 else None
                            invoice_date_4 = invoice_dates[3] if len(invoice_dates) > 3 else None
                            invoice_date_5 = invoice_dates[4] if len(invoice_dates) > 4 else None
                            invoice_date_6 = invoice_dates[5] if len(invoice_dates) > 5 else None

                            no_of_words_1 = no_of_words[0] if len(no_of_words) > 0 else None
                            no_of_words_2 = no_of_words[1] if len(no_of_words) > 1 else None
                            no_of_words_3 = no_of_words[2] if len(no_of_words) > 2 else None
                            no_of_words_4 = no_of_words[3] if len(no_of_words) > 3 else None
                            no_of_words_5 = no_of_words[4] if len(no_of_words) > 4 else None  
                            no_of_words_6 = no_of_words[5] if len(no_of_words) > 5 else None
                        # for items in data_array:
                        #     print("items", items)
                        #     invoice_date = items.get('invoiceDate')
                        #     end_date_conv = invoice_date.split('T')[0]
                        #     no_of_words =  items.get('wordCount', 0)
                            # for order_to_update in update_order:
                            #     print("ordet", order_to_update)
                            #     order_to_update.no_of_words = no_of_words
                            #     order_to_update.assigned_expert = expert_id
                            #     order_to_update.assigned_expert_deadline = end_date_conv
                            #     order_to_update.tl_deadline = end_date_conv
                                
                            pdeadline = AssignedOrders.query.filter_by(orders_id=order.orders_id).order_by(AssignedOrders.id).first()
                            print("========ffff=====", pdeadline.qc_expert, pdeadline.id ,pdeadline.is_admin_assigned_by)
                            is_admin_assigned_update = AssignedOrders.query.filter(
                                and_(
                                    AssignedOrders.orders_id == order.orders_id,
                                    AssignedOrders.is_admin_assigned_by == 0,
                                    AssignedOrders.is_admin_assigned_by.isnot(None)
                                )
                            ).order_by(AssignedOrders.id.desc()).first()
                            if is_admin_assigned_update and is_admin_assigned_update.is_admin_assigned_by == 0:
                                    # Update the field to None
                                    is_admin_assigned_update.is_admin_assigned_by = None
                                    db.session.commit()
                            if pdeadline.expert_id and pdeadline.orders_id:
                                  pdeadline.assigned_expert= expert_id
                                  pdeadline.assigned_expert_deadline = invoice_date_1
                                  pdeadline.assigned_expert_deadline1 = invoice_date_2
                                  pdeadline.assigned_expert_deadline2 = invoice_date_3
                                  pdeadline.assigned_expert_deadline3 = invoice_date_4
                                  pdeadline.assigned_expert_deadline4 = invoice_date_5
                                  pdeadline.assigned_expert_deadline5 = invoice_date_6
                                  pdeadline.expert_no_of_words = no_of_words_1
                                  pdeadline.expert_no_of_word1 = no_of_words_2
                                  pdeadline.expert_no_of_word2 = no_of_words_3
                                  pdeadline.expert_no_of_word3 = no_of_words_4
                                  pdeadline.expert_no_of_word4 = no_of_words_5
                                  pdeadline.expert_no_of_word5 = no_of_words_6
                            else:     
                                new_assigned_order = AssignedOrders(
                                    orders_id=orderId,
                                    expert_id=pdeadline.expert_id,
                                    assigned_date=task_date,
                                    #deadline=pdeadline.deadline ,
                                    no_of_words=no_of_words, 
                                    assigned_expert=expert_id,
                                    assigned_expert_deadline=end_date_conv,
                                    teammember_comment=comments,
                                    comments=pdeadline.comments,
                                    #qc_expert=pdeadline.qc_expert,
                                    is_admin_assigned_by=pdeadline.is_admin_assigned_by


                                ) 
                                db.session.add(new_assigned_order)
                        db.session.commit()
                    
                elif user_roles == 'operationMember':
                    print("====OPERATION CHECK==")
                    is_order_assigned =  AssignedOrders.query.filter_by(orders_id=orderId).first()
                    if is_order_assigned is not None:        
                        update_order = AssignedOrders.query.filter(AssignedOrders.orders_id == orderId).all()
                        if isinstance(data_array, list):
                            for item in data_array:
                                if isinstance(item, dict):
                                    # Collect invoice dates and no_of_words
                                    invoice_dates.append(format_invoice_date(item.get('invoiceDate')))
                                    no_of_words.append(item.get('wordCount', 0))  # Default to 0 if not present
                            # Extract values with safe checks
                            invoice_date_1 = invoice_dates[0] if len(invoice_dates) > 0 else None
                            invoice_date_2 = invoice_dates[1] if len(invoice_dates) > 1 else None
                            invoice_date_3 = invoice_dates[2] if len(invoice_dates) > 2 else None
                            invoice_date_4 = invoice_dates[3] if len(invoice_dates) > 3 else None
                            invoice_date_5 = invoice_dates[4] if len(invoice_dates) > 4 else None
                            invoice_date_6 = invoice_dates[5] if len(invoice_dates) > 5 else None

                            no_of_words_1 = no_of_words[0] if len(no_of_words) > 0 else None
                            no_of_words_2 = no_of_words[1] if len(no_of_words) > 1 else None
                            no_of_words_3 = no_of_words[2] if len(no_of_words) > 2 else None
                            no_of_words_4 = no_of_words[3] if len(no_of_words) > 3 else None
                            no_of_words_5 = no_of_words[4] if len(no_of_words) > 4 else None  
                            no_of_words_6 = no_of_words[5] if len(no_of_words) > 5 else None
                        # for items in data_array:
                        #     print("items", items)
                        #     invoice_date = items.get('invoiceDate')
                        #     end_date_conv = invoice_date.split('T')[0]
                        #     no_of_words =  items.get('wordCount', 0)
                            # for order_to_update in update_order:
                            #     print("ordet", order_to_update)
                            #     order_to_update.no_of_words = no_of_words
                            #     order_to_update.assigned_expert = expert_id
                            #     order_to_update.assigned_expert_deadline = end_date_conv
                            #     order_to_update.tl_deadline = end_date_conv
                                
                            pdeadline = AssignedOrders.query.filter_by(orders_id=order.orders_id).order_by(AssignedOrders.id).first()
                            print("========ffff=====", pdeadline.qc_expert, pdeadline.id ,pdeadline.is_admin_assigned_by_operation)
                            is_admin_assigned_update = AssignedOrders.query.filter(
                                and_(
                                    AssignedOrders.orders_id == order.orders_id,
                                    AssignedOrders.is_admin_assigned_by_operation == 0,
                                    AssignedOrders.is_admin_assigned_by_operation.isnot(None)
                                )
                            ).order_by(AssignedOrders.id.desc()).first()
                            if is_admin_assigned_update and is_admin_assigned_update.is_admin_assigned_by_operation == 0:
                                    # Update the field to None
                                    is_admin_assigned_update.is_admin_assigned_by_operation = None
                                    db.session.commit()
                            if pdeadline.expert_id and pdeadline.orders_id:
                                  pdeadline.assigned_expert= expert_id
                                  pdeadline.assigned_expert_deadline = invoice_date_1
                                  pdeadline.assigned_expert_deadline1 = invoice_date_2
                                  pdeadline.assigned_expert_deadline2 = invoice_date_3
                                  pdeadline.assigned_expert_deadline3 = invoice_date_4
                                  pdeadline.assigned_expert_deadline4 = invoice_date_5
                                  pdeadline.assigned_expert_deadline5 = invoice_date_6
                                  pdeadline.expert_no_of_words = no_of_words_1
                                  pdeadline.expert_no_of_word1 = no_of_words_2
                                  pdeadline.expert_no_of_word2 = no_of_words_3
                                  pdeadline.expert_no_of_word3 = no_of_words_4
                                  pdeadline.expert_no_of_word4 = no_of_words_5
                                  pdeadline.expert_no_of_word5 = no_of_words_6
                            else:     
                                new_assigned_order = AssignedOrders(
                                    orders_id=orderId,
                                    expert_id=pdeadline.expert_id,
                                    assigned_date=task_date,
                                    #deadline=pdeadline.deadline ,
                                    no_of_words=no_of_words, 
                                    assigned_expert=expert_id,
                                    assigned_expert_deadline=end_date_conv,
                                    teammember_comment=comments,
                                    comments=pdeadline.comments,
                                    #qc_expert=pdeadline.qc_expert,
                                    is_admin_assigned_by_operation=pdeadline.is_admin_assigned_by_operation


                                ) 
                                db.session.add(new_assigned_order)
                                
                        db.session.commit()              
                  
        
        elif updateCondition == "qc_expert":
            qc_expert = flask.request.form['qc_expert_id']
            assign_expert.qc_expert = qc_expert
            db.session.commit()  
            
        elif updateCondition == "order_deadline":
            order.end_date = new_order_deadline
            db.session.commit()  
        
        elif updateCondition == "operationMember":
            assign_expert.deadline_for_operation = operationMember
            db.session.commit()      
            
        elif updateCondition == "expert_deadline":
            print("inside last")
            print("===", new_expert_deadline)
            print("expert_update_order", expert_update_order)
            
            expert_update_order.deadline = new_expert_deadline
            db.session.commit()      
            
        elif updateCondition == "assigned_expert_deadline":
            expert_deadline_order.assigned_expert_deadline = new_assigned_expert_deadline
            db.session.commit()  
        
        elif updateCondition == "task_subject":

            order.task_subject = task_subject
            db.session.commit()      
            
        else:
            print("else for status", order.status)
            if operation_user_role == "operationMember":
                order.operation_status = new_status
            elif operation_user_role == "lead":
                order.team_lead_status = new_status
            else:        
               order.status = new_status
            db.session.commit()   

        # Commit the changes to the database
            
        return jsonify({"message": "Order Updated successfully"}), 200
    else:
        return jsonify({"message": "Error occurred"}), 404
    # except Exception as e:
    #     print(e) 
    #     return jsonify({"message": "Order not found "}), 404   


@app.route('/removeAssignedOrder/<id>', methods=['POST'])
@jwt_required()
def removeAssignedOrder(id):
    try:
        expert_id = int(flask.request.form.get('expert_id'))   # Use get method to avoid KeyError
        
        # Fetch the assigned order by its ID
        order_to_remove = AssignedOrders.query.get(id)  # Use get method for primary key lookup
        if not order_to_remove:
            return jsonify({"message": "Assigned Order not found"}), 404
        
        # Get the order ID from the assigned order
        order_id = order_to_remove.orders_id
        # Fetch the order by orders_id using filter_by() for non-primary key
        status_update_in_orders = Orders.query.filter_by(orders_id=order_id).first()  # Use filter_by() for non-primary key
        
        if status_update_in_orders:
            
            # Handle the removal of expert assignment
            if order_to_remove.assigned_expert == expert_id:
                order_to_remove.assigned_expert = None
                order_to_remove.assigned_expert_deadline = None
            
            elif expert_id == order_to_remove.expert_id:
                db.session.delete(order_to_remove)

            # After removing, check if there are any remaining assigned orders for this order_id
            remaining_assigned_orders = AssignedOrders.query.filter_by(orders_id=order_id).all()
            
            # If no assigned orders remain, update the status of the order
            if not remaining_assigned_orders:
                status_update_in_orders.status = "new order"
            
            db.session.commit()

            return jsonify({"message": "Order Removed"}), 200
        else:
            return jsonify({"message": "Order not found for status update"}), 404
    except Exception as e:
        # Catch any unexpected errors and return them in the response
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# -------------------Fatch Task Id for update  data in data table Module Route End -------------------__

# -------------------Update task data in data table Module Route start -------------------__

@app.route('/updateOrderWithId/<orderId>', methods=['POST'])
@jwt_required()
def updateOrderWithId(orderId):
    ist = timezone(timedelta(hours=5, minutes=30))
    task_data = request.form
    print("===", task_data)

    # Fetch the order using the provided orderId
    order = Orders.query.filter_by(orders_id=orderId).first()
    if not order:
        return 'Order not found', 404

    # Check if the order exists in the assigned_orders table
    assigned_order = AssignedOrders.query.filter_by(orders_id=order.orders_id).first()
    if assigned_order:
        expert_name = Employees.query.filter_by(employee_id=assigned_order.expert_id).first()
        name = expert_name.firstname if expert_name else None
        if not expert_name:
            return 'Expert not found', 404
        
        # Check if expert is a team lead or a team member
        is_team_lead = expert_name.roles == 'lead'  # Adjust the condition based on your model
        # Update only the fields that are provided in the request
        if 'word_count' in task_data:
            assigned_order.no_of_words = task_data['word_count']
        
         
        if 'deadline' in task_data:
            end_date = task_data['deadline']
            end_date_conv = datetime.datetime.strptime(end_date, "%Y-%m-%d").astimezone(ist)
            if is_team_lead:
                assigned_order.deadline = end_date_conv  # Update the main order deadline
            else:
                assigned_order.assigned_expert_deadline = end_date_conv  # Update assigned order deadline

        if 'comment' in task_data:
            assigned_order.comment = task_data['comment']

        if 'subject' in task_data:
            order.task_subject = task_data['subject']

        if 'description' in task_data:
            order.description = task_data['description']
        
        # Commit the changes to the database
        db.session.commit()

        # Retrieve expert and client information

        
        client_data = Client.query.filter_by(client_id=order.client_id).first()
        client_name = client_data.client_name if client_data else ""

        print(assigned_order)
        order_data = {
            'id': order.orders_id,
            'subject': order.task_subject,
            'expert_id': name,
            'client_id': client_name,
            'order_status': order.status,
            'order_start_date': order.start_date,
            'order_end_date': order.end_date,
            'description': order.description,
            'word_count': assigned_order.no_of_words,
            'order_end_date': assigned_order.assigned_expert_deadline
        }
        response_data = [order_data]
        return jsonify(response_data), 200
    else:
        return 'Order not found', 404
    
@app.route('/fetchOrderWithOrderIdExpertId/<orderId>/<expert_id>', methods=['POST'])
@jwt_required()
def fetchOrderWithorderId(orderId, expert_id):
    expert_id = int(expert_id)
    
    # Fetch the order
    order = Orders.query.filter_by(orders_id=orderId).first()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Fetch the assigned orders for this order
    assigned_orders = AssignedOrders.query.filter_by(orders_id=order.orders_id).all()
    if not assigned_orders:
        return jsonify({'error': 'No assigned orders found for the specified criteria'}), 404
    
    # Fetch the expert details
    expert = Employees.query.filter_by(employee_id=expert_id).first()
    if not expert:
        return jsonify({'error': 'Expert not found'}), 404
    
    expert_type = expert.roles
    response_data = []
    
    def format_date(date):
        return date.strftime('%Y-%m-%d') if date else None
    
    for assigned_order in assigned_orders:
       
        expert_id_match = assigned_order.assigned_expert if assigned_order.assigned_expert and assigned_order.expert_id else assigned_order.expert_id
        lead_id_match = assigned_order.expert_id if assigned_order.expert_id else assigned_order.expert_id
        
        # Fetch the expert for the assigned order
        order_expert = Employees.query.filter(
            or_(Employees.employee_id == expert_id_match, Employees.employee_id == lead_id_match)
        ).first()

        # Debugging: Log the expert for the assigned order
        if order_expert:
            print(f"Found Expert: {order_expert.firstname}, Role: {order_expert.roles}")
        else:
            print("No expert found for this assignment.")
        
        expert_type = order_expert.roles if order_expert else None
        
        if expert_type == "expert" and expert_id_match == expert_id:
            order_data = {
                'order_id': order.orders_id,
                'expert_id': assigned_order.expert_id,
                'id': assigned_order.id,
                'expert_name': order_expert.firstname if order_expert else None,
                'expert_type': expert_type,
                'current_expert_id': expert_id,
                'current_expert_type': expert_type,
            }
            
            
            order_data.update({
                'assigned_expert_deadline': [
                    format_date(assigned_order.assigned_expert_deadline) if assigned_order.assigned_expert_deadline else None
                ] + [
                    format_date(getattr(assigned_order, f'assigned_expert_deadline{i}', None)) if getattr(assigned_order, f'assigned_expert_deadline{i}', None) else None for i in range(1, 7)
                ],
                'expert_no_of_words': [
                    assigned_order.expert_no_of_words if assigned_order.expert_no_of_words is not None else 0
                ] + [
                    getattr(assigned_order, f'expert_no_of_word{i}', 0) for i in range(1, 7)
                ]
            })

            response_data.append(order_data)  # Add the order data to the response list

        elif expert_type == "lead" and lead_id_match == expert_id:
            order_expert = Employees.query.filter_by(employee_id=assigned_order.expert_id).first()
            order_data = {
                'order_id': order.orders_id,
                'expert_id': assigned_order.expert_id,
                'id': assigned_order.id,
                'expert_name': order_expert.firstname if order_expert else None,
                'expert_type': order_expert.roles if order_expert else None,
                'current_expert_id': expert_id,
                'current_expert_type': expert_type,
            }
            
            order_data.update({
                'team_deadline': [
                    format_date(assigned_order.deadline) if assigned_order.deadline else None
                ] + [
                    format_date(getattr(assigned_order, f'team_deadline{i}', None)) if getattr(assigned_order, f'team_deadline{i}', None) else None for i in range(1, 7)
                ],
                'no_of_words': [
                    assigned_order.no_of_words if assigned_order.no_of_words is not None else 0
                ] + [
                    getattr(assigned_order, f'no_of_word{i}', 0) for i in range(1, 7)
                ]
            })

            
            response_data.append(order_data)
            
        elif expert_type == "operationMember" and lead_id_match== expert_id:
                    order_expert = Employees.query.filter_by(employee_id=assigned_order.expert_id).first()
                    order_data = {
                        'order_id': order.orders_id,
                        'expert_id': assigned_order.expert_id,
                        'id': assigned_order.id,
                        'expert_name': order_expert.firstname if order_expert else None,
                        'expert_type': order_expert.roles if order_expert else None,
                        'current_expert_id': expert_id,
                        'current_expert_type': expert_type,
                    }
                    
                    order_data.update({
                        'opeartion_member_deadline': [format_date(assigned_order.deadline_for_operation)] +
                                        [format_date(getattr(assigned_order, f'deadline_for_operation{i}', None)) for i in range(1, 7)],
                                        
                        'no_of_words': []
                    })
                    
                    response_data.append(order_data)

           #response_data.append(order_data)  # Add the lead order data to the response list

    # Final check if no data was added to the response
    if not response_data:
        return jsonify({'error': 'No data available for the specified criteria'}), 404
    
    return jsonify(response_data), 200



@app.route('/updateOrderDeadlines/<orderId>', methods=['PUT'])
@jwt_required()
def updateOrderDeadlines(orderId):
    import logging
    from datetime import datetime
    import traceback

    logging.basicConfig(level=logging.DEBUG)

    try:
        data = request.json
        logging.debug(f"Received data: {data}")

        updates = data.get("updates")
        if not updates:
            logging.error("Updates are required in the request body")
            return jsonify({'message': 'Updates are required'}), 400

        for update in updates:
            assigned_order_id = update.get("id")
            if not assigned_order_id:
                logging.error("assigned_order_id is required in the update")
                return jsonify({'message': 'assigned_order_id is required'}), 400

            # Fetch the specific assigned order by both IDs
            assigned_order = AssignedOrders.query.filter_by(
                id=assigned_order_id,
                orders_id=orderId
            ).first()
            
            if not assigned_order:
                logging.error(f"Assigned order not found for ID: {assigned_order_id} and order ID: {orderId}")
                continue  # Skip this update, or handle as needed

            # Update the fields for this assigned order
            for field, value in update.items():
                if field != "id" and value is not None:  # Check for None to skip updates
                    old_value = getattr(assigned_order, field, None)
                    logging.debug(f"Updating {field} for assigned order ID {assigned_order.id} from {old_value} to {value}")
                    setattr(assigned_order, field, value)

            if "expert_id" in update:
                new_expert_id = update["expert_id"]
                old_expert_id = assigned_order.expert_id

                # Fetch details of both the old and new experts
                old_expert = Employees.query.filter_by(employee_id=old_expert_id).first()
                new_expert = Employees.query.filter_by(employee_id=new_expert_id).first()                
                if old_expert and old_expert.roles == 'lead':
                    # If the old expert was a lead, we need to remove the deadline
                    logging.debug(f"Old expert (ID: {old_expert_id}) was a lead, removing deadline for assigned order ID {assigned_order.id}")
                    assigned_order.deadline = None  # Clear the deadline when expert changes from lead to something else
                
                if new_expert and new_expert.roles == 'lead':
                    assigned_order.assigned_expert_deadline == None
                    # If the new expert is an expert, set the assigned_expert_deadline
                    assigned_order.deadline = update.get("deadline")
                    logging.debug(f"Assigned expert deadline updated for assigned order ID {assigned_order.id} to {assigned_order.deadline}")    

                if new_expert and new_expert.roles == 'expert':
                    assigned_order.deadline == None
                    # If the new expert is an expert, set the assigned_expert_deadline
                    assigned_order.assigned_expert_deadline = update.get("assigned_expert_deadline")
                    logging.debug(f"Assigned expert deadline updated for assigned order ID {assigned_order.id} to {assigned_order.assigned_expert_deadline}")
                
                
                if new_expert and new_expert.roles == 'operationMember':
                    assigned_order.deadline == None
                    assigned_order.deadline_for_operation = update.get("opeartion_member_deadline")
                    logging.debug(f"Assigned expert deadline_for_operation updated for assigned order ID {assigned_order.id} to {assigned_order.deadline_for_operation}")

                # Finally, update the expert_id
                assigned_order.expert_id = new_expert_id
                logging.debug(f"Updated expert_id for assigned order ID {assigned_order.id} to {new_expert_id}")

        logging.info("Preparing to commit changes to the database")
        db.session.commit()
        logging.info("Successfully committed changes")

        return jsonify({'message': 'Successfully updated assigned orders'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"An error occurred: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({'message': 'An error occurred, please check logs.'}), 500


# @app.route('/updateOrderWithId/<orderId>', methods=['POST'])
# @jwt_required()
# def updateOrderWithId(orderId):
#     print("orderId FOR CHECK", orderId)
#     ist = timezone(timedelta(hours=5, minutes=30))
#     task_data = request.form
#     word_count = task_data['word_count']
#     expert_price = task_data['expert_price']
    
#     subject = task_data['subject']
#     end_date = task_data['deadline']
#     end_date_conv = datetime.datetime.strptime(end_date, "%Y-%m-%d").astimezone(ist)

#     budget = task_data['budget']
#     budget_currency = task_data['currency']
#     expert_currency = task_data['expert_currency']
#     comment = task_data['comment']
#     if budget == 'null':
#         budget = 0
#     order = Orders.query.filter_by(orders_id = orderId).first()
#     if order:
#         order.word_count = word_count
#         order.expert_price = expert_price
#         order.end_date = end_date_conv
#         order.task_subject = subject
#         order.order_budget = budget
#         order.currency = budget_currency
#         order.expert_currency = expert_currency
#         order.description = comment
#         # order.qc_Expert_id = Qc_Expert_id
#         # order.otm_id = Otm_id
#         db.session.commit()
#         expert_name = Employees.query.filter_by(employee_id=order.expert_id).first()
#         if expert_name is not None:
#             name = expert_name.firstname
#         else:
#             name = None
        
#         client_data = Client.query.filter_by(client_id=order.client_id).first()
#         if client_data is not None:
#             client_name = client_data.client_name
#         else:
#             client_name = ""

#         print(order)
#         order_data = {
#             'id': order.orders_id,
#             'subject': order.task_subject,
#             'expert_id': name,
#             'client_id': client_name,
#             'order_status': order.status,
#             'order_start_date': order.start_date,
#             'order_end_date': order.end_date,
#             'qc_expert_id': order.qc_expert_id,
#             'otm_id': order.otm_id,
#             'description': order.description,
#             'word_count': order.word_count,
#             'expert_price': order.expert_price,
#         }
#         response_data = [order_data]
#         return jsonify(response_data), 200
#     else:
#         return 'Order not found', 404



@app.route('/deleteOrder/<orderId>', methods=['POST'])
@jwt_required()
def deleteOrder(orderId):
    order = Orders.query.filter_by(orders_id=orderId).first()
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"}), 200
    else:
        return jsonify({"message": "Order not found"}), 200
# -------------------Update task data in data table Module Route End -------------------__

# -------------------Update task status data in data table Module Route start -------------------__


@app.route('/updatestatustask/<userId>', methods=['POST'])
@jwt_required()
def updatestatustask(userId):
    status = request.form.get('Status')
    print(status)
    order = Orders.query.get(userId)
    if order:
        order.status = status
        db.session.commit()
        return 'Status update successful', 200
    else:
        return 'Order not found', 404


# -------------------Update tasks status data in data table Module Route End -------------------__

# -------------------Fatch client Id for vendor invoice in data table Module Route start -------------------__


@app.route('/getclientvendoreid/<clientId>', methods=['GET'])
@jwt_required()
def getclientvendoreid(clientId):
    # current_month = datetime.datetime.now().month
    # current_year = datetime.datetime.now().year

    # orders = Orders.query.filter_by(client_id=userId).filter(db.func.month(Orders.end_date) == current_month).filter(db.func.year(Orders.end_date) == current_year).all()
    orders = Orders.query.filter_by(client_id=clientId).all()
    data = []
    for order in orders:
        order_data = {
            'Order_id': order.orders_id,
            'task_subject': order.task_subject,
            'End_date': order.end_date.strftime('%Y-%m-%d'),
            'price': order.order_budget
        }
        data.append(order_data)

    respp = flask.Response()
    respp.headers['Access-Control-Allow-Origin'] = '*'
    respp.headers['Content-Type'] = 'application/json'
    respp.set_data(json.dumps(data))

    return respp


@app.route('/team-member-table/<userId>', methods=['POST'])
@jwt_required()
def teamMemberTable(userId):
    from datetime import datetime
    from sqlalchemy import func, or_

    # Get the current user
    current_user = get_jwt_identity()
    current_date = datetime.now()

    # Get current month and year
    current_month = current_date.month
    current_year = current_date.year
    user = Users.query.filter_by(email=current_user).first()
    page = int(request.args.get('page', 1))
    search_term = request.form.get('search', '')
    status = request.form['status']


    per_page = int(request.args.get('per_page', 10))

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Get selected month and year from form data
    selected_month = request.form.get('month', current_month)
    selected_year = request.form.get('year', current_year)

    # Check if the userId corresponds to a lead or an expert
    employee = Employees.query.filter_by(employee_id=userId).first()
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    # Query to get all relevant orders
    orders_query = AssignedOrders.query.filter(
        or_(
            AssignedOrders.assigned_expert == userId,  # Filter by assigned_expert
            AssignedOrders.expert_id == userId          # Filter by expert_id
        ),
        func.extract('month', AssignedOrders.assigned_expert_deadline) == selected_month,
        func.extract('year', AssignedOrders.assigned_expert_deadline) == selected_year
    )

    # Apply search filter if search_term is provided
    if search_term:
        orders_query = orders_query.join(
            Orders,
            AssignedOrders.orders_id == Orders.orders_id
        ).filter(
            or_(
                Orders.orders_id.ilike(f"%{search_term}%"),
                Orders.description.ilike(f"%{search_term}%"),
                Orders.task_subject.ilike(f"%{search_term}%")
            )
        )
     # Apply status filter if status is provided
    if status:
        # Explicitly define the join and use select_from
        orders_query = (
            orders_query
            .join(Orders, AssignedOrders.orders_id == Orders.orders_id)
            .filter(Orders.status == status)
        )

        
    # Apply pagination
    total_orders = orders_query.count()
    orders_paginated = orders_query.order_by(AssignedOrders.assigned_expert_deadline).offset((page - 1) * per_page).limit(per_page).all()

    response_data = []
    

    for order in orders_paginated:
        order_status = Orders.query.filter(Orders.orders_id == order.orders_id).first()
        
        # Base order data
        base_order_data = {
            'id': order.id,
            'order_id': order.orders_id,
            'comment_for_teammember': order.teammember_comment,
            'remarks': order.remarks,
            'incentive': order.incentive,
            'status':order_status.status if order_status else None
        }

        # Collect all deadlines for comparison
        deadlines = []

        # Check the assigned expert deadlines and append them to response_data
        if order.assigned_expert_deadline and order.assigned_expert_deadline != "0000-00-00":
            expert_order_data = base_order_data.copy()
            expert_order_data['assigned_expert_deadline'] = order.assigned_expert_deadline.strftime("%Y-%m-%d")
            expert_order_data['expert_no_of_words'] = order.expert_no_of_words

            response_data.append(expert_order_data)
            deadlines.append(order.assigned_expert_deadline)

        for i in range(1, 7):
            assigned_expert_deadline = getattr(order, f'assigned_expert_deadline{i}', None)
            if assigned_expert_deadline and assigned_expert_deadline != "0000-00-00":
                expert_order_data = base_order_data.copy()
                expert_order_data[f'assigned_expert_deadline{i}'] = assigned_expert_deadline.strftime("%Y-%m-%d")
                expert_order_data[f'expert_no_of_words{i}'] = getattr(order, f'expert_no_of_word{i}', "0")
                response_data.append(expert_order_data)
                deadlines.append(assigned_expert_deadline)

        # Get the minimum date for each specific deadline column
        if deadlines:
            min_date = min(deadlines).strftime("%Y-%m-%d")
            # Add to each entry in the response_data
            for entry in response_data:
                entry['min_deadline'] = min_date  # You may remove this if you don't want to include a new key

    # Sort response data based on the earliest assigned expert deadline column
    response_data.sort(key=lambda x: (
        x.get('assigned_expert_deadline', None) or
        x.get('assigned_expert_deadline1', None) or
        x.get('assigned_expert_deadline2', None) or
        x.get('assigned_expert_deadline3', None) or
        x.get('assigned_expert_deadline4', None) or
        x.get('assigned_expert_deadline5', None) or
        x.get('assigned_expert_deadline6', None)
    ))

    # Debugging: Print the response data after sorting
    print("Response Data after sorting:", response_data)

    pagination_info = {
        'total_orders': total_orders,
        'current_page': page,
        'per_page': per_page,
        'total_pages': (total_orders + per_page - 1) // per_page,
    }

    return jsonify({"data": response_data, "pagination_info": pagination_info}), 200







@app.route('/getDpr/<userId>', methods=['POST'])
@jwt_required()
def getDpr(userId):
    from datetime import datetime
    from sqlalchemy import func

    # Get the current user
    current_user = get_jwt_identity()
    current_date = datetime.now()

    # Get current month and year
    current_month = current_date.month
    current_year = current_date.year
    user = Users.query.filter_by(email=current_user).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Get selected month and year from form data
    selected_month = request.form.get('month')
    selected_year = request.form.get('year')

    # If no month is specified, default to current month
    if not selected_month:
        selected_month = current_month
    if not selected_year:
        selected_year = current_year

    # Check if the userId corresponds to a lead or an expert
    employee = Employees.query.filter_by(employee_id=userId).first()
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    # Query to get all relevant orders
    if employee.roles == 'lead':
        orders_query = AssignedOrders.query.filter(
            AssignedOrders.expert_id == userId,
            func.extract('month', AssignedOrders.deadline) == selected_month,
            func.extract('year', AssignedOrders.deadline) == selected_year
        ).order_by(AssignedOrders.deadline.asc())
    elif employee.roles == 'operationMember':
        orders_query = AssignedOrders.query.filter(
            AssignedOrders.expert_id == userId,
            func.extract('month', AssignedOrders.deadline_for_operation),
            func.extract('year', AssignedOrders.deadline_for_operation)
        ).order_by(AssignedOrders.deadline_for_operation.asc())
    else:
        orders_query = AssignedOrders.query.filter(
            or_(
                AssignedOrders.assigned_expert == userId,  # Filter by assigned_expert
                AssignedOrders.expert_id == userId          # Filter by expert_id
            ),
            func.extract('month', AssignedOrders.assigned_expert_deadline) == selected_month,
            func.extract('year', AssignedOrders.assigned_expert_deadline) == selected_year
        ).order_by(AssignedOrders.assigned_expert_deadline.asc())
    # Execute the query to get the full results
    orders = orders_query.all()

    # Prepare the response data
    response_data = []
    
    for order in orders:
        order_exists = Orders.query.filter_by(orders_id=order.orders_id).first()
        if not order_exists:
            continue  # Skip if order does not exist in Orders table
        # Base order data
        base_order_data = {
            'id': order.id,
            'order_id': order.orders_id,
            'comments': order.comments,
            'comment_for_tl': order.comment_for_tl,
            "expert_type":employee.roles,
            'remarks': order.remarks,
            'incentive': order.incentive,
            'no_of_words': order.no_of_words,
        }

        if employee.roles == 'lead':
            # Handle deadlines for leads
            if order.deadline and order.deadline != "0000-00-00":
                lead_order_data = base_order_data.copy()
                lead_order_data['deadline'] = order.deadline.strftime("%Y-%m-%d")
                lead_order_data['no_of_words'] = order.no_of_words
                response_data.append(lead_order_data)

            # Handle team deadlines
            for i in range(1, 7):  # Loop through 1 to 6 for team deadlines
                team_deadline = getattr(order, f'team_deadline{i}', None)
                team_no_of_words = getattr(order, f'no_of_word{i}', None)

                if team_deadline and team_deadline != "0000-00-00":
                    team_order_data = base_order_data.copy()
                    team_order_data[f'team_deadline{i}'] = team_deadline.strftime("%Y-%m-%d")
                    team_order_data['no_of_words'] = team_no_of_words
                    response_data.append(team_order_data)
        elif employee.roles == 'operationMember':
            # Handle assigned expert deadlinesdeadline_for_operation
            if order.deadline_for_operation  and order.deadline_for_operation != "0000-00-00":
                expert_order_data1 = base_order_data.copy()
                expert_order_data1['deadline_for_operation'] = order.deadline_for_operation.strftime("%Y-%m-%d")
                response_data.append(expert_order_data1)           
           
            for i in range(1, 7):  # Loop through 1 to 6 for assigned expert deadlines
                deadline_for_operation = getattr(order, f'deadline_for_operation{i}',None)

                if deadline_for_operation and deadline_for_operation != "0000-00-00":
                    expert_order_data = base_order_data.copy()
                    expert_order_data[f'deadline_for_operation{i}'] = deadline_for_operation.strftime("%Y-%m-%d")

                    response_data.append(expert_order_data)

        elif employee.roles == 'expert':
            # Handle assigned expert deadlines
            if order.assigned_expert_deadline and order.assigned_expert_deadline != "0000-00-00":
                expert_order_data1 = base_order_data.copy()
                expert_order_data1['assigned_expert_deadline'] = order.assigned_expert_deadline.strftime("%Y-%m-%d")
                expert_order_data1['expert_no_of_words'] = order.expert_no_of_words
                response_data.append(expert_order_data1)           
           
            for i in range(1, 7):  # Loop through 1 to 6 for assigned expert deadlines
                assigned_expert_deadline = getattr(order, f'assigned_expert_deadline{i}', None)
                expert_no_of_words = getattr(order, f'expert_no_of_word{i}', None)

                if assigned_expert_deadline and assigned_expert_deadline != "0000-00-00":
                    expert_order_data = base_order_data.copy()
                    expert_order_data[f'assigned_expert_deadline{i}'] = assigned_expert_deadline.strftime("%Y-%m-%d")
                    expert_order_data[f'expert_no_of_word{i}'] = expert_no_of_words if expert_no_of_words is not None else "0"
                    response_data.append(expert_order_data)
            
    return jsonify(response_data), 200

@app.route('/editDpr', methods=['PUT'])
@jwt_required()
def updateOrders():
    from flask import request, jsonify
    from datetime import datetime
    import logging

    logging.basicConfig(level=logging.DEBUG)

    try:
        # Get the current user's identity
        current_user = get_jwt_identity()

        # Get the JSON data from the request
        data = request.get_json()
        logging.debug(f"Received data for update: {data}")

        # Loop through each update in the request body
        for update in data.get('updates', []):
            object_id = update.get('id')  # Specific object ID to update
            print("---data-------",update )

            # Fetch the order using the object_id
            order = AssignedOrders.query.filter_by(id=object_id).first()
            if not order:
                return jsonify({"message": f"Order with id {object_id} not found"}), 404

            # Update assigned_expert_deadline fields if provided
            for i in range(0, 7):
                expert_deadline_key = f'assigned_expert_deadline{i}' if i > 0 else 'assigned_expert_deadline'
                if update.get(expert_deadline_key):
                    setattr(order, expert_deadline_key, datetime.strptime(update[expert_deadline_key], "%Y-%m-%d"))
                    logging.debug(f"Updated {expert_deadline_key}: {getattr(order, expert_deadline_key)}")
                    
            # Update team deadlines if provided
            if update.get('deadline'):  # Check for the first field named 'deadline'
                order.deadline = datetime.strptime(update['deadline'], "%Y-%m-%d")
                logging.debug(f"Updated deadline: {order.deadline}")        

            # Update team deadlines if provided
            for i in range(0, 7):  # Assuming team_deadline1 to team_deadline6
                team_deadline_key = f'team_deadline{i}'
                if update.get(team_deadline_key):
                    setattr(order, team_deadline_key, datetime.strptime(update[team_deadline_key], "%Y-%m-%d"))
                    logging.debug(f"Updated {team_deadline_key}: {getattr(order, team_deadline_key)}")
            
               # Update expert_no_of_words and no_of_words fields if provided
            for i in range(0, 7):  # From 0 to 6 for expert_no_of_words and no_of_words
                expert_word_key = f'expert_no_of_word{i}' if i > 0 else 'expert_no_of_words'
                no_word_key = f'no_of_word{i}' if i > 0 else 'no_of_words'
                
                if update.get(expert_word_key) is not None:  # Check if the key exists and is not None
                    setattr(order, expert_word_key, update[expert_word_key])
                    logging.debug(f"Updated {expert_word_key}: {getattr(order, expert_word_key)}")

                if update.get(no_word_key) is not None:  # Check if the key exists and is not None
                    setattr(order, no_word_key, update[no_word_key])
                    logging.debug(f"Updated {no_word_key}: {getattr(order, no_word_key)}")

        

            # Update other fields if provided
            order.comments = update.get('comments', order.comments)
            order.remarks = update.get('remarks', order.remarks)
            order.incentive = update.get('incentive', order.incentive)

        # Commit changes to the database
        db.session.commit()
        logging.info("Successfully committed changes")
        return jsonify({"message": "Successfully updated deadlines"}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"message": "An error occurred, please check logs."}), 500






# @app.route('/editDpr', methods=['POST'])
# @jwt_required()
# def editDpr():
#     try:
#         # Get the updated data from the request
#         updated_data = request.json
#         print("updated dpr data", updated_data)
#         # Update the records in the AssignedOrders table
#         for data in updated_data:
#             id = data.get('id')
#             assigned_order = AssignedOrders.query.filter_by(id=id).first()
#             if assigned_order:
#                 # Convert the date format
#                 print("datas============", data.get('deadline'))
#                 print("data.get('deadline')", data.get('deadline'))
#                 deadline_str = data.get('deadline')
#                 deadline_datetime = datetime.datetime.strptime(deadline_str, '%a, %d %b %Y %H:%M:%S %Z')
#                 formatted_deadline = deadline_datetime.strftime('%Y-%m-%d %H:%M:%S')

#                 # Update the record
#                 assigned_order.deadline = formatted_deadline
#                 assigned_order.no_of_words = data.get('no_of_words', assigned_order.no_of_words)
#                 assigned_order.remarks = data.get('remarks', assigned_order.remarks)
#                 assigned_order.incentive = data.get('incentive', assigned_order.incentive)
#                 assigned_order.comments = data.get('comments', assigned_order.comments)                

                
#                 db.session.commit()
        
#         return jsonify({'message': 'Data updated successfully'}), 200
#     except Exception as e:
#         print(e)
#         return jsonify({'error': str(e)}), 500



# -------------------Fatch vendore Id for vendor invoice  data in data table Module Route End -------------------__

# -------------------Fatch tutors id  for tutors invoice in data table Module Route start -------------------__


@app.route('/gettutorsidforinvoice/<userId>', methods=['GET'])
@jwt_required()
def gettutorsidforinvoice(userId):
    orders = Orders.query.filter(Orders.expert_id == userId,
                                 db.func.MONTH(Orders.end_date) == db.func.MONTH(db.func.now()),
                                 db.func.YEAR(Orders.end_date) == db.func.YEAR(db.func.now())).all()

    data = []
    for order in orders:
        data.append({
            'Order_id': order.orders_id,
            'Expert_id': order.expert_id,
            'End_date': order.end_date,
            'Expert_price': order.expert_price
            # Add other fields you want to include in the response
        })

    respp = flask.Response()
    respp.headers['Access-Control-Allow-Origin'] = '*'
    respp.headers['Content-Type'] = 'application/json'
    jsondata = json.dumps(data, default=datetime_handler)

    print("Json formatted data")
    print(jsondata)

    respp.set_data(jsondata)

    return respp


# -------------------Fatch tutors Id for tutors invoice  data in data table Module Route End -------------------__

# -------------------Fatch orders data dashbord Module Route start -------------------__


@app.route('/getorderfordashbord', methods=['GET', 'POST', "OPTIONS"])
@jwt_required()
def getorderfordashbord():
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    orders = Orders.query.filter(db.func.month(Orders.end_date) == current_month).filter(
        db.func.year(Orders.end_date) == current_year).all()

    data = []
    for order in orders:
        order_data = {
            'Order_id': order.orders_id,
            'End_date': order.end_date.strftime('%Y-%m-%d')
        }
        data.append(order_data)

    respp = jsonify(data)
    respp.headers['Access-Control-Allow-Origin'] = '*'
    respp.headers['Content-Type'] = 'application/json'

    return respp


# -------------------Fatch   orders data dashbord Module Route End -------------------__

# -------------------Fatch vendor Id for update invoice data in data table Module Route start -------------------__


@app.route('/getvendordataforupinvoice/<userId>', methods=['GET'])
@jwt_required()
def getvendordataforupinvoice(userId):
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    orders = Orders.query.filter_by(client_id=userId).filter(db.func.month(Orders.end_date) == current_month).filter(
        db.func.year(Orders.end_date) == current_year).all()

    data = []
    for order in orders:
        order_data = {
            'Order_id': order.orders_id,
            'Client_id': order.client_id,
            'End_date': order.end_date.strftime('%Y-%m-%d'),
            'price': order.expert_price
        }
        data.append(order_data)

    respp = flask.Response()
    respp.headers['Access-Control-Allow-Origin'] = '*'
    respp.headers['Content-Type'] = 'application/json'
    respp.set_data(json.dumps(data))

    return respp


# -------------------Fatch vendor Id for update invoice data in data table Module Route End -------------------__


# ------------------Fatch tutor id for update invoice data  Module Route start -------------------__


@app.route('/gettutorsdataforupinvoice/<userId>', methods=['GET'])
@jwt_required()
def gettutorsdataforupinvoice(userId):
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    orders = Orders.query.filter_by(expert_id=userId).filter(db.func.month(Orders.end_date) == current_month).filter(
        db.func.year(Orders.end_date) == current_year).all()

    data = []
    for order in orders:
        order_data = {
            'Order_id': order.orders_id,
            'Expert_id': order.expert_id,
            'End_date': order.end_date.strftime('%Y-%m-%d')
        }
        data.append(order_data)

    respp = flask.Response()
    respp.headers['Access-Control-Allow-Origin'] = '*'
    respp.headers['Content-Type'] = 'application/json'
    respp.set_data(json.dumps(data))

    return respp


# -------------------Fatch tutor Id for update invoice data  Module Route End -------------------__

# -------------------Update vendor invoice  data in Invoice pdf Module Route start -------------------__


@app.route('/updatevendorinvoicebudget/<userId>', methods=['POST'])
@jwt_required()
def updatevendorinvoicebudget(userId):
    data = flask.request.form
    Task_Subject = data['Task_Subject']
    Vendor_budget = data['Vendor_budget']
    Expert_price = data['Expert_price']

    order = Orders.query.get(userId)
    if order:
        order.Task_Subject = Task_Subject
        order.Vendor_budget = Vendor_budget
        order.Expert_price = Expert_price
        db.session.commit()

        response_data = {
            'message': 'Update successful'
        }

        respp = flask.Response(json.dumps(response_data), mimetype='application/json')
        respp.headers['Access-Control-Allow-Origin'] = '*'
        return respp
    else:
        response_data = {
            'message': 'Order not found'
        }
        respp = flask.Response(json.dumps(response_data), mimetype='application/json')
        respp.headers['Access-Control-Allow-Origin'] = '*'
        return respp


# -------------------Update vendor invoice  data in Invoice pdf Module Route End -------------------__

# ----------------------------------insert invoice tutor   data in invoice table -------------------------

# Configure the upload folder and allowed file types (Word and PDF)
# documents = UploadSet('documents', ('doc', 'docx', 'pdf'))
# app.config['UPLOADED_DOCUMENTS_DEST'] = 'uploads'
# configure_uploads(app, documents)

# AWS S3 configuration
AWS_S3_BUCKET_NAME = 'file-upload-om'
AWS_REGION = ''
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

s3 = boto3.client('s3', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


@app.route('/saveInvoice/<clientId>', methods=['POST'])
@jwt_required()
def saveInvoice(clientId):
    try:
        data = flask.request.form['data']
        data_dict = json.loads(data)
        data_array = data_dict.get('data', [])

        file = request.files
        print("checking upload attach", file)
        if file:
            file_data = file.getlist('document')
            #pdf_file = file.get('invoicepdf')
        else:
            file_data = None
            print("none")
            #pdf_file = None

        check = check_invoice(data_array)
        print(check , "Status check")
        if not check:
            result = insert_data(data, file_data, clientId)
            print("check done")
        else:
            result = jsonify({'message': f'Invoice already exists with order id {check}'}), 400
        print(result)
        return result
    except Exception as e:
        return jsonify({"error": str(e)})

def check_invoice(data):
    try:
        filtered_data = [item for item in data if 'order_id' in item]
        print(filtered_data, "filtered_data")
        matching_orders = []

        for item_data in filtered_data:
            print(item_data)
            existing_order = InvoiceOrders.query.filter_by(orders_id=item_data['order_id']).first()

            if existing_order:
                print("Contains order_id", existing_order.orders_id)
                matching_orders.append(existing_order.orders_id)

        return matching_orders
    except Exception as e:
        print(str(e))
        return jsonify({'message': f'Some error occurred {str(e)}'}), 500

def insert_data(data, files, client_id):
    try:
        print("files", files)

        data_dict = json.loads(data)
        
        data_array = data_dict.get('data', [])

        invoice_date = data_dict['invoiceDate']
        due_date = data_dict['dueDate']
        date_object = datetime.datetime.strptime(invoice_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_invoice_date = date_object.strftime("%Y-%m-%d")

        date_object_due = datetime.datetime.strptime(due_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_due_date = date_object_due.strftime("%Y-%m-%d")

        tax_type = data_dict['taxType']
        discount = data_dict['discount']
        discount_type = data_dict['discountType']
        disc_percent = data_dict['diskPercent']
        currency = data_dict['currency']
        invoiceNumber = data_dict['invoiceNumber']
        total = data_dict['total']
        totalAmount = data_dict['totalAmount']
        sub_tax = data_dict['subTax']
        print('sub_tax', sub_tax)
        paid_amount = data_dict['paidAmount']
        
        if paid_amount is None:
            paid_amount = 0

        print('paid_amount', paid_amount)
        
        tax_amount = 0
        print(data_array)

        for item_data in data_array:
            if tax_type == 'vat':
                tax_amount += item_data.get('vat', 0)
            elif tax_type == 'gst' and sub_tax == 'gst':
                tax_amount += item_data.get('cgst', 0) + item_data.get('sgst', 0)
            elif tax_type == 'gst' and sub_tax == 'igst':
                tax_amount += item_data.get('igst', 0)

        print(tax_amount)
       
        if files is not None:
            print("file not none")
            for file in files:
                filename = secure_filename(file.filename)
                print(filename)
                new_attachment = Attachments(
                    name=filename,
                    invoice_number=invoiceNumber
                )
                db.session.add(new_attachment)
            db.session.commit()
        else:
            file = None
            print("file none")
        
        for item_data in data_array:
            tax_rate=item_data.get('taxRate', 0),
        
        print("working till here !!")
        new_invoice = Invoice(
            client_id=client_id,
            discount=discount,
            discountType = discount_type,
            invoice_date=formatted_invoice_date,
            due_date=formatted_due_date,
            invoice_number=invoiceNumber,
            tax_amount=tax_amount,
            total=total,
            total_amount=totalAmount,
            tax_type=tax_type,
            sub_tax=sub_tax,
            currency=currency,
            dis_percent=disc_percent,
            paid_amount = paid_amount,
            tax_rate = tax_rate
        )


        for item_data in data_array:
            new_invoice_orders = InvoiceOrders(
                invoice_number=invoiceNumber,
                rate=item_data['rate'],
                amount=item_data['amount'],
                item_total=item_data['total'],
                item=item_data['item'],
                orders_id=item_data['order_id'],
                vat=item_data.get('vat', 0),
                cgst=item_data.get('cgst', 0),
                sgst=item_data.get('sgst', 0),
                igst=item_data.get('igst',0),
                tax_rate=item_data.get('taxRate', 0),
                quantity = item_data['quantity'],
            )
            print(new_invoice_orders)
            
            db.session.add(new_invoice_orders)
            db.session.add(new_invoice)
            
            if file != None:
                upload_file(file)
        
        db.session.commit()
        return getInvoice(invoiceNumber), 200
    except Exception as e:
        print(e)
        return jsonify({'message': f'Some error occured {e}'}), 500

def upload_file(file):
    print(file)
    if file:
        try:
            # Generate a secure filename
            filename = secure_filename(file.filename)

            # Upload the file to S3
            s3.upload_fileobj(file, AWS_S3_BUCKET_NAME, filename)

            return jsonify({'message': 'File uploaded successfully', 'filename': filename})
        except botocore.exceptions.NoCredentialsError:
            return jsonify({'error': 'AWS credentials not available'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'No file provided or invalid file type'}), 400


@app.route('/uploadInvoice/<invoiceNumber>', methods=['POST'])
@jwt_required()
def uploadInvoice(invoiceNumber):
    file = request.files
    if file:
        file_data = file.get('invoicepdf')
        #pdf_file = file.get('invoicepdf')
        if save_pdf_to_s3(file_data, invoiceNumber) == "success":
            return jsonify({'message': 'Invoice Uploaded Successfully'}), 200
        else:
            return jsonify({'message': 'Cannot upload invoice'}), 400
        


def save_pdf_to_s3(pdf, invoiceNumber):
    try:
        #pdf = generate_pdf(data)

        # Generate a secure filename
        filename = f"{invoiceNumber}.pdf"
        print(filename)
        # Upload the file to S3
        s3.upload_fileobj(pdf, AWS_S3_BUCKET_NAME, filename)

        return "success"
    except Exception as e:
        return str(e)

@app.route('/updateInvoice', methods=['POST'])
@jwt_required()
def updateInvoice():
    try:
        data = flask.request.form['data']
        data_dict = json.loads(data)
        #data_array = data_dict.get('data', [])

        file = request.files
        if file:
            file_data = file.get('document')
            #pdf_file = file.get('invoicepdf')
        else:
            file_data = None
            #pdf_file = None
        check = update_invoice_data(data, file_data)
        return check
    except Exception as e:
        return jsonify({"error": str(e)})


def update_invoice_data(data, file):
    try:
        data_dict = json.loads(data)

        data_array = data_dict.get('data', [])

        print(data_dict)

        invoiceNumber = data_dict['invoiceNumber']
        existing_invoice = Invoice.query.filter_by(invoice_number=invoiceNumber).first()

        if not existing_invoice:
            return jsonify({'error': f'Invoice with invoice number {invoiceNumber} not found'}), 404
        print("Invoice exists")
        
        invoice_date = data_dict['invoiceDate']
        due_date = data_dict['dueDate']

        # Convert strings to datetime objects
        invoice_date_obj = datetime.datetime.strptime(invoice_date, "%d-%m-%Y")
        due_date_obj = datetime.datetime.strptime(due_date, "%d-%m-%Y")

        # Format the dates as needed
        formatted_invoice_date = invoice_date_obj.strftime("%Y-%m-%d")
        formatted_due_date = due_date_obj.strftime("%Y-%m-%d")
        
        if file != None:
            filename = secure_filename(file.filename)
            new_attachment = Attachments(
                name = filename,
                invoice_number = invoiceNumber
            )
            db.session.add(new_attachment)
        else:
            filename = None

        print("attachement", filename)
       

        tax_type = data_dict['taxType']
        discount = data_dict['discount']
        disc_percent = data_dict['diskPercent']
        currency = data_dict['currency']
        client_id = data_dict['clientId']
        total = data_dict['total']
        totalAmount = data_dict['totalAmount']
        sub_tax = data_dict['subTax']
        paid_amount = data_dict['paidAmount']

        removed_orders = data_dict['removedOrders']

        print("removed list", removed_orders)


        tax_amount = 0

        for item_data in data_array:
            if tax_type == 'vat':
                tax_amount += item_data.get('vat', 0)
            elif tax_type == 'gst' and sub_tax == 'gst':
                tax_amount += item_data.get('cgst', 0) + item_data.get('sgst', 0)
            elif tax_type == 'gst' and sub_tax == 'igst':
                tax_amount += item_data.get('igst', 0)
        
        for order_id in removed_orders:
            # Check if the order exists
            order_exists = InvoiceOrders.query.filter(InvoiceOrders.orders_id == order_id).first()

            if order_exists:
                # Delete the order
                db.session.delete(order_exists)
                db.session.commit()
                print(f"Order with orders_id {order_id} has been deleted.")
            else:
                print(f"Order with orders_id {order_id} does not exist.")

        
        for item_data in data_array:
            order_exists = InvoiceOrders.query.filter(InvoiceOrders.orders_id == item_data.get('order_id')).first()
            if order_exists:
                existing_invoice = Invoice.query.filter_by(invoice_number=invoiceNumber).first()
                existing_invoice.client_id=client_id,
                existing_invoice.discount=discount,
                existing_invoice.invoice_date=formatted_invoice_date,
                existing_invoice.due_date=formatted_due_date,
                existing_invoice.tax_amount=tax_amount,
                existing_invoice.total=total,
                existing_invoice.total_amount=totalAmount,
                existing_invoice.tax_type=tax_type,
                existing_invoice.sub_tax=sub_tax,
                existing_invoice.currency=currency,
                existing_invoice.dis_percent=disc_percent,
                existing_invoice.paid_amount = paid_amount
                existing_invoice.tax_rate=item_data.get('taxRate', 0),

                existing_order = InvoiceOrders.query.filter_by(orders_id = item_data.get('order_id') ).first()
                existing_order.rate=item_data['rate'],
                existing_order.orders_id=item_data['order_id'],
                existing_order.vat=item_data.get('vat', 0),
                existing_order.cgst=item_data.get('cgst', 0),
                existing_order.sgst=item_data.get('sgst', 0),
                existing_order.igst=item_data.get('igst',0),
                existing_order.tax_rate=item_data.get('taxRate', 0),
                existing_order.amount=item_data['amount'],
                existing_order.item_total=item_data['total'],
                existing_order.item=item_data['item'],
                existing_order.quantity = item_data['quantity'],

            else:
                try:
                    print("invoice number else",invoiceNumber)
                    print(item_data['item'])
                    print(item_data['rate'])
                    existing_invoice = Invoice.query.filter_by(invoice_number=invoiceNumber).first()
                    existing_invoice.client_id=client_id,
                    existing_invoice.discount=discount,
                    existing_invoice.invoice_date=formatted_invoice_date,
                    existing_invoice.due_date=formatted_due_date,
                    existing_invoice.tax_amount=tax_amount,
                    existing_invoice.total=total,
                    existing_invoice.total_amount=totalAmount,
                    existing_invoice.tax_type=tax_type,
                    existing_invoice.sub_tax=sub_tax,
                    existing_invoice.currency=currency,
                    existing_invoice.dis_percent=disc_percent,
                    existing_invoice.paid_amount = paid_amount
                    existing_invoice.tax_rate=item_data.get('taxRate', 0),

                    order_in_invoice = InvoiceOrders(
                        invoice_number=invoiceNumber,
                        amount=item_data['amount'],
                        item_total=item_data['total'],
                        item=item_data['item'],
                        rate=item_data['rate'],
                        orders_id=item_data.get('order_id'),
                        vat=item_data.get('vat', 0),
                        cgst=item_data.get('cgst', 0),
                        sgst=item_data.get('sgst', 0),
                        igst=item_data.get('igst',0),
                        tax_rate=item_data.get('taxRate', 0),
                        quantity = item_data['quantity'],
                    )
                    print(existing_invoice)
                    db.session.add(existing_invoice)
                    db.session.add(order_in_invoice)
                except Exception as e:
                    print(str(e))

        db.session.commit() 
        #return jsonify({'message': 'Error removing invoice from s3'}), 400
        if file != None:
            upload_file(file)
        if delete_pdf_from_s3(invoiceNumber) == "success":
            return getInvoice(invoiceNumber), 200
        else:
            return jsonify({'message': 'Error removing invoice from s3'}), 400
    except Exception as e:

        return {"error": str(e)}

@app.route('/remove_order', methods=['POST'])
def remove_order(order_id):
    try:
        #order_id_to_remove = request.json.get('order_id')  # Assuming you're sending the order_id in the request JSON
        existing_order = InvoiceOrders.query.filter_by(orders_id=order_id).first()

        if existing_order:
            db.session.delete(existing_order)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Order removed successfully'})
        else:
            return jsonify({'success': False, 'message': 'Order not found'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
@app.route('/download-invoice/<invoice_number>', methods=['GET'])
def download_invoice(invoice_number):
    try:
        
        # Specify the S3 key based on the invoice number
        s3_key = f'{invoice_number}.pdf'

        # Download the file from S3
        response = s3.get_object(Bucket=AWS_S3_BUCKET_NAME, Key=s3_key)
        pdf_content = response['Body'].read()

        # Create an in-memory file-like object to send as a response
        pdf_io = BytesIO(pdf_content)

        # Send the PDF file as a response
        return send_file(pdf_io, download_name=f'{invoice_number}_invoice.pdf', as_attachment=True)

    except NoCredentialsError:
        return jsonify({'error': 'AWS credentials not available'}), 500
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/download-attachemts', methods=['POST'])
@jwt_required()
def download_attachment():
    try:
        attachment = flask.request.form['attachments']
        s3_key = f'{attachment}'
        print(s3_key)

        # Download the file from S3
        response = s3.get_object(Bucket=AWS_S3_BUCKET_NAME, Key=s3_key)
        file_content = response['Body'].read()

        # Create an in-memory file-like object to send as a response
        file_io = BytesIO(file_content)

        # Extract the filename from the S3 key
        filename = os.path.basename(s3_key)

        # Send the file as a response without converting to PDF
        return send_file(file_io, download_name=filename, as_attachment=True)

    except NoCredentialsError:
        return jsonify({'error': 'AWS credentials not available'}), 500
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/getAllInvoices', methods=['POST'])
@jwt_required()
def getAllInvoices():
    try:
        invoice_dict = {}

        # Iterate over students and their invoices
        
        get_invoices = Invoice.query.all()
        for invoice in get_invoices:
            # Store the invoice in the dictionary using the invoice number as the key
            invoice_number = invoice.invoice_number
            client_id = invoice.client_id
            client_name = Client.query.filter_by(client_id=client_id).first()
            if invoice_number not in invoice_dict:
                invoice_dict[invoice_number] = {
                    'id': invoice.id,
                    'client_id': client_id,
                    'name': client_name.client_name,
                    'invoice_number': invoice.invoice_number,
                    'amount': invoice.total_amount,
                    'invoice_date': invoice.invoice_date.strftime('%Y-%m-%d'),
                    'due_date': invoice.due_date.strftime('%Y-%m-%d'),
                    'currency': invoice.currency,
                    'payment_date': invoice.payment_date,
                    'paid_amount': invoice.paid_amount,
                }

        # Convert the dictionary values to a list to get the unique invoices
        all_invoices = list(invoice_dict.values())
        return jsonify(all_invoices)
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.route('/getInvoice/<invoice_number>', methods=['GET'])
@jwt_required()
def getInvoice(invoice_number):
    try:
        # Filter invoices by the provided invoice number
        invoices = InvoiceOrders.query.filter_by(invoice_number=invoice_number).all()

        # Initialize a list to store selected invoice details
        selected_invoice_details = []
        invoice_dict = {}

        attachments_array = []
        
        attachements = Attachments.query.filter_by(invoice_number = invoice_number).all()
        for attachement in attachements:
            attach = {
                'attachment_id': attachement.attachment_id,
                'name': attachement.name    
            }
            attachments_array.append(attach)
        
        invoices_data = Invoice.query.filter_by(invoice_number=invoice_number).first()
        
        client = Client.query.filter_by(client_id = invoices_data.client_id).first()
        invoice_number = invoices_data.invoice_number
        
        if invoice_number not in invoice_dict:
            invoice_dict = {
                'invoice_number': invoices_data.invoice_number,
                'client_id': invoices_data.client_id,
                'client_name': client.client_name,
                'client_email': client.client_email,
                'client_phone' : client.client_contact,
                'client_university': client.university,
                'invoice_date': invoices_data.invoice_date.strftime('%Y-%m-%d'),
                'due_date': invoices_data.due_date.strftime('%Y-%m-%d'),
                'dis_percent': invoices_data.dis_percent,
                'discount_type': invoices_data.discountType,
                'discount': invoices_data.discount,
                'tax_type': invoices_data.tax_type,
                'sub_tax': invoices_data.sub_tax,
                'tax_rate': invoices_data.tax_rate,
                'tax_amount': invoices_data.tax_amount,
                'total_amount': invoices_data.total_amount,
                'paid_amount': invoices_data.paid_amount,
                'currency': invoices_data.currency,
                'total': invoices_data.total,
                'attachment': attachments_array
            }

        # Iterate over each invoice with the same invoice number
        for invoice in invoices:
            invoice_details = {
                'id': invoice.id,
                'invoice_number': invoice.invoice_number,
                'item_total': invoice.item_total,
                'amount': invoice.amount,
                'item' : invoice.item,
                'order_id': invoice.orders_id,
                'tax_rate': invoice.tax_rate,
                'rate': invoice.rate,
                'quantity': invoice.quantity,
                'vat': invoice.vat,
                'cgst': invoice.cgst,
                'sgst': invoice.sgst,
                'igst': invoice.igst
            }
            selected_invoice_details.append(invoice_details)

        # Return the list of selected invoice details as JSON
        return jsonify({"data": invoice_dict, "invoices": selected_invoice_details})

    except Exception as e:
        print(e)  # Log the error for debugging
        return jsonify({"error": str(e)})

@app.route('/updatePaymentById/<id>', methods=['POST'])
@jwt_required()
def updatePaymentById(id):
    
    amount = flask.request.form['amount']
    payment_date = flask.request.form['payment_date']
    Mode_of_payment = flask.request.form['payment_method']
    """  date_object = datetime.datetime.strptime(payment_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    formatted_invoice_date = date_object.strftime("%Y-%m-%d")
    """
    # Convert the original date string to a datetime object
    original_date = datetime.datetime.strptime(payment_date, '%a, %d %b %Y %H:%M:%S GMT')

    # Format the datetime object to the MySQL date format
    formatted_date = original_date.strftime('%Y-%m-%d')

    # Update the payment
    invoices = Invoice.query.filter_by(invoice_number=id).all()
    if invoices:
        for invoice in invoices: 
            invoice.paid_amount = amount
            invoice.payment_date = formatted_date
            invoice.payment_method = Mode_of_payment
        
        db.session.commit()
        return jsonify({'message': 'Amount Recieved'}), 200
    else:   
        return jsonify({'message': 'Error in updating'}), 400



def datetime_handler(x):
    if isinstance(x, datetime.date):
        return x.isoformat()
    raise TypeError("Unknown type")


@app.route('/send_mail', methods=['POST'])
@jwt_required()
def sendMail():
    data = request.json
    print(data)
    response = send(data)
    print("response ", response)
    return jsonify({'message': 'Mail sent Successfully'}), 200

# ----------------------------------fetch client invoice data for invoice table -------------------------


# ------------------- Delete client invoice data  from data table Module Route End -------------------__

@app.route('/logout', methods=["GET"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


# ------------------- Delete  client invoice data  from data table Module Route End -------------------__
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)