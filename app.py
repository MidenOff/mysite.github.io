from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Получаем данные из формы
    a1 = int(request.form['a1'])
    a2 = int(request.form['a2'])
    a3 = int(request.form['a3'])
    a4 = int(request.form['a4'])

    # Проверяем, был ли выбран вектор из списка или введен пользовательский
    E_select = request.form.get('E_select')
    E_custom = request.form.get('E_custom')

    if E_custom:
        # Очищаем пользовательский ввод от пробелов и разделяем по запятым или пробелам
        E_custom = E_custom.replace(" ", ",").replace(";", ",").replace("|", ",")
        E = list(map(int, E_custom.split(',')))
    else:
        E = list(map(int, E_select.split(',')))

    # Выполняем код
    result = execute_code(a1, a2, a3, a4, E)

    # Перенаправляем на страницу с результатами
    return render_template('result.html', result=result)

def execute_code(a1, a2, a3, a4, E):
    # Код из вашего файла
    result = []

    result.append("Входной информационный вектор:")
    result.append(f"U = ({a1}, {a2}, {a3}, {a4})")
    result.append("")
    c1 = a1 ^ a3 ^ a4
    c2 = a1 ^ a2 ^ a4
    c3 = a1 ^ a2 ^ a3
    c4 = a1 ^ a2 ^ a3

    V = [a1, a2, a3, a4, c1, c2, c3, c4]
    result.append("Вектор группового кода")
    result.append(f"V = ({', '.join(map(str, V))})")
    result.append("")

    result.append("Вектор ошибки")
    result.append(f"E = ({', '.join(map(str, E))})")
    result.append("")

    a1_ = a1 ^ E[0]
    a2_ = a2 ^ E[1]
    a3_ = a3 ^ E[2]
    a4_ = a4 ^ E[3]
    c1_ = c1 ^ E[4]
    c2_ = c2 ^ E[5]
    c3_ = c3 ^ E[6]
    c4_ = c4 ^ E[7]

    V_ = [a1_, a2_, a3_, a4_, c1_, c2_, c3_, c4_]
    result.append("Вектор кода после помехи")
    result.append(f"V` = ({', '.join(map(str, V_))})")
    result.append("")

    s1 = c1_ ^ a1_ ^ a3_ ^ a4_
    s2 = c2_ ^ a1_ ^ a2_ ^ a4_
    s3 = c3_ ^ a1_ ^ a2_ ^ a3_
    s4 = c4_ ^ a1_ ^ a2_ ^ a3_ ^ a4_ ^ c1_ ^ c2_ ^ c3_
    S = [s1, s2, s3, s4]
    result.append("Вектор синдрома:")
    result.append(f"S = ({', '.join(map(str, S))})")
    result.append("")

    if (s1 and s2 and s3 and s4) == True:
        e_a1 = 1
        result.append("Ошибка в разряде a1")
        result.append(f"e_a1 = {e_a1}")
    else:
        e_a1 = 0

    if (not s1 and s2 and s3 and s4) == True:
        e_a2 = 1
        result.append("Ошибка в разряде a2")
        result.append(f"e_a2 = {e_a2}")
    else:
        e_a2 = 0

    if (s1 and not s2 and s3 and s4) == True:
        e_a3 = 1
        result.append("Ошибка в разряде a3")
        result.append(f"e_a3 = {e_a3}")
    else:
        e_a3 = 0

    if (s1 and s2 and not s3 and s4) == True:
        e_a4 = 1
        result.append("Ошибка в разряде a4")
        result.append(f"e_a4 = {e_a4}")
    else:
        e_a4 = 0

    if ((s1 or s2 or s3) and not s4) == True:
        Erase = 1
        result.append("Erase")
    else:
        Erase = 0

    if Erase == 0:
        U = [a1_ ^ e_a1, a2_ ^ e_a2, a3_ ^ e_a3, a4_ ^ e_a4]
    else:
        U = [0, 0, 0, 0]

    result.append("Выходной вектор:")
    result.append(f"U = ({', '.join(map(str, U))})")

    return "\n".join(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
