import os
from flask import Flask, flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename

from encrypt import encryptpdf as enc, imgtopdf as imf
from flask import Flask

UPLOAD_FOLDER = 'uploads'
try:
    import os
    os.mkdir('uploads')
except:
    pass

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the files part
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
		files = request.files.getlist('files[]')
		for file in files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
				print('.............', loc)
				file.save(loc)

				try:
					enc(loc, 'vix')
				except:
					try:
						enc(imf(loc), 'vix')
					except:
						pass

		flash('File(s) successfully uploaded')
		return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
