from flask import Flask, render_template, request
import csv
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')


# Function to get the folder path containing attendance CSV files
def get_attendance_folder_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    attendance_folder_path = os.path.join(current_dir, 'C:\\Users\\dell\\Desktop\\AI_COMPET')  # Replace 'path_to_attendance_folder' with the actual folder path
    return attendance_folder_path


# Function to get the list of attendance dates
def get_attendance_dates():
    attendance_folder_path = get_attendance_folder_path()
    attendance_dates = []
    for filename in os.listdir(attendance_folder_path):
        if filename.endswith('.csv'):
            attendance_dates.append(os.path.splitext(filename)[0])
    return attendance_dates


def read_attendance_data(date):
    attendance_folder_path = get_attendance_folder_path()
    attendance_file_path = os.path.join(attendance_folder_path, f'{date}.csv')
    attendance_data = []
    with open(attendance_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        for row in csv_reader:
            # Check if the row has enough elements
            if len(row) >= 3:
                attendance_data.append(row)
            else:
                # If the row doesn't have enough elements, add empty strings for time
                row += [''] * (3 - len(row))
                attendance_data.append(row)
    return attendance_data


# Function to write the attendance data for a specific date to the CSV file
def write_attendance_data(date, attendance_data):
    attendance_folder_path = get_attendance_folder_path()
    attendance_file_path = os.path.join(attendance_folder_path, f'{date}.csv')
    with open(attendance_file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Name', 'Status', 'Time'])
        csv_writer.writerows(attendance_data)

# Function to get the attendance data for all dates and calculate present/absent counts
def get_attendance_data():
    attendance_folder_path = get_attendance_folder_path()
    attendance_data = {}
    for filename in os.listdir(attendance_folder_path):
        if filename.endswith('.csv'):
            date = os.path.splitext(filename)[0]
            attendance_file_path = os.path.join(attendance_folder_path, filename)
            with open(attendance_file_path, 'r') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)
                for row in csv_reader:
                    student_name = row[0]
                    status = row[1]
                    if student_name not in attendance_data:
                        attendance_data[student_name] = {'Present': 0, 'Absent': 0}
                    attendance_data[student_name][status] += 1
    return attendance_data

# Route for the main attendance interface
@app.route('/')
def attendance_interface():
    attendance_dates = get_attendance_dates()
    attendance_data = {}  # Initialize an empty dictionary for attendance data
    for date in attendance_dates:
        attendance_data[date] = read_attendance_data(date)
    return render_template('attendance.html', attendance_dates=attendance_dates, attendance_data=attendance_data)

# Route for a specific attendance date
@app.route('/attendance/<date>')
def attendance_date(date):
    attendance_data = read_attendance_data(date)
    return render_template('attendance_date.html', date=date, attendance_data=attendance_data)


# Route for the student information page
@app.route('/attendance/<date>/student/<student_id>', methods=['GET', 'POST'])
def student_information(date, student_id):
    attendance_data = read_attendance_data(date)
    student_info = None
    for row in attendance_data:
        # print(row)
        if row[0] == student_id:
            student_info = row
            break

    if request.method == 'POST':
        status = request.form.get('status')
        if status:
            time = ""  # Set the time to an empty string
            # time = datetime.now().strftime("%H:%M:%S")
            status = status
            student_info[1] = status
            student_info[2] = time
            write_attendance_data(date, attendance_data)

    return render_template('student.html', student_info=student_info, date=date)

@app.route('/attendance/<date>/student/<student_id>/details')
def student_details(date, student_id):
    attendance_data = read_attendance_data(date)
    student_info = None
    for row in attendance_data:
        if row[0] == student_id:
            student_info = row
            break

    return render_template('student_details.html', student_info=student_info, date=date)


if __name__ == '__main__':
    app.run(debug=True)
