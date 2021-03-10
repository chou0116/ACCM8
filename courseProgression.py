from flask import Blueprint, render_template
import MySQLdb as mdb1
import sys

courseProgressionBlueprint = Blueprint("courseProgression", __name__, static_folder="static", template_folder="template")

@courseProgressionBlueprint.route("/administrator/courseprogression")
def courseProgression():
    allCoreCourses = readCoreCourses()

    for course in allCoreCourses:

        # Create new columns
        course['prerequisite_1'] = ""
        course['prerequisite_2'] = ""
        course['prerequisite_3'] = ""
        course['prerequisite_4'] = ""
        course['prerequisite_5'] = ""

        prerequisiteColumns = ['prerequisite_1', 'prerequisite_2', 'prerequisite_3', 'prerequisite_4', 'prerequisite_5']

        # fetch it's prerequisites
        coursePrerequisites = fetchPrerequisites(course['core_course_num'])

        prerequisites = []

        if len(coursePrerequisites) > 0:
            # go through the dictionary of queried prerequisites
            for singlePrerequisite in coursePrerequisites:
                prerequisites.append(singlePrerequisite['prerequisite_num'])

        for index in range(0, 5):
            if 0 <= index < len(prerequisites):
                course[prerequisiteColumns[index]] = prerequisites[index]

    return render_template("courseProgression.html", allCoreCourses=allCoreCourses)




def createCursor():
    try:
        con = mdb1.connect(host='localhost', user='root', password='root', database='accm', port=3306)

    except mdb1.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    return con


def fetchPrerequisites(courseNum):
    con = createCursor()
    cursor = con.cursor()

    query = f"""select * from core_course_prerequisites where core_course_num = '{courseNum}' ;"""

    # execute query
    cursor.execute(query)
    rows = cursor.fetchall()

    # Write all query rows into dictionary with column headers
    names = [d[0] for d in cursor.description]
    coursePrerequisites = [dict(zip(names, row)) for row in rows]

    return coursePrerequisites



def readCoreCourses():
    con = createCursor()
    cursor = con.cursor()

    query = f"""SELECT * FROM core_course_flowchart order by sequence;"""

    # execute query
    cursor.execute(query)
    rows = cursor.fetchall()

    # Write all query rows into dictionary with column headers
    names = [d[0] for d in cursor.description]
    allCoreCourses = [dict(zip(names, row)) for row in rows]

    con.close()

    return allCoreCourses




