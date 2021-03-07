from flask import Blueprint, render_template, request, jsonify
import sys
import MySQLdb as mdb1

programsBlueprint = Blueprint("programs", __name__, static_folder="static", template_folder="template")


@programsBlueprint.route("/administrator/programs", methods=["POST", "GET"])
def programs():
    programs = readPrograms()

    parameters = request.form.to_dict()

    _list = list(parameters.keys())

    buttonType = ""
    inputFieldName = ""

    if len(_list) > 0:
        buttonName = _list[1]
        inputFieldName = _list[0]
        buttonType = buttonName.split('_')[0]

    if request.method == 'POST' and 'submitBtn' in request.form:
        programName = request.form['programName']
        programCode = request.form['programCode']

        if checkIfProgramOfferedExists(programCode):
            message = "The specified program already exists"
            return render_template("programs.html", programs=programs, message=message, success=False, failure=True)

        createProgramOfferingQuery(programCode, programName)
        message = "The program was added successfully"
        programs = readPrograms()  # read the new list of programs from database again

        return render_template("programs.html", programs=programs, message=message, success=True, failure=False)

    elif request.method == 'POST' and buttonType == "deleteBtn":

        programCode = request.form[inputFieldName]

        if checkIfProgramVersionsExist(programCode):
            message = "The program has other data associated with it and cannot be deleted"
            return render_template("programs.html", programs=programs, message=message, success=False, failure=True)

        deleteProgramOfferedQuery(programCode)

        programs = readPrograms()  # read the new list of programs from database again

        message = "Program was deleted successfully"
        return render_template("programs.html", programs=programs, message=message, success=True, failure=False)

    else:
        return render_template("programs.html", programs=programs, message="", success=False, failure=False)



def readPrograms():
    con = createCursor()
    query = f"""SELECT * FROM accm.program_offered;"""

    cursor = con.cursor()
    cursor.execute(query)

    names = [d[0] for d in cursor.description]
    programs = [dict(zip(names, row)) for row in cursor.fetchall()]

    con.close()

    return programs




def createCursor():
    try:
        con = mdb1.connect(host='localhost', user='root', password='5Iodine3', database='accm', port=3306)


    except mdb1.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    return con




def createProgramOfferingQuery(programCode, programName):

    con = createCursor()
    cursor = con.cursor()
    query = f"""INSERT INTO program_offered(program_code, program_name) 
            VALUES('{programCode}','{programName}');"""

    cursor.execute(query)
    con.commit()
    con.close()





def deleteProgramOfferedQuery(programCode):
    con = createCursor()
    query = f"DELETE FROM program_offered WHERE program_code = '{programCode}' ;"
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    con.close()


def checkIfProgramOfferedExists(programCode):

    con = createCursor()
    query = f"SELECT COUNT(*) FROM program_offered WHERE program_code='{programCode}';"
    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]
    con.close()


    if count == 1:
        return True

    return False


def checkIfProgramVersionsExist(programCode):

    con = createCursor()
    query = f"SELECT COUNT(*) FROM program WHERE code='{programCode}';"
    cursor = con.cursor()
    cursor.execute(query)
    rowCount = cursor.fetchone()
    count = rowCount[0]
    con.close()


    if count > 1:
        return True

    return False

