from flask import Flask, request, render_template, url_for, session, redirect
import os
import cv2
import tensorflow as tf


app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file != '':
            imagepath = os.path.join(name_of_folder_which_will_store_uploaded_image,uploaded_file.filename)
            imagepath = path_to_store_uploaded_images + imagepath
            uploaded_file.save(imagepath)
            
            IMG_SIZE = size_of_image_used_while_training_model
            img_array = cv2.imread(imagepath,cv2.IMREAD_GRAYSCALE)
            new_array = cv2.resize(img_array,(IMG_SIZE,IMG_SIZE))
            new_array = new_array.reshape(-1,IMG_SIZE,IMG_SIZE,1)

            CATEGORIES = [category1,category2]
            model = tf.keras.models.load_model(path_to_model)  #give path to the model
            prediction = model.predict(new_array)
            prediction = CATEGORIES[int(prediction[0][0])]
            session['imagepath'] = uploaded_file.filename
            session['result'] = prediction
        return redirect('result')
        
    return render_template('index.html')

@app.route('/result',methods=['GET'])
def result():
    return render_template('result.html',imagepath=session['imagepath'],result=session['result'])

if __name__ == '__main__':
    app.secret_key = 'highlyconfidential'
    app.run(debug=True)
