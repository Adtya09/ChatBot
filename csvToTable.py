ques=input("Enter Question\n")
if(ques.strip()!=""):
    filein = open("C:\\Users\\AmitJ\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\chatterbot_corpus\\data\\siya\\input\\inputCsvData.csv", "r")
    fileout = open("C:\\Users\\AmitJ\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\chatterbot_corpus\\data\\siya\\training_files\\table_"+ques[0:20]+".yml", "w",encoding="utf-8")
    data = filein.readlines()

    print("\n")
    beginConv="categories:\n- Induction Training\nconversations:\n- - "+ques
    fileout.write(beginConv)

    table = "\n  - <table>\n"

    # Create the table's column headers
    header = data[0].split(",")
    table += "    <tr>\n"
    for column in header:
        table += "    <th>{0}</th>\n".format(column.strip())
    table += "    </tr>\n"

    # Create the table's row data
    for line in data[1:]:
        row = line.split(",")
        table += "    <tr>\n"
        for column in row:
            table += "    <td>{0}</td>\n".format(column.strip())
        table += "    </tr>\n"

    table += "    </table>"

    fileout.writelines(table)
    fileout.close()
    filein.close()
