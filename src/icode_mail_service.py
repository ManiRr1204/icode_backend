from datetime import date
from fastapi import FastAPI, HTTPException, Body, Request
import mangum
import pymysql
import stripe
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import yagmail

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["https://arjavatech.github.io", "http://127.0.0.1:5504", "https://arunkavitha1982.github.io/icode","*"], allow_credentials = True, allow_methods=["*"], allow_headers=["https://arjavatech.github.io", "http://127.0.0.1:5504", "https://arunkavitha1982.github.io/icode","*"]
)

sender_mail = "contact@tap-time.com"
app_passcode = "vavx hkdp rfwa wfgc"

# Initialize Stripe with your secret key
stripe.api_key = 'sk_test_51OB8JlIPoM7JHRT2Dz4UeKOU5Snexc9lFpmu2Hp6d0PfCZKCwqWE4NanolwHC5fSd5hbLwsnpHAEJphTByN5c93w00pEpp1vJt'


def connect_to_database():
    try:
        connection = pymysql.connect(
            host="icodetestdb.cxms2oikutcu.us-west-2.rds.amazonaws.com",
            user="admin",
            password="AWSpass01#",
            database="icodetestdb",
            cursorclass=pymysql.cursors.DictCursor 
        )
        return connection
    except pymysql.MySQLError as err:
        print(f"Error connecting to database: {err}")
        return None

@app.get("/test")
def get_test():
   return {"response": "Test get call successfully called"}

@app.get("/report_mail_trigger")
def mail_trigger():
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        company_with_device_dict = {}
        with connection.cursor() as cursor:
            company_detail_sql = 'CALL spGetAllCompanies'
            cursor.execute(company_detail_sql)
            company_result = cursor.fetchall()
            if company_result:
                for company_details in company_result:
                    device_get_sql = 'CALL spGetAllDevices(%s);'
                    cursor.execute(device_get_sql, (company_details['CID']))
                    device_result = cursor.fetchall()

                    if device_result:
                        for device in device_result:
                            if(device["DeviceID"] != "Not Registered"):
                                company_with_device_dict[company_details['CID']] = {"Timezone" : device["TimeZone"],}                       
                                
                                report_type_sql = 'CALL spGetAllCompanyReportType(%s)'
                                cursor.execute(report_type_sql, (company_details['CID'],))
                                report_type_result = cursor.fetchall()

                                if report_type_result:
                                    # Initialize an empty dictionary for the output
                                    consolidated_output = {"Daily": [], "Weekly": [], "Monthly": [], "Bimonthly": [], "Biweekly": []}

                                    # Loop through the list of dictionaries
                                    for item in report_type_result:
                                        if item['IsDailyReportActive'] == 1:
                                            consolidated_output["Daily"].append(item['CompanyReporterEmail'])
                                        if item['IsWeeklyReportActive'] == 1:
                                            consolidated_output["Weekly"].append(item['CompanyReporterEmail'])
                                        if item['IsBiWeeklyReportActive'] == 1:
                                            consolidated_output["Biweekly"].append(item['CompanyReporterEmail'])
                                        if item['IsBiMonthlyReportActive'] == 1:
                                            consolidated_output["Bimonthly"].append(item['CompanyReporterEmail'])
                                        if item['IsMonthlyReportActive'] == 1:
                                            consolidated_output["Monthly"].append(item['CompanyReporterEmail'])

                                    company_with_device_dict[company_details['CID']]["ReportTypeList"] = consolidated_output


                for company_det in company_with_device_dict:  
                    is_monday = is_today_monday()
                    is_month_start_date = is_first_day_of_month()
                    is_second_half_of_month_start_date = is_today_in_second_half_of_month()

                    if( "ReportTypeList" in company_with_device_dict[company_det] and "Daily" in company_with_device_dict[company_det]["ReportTypeList"] and company_with_device_dict[company_det]["ReportTypeList"]["Daily"] != []):
                        today = datetime.now().date()
                        yesterday = today - timedelta(days=1)
                        sql = "CALL spGetEmployeeDailyReport(%s, %s);"
                        cursor.execute(sql, (company_det , yesterday,))  
                        daily_report = cursor.fetchall()
                        if daily_report:
                            message = create_daily_report_html_table(daily_report, yesterday)
                            to_address = company_with_device_dict[company_det]["ReportTypeList"]["Daily"]
                            sender = sender_mail
                            app_password = app_passcode
                            subject = f'{yesterday} Report Data'

                            # Initialize Yagmail with the sender's Gmail credentials
                            yag = yagmail.SMTP(user=sender, password=app_password)

                            # Sending the email
                            yag.send(to= to_address, subject=subject, contents=message, )


                    if(is_monday):
                        if("ReportTypeList" in company_with_device_dict[company_det] and "Weekly" in company_with_device_dict[company_det]["ReportTypeList"] and company_with_device_dict[company_det]["ReportTypeList"]["Weekly"] != []):
                            
                            dateRange = get_last_week_date_range()

                            report_type_sql = 'CALL spGetCompanyDailyReportFromDateRange(%s, %s,%s)'
                            cursor.execute(report_type_sql, (company_details['CID'], dateRange["startRange"], dateRange["endRange"]))
                            report_result = cursor.fetchall()
                            
                            if(report_result):
                                message = create_salaried_report_html_table( calculate_total_time_worked(report_result) , "Weekly", dateRange["startRange"], dateRange["endRange"])
                                to_address = company_with_device_dict[company_det]["ReportTypeList"]["Weekly"]
                                
                                sender = sender_mail
                                app_password = app_passcode
                                subject = f'Weekly Report Data - {dateRange["startRange"]} to {dateRange["endRange"]}'

                                

                                # Initialize Yagmail with the sender's Gmail credentials
                                yag = yagmail.SMTP(user=sender, password=app_password)

                                # Sending the email
                                yag.send(to= to_address, subject=subject, contents=message, )


                        if("ReportTypeList" in company_with_device_dict[company_det] and "Biweekly" in company_with_device_dict[company_det]["ReportTypeList"] and company_with_device_dict[company_det]["ReportTypeList"]["Biweekly"] != []):
                            dateRange = get_last_two_weeks_date_range()

                            report_type_sql = 'CALL spGetCompanyDailyReportFromDateRange(%s, %s,%s)'
                            cursor.execute(report_type_sql, (company_details['CID'], dateRange["startRange"], dateRange["endRange"]))
                            report_result = cursor.fetchall()

                            if(report_result):
                                message = create_salaried_report_html_table( calculate_total_time_worked(report_result) , "Biweekly", dateRange["startRange"], dateRange["endRange"])
                                to_address = company_with_device_dict[company_det]["ReportTypeList"]["Biweekly"]
                                
                                sender = sender_mail
                                app_password = app_passcode
                                subject = f'Biweekly Report Data - {dateRange["startRange"]} to {dateRange["endRange"]}'

                                

                                # Initialize Yagmail with the sender's Gmail credentials
                                yag = yagmail.SMTP(user=sender, password=app_password)

                                # Sending the email
                                yag.send(to= to_address, subject=subject, contents=message, )
                        

                    if(is_month_start_date):
                        if("ReportTypeList" in company_with_device_dict[company_det] and "Bimonthly" in company_with_device_dict[company_det]["ReportTypeList"] and company_with_device_dict[company_det]["ReportTypeList"]["Bimonthly"] != []):
                            dateRange = get_bimonthly_start_and_end_dates()

                            report_type_sql = 'CALL spGetCompanyDailyReportFromDateRange(%s, %s,%s)'
                            cursor.execute(report_type_sql, (company_details['CID'], dateRange["startRange"], dateRange["endRange"]))
                            report_result = cursor.fetchall()
                            if(report_result):
                                message = create_salaried_report_html_table( calculate_total_time_worked(report_result) , "Bimonthly", dateRange["startRange"], dateRange["endRange"])
                                to_address = company_with_device_dict[company_det]["ReportTypeList"]["Bimonthly"]
                                
                                sender = sender_mail
                                app_password = app_passcode
                                subject = f'Bimonthly Report Data - {dateRange["startRange"]} to {dateRange["endRange"]}'

                                

                                # Initialize Yagmail with the sender's Gmail credentials
                                yag = yagmail.SMTP(user=sender, password=app_password)

                                # Sending the email
                                yag.send(to= to_address, subject=subject, contents=message, )

                        if("ReportTypeList" in company_with_device_dict[company_det] and "Monthly" in company_with_device_dict[company_det]["ReportTypeList"] and company_with_device_dict[company_det]["ReportTypeList"]["Monthly"] != []):
                            dateRange = get_last_month_start_and_end_dates()

                            report_type_sql = 'CALL spGetCompanyDailyReportFromDateRange(%s, %s,%s)'
                            cursor.execute(report_type_sql, (company_details['CID'], dateRange["startRange"], dateRange["endRange"]))
                            report_result = cursor.fetchall()
                            if(report_result):
                                message = create_salaried_report_html_table( calculate_total_time_worked(report_result) , "Monthly", dateRange["startRange"], dateRange["endRange"])
                                to_address = company_with_device_dict[company_det]["ReportTypeList"]["Monthly"]
                                
                                sender = sender_mail
                                app_password = app_passcode
                                subject = f'Monthly Report Data - {dateRange["startRange"]} to {dateRange["endRange"]}'

                                

                                # Initialize Yagmail with the sender's Gmail credentials
                                yag = yagmail.SMTP(user=sender, password=app_password)

                                # Sending the email
                                yag.send(to= to_address, subject=subject, contents=message, )

                    if(is_second_half_of_month_start_date ):
                        if("ReportTypeList" in company_with_device_dict[company_det] and "Bimonthly" in company_with_device_dict[company_det]["ReportTypeList"] and company_with_device_dict[company_det]["ReportTypeList"]["Bimonthly"] != []):
                            dateRange = get_bimonthly_start_and_end_dates()

                            report_type_sql = 'CALL spGetCompanyDailyReportFromDateRange(%s, %s,%s)'
                            cursor.execute(report_type_sql, (company_details['CID'], dateRange["startRange"], dateRange["endRange"]))
                            report_result = cursor.fetchall()
                            if(report_result):
                                message = create_salaried_report_html_table( calculate_total_time_worked(report_result) , "Bimonthly", dateRange["startRange"], dateRange["endRange"])
                                to_address = company_with_device_dict[company_det]["ReportTypeList"]["Bimonthly"]
                                
                                sender = sender_mail
                                app_password = app_passcode
                                subject = f'Bimonthly Report Data - {dateRange["startRange"]} to {dateRange["endRange"]}'

                                # Initialize Yagmail with the sender's Gmail credentials
                                yag = yagmail.SMTP(user=sender, password=app_password)

                                # Sending the email
                                yag.send(to= to_address, subject=subject, contents=message, )
       
                return {"message" : "Output Got it!!!!!"}
            else:
                return {"message": "No one companies is registered in our app!!"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


def get_last_week_date_range(today=None):
    if today is None:
        today = datetime.now().date()

    # Monday of the current week  
    start_of_week = today - timedelta(days=today.weekday())
  
    # Last Monday
    last_monday = start_of_week - timedelta(weeks=1)
  
    # Last Sunday
    last_sunday = last_monday + timedelta(days=6)
  
    return {
        "startRange": last_monday.strftime("%Y-%m-%d"),
        "endRange": last_sunday.strftime("%Y-%m-%d")
    }

def get_last_two_weeks_date_range(today=None):
    if today is None:
        today = datetime.now().date()

    # Monday of the current week
    start_of_week = today - timedelta(days=today.weekday())
  
    # Start of the last two weeks (Monday two weeks ago)
    start_date = start_of_week - timedelta(weeks=2)
  
    # End of the last two weeks (Sunday two weeks later)
    end_date = start_date + timedelta(days=13)
  
    return {
        "startRange": start_date.strftime("%Y-%m-%d"),
        "endRange": end_date.strftime("%Y-%m-%d")
    }

def get_bimonthly_start_and_end_dates():
    today = datetime.now()   

    # Calculate the number of days in the current month
    days_in_month = (datetime(today.year, today.month + 1, 1) - timedelta(days=1)).day
    mid_month_day = (days_in_month + 1) // 2

    if today.day >= mid_month_day:
        # Second half of the month, so return the first half
        start_date = datetime(today.year, today.month, 1)
        end_date = datetime(today.year, today.month, mid_month_day - 1)
    else:
        # First half of the month, so return the second half of the previous month
        previous_month = datetime(today.year, today.month - 1, 1)
        days_in_prev_month = (datetime(previous_month.year, previous_month.month + 1, 1) - timedelta(days=1)).day
        start_date = datetime(previous_month.year, previous_month.month, (days_in_prev_month + 1) // 2)
        end_date = datetime(previous_month.year, previous_month.month, days_in_prev_month)

    return {
        'startRange': start_date.strftime('%Y-%m-%d'),
        'endRange': end_date.strftime('%Y-%m-%d')
    }

def get_last_month_start_and_end_dates(today=None):
    if today is None:
        today = datetime.now().date()

    # Start date of the last full month
    start_date_last_month = datetime(today.year, today.month - 1, 1)
  
    # End date of the last full month
    end_date_last_month = datetime(today.year, today.month, 1) - timedelta(days=1)
  
    return {
        "startRange": start_date_last_month.strftime("%Y-%m-%d"),
        "endRange": end_date_last_month.strftime("%Y-%m-%d")
    }

def is_today_monday():
    now = datetime.now()
    
    return now.weekday() == 0

def is_first_day_of_month():
    now = datetime.now()
    
    return now.day == 1

def is_today_in_second_half_of_month():
    today = datetime.now()

    next_month = today.replace(day=28) + timedelta(days=4)  # Move to next month
    last_day_of_month = next_month - timedelta(days=next_month.day)
    days_in_month = last_day_of_month.day
    
    # Determine the start date of the second half of the month
    if days_in_month in [28, 29]:
        second_half_start = 15
    else:  # 30 or 31 days
        second_half_start = 16

    second_half_start_date = today.replace(day=second_half_start, hour=0, minute=0, second=0, microsecond=0)
    
    return today >= second_half_start_date


def format_timedelta(td):
   # Convert timedelta to total minutes
    total_minutes = int(td.total_seconds() // 60)
    hours, minutes = divmod(total_minutes, 60)
    # Format as HH:MM
    return f"{hours:02}:{minutes:02}"

def consolitaded_result(report_result):
    print(report_result)
    formatted_result = [
        {
            # 'EmpID': item['EmpID'],
            # 'FullName': item['FullName'],
            # 'TotalTimeWorked': format_timedelta(item['TotalTimeWorked'])
            'EmpID': item['Pin'],
            'FullName': item['Name'],
            'TotalTimeWorked': item['TimeWorked']
        }
        for item in report_result
    ]

    return formatted_result


def create_salaried_report_html_table(data, reportType, startDate, endDate):
    html = f"<html><body style='text-align: center;'><h4>{reportType} Report - {startDate} to {endDate}</h4><table border='1' cellpadding='5' cellspacing='0' style='margin: 0 auto;'>"
    # Create table header
    html += "<tr><th style='text-align: center;'>Name</th><th>Pin</th><th>Total Worked Hours (HH:MM)</th></tr>"
    
    # index = 1

    # Add table rows
    for key, value in data.items():
        html += f"<tr><td style='text-align: center;'>{data[key]['name']}</td><td>{key}</td><td style='text-align: center;'>{data[key]['total_hours_worked']}</td></tr>"
        # index = index + 1
    html += "</table></body></html>"
    return html

def create_daily_report_html_table(data, date):
    html = f"<html><body style='text-align: center;'><h4>{date} Report</h4><table border='1' cellpadding='5' cellspacing='0' style='margin: 0 auto;'>"
    # Create table header
    html += "<tr><th style='text-align: center;'>S.No</th><th>Employee ID</th><th>Employee Name</th><th>Class Type</th><th>Check-In Time</th><th>Check-Out Time</th><th>TimeWorked (HH:MM)</th></tr>"
    # Add table rows
    index =1
    for item in data:
        html += f"<tr><td style='text-align: center;'>{index}</td><td style='text-align: center;'>{item['Pin']}</td><td>{item['Name']}</td><td style='text-align: center;'>{item['Type']}</td><td>{item['CheckInTime']}</td><td>{item['CheckOutTime']}</td><td style='text-align: center;'>{item['TimeWorked']}</td></tr>"
        index = index+1
    html += "</table></body></html>"
    return html

# Functions to convert time and calculate totals

def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def minutes_to_time(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}:{str(mins).zfill(2)}"

def calculate_total_time_worked(data):
    employee_times = {}

    for entry in data:
        name = entry.get('Name')
        pin = entry.get('Pin')
        time_worked = entry.get('TimeWorked')

        if time_worked:
            minutes_worked = time_to_minutes(time_worked)

            if pin not in employee_times:
                employee_times[pin] = {'name': name, 'total_minutes': 0}

            employee_times[pin]['total_minutes'] += minutes_worked

    # Convert total minutes to time string
    for pin, details in employee_times.items():
        details['total_hours_worked'] = minutes_to_time(details['total_minutes'])

    return employee_times

handler=mangum.Mangum(app)