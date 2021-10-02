from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__) #reference this file 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # three forward slashes is relative path
db = SQLAlchemy(app) #initialize database 

# create a data model 

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False) #dont want to left the column empty 
    date_created = db.Column(db.DateTime, default = datetime.utcnow) #keep a record 

    def __repr__(self):
        return '<Taske %r>' % self.id

# index route 
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        # logic for adding tasks
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the task'
    else:
        # look at the db content in the order it was creatd and return 
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/') #back to home page
    except:
        return 'There was a problem deleting that task.'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        # update logic 
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:    
            return 'There was an issue updating the task.'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True) 
