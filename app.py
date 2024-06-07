from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/next_page', methods=['POST'])
def next_page():
    form_data = request.form.to_dict()
    
    # Retrieve the servicetype option from the form data
    servicetype = form_data.get('servicetype')
    
    # Redirect based on servicetype selection
    if servicetype == 'internet':
        return redirect(url_for('internet'))
    elif servicetype == 'voix':
        return redirect(url_for('voix'))
    else:
        return redirect(url_for('index'))

@app.route('/internet')
def internet():
    return render_template('internet.html')

@app.route('/voix')
def voix():
    return render_template('voix.html')


@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Get form data
    vlan = request.form['vlan']
    wan = request.form['wan']
    gw = request.form['gw']
    mgmt = request.form['mgmt']
    add_default_route = 'default-route' in request.form  # Checkbox handling
    add_aaa = 'aaa' in request.form  # Checkbox handling
    add_snmp = 'snmp' in request.form  # Checkbox handling
    
    # Generate playbook content based on form inputs
    playbook_content = f"""---
- name: Configure Internet Customer
  hosts: your_hosts_group
  tasks:
    - name: Configure VLAN {vlan}
      vlan:
        vlan_id: {vlan}
        state: present

    - name: Configure WAN Interface
      ip_interface:
        interface: WAN
        ip: {wan}
        state: present

    - name: Configure Gateway
      ip_route:
        network: 0.0.0.0/0
        gateway: {gw}
        state: present
      when: {add_default_route}

    - name: Configure Management Interface
      ip_interface:
        interface: Management
        ip: {mgmt}
        state: present

    - name: Configure AAA
      # Add your AAA configuration task here
      # Example: aaa_configuration_task:
      #   option: value
      when: {add_aaa}

    - name: Configure SNMP
      # Add your SNMP configuration task here
      # Example: snmp_configuration_task:
      #   option: value
      when: {add_snmp}
    """
    
    # Save playbook to a file
    playbook_path = os.path.join(os.getcwd(), 'generated_playbook.yml')
    with open(playbook_path, 'w') as playbook_file:
        playbook_file.write(playbook_content)
    
    return jsonify({'status': 'success', 'message': f'Playbook generated and saved to {playbook_path}'})


if __name__ == '__main__':
    app.run(debug=True)

