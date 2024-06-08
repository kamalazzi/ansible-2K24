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
    lan = request.form['lan']
    add_default_route = 'default-route' in request.form  # Checkbox handling
    add_aaa = 'aaa' in request.form  # Checkbox handling
    add_snmp = 'snmp' in request.form  # Checkbox handling
    
    # Generate playbook content based on form inputs
    playbook_content = f"""---
- name: Configure Internet Customer
  hosts: your_hosts_group
  vars:
    ansible_network_os: cisco.ios.ios
    ansible_become: true
    ansible_become_method: enable
    ansible_become_password: semaphore
    ansible_ssh_user: semaphore
    ansible_ssh_password: semaphore
    ansible_connection: ansible.netcommon.network_cli
    ansible_network_cli_ssh_type: paramiko
  tasks:
  - name: Activate and add description to the interfaces
    cisco.ios.ios_interfaces:
      config:
        - name: FastEthernet0/0
          description: Configured and managed by Ansible Network
          enabled: true
        - name: FastEthernet0/1
          description: WAN interface
          enabled: true
        - name: FastEthernet1/0
          description: Lan Client interface
          enabled: true
      state: merged

  - name: gather snmp configuration
    cisco.ios.ios_command:
      commands:
         - show running-config | include snmp
    register: snmp_output
  - name: check
    set_fact:
      snmp_config_present: "{{ 'snmp' in snmp_output.stdout[0] }}"

  - name: add snmp configuration
    cisco.ios.ios_config:
      lines:
        - snmp-server community Ansible_ro ro
        - snmp-server community Ansible_rw rw
        - snmp-server enable traps cpu threshold
        - snmp-server host 10.10.10.10 test
    when: snmp_output != snmp_config_present
	  when: {add_snmp}

  - name: gather AAA configuration
    cisco.ios.ios_command:
      commands:
         - show running-config | include aaa
    register: aaa_output
  - name: check AAA
    set_fact:
      aaa_config_present: "{{ 'aaa new-model' in aaa_output.stdout[0] }}"

  - name: add AAA
    cisco.ios.ios_config:
      lines:
        - aaa new-model
        - aaa authentication login default local
        - aaa authentication enable default enable
        - aaa authorization exec default local
        - aaa authorization commands 1 default local
        - aaa authorization commands 15 default local group tacacs+
        - aaa accounting exec default start-stop group tacacs+
        - aaa accounting commands 15 default stop-only group tacacs+
        - aaa accounting system default start-stop group tacacs+
    when: {add_aaa}
    
  - name: Create subinterface FastEthernet0/1.{vlan}
    cisco.ios.ios_config:
      lines:
        - encapsulation dot1Q {vlan}
      parents: interface FastEthernet0/1.{vlan}

  - name: Create subinterface FastEthernet0/1.882
    cisco.ios.ios_config:
      lines:
        - encapsulation dot1Q 882
      parents: interface FastEthernet0/1.882

  - name: Configure FastEthernet0/1.{vlan} - Service
    cisco.ios.ios_l3_interfaces:
      config:
        - name: FastEthernet0/1.{vlan}
          ipv4:
            - address: {wan}
      state: merged

  - name: Configure FastEthernet0/1.882 - Supervision
    cisco.ios.ios_l3_interfaces:
      config:
        - name: FastEthernet0/1.882
          ipv4:
            - address: {mgmt}
      state: merged

  - name: Configure FastEthernet1/0 - LAN CLIENT
    cisco.ios.ios_l3_interfaces:
      config:
        - name: FastEthernet1/0
          ipv4:
            - address: {lan}
      state: merged

  - name: Configure static route service
    cisco.ios.ios_static_routes:
      config:
        - address_families:
          - afi: ipv4
            routes:
              - dest: 0.0.0.0/0
                next_hops:
                  - forward_router_address: 10.43.81.216
                    name: default_route_service

  - name: Configure static route Supervision
    cisco.ios.ios_static_routes:
      config:
        - address_families:
          - afi: ipv4
            routes:
              - dest: 10.55.55.64/26
                next_hops:
                  - forward_router_address: 10.251.122.129
                    name: supervision_route
      state: merged

  - name: Configuration BGP with route-map
    cisco.ios.ios_bgp_global:
      config:
        as_number: 65000
        bgp:
          log_neighbor_changes: true
        neighbor:
          - address: 10.43.81.216
            description: ISP neighbor
            remote_as: 65001
            route_map:
              name: Advertised_routes
              out: true
      state: merged

  - name: Prefix lists configuration
    cisco.ios.ios_prefix_lists:
      config:
        - afi: ipv4
          prefix_lists:
            - name: Advertised_routes
              description: allow lans to be advertised to bgp neighber
              entries:
                - action: permit
                  prefix: 192.168.12.0/24
                  sequence: 5
      state: merged

  - name: Route maps configuration
    cisco.ios.ios_route_maps:
      config:
        - route_map: Advertised_routes
          entries:
            - sequence: 10
              action: permit
              description: Advertised_routes
              match:
                ip:
                  address:
                    prefix_lists:
                      - Advertised_routes
            - sequence: 20
              action: deny
              description: Advertised_routes
      state: merged

  - name: save configuration
    cisco.ios.ios_config:
      save_when: modified
	
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
