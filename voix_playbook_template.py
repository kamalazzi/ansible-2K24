playbook_voix_content_template = """---
- name: Configure voix Customer
  hosts: customer_{customer}
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
    when: {add_snmp}
  - name: check SNMP configuration
    set_fact:
      snmp_config_present: "{{ 'snmp' in snmp_output.stdout[0] }}"
    when: {add_snmp}
  - name: add snmp configuration
    cisco.ios.ios_config:
      lines:
        - snmp-server community Ansible_ro ro
        - snmp-server community Ansible_rw rw
        - snmp-server enable traps cpu threshold
        - snmp-server host 10.10.10.10 test
    when: {add_snmp} and snmp_output != snmp_config_present

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

  - name: Configure static route Supervision
    cisco.ios.ios_static_routes:
      config:
        - address_families:
          - afi: ipv4
            routes:
              - dest: 10.55.55.64/26
                next_hops:
                  - forward_router_address: {gw_mgmt}
                    name: supervision_route
      state: merged

  - name: save configuration
    cisco.ios.ios_config:
      save_when: modified
"""