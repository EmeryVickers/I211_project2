from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

#global variables to help with getting and setting dinosaur data
DINO_PATH = app.root_path + '/dinosaurs.csv'
DINO_KEYS = ['slug', 'name', 'description', 'image', 'image-credit', 'source-url', 'source-credit']

with open(DINO_PATH, 'r') as csvfile:
   data = csv.DictReader(csvfile)
   dinosaurs = {row['slug']:{'name':row['name'], 'description':row['description'], 'image':row['image'], 'image-credit':row['image-credit'], 'source-url':row['source-url'], 'source-credit':row['source-credit']} for row in data}

@app.route('/')
@app.route('/dino')
@app.route('/dino/<dino>')
def index(dino=None):
    print(dino)
    if dino and dino in dinosaurs.keys():
        dinosaur = dinosaurs[dino]
        return render_template('dino.html',dinosaur=dinosaur)
    else:
        return render_template('index.html', dinosaurs=dinosaurs)

@app.route('/favorite')
def favorite():    
    return render_template('favorite.html', dino="T-Rex")

@app.route('/about')
def about():
    return render_template('about.html')





#function to get the dinosaurs dictionary of dictionaries data from csv file
def get_dinos():
    try:
        with open(DINO_PATH, 'r') as csvfile:
            data = csv.DictReader(csvfile)
            dinosaurs = {}
            for dino in data:
                dinosaurs[dino['slug']] = dino
    except Exception as e:
        print(e)
    return dinosaurs


# Function that takes a dictionary and saves it to csv
def set_dinos(dinosaurs):
    try:
        with open(DINO_PATH, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=DINO_KEYS)
            writer.writeheader()
            for dino in dinosaurs.values():
                writer.writerow(dino)
    except Exception as err:
        print(err)


@app.route('/add-dino', methods=['GET','POST'])
def add_dino():
    if request.method == 'POST':
        # get dinosaurs.csv data
        current_dinos = get_dinos()
    
        # create new dict to hold new dino data from form
        new_dinos = {}
        # add form data to new dict
        for key in DINO_KEYS:
            new_dinos[key]=request.form[key]
        # add new dict to csv data
        current_dinos[request.form['name']]= new_dinos
        # write csv data back out to csv file
        set_dinos(current_dinos)
        # since POST request, redirect to home after Submit
        return redirect(url_for('index'))
    else:
        return render_template('add-dino.html')

@app.route('/dino-quiz',methods=['GET','POST'])
def dino_quiz():
    if request.method == 'POST':
        quizGuesses = {}
        quizGuesses['Question 1'] = request.form['continents']
        quizGuesses['Question 2'] = request.form.get('eggs','false')
        quizGuesses['Question 3'] = request.form.getlist('herbivores')
        quizGuesses['Question 4'] = request.form['extinct']

        quizGuesses['Question 3'] = " and ".join(quizGuesses['Question 3'])

        quizAnswers={
            'Question 1' : 'North America',
            'Question 2' : 'true',
            'Question 3' : 'Stegosaurus and Triceratops',
            'Question 4' : '66'
        }

        return render_template('quiz-results.html',quizGuesses=quizGuesses, quizAnswers=quizAnswers)
    
    else:
        return render_template('dino-quiz.html')