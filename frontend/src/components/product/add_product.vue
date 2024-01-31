<template>
    <div class="containerr">
        <img @click="close" class="cross-img" src="../../assets/cross.png" alt="Close">
        <h2 class="login-title">Add Product</h2>

        <form @submit="onSubmit" class="login-form" autocomplete="off">
            <div class="form-group">
                <label for="name">Product name :</label>
                <input id="name" type="text" name="name" required />
            </div>
            <div class="form-group">
                <label for="rate">Rate :</label>
                <input id="rate" type="number" min="0" name="rate" required />
            </div>
            <div class="form-group">
                <label for="unit">Unit :</label>
                <div class="dropdown-container">
                    <select class="dropdown-select" id="myDropdown" @change="quantity_change">
                        <option value="g">Rs / gram</option>
                        <option value="Kg">Rs / Kilogram</option>
                        <option value="L">Rs / Litre</option>
                        <option value="mL">Rs / Mililitre</option>
                        <option value="Dz">Rs / Dozen</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label for="quantity">Quantity :</label>

                <input id="quantity" type="number" min="0" name="quantity" required
                    style="border-bottom-right-radius: 0px; border-top-right-radius: 0px;" />

                <input
                    style="display: inline-block; width: 16%; border-bottom-left-radius: 0px; border-top-left-radius: 0px; border-left: 1px solid #746e6e;"
                    type="text" :value="unit_tag" disabled>
            </div>

            <div class="form-group">
                <label for="stock">Stock :</label>

                <input id="stock" type="number" name="stock" min="0" required
                    style="border-bottom-right-radius: 0px; border-top-right-radius: 0px;" />

                <input
                    style="display: inline-block; width: 16%; border-bottom-left-radius: 0px; border-top-left-radius: 0px; border-left: 1px solid #746e6e;"
                    type="text" :value="unit_tag" disabled>
            </div>
            <div class="form-group">
                <label for="expiry">Expiry :</label>
                <input id="expiry" type="date" min="" name="expiry"  />
            </div>

            <button class="btn btn--form" type="submit" value="Log in">
                Submit
            </button>
        </form>
    </div>
</template>


<script>
import axios from 'axios';
import check from "../../utils/refresh_token.js";

export default {
    data() {
        return {
            category: "",
            original_product_name: "",
            quantity_tag: "",
            stock_tag: "",
            unit_tag: "",
        }
    },
    props: {
        category_name: String,
    },

    mounted() {
        this.quantity_change()
        document.getElementById("expiry").min = new Date().toISOString().split("T")[0];
    },

    methods: {

        quantity_change() {
            const dropdown = document.getElementById("myDropdown");
            const selectedOption = dropdown.options[dropdown.selectedIndex];
            this.unit_tag = selectedOption.value;
            console.log(this.unit_tag)
        },

        close() {
            this.$emit('close');
        },

        async onSubmit(e) {
            e.preventDefault();

            if (check()) {
                var dropdown = document.getElementById("myDropdown");
                var selectedOption = dropdown.options[dropdown.selectedIndex];
                var unit = selectedOption.value;
                console.log(unit)
                console.log(this.category_name)

                let product_name = document.getElementById('name').value;
                let rate = document.getElementById('rate').value;
                let quantity = document.getElementById('quantity').value;
                let stock = document.getElementById('stock').value;
                let expiry = document.getElementById('expiry').value;

                await axios.post('http://127.0.0.1:5000/products', {
                    category_name: this.category_name,
                    product_name: product_name,
                    rate: rate,
                    quantity: quantity,
                    unit: unit,
                    stock: stock,
                    expiry: expiry
                })
                    .then((res) => {
                        if (res.data == 'success') {
                            axios.post('http://127.0.0.1:5000/get-img', { name: product_name, }).then(
                                (res) => { console.log("image started") }
                            )
                            alert('Done')
                            window.location.reload()
                        }
                        else {
                            alert('Product already present!')
                        }
                    }).catch((rej) => {
                        console.log(rej)
                        alert('Please Login Again !')
                    })


            }

        },
    },

};
</script>




<style scoped>
.form-group {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
}

.form-group label {
    width: 120px;
    /* Adjust the width as needed */
    font-family: cursive;
    margin-right: 18px;
}

.dropdown-container {
    flex: 1;
    position: relative;
}

.dropdown-select {
    width: 100%;
    /* Make the dropdown fill the available space */
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #fff;
    font-size: 16px;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
}

.dropdown-select option {
    padding: 10px;
}

.dropdown-container::after {
    content: '\25BC';
    position: absolute;
    top: 50%;
    right: 8px;
    transform: translateY(-50%);
    pointer-events: none;
}

.cross-img {
    width: 30px;
    position: absolute;
    top: -13px;
    right: -16px;
}

.containerr {
    width: 400px;
    margin: auto;
    padding: 36px 48px 48px 48px;
    border-radius: 11px;
    background-color: rgb(46 45 45);
    box-shadow: rgba(128, 106, 98, 0.15) 4px 1rem 1.7rem;
    position: fixed;
    display: inline-block;
    z-index: 2;
    top: 6%;
    z-index: 2;
    left: 37%;
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
    display: inline-block;
    margin-bottom: 8px;
    margin-right: 18px;
    font-family: cursive;
}

.login-form input {
    width: 50%;
    padding: 0.7rem;
    border-radius: 9px;
    border: none;
    display: inline-block;
    text-align: center;
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
</style>





