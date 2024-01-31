<template>
    <adminNavbar />

    <div v-if="manager || edit_category || delete_category || addd_category"></div>
    <div v-else class="pp">Nothing to show !</div>

    <section v-if="addd_category">
        <div class="">
            <div class="row d-flex justify-content-center align-items-center">
                <div class="col col-lg-9 col-xl-7">
                    <div class="card rounded-3">
                        <div class="card-body p-4">

                            <h4 class="text-center my-3 pb-3">Requests for Adding Categories</h4>

                            <table class="table mb-4">
                                <thead>
                                    <tr>
                                        <th scope="col">S.No</th>
                                        <th scope="col">Category Name</th>
                                        <th scope="col">Manager Name</th>
                                        <th scope="col">Actions</th>
                                    </tr>

                                </thead>
                                <tbody>
                                    <tr v-for="(items, index) in category_add_list">
                                        <th scope="row">{{ index + 1 }}</th>
                                        <td>{{ items[0] }}</td>
                                        <td>{{ items[1] }}</td>
                                        <td class="btn_combo">
                                            <button @click="del_category(`${items[0]}`)"
                                                class="btn btn-danger">Delete</button>
                                            <button @click="add_category(`${items[0]}`)"
                                                class="btn btn-success ms-1">Accept</button>
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


    <section v-if="edit_category">
        <div class="">
            <div class="row d-flex justify-content-center align-items-center">
                <div class="col col-lg-9 col-xl-7">
                    <div class="card rounded-3">
                        <div class="card-body p-4">

                            <h4 class="text-center my-3 pb-3">Requests for Editing Categories</h4>

                            <table class="table mb-4">
                                <thead>
                                    <tr>
                                        <th scope="col">S.No</th>
                                        <th scope="col">Original Category Name</th>
                                        <th scope="col">Requested Category Name</th>
                                        <th scope="col">Manager Name</th>
                                        <th scope="col">Actions</th>
                                    </tr>

                                </thead>
                                <tbody>
                                    <tr v-for="(items, index) in category_edit_list">
                                        <th scope="row">{{ index + 1 }}</th>
                                        <td>{{ items[1] }}</td>
                                        <td>{{ items[0] }}</td>
                                        <td>{{ items[2] }}</td>
                                        <td class="btn_combo">
                                            <button @click="del_category(`${items[0]},${items[1]}`)"
                                                class="btn btn-danger">Delete</button>
                                            <button @click="update_category(`${items[0]}+${items[1]}`)"
                                                class="btn btn-success ms-1">Accept</button>
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


    <section v-if="delete_category">
        <div class="">
            <div class="row d-flex justify-content-center align-items-center">
                <div class="col col-lg-9 col-xl-7">
                    <div class="card rounded-3">
                        <div class="card-body p-4">

                            <h4 class="text-center my-3 pb-3">Requests for Deleting Categories</h4>

                            <table class="table mb-4">
                                <thead>
                                    <tr>
                                        <th scope="col">S.No</th>
                                        <th scope="col">Category Name</th>
                                        <th scope="col">Manager Name</th>
                                        <th scope="col">Actions</th>
                                    </tr>

                                </thead>
                                <tbody>
                                    <tr v-for="(items, index) in category_delete_list">
                                        <th scope="row">{{ index + 1 }}</th>
                                        <td>{{ items[0] }}</td>
                                        <td>{{ items[1] }}</td>
                                        <td class="btn_combo">
                                            <button @click="del_category(`${items[0]}`)"
                                                class="btn btn-danger">Delete</button>
                                            <button @click="accept_del_category(`${items[0]}+`)"
                                                class="btn btn-success ms-1">Accept</button>
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


    <section v-if="manager">
        <div class="">
            <div class="row d-flex justify-content-center align-items-center">
                <div class="col col-lg-9 col-xl-7">
                    <div class="card rounded-3">
                        <div class="card-body p-4">

                            <h4 class="text-center my-3 pb-3">Requests for Adding Managers</h4>

                            <table class="table mb-4">
                                <thead>
                                    <tr>
                                        <th scope="col">S.No</th>
                                        <th scope="col">Manager Name</th>
                                        <th scope="col">Actions</th>
                                    </tr>

                                </thead>
                                <tbody>
                                    <tr v-for="(name, index) in manager_list">
                                        <th scope="row">{{ index + 1 }}</th>
                                        <td>{{ name[1] }}</td>
                                        <td class="btn_combo">
                                            <button type="submit" @click="del_manager(`${name[0]}+${name[1]}`)"
                                                class="btn btn-danger">Delete</button>
                                            <button type="submit" @click="add_manager(`${name[0]}+${name[1]}`)"
                                                class="btn btn-success ms-1">Accept</button>
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

    <div class="bottom"></div>
</template>
  
<script>
import axios from "axios";
import check from '../../utils/refresh_token.js';
import adminNavbar from "../../components/admin_navbar.vue";

export default {

    data() {
        return {
            logged_in: true,
            logged_user: 'Login',
            manager_list: [],
            category_edit_list: [],
            category_add_list: [],
            category_delete_list: [],
            edit_category: true,
            addd_category: true,
            delete_category: true,
            manager: true,
        };

    },

    async mounted() {
        if (await check()) {
            this.get_item_dashboard()
        }
    },

    methods: {
        async del_category(id) {
            if (await check()) {
                await axios.delete(`http://127.0.0.1:5000/admin_dashboard/${id}`)
                    .then((res) => {
                        window.location.reload()
                    }).catch((rej) => {
                        alert('something went wrong !')
                    })
            }

        },

        async accept_del_category(id) {
            if (await check()) {
                await axios.delete(`http://127.0.0.1:5000/admin_dashboard/${id}`)
                    .then((res) => {
                        window.location.reload()
                    }).catch((rej) => {
                        alert('something went wrong !')
                    })
            }

        },

        async add_category(id) {
            await axios.post(`http://127.0.0.1:5000/admin_dashboard`, {
                name: id,
                new_name: id,
            })
                .then((res) => {
                    window.location.reload()
                }).catch((rej) => {
                    alert('something went wrong !')
                })
        },

        async update_category(id) {
            let arr = id.split('+')
            await axios.put(`http://127.0.0.1:5000/admin_dashboard`, {
                new_name: arr[0],
                name: arr[1],
            })
                .then((res) => {
                    window.location.reload()
                }).catch((rej) => {
                    alert('something went wrong !')
                })
        },

        async add_manager(id) {
            let arr = id.split('+')
            await axios.post(`http://127.0.0.1:5000/add_manager_from_admin`, {
                username: arr[1],
                password: arr[0],
            })
                .then((res) => {
                    window.location.reload()
                }).catch((rej) => {
                    alert('something went wrong !')
                })
        },

        async del_manager(id) {
            let arr = id.split('+')
            await axios.delete(`http://127.0.0.1:5000/add_manager_from_admin/${arr[1]}/${arr[0]}`)
                .then((res) => {
                    window.location.reload()
                }).catch((rej) => {
                    alert('something went wrong !')
                })
        },

        async get_item_dashboard() {
            console.log("checking")
            await axios.get("http://127.0.0.1:5000/admin_dashboard")
                .then((res) => {
                    this.category_add_list = res.data.cat_add_list;
                    this.category_edit_list = res.data.cat_edit_list;
                    this.category_delete_list = res.data.cat_delete_list;
                    this.manager_list = res.data.manager_list;

                    console.log(res.data.cat_edit_list)
                    if (this.category_edit_list.length == 0) { this.edit_category = false }
                    if (this.category_add_list.length == 0) { this.addd_category = false }
                    if (this.category_delete_list.length == 0) { this.delete_category = false }
                    if (this.manager_list.length == 0) { this.manager = false }
                }).catch((rej) => { console.log(rej) })


        },

    },

    components: {
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
    overflow-x: hidden;
}

html {
    scroll-behavior: smooth;
}

.pp {
    font-size: 41px;
    position: relative;
    margin-left: 35px;
    margin-top: 37px;
    font-family: 'Skranji', cursive;
    display: flex;
    color: rgb(156 56 206);
    justify-content: center;
}

.col-xl-7 {
    width: 70.333333%;
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
}</style>