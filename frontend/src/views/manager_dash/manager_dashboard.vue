<template>
  <adminNavbar id="navbar" />
  <p v-if="no_item" id="txtcat" class="txtcat">There is no Category yet !</p>
  <p v-else id="txtcat" class="txtcat">Categories</p>

  <div id="container" class="container">
    <ul>

      <li v-for="item in item_list">
        <div class="yo">
          <div class="venue">{{ item }}</div>

          <form>
            <button class="btn btn-outline-primary shows" @click="product(`${item}`)">
              Products on this Category
            </button>

            <button class="btn btn-outline-warning edit" @click="toggle_category(`Edit+${item}`)">
              Edit
            </button>

            <button class="btn btn-outline-danger delete" @click="del_item(`${item}`)">
              Delete
            </button>
          </form>
        </div>
      </li>
    </ul>
  </div>


  <Edit_Category v-if="edit_category" @close="toggle_category" class="popup" :category_type="category_type"
    :category_name="category_name" />


  <div>
    <a @click="toggle_category('Add')"><img class="plus" id="plus" src="../../assets/plus.png" /></a>
  </div>
</template>
  
<script>
import axios from "axios";
import adminNavbar from "../../components/admin_navbar.vue"
import Edit_Category from "../../components/category/edit_category.vue";
import check from '../../utils/refresh_token.js';


export default {

  data() {
    return {
      item_list: {},
      edit_category: false,
      no_item: false,
      category_type: "",
      category_name: "",
      id: 0,
    };

  },

  async mounted() {
    if (await check()) {
      this.get_item_dashboard()
    }
  },

  methods: {
    async del_item(item) {
      item.preventDefault

      if (await check()) {
        console.log(1)
        await axios.put('http://127.0.0.1:5000/store_manager_dashboard', {
          category: item,
        })
          .then((res) => {
            if (res.data == 'success') {
              alert('Request sent !')
            }
            else {
              alert('Request for deleting this item have alreeady been sent !')
            }

          })
          .catch((rej) => {
            console.log(rej)
            alert('Request have already been sent !')
          })
      }
    },

    toggle_category(category_type) {

      this.edit_category = !this.edit_category

      try {
        let arr = category_type.split('+');
        this.category_type = arr[0];
        this.category_name = arr[1];
      }
      catch { this.category_name = '' }

      if (this.edit_category) {
        document.getElementById('container').style.filter = 'blur(4px)'
        document.getElementById('container').style.pointerEvents = 'none'
        document.getElementById('navbar').style.filter = 'blur(4px)'
        document.getElementById('navbar').style.pointerEvents = 'none'
        document.getElementById('plus').style.filter = 'blur(4px)'
        document.getElementById('plus').style.pointerEvents = 'none'
        document.getElementById('txtcat').style.filter = 'blur(4px)'
        document.getElementById('txtcat').style.pointerEvents = 'none'
        document.body.style.overflow = "hidden";
      }
      else {
        document.getElementById('container').style.filter = 'blur(0px)'
        document.getElementById('container').style.pointerEvents = 'auto'
        document.getElementById('navbar').style.filter = 'blur(0px)'
        document.getElementById('navbar').style.pointerEvents = 'auto'
        document.getElementById('plus').style.filter = 'blur(0px)'
        document.getElementById('plus').style.pointerEvents = 'auto'
        document.getElementById('txtcat').style.filter = 'blur(0px)'
        document.getElementById('txtcat').style.pointerEvents = 'auto'
        document.body.style.overflow = "none";
      }

    },


    product(id) {
      const currentUrl = window.location.href;
      const urlSegments = currentUrl.split("/");
      this.id = urlSegments[urlSegments.length - 1];
      console.log(this.id)
      this.$router.push(`/${id}/products/${this.id}`)
    },


    async get_item_dashboard() {
      console.log("checking")
      await axios.get("http://127.0.0.1:5000/store_manager_dashboard")
        .then((res) => {
          this.item_list = res.data.list;
          this.logged_user = res.data.identity;
          if (this.item_list.length == 0) { this.no_item = true }
        }).catch((rej) => { console.log(rej) })


    },

  },

  components: {
    Edit_Category,
    adminNavbar,
  },


};


</script>
  
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Linear+B&family=Roboto:ital,wght@1,300&display=swap');




.txtcat {
  font-family: "Alkatra", cursive;
  font-size: 30px;
}

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
}


.body {
  height: 100%;
  overflow-x: hidden;
}

.bg-body-tertiary {
  --darkreader-bg--bs-bg-opacity: 1;
  background-color: #8a2be2 !important;
}

.navbar-expand-lg .navbar-nav {
  flex-direction: row;
  left: 78%;
  position: relative;
}

.textt {
  left: 43%;
  position: relative;
  top: 23%;
  margin-top: 2%;
  display: inline-block;
  font-size: 29px;
}

.yo {
  width: 100%;
  height: 100%;
  position: relative;
}

.container {
  width: 96%;
  position: relative;
  display: block;
  top: 42%;
  margin: auto;
  background-image: linear-gradient(-225deg,
      rgb(201, 0, 96) 0%,
      rgb(57, 36, 133) 48%,
      rgb(0, 105, 158) 100%) !important;
  overflow: hidden;
  background: skyblue;
  margin-top: 50px;
  border-radius: 15px;
}

.container ul {
  padding: 0px;
  margin: 0px;
}

.container ul li {
  float: left;
  list-style: none;
  width: 20%;
  height: 180px;
  box-shadow: #0c0b0b 20px 19px 21px -7px !important;
  background-color: rgb(30, 32, 33) !important;
  margin: 20px 0px 20px 55px;
  box-sizing: border-box;
  border-radius: 15px;
}

.container ul li .bottom {
  width: 19%;
  height: 260px;
  line-height: 50px;
  background: blue;
  text-align: center;
  color: white;
  font-size: 20px;
}

.plus {
  position: relative;
  padding-top: 3%;
  width: 6%;
  padding-bottom: 3%;
}

.venue {
  width: 79%;
  font-family: "Alkatra", cursive;
  word-wrap: break-word;
  text-align: center;
  position: relative;
  left: 10%;
  font-size: 22px;
  margin-top: 4%;
  margin-bottom: 1%;
  overflow: hidden;
}

.text {
  font-family: "Montserrat", sans-serif;
  left: 31%;
  position: relative;
  margin-top: 7%;
  color: whitesmoke;
}

.edit {
  position: absolute;
  left: 18%;
  bottom: 11%;
  flex-direction: row;
}

.delete {
  position: absolute;
  left: 52%;
  bottom: 11%;
  flex-direction: row;
}

.shows {
  position: absolute;
  left: 9%;
  bottom: 40%;
  flex-direction: row;
}

@media screen and (max-width: 1250px) {
  .container ul li {
    width: 40%;
    margin-left: 40px;
  }
}
</style>