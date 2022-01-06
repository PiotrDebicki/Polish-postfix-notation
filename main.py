from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.core import RadioField, StringField 
from wtforms.validators import DataRequired
import os


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(24)


class FormOpen(FlaskForm):
    expression = StringField(validators=[DataRequired()])
    radioButton = RadioField(choices=[('1',"Notacja infiksowa -> ONP"), ('2', "ONP -> Notacja infiksowa")])
    submit = SubmitField('Licz')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FormOpen()
    value = ""
    expression_changed = ""
    last_expression = ""
    if form.validate_on_submit():
        last_expression = form.expression.data
        form.expression.data = ""
        boolean = True

        if(form.radioButton.data == '2'):
            licznik = 0
            for i in last_expression:
                if i.isnumeric():
                    licznik += 1
                if i in "+–*/ ":
                    if licznik < 2:
                        boolean = False
                    else:
                        licznik += -1
            if licznik != 1:
                boolean =  False
            else:
                boolean = True

            if(boolean):
                a=[]
                b={'+': lambda x,y: y+x, '-': lambda x,y: y-x, '*': lambda x,y: y*x,'/': lambda x,y:y/x}
                for c in last_expression.split():
                    if c in b: a.append(b[c](a.pop(),a.pop()))
                    else: a.append(float(c))

                expression_changed = "<<wyrażenie w notacji infiksowej>>"
                



                return render_template('index.html', form=form, value=str(a[0]), expression_changed=expression_changed, last_expression=last_expression)

        else:
            for y in last_expression:
                if(y not in "1234567890-+* "):
                    boolean = False
            if (boolean == True):
                expression_changed = ""

                points_dict={"(":0,"+":1,"-":1,")":1,"*":2,"/":2,}
                stack = ""
                stack_top_point = 0

                for x in last_expression:
                    if(x in "1234567890"):
                        expression_changed += x
                    else:
                        expression_changed += " "
                        if(x == "("):
                            stack = "(" + stack
                            stack_top_point = points(stack[0])
                        elif(x == ")"):
                            expression_changed += stack[(stack.index("(")):]
                            stack = stack[(stack.index("(")+1):]
                            stack_top_point = points(stack[0])
                        elif(x in "/*-+"):
                            if(points_dict[x] > stack_top_point):
                                stack = x + stack
                                stack_top_point = points(stack[0])
                            else:
                                expression_changed += " " + stack[:LastLess(stackToPoints(stack), points_dict[x])]
                                stack = x + stack[LastLess(stackToPoints(stack), points_dict[x]):]
                                stack_top_point = points(stack[0])
                expression_changed += stack

                value = eval(last_expression.replace(" ",""))

                return render_template('index.html', form=form, value=value, expression_changed=expression_changed, last_expression=last_expression)



    return render_template('index.html', form=form, value=value, expression_changed=expression_changed, last_expression=last_expression)

def points(a):
    points_dict={"(":0,"+":1,"-":1,")":1,"*":2,"/":2,}
    try:
        stack_top_point = points_dict[a]
    except:
        stack_top_point = 0
    return stack_top_point

def stackToPoints(stack):
    points_dict={"(":0,"+":1,"-":1,")":1,"*":2,"/":2,}
    points_stack = ""
    for x in stack:
        points_stack += str(points_dict[x])
    return points_stack

def LastLess(points_stack, actuall):
    num = 0
    for x in range(-1, ((-1)*(len(points_stack))), -1):
        if(int(points_stack[x]) < actuall):
            num = x
    return num