import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import LoadScript from "vue-plugin-load-script";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
import axios from 'axios'
import VueRouter from 'vue-router'

// const socket = new WebSocket('ws://192.168.241.240:8080/ws');
// const sockett = new WebSocket("ws://localhost:8080");
window.$ = window.jQuery = require('jquery');
window.bootstrap = require('bootstrap/dist/js/bootstrap.bundle.js');

const app = createApp(App);
app.use(LoadScript);
app.use(router);

app.mount("#app");