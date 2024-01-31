<template>
  <nav>
    <div class="menu-icon">
      <span class="fas fa-bars"></span>
    </div>
    <div class="logo">Urahara's Shop</div>
    <div class="search-icon">
      <span class="fas fa-search"></span>
    </div>
    <div class="cancel-icon">
      <span class="fas fa-times"></span>
    </div>

    <!-- search bar -->
    <form @submit="performSearch">
      <input v-model="searchQuery" type="search" class="search-data" placeholder="Search" />
      <button type="submit" class="fas fa-search">
        <img
          src="data:image/png;base64,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"
          alt="logo" />
      </button>
    </form>


    <!-- filter by price -->
    <label class="dropdown">

      <div class="dd-button">
        Filter
      </div>

      <input type="checkbox" class="dd-input" id="test">

      <ul class="dd-menu" style="margin: 0px 0px 0px 28px;">
        <li style="color: antiquewhite;" @click="selectPriceRange('10')">{{ '< 10' }}</li>
        <li style="color: antiquewhite;" @click="selectPriceRange('100')">{{ '< 100' }}</li>
        <li style="color: antiquewhite;" @click="selectPriceRange('500')">{{ '< 500' }}</li>
        <li style="color: antiquewhite;" @click="selectPriceRange('1000')">{{ '< 1000' }}</li>
      </ul>

    </label>



    <!-- account -->
    <div class="button-combo">

      <label v-if="logged_in" class="dropdown">

        <div class="dd-button">
          Account
        </div>

        <input type="checkbox" class="dd-input" id="test">

        <ul class="dd-menu">
          <li style="color: antiquewhite;"><img class="user" src="../assets/user.png" alt="user" style="width: 37px;">{{
            logged_user }}</li>
          <li class="divider"></li>
          <li>
            <a @click="logout"><img src="../assets/exit.png" style="width: 30px; margin-right: 10px;"
                alt="exit">Logout</a>
          </li>
        </ul>

      </label>



      <button v-else type="button" @click="goto_login" class="btn btn-outline-primary">{{ logged_user }}</button>

      <button v-if="changename" type="button" @click="goto_cart" class="btn btn-outline-success custom-button">
        <img src="../assets/empty-cart.png" class="button-image" />
        <div class="items">{{ item_count }} items</div><br>
        <div class="total">&#8377; {{ total_price }}</div>
      </button>

      <button v-else type="button" @click="goto_home" class="btn btn-outline-success">
        Home
      </button>

    </div>

  </nav>
</template>

<script>
export default {
  data() {
    return {
      // changename: true,
      searchQuery: "",
      selectedFilter: 'Filter',
      id: 0,
    }
  },
  props: {
    item_count: Number,
    total_price: Number,
    logged_user: String,
    changename: Boolean,
    logged_in: Boolean,
  },

  mounted() {
    let currentURL = window.location.href;
    // console.log(currentURL)
    if (currentURL == 'http://localhost:8080/#/cart' || currentURL == 'http://localhost:8080/?#/cart') {
      this.changename = false
    }
  },

  methods: {
    logout() {
      const currentUrl = window.location.href;
      const urlSegments = currentUrl.split("/");
      const idd = urlSegments[urlSegments.length - 1];

      localStorage.removeItem(`access_token-${idd}`);
      localStorage.removeItem(`refresh_token-${idd}`);
      localStorage.removeItem(`username-${idd}`)

      this.$router.push('/login')
    },

    selectPriceRange(range) {
      if (this.searchQuery != '') {
        this.searchQuery = "";

      }
      this.selectedFilter = "<" + range;
      if (range == 0) {
        this.selectedFilter = "Filter"
      }
      this.$emit("selectPriceRange", range);
    },


    performSearch() {
      if (this.selectedFilter != 'Filter') {
        this.selectedFilter = 'Filter';
      }
      // console.log("from navbar", this.searchQuery)
      this.searchQuery = this.searchQuery.trim();
      // if (this.searchQuery != null && this.searchQuery != ""){
      this.$emit("search", this.searchQuery);
      // }
    },
    pre_order() {
      this.$router.push('/your-orders')
    },
    async goto_login() {
      await this.$router.push('/login')
    },
    async goto_home() {
      console.log("home")
      const currentUrl = window.location.href;
      const urlSegments = currentUrl.split("/");
      this.id = urlSegments[urlSegments.length - 1];
      await this.$router.push(`/${this.id}`)
      window.location.reload();
    },
    async goto_cart() {
      console.log("cart")
      const currentUrl = window.location.href;
      const urlSegments = currentUrl.split("/");
      this.id = urlSegments[urlSegments.length - 1];
      await this.$router.push(`/cart/${this.id}`)
    }
  },
};
</script>


<style scoped>
@import url("https://fonts.googleapis.com/css?family=Montserrat:400,500,600,700&display=swap");




a {
  text-decoration: none;
  color: #000000;
}

a:hover {
  color: #222222;
}


.dropdown {
  display: inline-block;
  position: relative;
  margin-right: 22px;
  z-index: 10;
}

.dd-button {
  display: inline-block;
  border: 1px solid gray;
  border-radius: 4px;
  padding: 10px 30px 10px 20px;
  background-color: #ffffff;
  cursor: pointer;
  white-space: nowrap;
}

.dd-button:after {
  content: "";
  position: absolute;
  top: 50%;
  right: 15px;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid black;
}

.dd-button:hover {
  background-color: #eeeeee;
}

.dd-input {
  display: none;
}

.dd-menu {
  position: absolute;
  top: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0;
  margin: 2px 0 0 0;
  box-shadow: 0 0 6px 0 rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  list-style-type: none;
  left: -30%;
}

.dd-input+.dd-menu {
  display: none;
}

.dd-input:checked+.dd-menu {
  display: block;
}

.dd-menu li {
  padding: 10px 20px;
  cursor: pointer;
  white-space: nowrap;
}

.dd-menu li:hover {
  background-color: #f6f6f6;
}

.dd-menu li a {
  display: block;
  margin: -10px -20px;
  padding: 10px 20px;
}

.dd-menu li.divider {
  padding: 0;
  border-bottom: 1px solid #cccccc;
}














* {
  margin: 0;
  padding: 0;
  outline: none;
  box-sizing: border-box;
  font-family: "Montserrat", sans-serif;
}

.user {
  width: 37px;
  height: 31px;
  display: inline-flex;
  position: relative;
  right: 8px;
}



.items {
  /* border: 1px solid red; */
  position: relative;
  display: inline;
  bottom: -1px;
  font-size: 15px;
  right: -7px;
}

.total {
  /* border: 1px solid rgb(86, 18, 243); */
  position: relative;
  display: none;
  bottom: 15px;
  font-size: 15px;
  left: 15px;
}

.custom-button {
  width: 125px;
  height: 53px;
}

body {
  background: #f2f2f2;
}

.button-image {
  width: 34px;
  height: 36px;
  display: inline-block;
  position: relative;
  right: 10px;
}

.button-combo {
  left: 6%;
  position: relative;
}

.btn {
  margin-right: 19px;
}

nav {
  background: #171c24;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  height: 70px;
  border-bottom: 1px solid #423f3f;
  padding: 0 100px;
  /* position: fixed; */
  width: 100%;
  z-index: 1;
}

nav .logo {
  color: #fff;
  font-size: 30px;
  right: 4%;
  position: relative;
  font-weight: 600;
  letter-spacing: -1px;
}

nav form {
  justify-content: center;
  display: flex;
  left: 2%;
  position: relative;
  height: 40px;
  padding: 2px;
  background: #1e232b;
  border-radius: 20px;
  width: 45%;
  border: 2px solid #423f3f;
}

nav form .search-data {
  width: 100%;
  height: 100%;
  padding: 0 10px;
  color: #fff;
  font-size: 17px;
  border: none;
  font-weight: 500;
  background: none;
}

img,
svg {
  vertical-align: middle;
  width: 90%;
  border-radius: 22px;
}

nav form button {
  font-size: 17px;
  position: relative;
  width: 7%;
  left: 2px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  bottom: .5px;
}

nav .menu-icon,
nav .cancel-icon,
nav .search-icon {
  width: 40px;
  text-align: center;
  margin: 0 50px;
  font-size: 18px;
  color: #fff;
  cursor: pointer;
  display: none;
}

nav .menu-icon span,
nav .cancel-icon,
nav .search-icon {
  display: none;
}

@media (max-width: 1245px) {
  nav {
    padding: 0 50px;
  }
}

@media (max-width: 1140px) {
  nav {
    padding: 0px;
  }

  nav .logo {
    flex: 2;
    text-align: center;
  }

  nav .nav-items {
    position: fixed;
    z-index: 99;
    top: 70px;
    width: 100%;
    left: -100%;
    height: 100%;
    padding: 10px 50px 0 50px;
    text-align: center;
    background: #14181f;
    display: inline-block;
    transition: left 0.3s ease;
  }

  nav .nav-items.active {
    left: 0px;
  }

  nav .nav-items li {
    line-height: 40px;
    margin: 30px 0;
  }

  nav .nav-items li a {
    font-size: 20px;
  }

  nav form {
    position: absolute;
    top: 80px;
    right: 50px;
    opacity: 0;
    pointer-events: none;
    transition: top 0.3s ease, opacity 0.1s ease;
  }

  nav form.active {
    top: 95px;
    opacity: 1;
    pointer-events: auto;
  }

  nav form:before {
    position: absolute;
    content: "";
    top: -13px;
    right: 0px;
    width: 0;
    height: 0;
    z-index: -1;
    border: 10px solid transparent;
    border-bottom-color: #1e232b;
    margin: -20px 0 0;
  }

  nav form:after {
    position: absolute;
    content: "";
    height: 60px;
    padding: 2px;
    background: #1e232b;
    border-radius: 2px;
    min-width: calc(100% + 20px);
    z-index: -2;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }

  nav .menu-icon {
    display: block;
  }

  nav .search-icon,
  nav .menu-icon span {
    display: block;
  }

  nav .menu-icon span.hide,
  nav .search-icon.hide {
    display: none;
  }

  nav .cancel-icon.show {
    display: block;
  }
}

.content {
  position: absolute;
  top: 50%;
  left: 50%;
  text-align: center;
  transform: translate(-50%, -50%);
}

.content header {
  font-size: 30px;
  font-weight: 700;
}

.content .text {
  font-size: 30px;
  font-weight: 700;
}

.space {
  margin: 10px 0;
}

nav .logo.space {
  color: red;
  padding: 0 5px 0 0;
}

@media (max-width: 980px) {

  nav .menu-icon,
  nav .cancel-icon,
  nav .search-icon {
    margin: 0 20px;
  }

  nav form {
    right: 30px;
  }
}

@media (max-width: 350px) {

  nav .menu-icon,
  nav .cancel-icon,
  nav .search-icon {
    margin: 0 10px;
    font-size: 16px;
  }
}

.content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.content header {
  font-size: 30px;
  font-weight: 700;
}

.content .text {
  font-size: 30px;
  font-weight: 700;
}

.content .space {
  margin: 10px 0;
}
</style>
