from flask import Flask
from flask import request
from flask import render_template

# creates a Flask application
app = Flask(__name__)


@app.route("/")
def form():
	return render_template('index.html')

@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    customer = request.form['customer']
    ip = request.form['ip']
    username = request.form['username']
    password = request.form['password']
    # Create Ansible playbook
    playbook_content = f"""
- hosts: {customer}
  vars:
    ansible_host: {customer}
    ansible_user: {customer}
    ansible_password: {customer}
  tasks:
    - name: Test connection
      ping:
    """
    
    # Save playbook to a file
    with open('playbook.yml', 'w') as file:
        file.write(playbook_content)
    
    return f"Ansible playbook created:<br><pre>{playbook_content}</pre>"

# run the application
if __name__ == "__main__":
	app.run(debug=True)
