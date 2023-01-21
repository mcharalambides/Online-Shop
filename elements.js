//Define Header and Footer

class MyHeader extends HTMLElement {
    connectedCallback(){
        this.innerHTML  =`
        <header>
        <nav class="navbar navbar-expand-lg navbar-light">
          <div class="container-fluid">
            <div class="collapse navbar-collapse container-fluid justify-content-center" id="navbarScroll">
              <div style="padding-right: 40px;">
                <a class="navbar-brand" href="/">
                  <div class="logo-image">
                        <img src="Logo.png" class="img-fluid">
                  </div>
                </a>
              </div>
              <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
                <li class="nav-item">
                  <a class="nav-link active" aria-current="page" href="#">Home</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#">2T Enduro</a>
                </li>
                <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" href="#" id="navbarScrollingDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Easy Enduro
                  </a>
                  <ul class="dropdown-menu" aria-labelledby="navbarScrollingDropdown">
                    <li><a class="dropdown-item" href="#">Action</a></li>
                    <li><a class="dropdown-item" href="#">Another action</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#">Something else here</a></li>
                  </ul>
                </li>
                <li class="nav-item">
                  <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">First Timers</a>
                </li>
              </ul>
              <div style="padding-left:60px;">
                <button style = "color: #accaac; font-weight: 500; background-color: #1d7d07;" class="btn btn-outline-success" type="submit">BOOK NOW</button></div>
            </div>
          </div>
        </nav>
      </header>`
    }
}

class MyFooter extends HTMLElement {
    connectedCallback(){
        this.innerHTML  =`
        <footer class="bg-light py-3">
        <div class="container">
          <p class="text-center">Copyright &copy;2021 Online Shop</p>
          <div class="d-flex justify-content-center">
            <a href="#">Terms of Service</a>
            <a href="#">Privacy Policy</a>
            <a href="#">Contact Us</a>
          </div>
        </div>
      </footer>`
    }
}


customElements.define('my-header', MyHeader);
customElements.define('my-footer', MyFooter);