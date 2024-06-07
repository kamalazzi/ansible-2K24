from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML form template
form_template = """
<!doctype html>
<html lang="en" data-bs-theme="auto">
  <head><script src="js/color-modes.js"></script>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">
    <meta name="generator" content="Hugo 0.122.0">
    <title>Automation</title>
    <link rel="canonical" href="https://getbootstrap.com/docs/5.3/examples/checkout/">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@docsearch/css@3">
    <link href="/static/bootstrap.min.css" rel="stylesheet">
    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }
      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
      .b-example-divider {
        width: 100%;
        height: 3rem;
        background-color: rgba(0, 0, 0, .1);
        border: solid rgba(0, 0, 0, .15);
        border-width: 1px 0;
        box-shadow: inset 0 .5em 1.5em rgba(0, 0, 0, .1), inset 0 .125em .5em rgba(0, 0, 0, .15);
      }
      .b-example-vr {
        flex-shrink: 0;
        width: 1.5rem;
        height: 100vh;
      }
      .bi {
        vertical-align: -.125em;
        fill: currentColor;
      }
      .nav-scroller {
        position: relative;
        z-index: 2;
        height: 2.75rem;
        overflow-y: hidden;
      }
      .nav-scroller .nav {
        display: flex;
        flex-wrap: nowrap;
        padding-bottom: 1rem;
        margin-top: -1px;
        overflow-x: auto;
        text-align: center;
        white-space: nowrap;
        -webkit-overflow-scrolling: touch;
      }
      .btn-bd-primary {
        --bd-violet-bg: #712cf9;
        --bd-violet-rgb: 112.520718, 44.062154, 249.437846;

        --bs-btn-font-weight: 600;
        --bs-btn-color: var(--bs-white);
        --bs-btn-bg: var(--bd-violet-bg);
        --bs-btn-border-color: var(--bd-violet-bg);
        --bs-btn-hover-color: var(--bs-white);
        --bs-btn-hover-bg: #6528e0;
        --bs-btn-hover-border-color: #6528e0;
        --bs-btn-focus-shadow-rgb: var(--bd-violet-rgb);
        --bs-btn-active-color: var(--bs-btn-hover-color);
        --bs-btn-active-bg: #5a23c8;
        --bs-btn-active-border-color: #5a23c8;
      }
      .bd-mode-toggle {
        z-index: 1500;
      }
      .bd-mode-toggle .dropdown-menu .active .bi {
        display: block !important;
      }
    </style>
    <!-- Custom styles for this template -->
    <link href="main.css" rel="stylesheet">
  </head>
  <body class="bg-body-tertiary">
    <svg xmlns="http://www.w3.org/2000/svg" class="d-none">
      <symbol id="check2" viewBox="0 0 16 16">
        <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
      </symbol>
      <symbol id="circle-half" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 0 8 1v14zm0 1A8 8 0 1 1 8 0a8 8 0 0 1 0 16z"/>
      </symbol>
      <symbol id="moon-stars-fill" viewBox="0 0 16 16">
        <path d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278z"/>
        <path d="M10.794 3.148a.217.217 0 0 1 .412 0l.387 1.162c.173.518.579.924 1.097 1.097l1.162.387a.217.217 0 0 1 0 .412l-1.162.387a1.734 1.734 0 0 0-1.097 1.097l-.387 1.162a.217.217 0 0 1-.412 0l-.387-1.162A1.734 1.734 0 0 0 9.31 6.593l-1.162-.387a.217.217 0 0 1 0-.412l1.162-.387a1.734 1.734 0 0 0 1.097-1.097l.387-1.162zM13.863.099a.145.145 0 0 1 .274 0l.258.774c.115.346.386.617.732.732l.774.258a.145.145 0 0 1 0 .274l-.774.258a1.156 1.156 0 0 0-.732.732l-.258.774a.145.145 0 0 1-.274 0l-.258-.774a1.156 1.156 0 0 0-.732-.732l-.774-.258a.145.145 0 0 1 0-.274l.774-.258c.346-.115.617-.386.732-.732L13.863.1z"/>
      </symbol>
      <symbol id="sun-fill" viewBox="0 0 16 16">
        <path d="M8 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z"/>
      </symbol>
    </svg>
<header>
  <div class="row" style="background-color: white; padding: 1%;">
    <div class="col-xs-6 col-md-6" style="text-align: center; width: 33.33%;"><img src="/static/Ansible_Logo.png" width="110px" height="110px"/></div>
    <div class="col-xs-6 col-md-6"style="text-align: center; width: 33.33%;">
      <h2>Automation project</h2>
      <p class="lead">Automate initial configuration for new network deployments.</p>
    </div>   
    <div class="col-xs-6 col-md-6"style="text-align: center; width: 33.33%;"><img src="/static/Orange_logo.svg" width="100px" height="100px"/></div>
  </div>
</header>    
<div class="container">
    <main>
    <div class="row g-5">
      <div class="col-md-7 col-lg-8" style="width: 100%; padding-top: 2%;">
        <h4 class="mb-3" style="text-align: center;">Customer informations : </h4>
        <hr class="my-4">
        <form class="needs-validation" action="/submit_form" method="post" >
          <div class="row g-3">
            <div class="col-sm-6">
              <label for="customer" class="form-label">Customer name : </label>
              <input type="text" class="form-control" id="customer" placeholder="CIH" value="" required>
              <div class="invalid-feedback">
                Valid customer name is required.
              </div>
            </div>

            <div class="col-sm-6">
              <label for="city" class="form-label">City :</label>
              <input type="text" class="form-control" id="city" placeholder="Casablanca" value="" required>
              <div class="invalid-feedback">
                Valid city is required.
              </div>
            </div>

            <div class="col-sm-6">
              <label for="Techno" class="form-label">Access Technology : </label>
              <input type="text" class="form-control" id="Techno" placeholder="Fibre optic" required>
              <div class="invalid-feedback">
                  Far-end is required.
              </div>
            </div>

            <div class="col-sm-6">
              <label for="farend" class="form-label">Far-end : </label>
              <input type="text" class="form-control" id="farend" placeholder="CA020 port 1/1/1" required>
              <div class="invalid-feedback">
                  Far-end is required.
              </div>
            </div>

            <div class="col-sm-6">
              <label for="service" class="form-label">Service :</label>
              <input type="text" class="form-control" id="service" placeholder="Internet" required>
              <div class="invalid-feedback">
                service type is required.
              </div>
            </div>

            <div class="col-sm-6">
              <label for="address" class="form-label">Address</label>
              <input type="text" class="form-control" id="address" placeholder="1234 Main St" required>
              <div class="invalid-feedback">
                Please enter customer address.
              </div>
            </div>

            <div class="col-sm-6">
              <label for="customer_category" class="form-label">Customer category :</label>
              <input type="text" class="form-control" id="customer_category" placeholder="BANK">
            </div>

            <h4 class="mb-3" style="text-align: center; padding-top: 2%;">Technical informations : </h4>
            <hr class="my-4">
            <div class="col-sm-6">
              <label for="vlan" class="form-label">Vlan ID :</label>
              <input type="text" class="form-control" id="vlan" placeholder="1100" required>
              <div class="invalid-feedback">
                Please enter vlan id.
              </div>
            </div>
            <div class="col-sm-6">
              <label for="wan" class="form-label">WAN IP address :</label>
              <input type="text" class="form-control" id="wan" placeholder="10.10.10.2/31" required>
              <div class="invalid-feedback">
                Please enter WAN ip address.
              </div>
            </div>
            <div class="col-sm-6">
              <label for="gw" class="form-label">GW IP address :</label>
              <input type="text" class="form-control" id="gw" placeholder="10.10.10.1" required>
              <div class="invalid-feedback">
                Please enter GW ip address.
              </div>
            </div>
            <div class="col-sm-6">
              <label for="mgmt" class="form-label">Management IP address :</label>
              <input type="text" class="form-control" id="mgmt" placeholder="10.22.22.22" required>
              <div class="invalid-feedback">
                Please enter WAN ip address.
              </div>
            </div>
            <div class="form-check">
              <input type="checkbox" class="form-check-input" id="default-route">
              <label class="form-check-label" for="default-route">Add default route</label>
            </div>

          <hr class="my-4">



          <hr class="my-4">
          <div class="col-md-4">
            <label for="machinetype" class="form-label">Machine type :</label>
            <select class="form-select" id="machinetype" required>
              <option value="">Choose...</option>
              <option>Cisco</option>
              <option>LBB (Soon)</option>
            </select>
            <div class="invalid-feedback">
              Please provide a valid state.
            </div>
          </div>
          <hr class="my-4">

          <hr class="my-4">

          <div class="form-check">
            <input type="checkbox" class="form-check-input" id="save-info">
            <label class="form-check-label" for="save-info">Save this informations</label>
          </div>
  <input type="submit" value="Submit">
          <button class="w-50 btn btn-primary btn-md mx-auto" type="submit" style="text-align: center;">Submit</button>
        </form>
      </div>
    </div>
  </main>
  <footer class="my-5 pt-5 text-body-secondary text-center text-small">
    <p class="mb-1">&copy; 2024 Automation project by Hanaa</p>
  </footer>
</div>
</html>
"""

@app.route('/')
def form():
    return render_template_string(form_template)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    customer = request.form['customer']
    # Create Ansible playbook

if __name__ == '__main__':
    app.run(debug=True)
