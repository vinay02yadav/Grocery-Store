
<template>
    <div class="containerr">
        <img @click="close" class="cross-img" src="../../assets/cross.png" alt="Close">
        <h2 class="login-title">{{ category_type }} Category</h2>

        <form @submit="onSubmit" class="login-form" autocomplete="off">
            <div>
                <input id="name" type="text" v-model="category"  placeholder="Category Name" name="name" required />
            </div>

            <button class="btn btn--form" type="submit" value="Log in">
                Send Request to Admin
            </button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
import check from '../../utils/refresh_token.js';

export default {
    data() {
        return {
            category: "",
        }
    },

    props: {
        category_type: String,
        category_name: String,
    },

    mounted(){
        this.category = this.category_name
    },

    methods: {
        close() {
            this.$emit('close');
        },

        async onSubmit(e) {
            e.preventDefault();

            if (await check()) {
                await axios.post('http://127.0.0.1:5000/store_manager_dashboard', {
                    original_category:this.category_name,
                    category: this.category,
                    category_type: this.category_type,
                })
                    .then((res) => {
                        if (res.data == 'success') {
                            alert('Request sent')
                        }
                        else {
                            alert('Category already present!')
                        }
                    }).catch((rej) => {
                        console.log(rej)
                        alert('Category already present!')
                    })
            }

        },
    },

};
</script>


<style scoped>
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
    box-shadow: rgb(126 126 126 / 15%) 0px 1.4rem 4.8rem;
    position: fixed;
    display: inline-block;
    z-index: 2;
    top: 25%;
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
    display: block;
    margin-bottom: 8px;
}

.login-form input {
    width: 100%;
    padding: 0.7rem;
    border-radius: 9px;
    border: 1px solid #5f5f60;
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