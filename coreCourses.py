from flask import Blueprint, render_template, request, session, redirect, url_for
import sys
import MySQLdb as mdb1
from flask_mysqldb import MySQL
from app import app
import copy

coreCoursesBlueprint = Blueprint("coreCourses", __name__, static_folder="static", template_folder="template")


@coreCoursesBlueprint.route("/administrator/corecourses", methods=['GET','POST'])
def coreCourses():
    global con

    parameters = request.form.to_dict()

    print(parameters)

    allCoreCourses = readCourses()

    if request.method == 'POST' and "addBtn" in parameters:
        courseCode = parameters['courseCode'].upper()
        courseTitle = parameters['courseTitle']
        addCourse(courseCode, courseTitle)
        allCoreCourses = readCourses()
        message = "The course was added successfully"
        return render_template("coreCourses.html", allCoreCourses=allCoreCourses, message=message, success=True, failure=False)

    if request.method == 'POST' and "confirmDeleteBtn" in parameters:
        courseCode = parameters['courseDeleteInput'].upper()
        deleteCourse(courseCode)
        allCoreCourses = readCourses()
        message = "The course was deleted successfully"
        return render_template("coreCourses.html", allCoreCourses=allCoreCourses, message=message, success=True, failure=False)

    if request.method == 'POST' and "confirmEditBtn" in parameters:
        oldCourseCode = parameters['oldCourseCode']
        courseCode = parameters['editCourseCodeInput'].upper()
        courseTitle = parameters['editCourseTitleInput']
        updateCourse(oldCourseCode, courseCode, courseTitle)
        allCoreCourses = readCourses()
        message = "The course information was successfully updated"
        return render_template("coreCourses.html", allCoreCourses=allCoreCourses, message=message, success=True,
                               failure=False)


    # confirmEditBtn

    return render_template("coreCourses.html", allCoreCourses=allCoreCourses, success=False, failure=False)


def createConnection():

    mysql = MySQL(app)

    try:
        con = mdb1.connect(host=mysql.app.config['MYSQL_HOST'],
                           user=mysql.app.config['MYSQL_USER'],
                           password=mysql.app.config['MYSQL_PASSWORD'],
                           #database=mysql.app.config['MYSQL_DB'],
                           database="accm_test",
                           port=mysql.app.config['MYSQL_PORT'])


    except mdb1.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    return con


def readCourses():
    global con

    con = createConnection()

    cursor = con.cursor()

    # >>> fetch all core courses
    query = f"""SELECT * FROM core_course;"""
    cursor.execute(query)
    rows = cursor.fetchall()

    # Write all query rows into dictionary with column headers
    names = [d[0] for d in cursor.description]
    allCoreCourses = [dict(zip(names, row)) for row in rows]

    return allCoreCourses


def addCourse(courseCode, courseTitle):
    global con

    cursor = con.cursor()

    # >>> fetch all core courses
    query = f"""INSERT INTO core_course(core_course_num, title) VALUES('{courseCode}','{courseTitle}');"""
    cursor.execute(query)
    con.commit()


def deleteCourse(courseCode):
    global con

    cursor = con.cursor()

    # >>> fetch all core courses
    query = f"""DELETE FROM core_course
                WHERE core_course_num = '{courseCode}';"""
    cursor.execute(query)
    con.commit()


def updateCourse(oldCourseCode, courseCode, courseTitle):
    global con

    cursor = con.cursor()

    query = f"""UPDATE core_course
            SET core_course_num = '{courseCode}', title = '{courseTitle}'
            WHERE core_course_num = '{oldCourseCode}';"""

    cursor.execute(query)
    con.commit()

