<template>
  <div class="container">
    <h2 class="login-title">Log in</h2>

    <form @submit="onSubmit" class="login-form" autocomplete="off">
      <div>
        <input id="name" type="text" v-model="username" placeholder="Username" name="name" required />
      </div>


      <div>
        <input id="password" type="password" placeholder="password" v-model="password" name="password" required />
      </div>


      <button class="btn btn--form" type="submit" value="Log in">
        Log in
      </button>

      <p class="text1">Don't have an account? <a class="text2" @click="register">Sign up</a> </p>

    </form>
  </div>

  <!-- <Navbar /> -->
</template>

<script>
import Navbar from "../../components/user_navbar.vue";
import axios from "axios";

export default {
  components: {
    Navbar,
  },

  data() {
    return {
      username: "",
      password: "",
    };
  },

  methods: {

    register() {
      this.$router.push('/register')
    },

    async onSubmit(event) {
      event.preventDefault()

      axios
        .post("http://127.0.0.1:5000/api/login", {
          username: this.username,
          password: this.password,
        }, {
          withCredentials: true,
        })
        .then((response) => {

          if (response.data.status === "success") {
            const access_token = response.data.access_token;
            const refresh_token = response.data.refresh_token;
            const username = response.data.username;
            const id = response.data.id;
            // console.log(access_token)

            localStorage.setItem(`access_token-${id}`, access_token);
            localStorage.setItem(`refresh_token-${id}`, refresh_token);
            localStorage.setItem(`username-${id}`, username)

            alert("Successfully Logged in !!");

            if (response.data.role == 'user') {
              this.$router.push(`/${id}`);
            }
            else if (response.data.role == 'manager') {
              this.$router.push(`/store_manager_dashboard/${id}`);
            }
            else if (response.data.role == 'admin') {
              this.$router.push(`/admin_dashboard/${id}`);
            }
          }
          else {
            alert("Invalid credentials !!");
          }
        })

        .catch((error) => {
          console.error(error);
          alert("An error occurred while logging in !!");
        });
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Linear+B&family=Roboto:ital,wght@1,300&family=Skranji&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body {
  height: 100%;
}

body {
  font-family: sans-serif;
  line-height: 1.4;
  display: flex;
}

.container {
  width: 400px;
  margin: auto;
  margin-top: 15vh;
  padding: 36px 48px 48px 48px;
  border-radius: 11px;
  background-color: rgb(46 45 45);
  box-shadow: rgb(126 126 126 / 15%) 0px 1.4rem 4.8rem;
}

.btn_div {
  margin-top: 22px;
}

.login-title {
  padding: 15px;
  margin-bottom: 29px;
  font-size: 39px;
  font-family: 'Skranji', cursive;
  font-weight: 600;
  text-align: center;
}

.text1 {
  margin-top: 23px;
  font-size: 17px;
  font-family: 'Skranji', cursive;
}

.text2 {
  cursor: pointer;
  color: blue;
}

.text2:hover {
  cursor: pointer;
  color: #af57e9;
}

.login-form {
  display: grid;
  grid-template-columns: 1fr;
  row-gap: 16px;
}

.login-form label {
  display: block;
  margin-bottom: 8px;
}

.login-form input {
  width: 100%;
  padding: 1.2rem;
  border-radius: 9px;
  border: none;
}

.login-form input:focus {
  outline: none;
  box-shadow: 0 0 0 4px rgba(253, 242, 233, 0.5);
}

.btn--form {
  background-color: #f48982;
  color: #fdf2e9;
  align-self: end;
  padding: 8px;
}

.btn,
.btn:link,
.btn:visited {
  display: inline-block;
  text-decoration: none;
  font-size: 20px;
  font-weight: 600;
  border-radius: 9px;
  border: none;

  cursor: pointer;
  font-family: inherit;

  transition: all 0.3s;
}

button {
  outline: 1px solid #f48982;
}

.btn--form:hover {
  background-color: #fdf2e9;
  color: #f48982;
}




.logintext {
  font-size: 52px;
  color: blueviolet;
}

#create-form {
  position: fixed;
  top: 20%;
  left: 37%;
  text-align: center;
  width: 28%;
  border: 2px solid blueviolet;
  padding-left: 2px;
  padding-top: 2px;
  padding-bottom: 17px;
}

.form-control {
  position: relative;
  text-align: center;
  left: 17%;
  width: 65%;
}

.btn {
  position: relative;
  left: -2.7%;
  margin-left: 20px;
}
</style>
