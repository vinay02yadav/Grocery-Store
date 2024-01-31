<template>
  <nav class="oo">
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


    <div class="button-combo">

      <button type="button" class="btn btn-outline-warning" @click="exportPostsCSV()">Export</button>

      <button @click="logout" type="button" class="btn btn-outline-primary"><img class="user" src="../assets/user.png"
          alt="user">Logout</button>

    </div>

  </nav>
</template>
  
<script>
import axios from "axios";

export default {
  data() {
    return {
      changename: true,
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

    async exportPostsCSV() {
      try {
        const currentUrl = window.location.href;
        const urlSegments = currentUrl.split("/");
        const idd = urlSegments[urlSegments.length - 1];

        let access_token = localStorage.getItem(`access_token-${idd}`)
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

        const response = await axios.get(`http://127.0.0.1:5000/api/export-posts-csv`, { responseType: 'arraybuffer' })
        console.log(response)

        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')

        // setting filenames.
        const now = new Date().toLocaleString().replace(/[^\w\s]/gi, '').replace(/ /g, '_')
        const post_filename = `posts_${now}.csv`

        link.href = url
        link.setAttribute('download', post_filename)
        document.body.appendChild(link)
        link.click()

        // code to : Save the file to a custom location.
        // const fileSaver = new FileSaver(url);
        // fileSaver.save(post_filename, {
        //     type: 'text/csv',
        // });


      } catch (error) {
        if (error.response && error.response.status === 401) {
          await refreshAccessToken()
          await this.exportPostsCSV()
        } else {
          console.error(error)
          alert('An error occurred while exporting CSV files.')
        }
      }
    },


  },
};
</script>
  
  
<style scoped>
@import url("https://fonts.googleapis.com/css?family=Montserrat:400,500,600,700&display=swap");

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
  bottom: 8px;
  font-size: 13px;
  right: 4px;
}

.total {
  /* border: 1px solid rgb(86, 18, 243); */
  position: relative;
  display: inline-block;
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
  