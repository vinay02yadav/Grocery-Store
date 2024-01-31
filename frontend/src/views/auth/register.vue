<template>
  <div class="container">
    <h2 class="login-title">Register</h2>

    <form @submit="validate" class="login-form" autocomplete="off">
      <div>
        <input id="name" @input="check_username" type="email" v-model="username" placeholder="Email" name="name"
          required />
      </div>
      <p id="name_text">Not a valid Email</p>

      <div>
        <input @input="check_password" id="password" type="password" placeholder="password" v-model="password"
          name="password" required />
      </div>
      <p id="name_text2">Password must contain capital letter, a digit, a special character and at least length of 8 </p>

      <div>
        <input @input="check_password_is_equal" id="check_password" type="text" placeholder="confirm password"
          name="passord" required />
      </div>
      <p id="name_text3">Password must be same</p>

      <p class="ttet">Role for your Account</p>
      <div id="myForm" class="containerrr">
        <div class="selector">
          <div class="selector-item">
            <input type="radio" id="radio1" name="selector" value="user" class="selector-item_radio" checked>
            <label for="radio1" class="selector-item_label">User</label>
          </div>
          <div class="selector-item">
            <input type="radio" id="radio2" value="manager" name="selector" class="selector-item_radio">
            <label for="radio2" class="selector-item_label">Manager</label>
          </div>
        </div>
      </div>

      <button class="btn btn--form" type="submit" value="Log in">
        Register
      </button>

      <p class="text1">Already have an account? <a class="text2" @click="login">Login</a> </p>

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

    async validate(e) {
      e.preventDefault();
      const role = document.querySelector('input[name="selector"]:checked').value
      const username = document.getElementById('name').value;
      const isValid_username = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(username);

      const password = document.getElementById('password').value;
      const isValid_password = /^(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\-])(?=.*\d).{8,}$/.test(password);

      const password2 = document.getElementById('check_password').value;


      if (isValid_username && isValid_password && password === password2) {
        if (role == 'user') {
          await axios.post('http://127.0.0.1:5000/api/register', {
            username: this.username,
            password: this.password,
          }).then((res) => {
            console.log(res.data['status'])

            if (res.data['status'] == 'success') {
              alert("Account created Successfully !")
              this.$router.push('/login')
            }
            else if (res.data['status'] == 'confirm_link_send') {
              alert('A confirmation email has been sent.\n Please check your inbox.')
            }
            else if (res.data['status'] == 'no such email') {
              alert('Email not found')
            }
            else {
              if (confirm("Account is Already registered.\nDo you want to sign in")) {
                this.$router.push('/login')
              }
            }
          })
        }
        else {
          await axios.post('http://127.0.0.1:5000/new_manager', {
            username: this.username,
            password: this.password,
          })
            .then((res) => {
              if (res.data == 'success') {
                alert('Request sent to Admin')
              }
              else if (res.data == 'already present') {
                alert('Request had already been sent !\n Please Wait...')
              }
              else if (res.data['status'] == 'confirm_link_send') {
                alert('A confirmation email has been sent.\n Please check your inbox.')
              }
              else if (res.data['status'] == 'no such email') {
                alert('Email not found')
              }

              else {
                if (confirm("Account is Already registered.\nDo you want to sign in")) {
                  this.$router.push('/login')
                }
              }
            }).catch((rej) => {
              console.log(rej)
              alert('User already present!')
            })
        }

      }
    },

    check_username() {
      document.getElementById('name_text').style.display = 'inline-block';
      const username = document.getElementById('name').value;
      const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(username);
      if (isValid) {
        document.getElementById('name').style.border = '2px solid lightgreen';
        document.getElementById('name_text').style.display = 'none';
      }
      else {
        document.getElementById('name').style.border = '2px solid red';
      }
      if (username == '') {
        document.getElementById('name').style.border = 'none';
        document.getElementById('name_text').style.display = 'none';
      }
    },

    check_password() {
      document.getElementById('name_text2').style.display = 'inline-block';
      const password = document.getElementById('password').value;
      const isValid = /^(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\-])(?=.*\d).{8,}$/.test(password);
      if (isValid) {
        document.getElementById('password').style.border = '2px solid lightgreen';
        document.getElementById('name_text2').style.display = 'none';
      }
      else {
        document.getElementById('password').style.border = '2px solid red';
      }
      if (password == '') {
        document.getElementById('password').style.border = 'none';
        document.getElementById('name_text2').style.display = 'none';
      }
    },


    check_password_is_equal() {
      document.getElementById('name_text3').style.display = 'inline-block';
      const password = document.getElementById('password').value;
      const password2 = document.getElementById('check_password').value;

      if (password === password2) {
        document.getElementById('check_password').style.border = '2px solid lightgreen';
        document.getElementById('name_text3').style.display = 'none';
      }
      else {
        document.getElementById('check_password').style.border = '2px solid red';
      }
      if (password2 == '') {
        document.getElementById('check_password').style.border = 'none';
        document.getElementById('name_text3').style.display = 'none';
      }
    },

    register() {
      this.$router.push('/register')
    },
    login() {
      this.$router.push('/login')
    },

  },
};
</script>
  
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Linear+B&family=Roboto:ital,wght@1,300&family=Skranji&display=swap');


@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap");

.ttet {
  margin-top: 23px;
  font-size: 17px;
  font-family: 'Skranji', cursive;
}

.containerrr {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

:root {
  --white: #fff;
  --smoke-white: #f1f3f5;
  --blue: #4169e1;
}

.selector {
  position: relative;
  width: 60%;
  background-color: var(--smoke-white);
  height: 60px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  border-radius: 9999px;
  box-shadow: 0 0 16px rgba(0, 0, 0, 0.2);
}

.selector-item {
  position: relative;
  flex-basis: calc(70% / 3);
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.selector-item_radio {
  appearance: none;
  display: none;
}

.selector-item_label {
  position: relative;
  height: 93%;
  width: 100%;
  text-align: center;
  border-radius: 9999px;
  line-height: 400%;
  font-family: "Poppins", sans-serif;
  font-weight: 700;
  transition-duration: 0.5s;
  transition-property: transform, box-shadow;
  transform: none;
}

.selector-item_radio:checked+.selector-item_label[data-v-0dfcf280] {
  background-color: var(--blue);
  color: var(--white);
  box-shadow: rgb(232 0 255 / 86%) 0px 0px 8px, rgb(12, 0, 0) 0px 3px 3px;
  vertical-align: middle;
  position: relative;
  transform: translateY(-2px);
  justify-content: center;
  display: inline-flex;
  height: 41px;
  padding-right: 15px;
  padding-left: 15px;
  border: 1px solid #9300ff;
  top: 5px;
  align-items: center;
}

@media (max-width: 480px) {
  .selector {
    width: 90%;
  }
}










#name_text {
  font-size: 12px;
  color: red;
  display: none;
}

#name_text2 {
  font-size: 12px;
  color: red;
  display: none;
}

#name_text3 {
  font-size: 12px;
  color: red;
  display: none;
}

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

.btn {
  margin-top: 20px;
}

.container {
  width: 400px;
  margin: auto;
  margin-top: 5vh;
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
  box-shadow: 0 0 0 1px rgba(106, 105, 105, 0.5);
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
  