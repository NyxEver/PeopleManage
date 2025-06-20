from flask import Flask, render_template, request, redirect, url_for
from DatabaseManager import all_person
from User_Template import User_Template
from User import User

print("2025.05.26")
print("管理系统")
print("SQL+FLASK+HTML storage version v0.4")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/account_verify', methods=['POST'])
def account_verify():
    number = request.form['username']
    password = request.form['password']
    result_verify = User_Template.verify_user_account(number, password)
    if result_verify:
        return redirect(url_for('welcome', username=number))
    else:
        return "账号或密码错误"


@app.route('/account_register', methods=['POST'])
def account_register():
    number = request.form['username']
    password = request.form['password']
    user=User(number, password,'name',1,'M', 'user', None, None)
    result_register = User_Template.register_account(user)
    if result_register:
        return redirect(url_for('index', message="注册成功"))
    else:
        return "注册失败"


@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)


@app.route('/main')
def main():
    results_all = all_person()
    return render_template('main.html', results=results_all)


@app.route('/add_people', methods=['POST'])
def add_people():
    try:
        number = request.form['number']
        #password = request.form['password']
        password = request.form.get('password', 'default123')
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        role = request.form['role']
        grade = request.form['grade']
        position = request.form['position']
        user = User(number, password, name, age, gender, role, grade, position)
        result_add = user.save_SQL()
        if result_add:
            return redirect(url_for('main'))
        else:
            return "添加失败"
    except ValueError as error:
        return f"输入数据格式错误：{error}"


@app.route('/delete_people', methods=['POST'])
def delete_people():
    field_type = request.form['field_type']
    del_value = request.form['value_1']
    list_number = request.form.get('list_number')
    person_find_data = User_Template.find_SQL(field_type,del_value)
    if not person_find_data:
        return "未找到符合条件的记录"
    list_number = int(list_number)
    person_data = person_find_data[list_number]
    person_obj = User(person_data[0], person_data[1], person_data[2], person_data[3], person_data[4], person_data[5], person_data[6], person_data[7])
    result_delete = person_obj.delete_SQL()
    if result_delete:
        return redirect(url_for('main'))
    else:
        return "未找到 or 删除失败"

@app.route('/update_people', methods=['POST'])
def update_people():
    field_type = request.form.get('field_type')
    value_find = request.form.get('value_1')
    person_find_data = User_Template.find_SQL(field_type, value_find)
    if not person_find_data:
        return "未找到符合条件的记录"
    list_number = request.form.get('list_number')
    list_number = int(list_number)
    person_data = person_find_data[list_number]
    original_person_obj = User(person_data[0], person_data[1], person_data[2], person_data[3], person_data[4], person_data[5], person_data[6], person_data[7])
    original_dict = dict(zip(['number','password', 'name', 'age', 'gender','role','grade','position'], person_data))
    if not original_dict:
        return "未找到要修改的记录"
    new_values_list = [
        request.form.get('number', original_dict['number']),# 如果未提供则使用原值
        request.form.get('password', original_dict['password']),
        request.form.get('name', original_dict['name']),
        int(request.form.get('age', original_dict['age'])),
        request.form.get('gender', original_dict['gender']),
        request.form.get('role', original_dict['role']),
        request.form.get('grade', original_dict['grade']),
        request.form.get('position', original_dict['position']),
    ]
    person_obj = User(new_values_list[0], new_values_list[1], new_values_list[2], new_values_list[3], new_values_list[4],
                         new_values_list[5], new_values_list[6],new_values_list[7])
    get_id=original_person_obj.get_person_ID()
    result_update= person_obj.update_SQL(get_id)
    if result_update:
        return redirect(url_for('main'))
    else:
        return "修改失败"


@app.route('/find_people', methods=['POST'])
def find_people():
    field_type = request.form['field_type']
    value_1 = request.form['value_1']
    result_find = User_Template.find_SQL(field_type, value_1)
    if result_find:
        #    return redirect(url_for('main'))
        return render_template('main.html', results=result_find, search_performed=True,
                               search_field=field_type, search_value=value_1)
    else:
        return render_template('main.html', results=[], search_performed=True,
                               search_field=field_type, search_value=value_1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
