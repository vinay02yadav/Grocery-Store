<template>
  <adminNavbar id="navbar" />
  <p v-if="no_item" id="txtcat" class="txtcat">No Products to show !</p>

  <section id="container" v-else>
    <div class="">
      <div class="row d-flex justify-content-center align-items-center">
        <div class="col col-lg-9 col-xl-7">
          <div class="card rounded-3">
            <div class="card-body p-4">

              <h4 class="text-center my-3 pb-3 hide">Products</h4>

              <table class="table mb-4">
                <thead class="hide">
                  <tr> <!-- name expiry rate quantity unit stock -->
                    <th scope="col">S.No</th>
                    <th scope="col">Product Name</th>
                    <th scope="col">Rate</th>
                    <th scope="col">Quantity</th>
                    <th scope="col">Stock</th>
                    <th scope="col">Expiry</th>
                    <th scope="col">Actions</th>
                  </tr>

                </thead>
                <tbody>
                  <tr v-for="(items, index) in item_list">
                    <td class="hide">{{ index + 1 }}</td>
                    <td class="hide">{{ items['name'] }}</td>
                    <td class="hide">{{ items['rate'] }}</td>
                    <td class="hide">{{ items['quantity'] }} {{ items['unit'] }}</td>
                    <td class="hide">{{ items['stock'] }}</td>
                    <td class="hide">{{ items['expiry'] }}</td>

                    <td class="btn_combo hide">
                      <button @click="toggle_category(`${items['name']}+${items['rate']}+${items['quantity']}+${items['unit']}+${items['stock']}+${items['expiry']}`)" class="btn btn-success ms-1">Edit</button>
                      <button @click="del_product(`${items['name']}`)" class="btn btn-danger">Delete</button>
                    </td>
                    
                  </tr>
                </tbody>
              </table>

            </div>
          </div>
        </div>
      </div>
    </div>
  </section>


  <Edit_Product v-if="edit_product" @close="toggle_category" :product_name="product_name" :rate="rate" :quantity="quantity" :unit="unit" :stock="stock" :expiry="expiry" :category_name="category_name" class="pop" />

  <Add_Product v-if="add_product" :category_name="category_name" @close="toggle_product" class="pop" />

  <div>
    <a @click="toggle_product"><img class="plus hide" id="plus" src="../../assets/plus.png" /></a>
  </div>
</template>
    
<script>
import axios from "axios";
import adminNavbar from "../../components/admin_navbar.vue";
import Edit_Product from "../../components/product/edit_product.vue";
import Add_Product from "../../components/product/add_product.vue";
import check from '../../utils/refresh_token.js';


export default {

  data() {
    return {
      item_list: [],
      edit_product: false,
      add_product: false,
      no_item: false,
      category_name:"",

      product_name: "",
      rate: 0,
      quantity: "",
      unit: "",
      stock: 0,
      expiry: "",
    };

  },


 async mounted() {
    const currentUrl = window.location.href;
    const urlSegments = currentUrl.split("/");
    let category = urlSegments[urlSegments.length - 3];
    this.category_name = decodeURIComponent(category);

    if (await check()) {
      this.get_item_dashboard()
    }
  },

  methods: {
    toggle_category(id) {
      this.edit_product = !this.edit_product

      if (this.edit_product) {
        let arr = id.split('+')
        this.product_name = arr[0]
        this.rate = parseInt(arr[1])
        this.quantity = parseInt([2])
        this.unit = arr[3]
        this.stock = parseInt(arr[4])
        this.expiry = arr[5]

        const elements = document.getElementsByClassName("hide");
        for (let i = 0; i < elements.length; i++) {
          elements[i].style.filter = 'blur(4px)';
          elements[i].style.pointerEvents = 'none';
        }

        document.getElementById('navbar').style.filter = 'blur(4px)'
        document.getElementById('navbar').style.pointerEvents = 'none'
        document.getElementById('plus').style.filter = 'blur(4px)'
        document.getElementById('plus').style.pointerEvents = 'none'
        document.body.style.overflow = "hidden";
      }
      else {
        const elements = document.getElementsByClassName("hide");
        for (let i = 0; i < elements.length; i++) {
          elements[i].style.filter = 'blur(0px)';
          elements[i].style.pointerEvents = 'auto';
        }

        document.getElementById('navbar').style.filter = 'blur(0px)'
        document.getElementById('navbar').style.pointerEvents = 'auto'
        document.getElementById('plus').style.filter = 'blur(0px)'
        document.getElementById('plus').style.pointerEvents = 'auto'
        document.body.style.overflow = "none";
      }

    },


    toggle_product() {
      this.add_product = !this.add_product

      if (this.add_product) {

        const elements = document.getElementsByClassName("hide");
        for (let i = 0; i < elements.length; i++) {
          elements[i].style.filter = 'blur(4px)';
          elements[i].style.pointerEvents = 'none';
        }

        document.getElementById('navbar').style.filter = 'blur(4px)'
        document.getElementById('navbar').style.pointerEvents = 'none'
        document.getElementById('plus').style.filter = 'blur(4px)'
        document.getElementById('plus').style.pointerEvents = 'none'
        document.body.style.overflow = "hidden";
      }
      else {

        const elements = document.getElementsByClassName("hide");
        for (let i = 0; i < elements.length; i++) {
          elements[i].style.filter = 'blur(0px)';
          elements[i].style.pointerEvents = 'auto';
        }

        document.getElementById('navbar').style.filter = 'blur(0px)'
        document.getElementById('navbar').style.pointerEvents = 'auto'
        document.getElementById('plus').style.filter = 'blur(0px)'
        document.getElementById('plus').style.pointerEvents = 'auto'
        document.body.style.overflow = "none";
      }

    },

    async get_item_dashboard() {
      await axios.get(`http://127.0.0.1:5000/${this.category_name}/products`)
        .then((res) => {
          this.item_list = res.data.list;
          this.item_list = JSON.parse(JSON.stringify(this.item_list));
          // console.log(this.item_list)
          // this.logged_user = res.data.identity;
          if (this.item_list.length == 0) { this.no_item = true }
        }).catch((rej) => { console.log(rej) })


    },

    async del_product(product_name){
      if(confirm('Do you want to Delete this Item ?')){
        await axios.delete(`http://127.0.0.1:5000/${this.category_name}/${product_name}/products`)
          .then((res) => {
            window.location.reload()
          }).catch((rej) => { console.log(rej) })
      }
      else{}
    },

  },

  components: {
    Edit_Product,
    Add_Product,
    adminNavbar,
  },


};


</script>
    
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Linear+B&family=Roboto:ital,wght@1,300&display=swap');

* {
  margin: 0;
  padding: 0;
}

html {
  scroll-behavior: smooth;
}
.pop{
  z-index: 10;
}
.col-xl-7 {
  width: 85.333333%;
}

.txt {
  font-size: 26px;
  position: relative;
  margin-bottom: 60px;
  font-family: cursive;

}

.btn {
  margin-right: 10px;
}

section {
  margin-top: 4%;

}

.bottom {
  margin-bottom: 8%;
}

.rounded-3 {
  border: 3px solid #8442a7;
  ;
}

.txtcat {
  margin-top: 4%;
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
  /* box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); */
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
  font-size: 18px;
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
}</style>