#/usr/bin/env python3
# _*_ coding: utf-8 _*_
import os,sys,re
from core import dbauth
from core import dbquerytime

def initdatabase(sql_cmd):    #选择数据库，初始化数据库、表
    sql_cmd2 = sql_cmd.lower()
    use_str_index = sql_cmd2.find("use")
    if use_str_index != -1:    #判断关键字是否正确
        use_str_position = len("use") + use_str_index
        use_dbname_str = sql_cmd2[use_str_position:]
        use_dbname = use_dbname_str.strip(";| ")
        if use_dbname in dbauth.DATABASES:    #判断数据库名是否存在
            print("Database changed")
            dbauth.USE_DB['name'] = use_dbname
            return True
        else :
            print("Unknown database '%s'" % use_dbname)
    else:
        print("You have an error in your SQL syntax.")

@dbquerytime.sql_querytime
def show(sql_cmd):    #查询系统中已存在的数据库和表
    #show databases
    sql_cmd2 = sql_cmd.lower()
    show_str_index = sql_cmd2.find("show")
    if show_str_index != -1:    #判断关键字是否正确
        show_str_position = len("show") + show_str_index
        show_object_str = sql_cmd2[show_str_position:]
        show_object = show_object_str.strip(";| ")

        view_query_table_first_line = "+--------------------+"
        view_query_table_first_line_len = len(view_query_table_first_line)

        if show_object == "databases":
            ltitle = "| Database"
            ltilte_len = len(ltitle)
            rtitle = " " * (view_query_table_first_line_len - ltilte_len - 1)
            title = ltitle + rtitle + "|"
            view_query_table_title = view_query_table_first_line + "\n" + title + "\n" + view_query_table_first_line
            print(view_query_table_title)

            view_query_object_list = []
            for database in dbauth.DATABASES:
                ldatabase_str = "| {0}".format(database)
                ldatabase_str_len = len(ldatabase_str)
                rdatabase_str = " " * (view_query_table_first_line_len - ldatabase_str_len -1) + "|"
                database = ldatabase_str + rdatabase_str
                print(database)
                view_query_object_list.append(database)
            print(view_query_table_first_line)
            print("%d rows in set" % len(dbauth.DATABASES), end=' ')
            return True

        if show_object == "tables":
            if dbauth.USE_DB['name'] != None:
                ltitle = "| Tables"
                ltilte_len = len(ltitle)
                rtitle = " " * (view_query_table_first_line_len - ltilte_len - 1)
                title = ltitle + rtitle + "|"
                view_query_table_title = view_query_table_first_line + "\n" + title + "\n" + view_query_table_first_line
                print(view_query_table_title)

                view_query_object_list = []
                for table in dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']].keys():
                    ltable_str = "| {0}".format(table)
                    ltable_str_len = len(ltable_str)
                    rtable_str = " " * (view_query_table_first_line_len - ltable_str_len - 1) + "|"
                    table = ltable_str + rtable_str
                    print(table)
                    view_query_object_list.append(table)
                print(view_query_table_first_line)
                print("%d rows in set" % len(dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']]), end=' ')
                return True
            else:
                print("ERROR: No database selected")

@dbauth.usedb_auth
@dbquerytime.sql_querytime
def select(sql_cmd):    #处理SELECT查询语句
    #select * from staff_table;
    #select * from staff_table where enroll_date like "2013";
    sql_cmd2 = sql_cmd.lower()
    view_table_first_line = "+----------------"
    view_table_first_line_len = len(view_table_first_line) - 1

    select_str_index = sql_cmd2.find("select")
    from_str_index = sql_cmd2.find("from")
    where_str_index = sql_cmd2.find("where")

    if select_str_index != -1 and from_str_index != -1:
        select_str_position = len("select") + select_str_index
        from_str_position = len("from") + from_str_index
        query_column_str = sql_cmd[select_str_position:from_str_index].strip()
        show_column_list = query_column_str.split(",")

        def table_title_view(query_column_list,table_first_line):
            column_name_str_list = []
            for column_name in query_column_list:
                column_name_str = column_name.center(view_table_first_line_len, " ")
                column_name_str = "|{0}".format(column_name_str)
                column_name_str_list.append(column_name_str)
            column_name_str_list_len = len(column_name_str_list)
            view_table_first_line = str(table_first_line) * column_name_str_list_len + "+"
            column_name_str_line = "".join(column_name_str_list) + "|"
            column_name_table_title = view_table_first_line + "\n" + column_name_str_line + "\n" + view_table_first_line
            return column_name_table_title

        if where_str_index == -1:
            compare_column_str = "ALL"
            table_name = sql_cmd[from_str_position:].strip(";| ")
            if table_name in dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']]:
                table = os.path.join(dbauth.datadir, dbauth.USE_DB['name'], table_name)
                table_column_name = dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']][table_name][0]
                if query_column_str == '*':
                    show_column_list = table_column_name
                table_title_view_title = table_title_view(show_column_list,view_table_first_line)
                print(table_title_view_title)

                show_column_list_len = len(show_column_list)
                if compare_column_str == "ALL":
                    with open(table, "r") as table_info:
                        rows = 0
                        for line in table_info:
                            info_list = line.strip().split(",")
                            info_dict = dict(zip(table_column_name,info_list))
                            rows += 1
                            show_column = []
                            for column in show_column_list:
                                column = info_dict[column]
                                column = column.center(view_table_first_line_len, " ")
                                column = "|{0}".format(column)
                                show_column.append(column)
                            show_column_line = "".join(show_column) + "|"
                            print(show_column_line)
                        print(view_table_first_line * show_column_list_len + "+")
                        print("%d rows in set" % rows, end=' ')
                        return True
            else:
                print("Table '%s' doesn't exist" % table_name)

        if where_str_index != -1:
            where_str_position = len("where") + where_str_index
            compare_column_str = sql_cmd[where_str_position:].strip(";| ")
            compare_column_str_list = compare_column_str.split()

            try:
                compare_column, compare_method, compare_value = compare_column_str_list
                compare_column = compare_column_str_list[0]
                compare_method = compare_column_str_list[1]
                compare_value = compare_column_str_list[2].strip("'|\"")
            except ValueError as diag:
                diag = "ERROR (S002): You have an error in your SQL syntax."
                print(diag)
            else:
                table_name = sql_cmd[from_str_position:where_str_index].strip()
                if table_name in dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']]:
                    table = os.path.join(dbauth.datadir, dbauth.USE_DB['name'], table_name)
                    table_column_name = dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']][table_name][0]
                    if query_column_str == '*':
                        show_column_list = table_column_name
                    table_title_view_title = table_title_view(show_column_list,view_table_first_line)
                    print(table_title_view_title)

                    def show_compare_value(match_method):
                        match_result = True
                        def match():
                            show_column = []
                            for column in show_column_list:
                                column = info_dict[column]
                                column = column.center(view_table_first_line_len, " ")
                                column = "|{0}".format(column)
                                show_column.append(column)
                            show_column_line = "".join(show_column) + "|"
                            print(show_column_line)

                        if match_method == ">":
                            if int(info_dict[compare_column]) > int(compare_value):
                                match_column = match()
                                return match_result

                        if match_method == "<":
                            if int(info_dict[compare_column]) < int(compare_value):
                                match_column = match()
                                return match_result

                        if match_method == "=":
                            if str(info_dict[compare_column]) == str(compare_value):
                                match_column = match()
                                return match_result

                        if match_method == "like":
                            if compare_value.strip("\"").upper() in info_dict[compare_column].upper():
                                match_column = match()
                                return match_result

                    show_column_list_len = len(show_column_list)
                    with open(table, "r") as table_info:
                        rows = 0
                        for line in table_info:
                            info_list = line.strip().split(",")
                            info_dict = dict(zip(table_column_name, info_list))
                            match_result = show_compare_value(compare_method)
                            if match_result == True:
                                rows += 1
                        print(view_table_first_line * show_column_list_len + "+")
                        print("%d rows in set" % rows, end=' ')
                        return True

                else:
                    print("Table '%s' doesn't exist" % table_name)

    else:
        print("ERROR (S001): You have an error in your SQL syntax.")


@dbauth.usedb_auth
@dbquerytime.sql_querytime
def insert(sql_cmd):    #处理INSERT插入数据语句
    #INSERT INTO staff_table VALUES("Jack Ma",23,13012546524,"IT","2014-07-22");
    #日期格式：re.search(r'(\d){4}-([0][1-9]|[1][0-2])-([0][1-9]|[1][0-9]|[2][0-9]|[3][0-1])', '2009-10-20').group()
    sql_cmd2 = sql_cmd.lower()
    into_str_index = sql_cmd2.find("into")
    value_str_index = sql_cmd2.find("values")
    if into_str_index == -1 or value_str_index == -1:
        print("ERROR (I001): You have an error in your SQL syntax.")
    else:
        into_str_position = len("into") + into_str_index
        value_str_position = len("values") + value_str_index
        try:
            insert_str_line = sql_cmd[value_str_position:].strip(";")
            insert_str_list = insert_str_line.strip("(|)").split(",")

            table_name_str = sql_cmd[into_str_position:value_str_index]
        except IndexError as diag:
            diag = "ERROR (I002): You have an error in your SQL syntax."
            print(diag)
        else:
            table_name = table_name_str.strip()
            insert_srt_values_len = len(insert_str_list)
            if table_name in dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']]:
                table = os.path.join(dbauth.datadir, dbauth.USE_DB['name'], table_name)
                table_column_name = dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']][table_name][0]
                primary_key_name = dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']][table_name][1]["primary_key"]

                table_column_name_len = len(table_column_name)
                if insert_srt_values_len + 1 == table_column_name_len:
                    name_col = insert_str_list[0].strip("\'|\"")
                    age_col = insert_str_list[1]
                    phone_col = insert_str_list[2]
                    dept_col = insert_str_list[3].strip("\'|\"")
                    enroll_date_col = insert_str_list[4].strip("\'|\"")
                    try:
                        age_col = int(age_col)
                        phone_col = int(phone_col)
                        enroll_date_col = re.search(r'(\d){4}-([0][1-9]|[1][0-2])-([0][1-9]|[1][0-9]|[2][0-9]|[3][0-1])', enroll_date_col).group()
                    except (ValueError,TypeError,AttributeError) as diag:
                        diag = "ERROR (I003): You have an error in your SQL syntax."
                        print(diag)
                    else:
                        with open(table, 'r') as employee_info:
                            employee_info_data = employee_info.readlines()

                            id_index = int(employee_info_data[-1][0])
                            id_col = id_index + 1
                            insert_new_line = "\n{0},{1},{2},{3},{4},{5}".format(id_col,name_col,age_col,phone_col,dept_col,enroll_date_col)
                            insert_str_list.insert(0,id_col)
                            insert_str_dict = dict(zip(table_column_name, insert_str_list))
                            primary_key = insert_str_dict[primary_key_name]
                            p_k = ""
                            for line in employee_info_data:
                                if str(primary_key) in line:
                                    p_k = "exist"
                                    break
                            if p_k == "exist":
                                print("ERROR: the 'phone' column is the primary key.")
                            else:
                                with open(table, 'a+') as employee_info2:
                                    employee_info2.write(insert_new_line)
                                    print("Query OK, 1 row affected",end=' ')
                                    return True
                else:
                    print("ERROR: Column unmatched")
            else:
                print("Table '%s' doesn't exist" % table_name)


@dbauth.usedb_auth
@dbquerytime.sql_querytime
def update(sql_cmd):    #处理UPDATE更新数据语句
    #UPDATE staff_table SET dept="Market",phone=13532016528 WHERE name="Jack Wang";
    sql_cmd2 = sql_cmd.lower()
    update_str_index = sql_cmd2.find("update")
    set_str_index = sql_cmd2.find("set")
    where_str_index = sql_cmd2.find("where")

    if set_str_index == -1 or where_str_index == -1 or update_str_index == -1:
        print("ERROR (U001): You have an error in your SQL syntax.")
    else:
        set_str_position = len("set") + set_str_index
        where_str_position = len("where") + where_str_index
        update_str_position = len("update") + update_str_index

        try:
            update_column_str = sql_cmd[set_str_position:where_str_index].strip()
            table_name_str = sql_cmd[update_str_position:set_str_index]
            compare_column_str = sql_cmd[where_str_position:].strip(";").strip()
        except IndexError as diag:
            diag = "ERROR (U002): You have an error in your SQL syntax."
            print(diag)
        else:
            table_name = table_name_str.strip()
            compare_column_str_list = compare_column_str.split("=")
            update_column_str_list = update_column_str.split(",")
            compare_column_name = compare_column_str_list[0].strip("\'|\"| ")
            compare_column_value = compare_column_str_list[1].strip("\'|\"| ")

            if table_name in dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']]:
                table = os.path.join(dbauth.datadir, dbauth.USE_DB['name'], table_name)
                table_column_name = dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']][table_name][0]
                if compare_column_name in table_column_name:
                    update_column_str_dict = {}
                    column_name = True
                    for update_column in update_column_str_list:
                        name = update_column.split("=")[0]
                        value = update_column.split("=")[1]
                        if name not in table_column_name:
                            print("ERROR: Column '%s' doesn't exist" % name)
                            column_name = False
                            break
                        else:
                            update_column_str_dict[name] = value

                    if column_name == True:
                        table_info = open(table, "r")
                        table_txns = table_info.readlines()
                        table_info.close()
                        table_info2 = open(table, "w+")
                        for line in table_txns:
                            infotable_list = line.strip().split(",")
                            infotable_dict = dict(zip(table_column_name,infotable_list))
                            infotable_column_value = infotable_dict.get(compare_column_name).strip()

                            if compare_column_value == infotable_column_value:
                                for column in update_column_str_dict:
                                    update_value = update_column_str_dict[column].strip("\"")
                                    old_column = infotable_dict[column]
                                    new_column = update_value
                                    line = re.sub(old_column,new_column, line)
                            table_info2.write(line)
                        table_info2.close()
                        print("Query OK, 1 row affected",end=" ")
                        return True
                else:
                    print("ERROR: Column '%s' doesn't exist" % compare_column_name)
            else:
                print("Table '%s' doesn't exist" % table_name)


@dbauth.usedb_auth
@dbquerytime.sql_querytime
def delete(sql_cmd):    #处理DELETE删除数据语句
    #DELETE FROM staff_table WHERE staff_id=5;
    sql_cmd2 = sql_cmd.lower()
    where_str_index = sql_cmd2.find("where")
    from_str_index = sql_cmd2.find("from")
    if where_str_index == -1 or from_str_index == -1:
        print("ERROR (D001): You have an error in your SQL syntax.")
    else:
        from_str_position = len("from") + from_str_index
        where_str_position = len("where") + where_str_index
        try:
            compare_column_str = sql_cmd2[where_str_position:].strip(";| ")
            compare_column_str_list = compare_column_str.split("=")
            table_name_str = sql_cmd[from_str_position:where_str_index]
            compare_column_name = compare_column_str_list[0]
            compare_column_value = compare_column_str_list[1]
        except (IndexError,TypeError) as diag:
            diag = "ERROR (D002): You have an error in your SQL syntax."
            print(diag)
        else:
            table_name = table_name_str.strip()
            if table_name in dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']]:
                table = os.path.join(dbauth.datadir, dbauth.USE_DB['name'], table_name)
                table_column_name = dbauth.DB_INFO_INDEX[dbauth.USE_DB['name']][table_name][0]

                if compare_column_name in table_column_name:
                    update_table_list = []
                    with open(table, 'r') as table_info:
                        table_txns = table_info.readlines()
                    with open(table, 'w+') as table_info2:
                        for line in table_txns:
                            infotable_line_str_list = line.strip("\n").split(",")
                            infotable_column_id = infotable_line_str_list[0]
                            if compare_column_value == infotable_column_id:
                                continue
                            update_table_list.append(line)
                        update_table_list[-1]=update_table_list[-1].strip()
                        for line in update_table_list:
                            table_info2.write(line)
                        print("Query OK, 1 row affected", end=" ")
                        return True
                else:
                    print("ERROR: Column '%s' doesn't exist" % compare_column_name)
            else:
                print("Table '%s' doesn't exist" % table_name)

def mydbhelp(sql_cmd):
    prompt = """
    员工信息表程序
    show databases
    show tables;
    select * from staff_table;
    select name,age,phone from staff_table where dept = 'IT';
    SELECT name,age FROM staff_table WHERE age > 22;
    select * from staff_table where enroll_date like "2013";
    INSERT INTO staff_table VALUES("Jack Ma",23,13012546524,"IT","2014-07-22");
    UPDATE staff_table SET dept="Market",phone=13532016528 WHERE name="Jack Wang";
    DELETE FROM staff_table WHERE staff_id=5;
    """
    print(prompt)
    return True


def empInfoManageSystem():
    prompt = '''Welcome to the MyDB monitor. Commands end with ;
Server version: MyDB1.0
Use the 'show databases' command to view the databases, and use 'show tables;' view the tables.
Type 'exit' or 'quit' to quit the MyDB.
Type 'help;' or '\h' for help.'''
    print(prompt)

    while True:
        sql_cmd = str(input("MyDB [(none)]> ")).strip()
        if str(sql_cmd) == "":
            continue
        elif str(sql_cmd) == "quit" or str(sql_cmd) == "exit":
            break
        global_action = sql_cmd.split()[0].lower()
        if global_action == "use":
            result = initdatabase(sql_cmd)
            while result == True:
                sql_cmd = str(input("MyDB [%s]> " % dbauth.USE_DB['name'])).strip()
                if str(sql_cmd) == "":
                    continue
                elif str(sql_cmd) == "quit" or str(sql_cmd) == "exit":
                    sys.exit()
                elif str(sql_cmd).strip(";") == "help" or str(sql_cmd) == "\h":
                    mydbhelp(sql_cmd)
                action = sql_cmd.split()[0].lower()
                action_func = {
                    "use": initdatabase,
                    "show": show,
                    "select": select,
                    "insert": insert,
                    "update": update,
                    "delete": delete,
                }
                res = action_func.get(action)
                if res:
                    while True:
                        if not sql_cmd.endswith(";"):
                            sql_cmd2 = str(input("  -> "))
                            sql_cmd = sql_cmd + " " + sql_cmd2
                            continue
                        break
                    res(sql_cmd)
                else:
                    continue
        elif global_action == "show":
            show(sql_cmd)
        elif global_action.strip(';') == "help" or global_action == "\h":
            mydbhelp(sql_cmd)
        else:
            print("ERROR: No database selected")