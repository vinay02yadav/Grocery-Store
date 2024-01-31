<template>
    <Navbar :item_count="item_count" :total_price="total_price" :logged_in="logged_in" :logged_user="logged_user" :changename=false />

    <div v-if="empty_cart" class="shadow_box jumbotron cart">
        <p class="displayy-4">Your Cart Is Empty</p>

        <p class="txtx">Your favourite items are just a click away</p>

        <p class="leaad">
            <a class="customm-btn btn btn-primary btn-lg" @click="goto_home" role="button">Start Shopping</a>
        </p>
    </div>

    <div v-else>
        <div class="shadow_box jumbotron cart">
            <p class="display-4">Your Cart</p>

            <p class="txt">Total Items : {{ item_count }}</p>
            <p class="txt">Total Price : &#8377; {{ total_price }}</p>

            <p class="lead">
                <a class="custom-btn btn btn-primary btn-lg" @click="checkoutt" role="button">Checkout</a>
            </p>
        </div>

        <div class="container">
            <div class="row">
                <div class="MultiCarousel" data-items="1,3,5,6" data-slide="1" id="MultiCarousel" data-interval="1000">
                    <div class="MultiCarousel-inner">
                        <div v-for="product in item_list" class="item">
                            <div class="pad15">
                                <div class="product_image_container">
                                    <img style="width: 100%; height: 100%; border-radius: 10px;" class="productimage"
                                        :src="`${publicPath}${product['image_link']}`" :alt="`${product['name']}`" />
                                </div>

                                <div class="product_name">
                                    <p>{{ product['product_name'] }}</p>
                                </div>

                                <div class="product_quantity">
                                    <p>{{ product['quantity'] }} {{ product['unit'] }}</p>
                                </div>

                                <div class="product_price">
                                    <p>&#8377; {{ product['rate'] }}</p>
                                </div>

                                <div class="add">
                                    <button type="button" :id="`${product['product_name']}+${product['category_name']}`"
                                        @click="addbutton(`${product['product_name']}+${product['category_name']}`, product['rate'])"
                                        class="btn btn-success">ADD</button>


                                    <div class="btn_3"
                                        :id="`${product['product_name']}+${product['category_name']}three_btn`">

                                        <button type="button"
                                            @click="deleteitem(`${product['product_name']}+${product['category_name']}`, product['rate'], 1)"
                                            class="btn my-btn btn-success">-</button>

                                        <button type="button"
                                            :id="`itemcount${product['product_name']}+${product['category_name']}`" disabled
                                            class="btn my-btn btn-success">1</button>

                                        <button type="button"
                                            @click="additem(`${product['product_name']}+${product['category_name']}`, product['rate'])"
                                            class="btn my-btn btn-success">+</button>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import axios from "axios";
import Navbar from "../../components/user_navbar.vue";
import refreshAccessToken, { check } from '../../utils/refresh_token.js';


export default {

    data() {
        return {
            logged_in: false,
            logged_user: 'Login',
            item_list: {},
            item_count: 0,
            total_price: 0,
            empty_cart: false,
            publicPath: process.env.BASE_URL,
        };

    },

    async created() {
        if (await check()) {
            await this.get_cart_item();
            this.button_ready();
        }
    },

    methods: {
        async goto_home() {
            const currentUrl = window.location.href;
            const urlSegments = currentUrl.split("/");
            const id = urlSegments[urlSegments.length - 1];
            await this.$router.push(`/${id}`)
            // window.location.reload();
        },

        out_of_stock(id) {

            let arr = id.split('+')
            const item_list = JSON.parse(localStorage.getItem("item_list"));
            console.log(arr)

            let itemcount = document.getElementById(`itemcount${id}`).innerText;

            for (const products in item_list) {
                console.log(item_list[products])
                console.log(item_list[products]['product_name'])
                // document.getElementById(id).innerText = 'Unavailable'
                //   document.getElementById(id).disabled = true
                if (item_list[products]['product_name'] === arr[0]) {
                    if (item_list[products]['stock'] - item_list[products]['quantity'] * parseInt(itemcount) >= item_list[products]['quantity']) {
                        return false;
                    } else {
                        return true;
                    }
                }

            };
        },

        async addbutton(id, rate) {
            // id.preventDefault()

            if (await check()) {
                if (this.out_of_stock(id)) {
                    document.getElementById(id).innerText = 'Unavailable'
                    document.getElementById(id).disabled = true
                    console.log("done")
                }
                else {
                    document.getElementById(id).style.display = 'none'
                    document.getElementById(`${id}three_btn`).style.display = 'inline-block'


                    let arr = id.split("+")

                    axios.post('http://127.0.0.1:5000/add_cart_item', {
                        product_name: arr[0],
                        category_name: arr[1],
                        item_count: 1,
                    })
                        .then((res) => {
                            if (res.data == 'success') {
                                this.item_count += 1
                                this.total_price += rate
                                // console.log("item added")
                            }
                            else {
                                this.$router.push('/forbidden')
                            }
                        })
                        .catch((rej) => {
                            if (confirm("'Missing token!\nPlease login Again.'")) {
                                this.$router.push('/login')
                            }
                        })
                }

            }
            else {
                if (confirm("Please Login before adding items to cart")) {
                    this.$router.push('/login')
                } else { }
            }
        },

        async additem(id, rate) {

            if (await check()) {
                if (this.out_of_stock(id)) {
                    alert('Cannot Add this item Anymore !')
                }
                else {
                    this.item_count += 1
                    this.total_price += parseInt(rate)

                    let itemcount = document.getElementById(`itemcount${id}`).innerText;
                    document.getElementById(`itemcount${id}`).innerText = parseInt(itemcount) + 1

                    let arr = id.split("+")

                    axios.post('http://127.0.0.1:5000/add_cart_item', {
                        product_name: arr[0],
                        category_name: arr[1],
                        item_count: parseInt(itemcount) + 1,
                    })
                        .then((res) => {
                            console.log("item added")
                        })
                }

            }

            else {
                if (confirm("Please Login before adding items to cart")) {
                    this.$router.push('/login')
                } else { }
            }

        },


        async deleteitem(id, rate, item_count) {
            if (await check()) {
                this.item_count -= 1
                this.total_price -= parseInt(rate)
                let itemcount = document.getElementById(`itemcount${id}`).innerText;

                if (parseInt(itemcount) - 1 == 0) {
                    document.getElementById(id).style.display = 'inline-block'
                    document.getElementById(`${id}three_btn`).style.display = 'none'
                }
                else {
                    document.getElementById(`itemcount${id}`).innerText = parseInt(itemcount) - 1
                }

                let arr = id.split("+")

                axios.delete(`http://127.0.0.1:5000/delete_cart_item/${arr[1]}/${arr[0]}/${item_count}`)
                    .then((res) => {
                        console.log("item deleted")
                    })
            }
            else {
                if (confirm("Please Login before deleting items in cart")) {
                    this.$router.push('/login')
                } else { }
            }

        },

        async get_cart_item() {
            await axios.get('http://127.0.0.1:5000/add_cart_item')
                .then((res) => {
                    console.log(this.publicPath)
                    if (res.data['data'] == 'empty') {
                        this.empty_cart = true
                        this.logged_user = res.data['user']
                        this.logged_in = true
                    }
                    else {
                        this.logged_user = res.data['user']
                        this.logged_in = true
                        this.item_list = res.data['message']
                        localStorage.setItem('item_list', JSON.stringify(this.item_list));


                        const item_list = JSON.parse(localStorage.getItem("item_list"));
                        // console.log(item_list)

                        for (const products in item_list) {
                            if (item_list[products]['stock'] == 0) {
                                let id = `${item_list[products]['name']}+${products}`
                                document.getElementById(id).innerText = 'Out of Stock'
                                document.getElementById(id).style.backgroundColor = '#e94242'
                                document.getElementById(id).style.borderColor = "#e94242"
                                document.getElementById(id).disabled = true
                            }
                        };
                    }
                });

        },

        async button_ready() {
            try {
                await axios.get('http://127.0.0.1:5000/add_cart_item')
                    .then((res) => {
                        this.logged_user = res.data['user']
                        this.logged_in = true
                        let item_arr = res.data['message']
                        console.log(item_arr)

                        for (let i = 0; i < item_arr.length; i++) {
                            let id = `${item_arr[i]['product_name']}+${item_arr[i]['category_name']}`
                            // console.log(item_arr[i]['stock'] - item_arr[i]['quantity'] * item_arr[i]['item_count'] )

                            let out_of_stock = item_arr[i]['stock'] - item_arr[i]['quantity'] * item_arr[i]['item_count']

                            if (out_of_stock >= 0) {
                                document.getElementById(id).style.display = 'none'
                                document.getElementById(`${id}three_btn`).style.display = 'inline-block'

                                this.item_count += item_arr[i]['item_count']
                                this.total_price += item_arr[i]['rate'] * item_arr[i]['item_count']

                                document.getElementById(`itemcount${id}`).innerText = item_arr[i]['item_count']
                            }
                            else {
                                this.deleteitem(id, item_arr[i]['rate'], item_arr[i]['item_count'])
                            }
                        }
                    })
            } catch (error) { }

        },

        async checkoutt() {
            if (await check()) {
                await axios.get('http://127.0.0.1:5000/checkout')
                    .then((res) => {
                        alert("Thank you for shopping !\n\nYour Items will be delivered shortly.")
                        window.location.reload()
                    })
                    .catch((rej) => { })
            }
            else {
                if (confirm("Please Login before adding items to cart")) {
                    this.$router.push('/login')
                }
            }
        },

    },

    components: {
        Navbar,
    },


};

</script>
  
<style scoped>
/* @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300&display=swap');  font-family: 'Kanit', sans-serif; */
/* @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Linear+B&family=Roboto:ital,wght@1,300&display=swap');font-family: 'Noto Sans Linear B', sans-serif; */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Linear+B&family=Roboto:ital,wght@1,300&family=Skranji&display=swap');

.my-btn {
    border-radius: 0px;
    justify-content: center;
    height: 29px;
    align-items: center;
    display: inline-flex;
}

.btn_3 {
    width: auto;
    display: none;
    position: relative;
    top: 9px;
    right: 5px;
}

.category_name {
    font-family: 'Kanit', sans-serif;
    position: absolute;
    font-size: 37px;
    left: 8%;
    color: #d9d4d4;
}

.categories {
    /* border: 2px solid red; */
    height: 336px;
    width: 88%;
    overflow: hidden;
    display: inline-flex;
    background-color: rgb(87, 82, 82);
    /* border: 1px solid rgb(221, 221, 221); */
    box-shadow: rgba(0, 0, 0, 0.2) 2px 2px 5px;
    margin: 10px;
    padding: 10px;
    opacity: 0.8;
    border-radius: 27px;
}

.add {
    width: auto;
    position: relative;
    left: 39px;
    display: inline-block;
    bottom: 39px;
    height: 34px;
}

.product_name {
    /* border: 1px solid lightgreen; */
    justify-content: center;
    width: 106%;
    /* border: 1px solid lightgreen; */
    display: inline-flex;
    right: 3%;
    position: relative;
    font-size: 18px;
    height: 44px;
    font-family: 'Roboto', sans-serif;
}

.product_quantity {
    width: 41%;
    /* border: 1px solid rgb(13, 102, 235); */
    right: 1%;
    position: relative;
    font-size: 13px;
    height: 22px;
    bottom: 2px;
    font-family: 'Roboto', sans-serif;
    color: rgb(236 234 231);
    font-weight: 500;

}

.product_price {
    width: 40%;
    /* border: 1px solid rgb(213, 235, 13); */
    right: 3%;
    position: relative;
    height: 22px;
    margin-top: 4px;
    font-size: 15px;
    font-family: 'Roboto', sans-serif;
    color: white;
    font-weight: 500;
}

.product_image_container {
    /* border: 1px solid blue; */
    width: 84%;
    position: relative;
    display: inline-block;
    align-items: center;
    height: 56%;
}

.productimage {
    width: 73%;
    height: 94%;
}

.container {
    max-width: 1140px;
}



.MultiCarousel {
    float: left;
    padding: 15px;
    width: 100%;
    position: relative;
    margin-top: 45px;
    border: 2px solid rgb(113, 113, 111);
    background-color: #3d3f3f;
    border-radius: 16px;
}


.MultiCarousel .MultiCarousel-inner {
    transition: 1s ease all;
    float: left;
}

.MultiCarousel .MultiCarousel-inner .item {
    width: 350px;
    float: left;
    height: 275px;
    width: 216px;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    /* border: 1px solid blue; */
}

.MultiCarousel .MultiCarousel-inner .item>div {
    text-align: center;
    padding: 10px;
    margin: 10px;
    height: 250px;
    border-radius: 10px;
    background: #f1f1f1;
    color: #666;
    width: 192px;
}









.txt {
    font-size: 22px;
    display: inline-block;
    width: 20%;
    position: relative;
    font-family: 'Kanit', sans-serif;
    color: rgb(202 0 250) !important;
}

.txtx {
    font-size: 22px;
    display: block;
    width: auto;
    position: relative;
    font-family: 'Kanit', sans-serif;
    color: rgb(202 0 250) !important;
    margin-top: 50px;
    left: 2%;
}

.custom-btn {
    position: relative;
    padding-left: 40px;
    padding-right: 40px;
}

.customm-btn {
    position: relative;
    padding-left: 40px;
    padding-right: 40px;
}

.shadow_box {
    background-color: rgb(40 42 44);
    box-shadow: rgb(79 74 74) 2px 5px 6px;
    border-radius: 8px;
}

.shadow {
    background-color: rgb(57 59 62);
    border-radius: 8px;
}

.cart {
    margin-top: 35px;
    display: inline-block;
    width: 75%;
    position: relative;
}

.lead {
    font-size: 1.25rem;
    display: inline-block;
    position: relative;
    left: 19%;
    font-weight: 300;
}

.leaad {
    font-size: 1.25rem;
    display: inline-block;
    position: relative;
    left: 2%;
    font-weight: 300;
}

.display-4 {
    font-size: 35px;
    position: relative;
    margin-left: 35px;
    margin-top: 10px;
    font-family: 'Skranji', cursive;
    display: flex;
    color: rgb(55 127 200);
}

.displayy-4 {
    font-size: 35px;
    position: relative;
    margin-left: 35px;
    margin-top: 10px;
    font-family: 'Skranji', cursive;
    display: flex;
    color: rgb(55 127 200);
    justify-content: center;
}
</style>
  
  