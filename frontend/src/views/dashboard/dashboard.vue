<template>
  <Navbar :item_count="item_count" :total_price="total_price" :logged_in="logged_in" :logged_user="logged_user" :changename=true
    @search="handleSearch" @selectPriceRange="handlePriceRangeSelection" />

  <div v-for="(product_list, categories) in (searchQuery || prrr ? filteredProducts : item_list)" :key="categories"
    class="categories">
    <div class="category_name">
      <p>{{ categories }}</p>
    </div>
    <div class="container">
      <div class="row">
        <div class="MultiCarousel" data-items="1,3,5,6" data-slide="1" id="MultiCarousel" data-interval="1000">
          <div class="MultiCarousel-inner">
            <div v-for="product in product_list" class="item">
              <div class="pad15">
                <div class="product_image_container">
                  <img style="width: 100%; height: 100%; border-radius: 10px;" loading="lazy" class="productimage" :src="`${publicPath}${product['image_link']}`" :alt="`${product['name']}`" />
                </div>

                <div class="product_name">
                  <p>{{ product['name'] }}</p>
                </div>

                <div class="product_quantity">
                  <p>{{ product['quantity'] }} {{ product['unit'] }}</p>
                </div>

                <div class="product_price">
                  <p>&#8377; {{ product['rate'] }}</p>
                </div>

                <div>
                  <button type="button" :id="`${product['name']}+${categories}`"
                    @click="addbutton(`${product['name']}+${categories}`, product['rate'])"
                    class="add btn btn-success">ADD</button>


                  <div class="btn_3" :id="`${product['name']}+${categories}three_btn`">

                    <button type="button" @click="deleteitem(`${product['name']}+${categories}`, product['rate'], 1)"
                      class="btn my-btn btn-success">-</button>

                    <button type="button" :id="`itemcount${product['name']}+${categories}`" disabled
                      class="btn my-btn btn-success">1</button>

                    <button type="button" @click="additem(`${product['name']}+${categories}`, product['rate'])"
                      class="btn my-btn btn-success" :id="`add${product['name']}+${categories}`">+</button>



                  </div>
                </div>

              </div>
            </div>
          </div>
          <button class="btn btn-primary leftLst" id="left">
            <img class="left-arrow" src="../../assets/left-arrow.png" alt="" />
          </button>
          <button class="btn btn-primary rightLst" id="right">
            <img class="right-arrow" src="../../assets/right-arrow.png" alt="" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "../../components/user_navbar.vue";
import { refreshAccessToken, check } from '../../utils/refresh_token.js';




export default {

  data() {
    return {
      logged_in: false,
      logged_user: 'Login',
      item_list: {},
      item_count: 0,
      total_price: 0,
      searchQuery: "",
      filteredProducts: {},
      selectedPriceRange: null,
      prrr: "",
      publicPath: process.env.BASE_URL,
    };

  },


  created() {
    this.get_item_dashboard()
  },

  async mounted() {
    if (await check()) {
      this.button_ready()
    }
  },

  methods: {

    handlePriceRangeSelection(range) {
      // range = range.slice(1)
      console.log('Selected Price Range:', range);
      this.filterItemsByPrice(range);

      // Implement your logic to filter items based on the selected price range
      // You may need to update the 'item_list' and 'filteredProducts' accordingly
    },
    filterItemsByPrice(priceRange) {
      // Implement your logic to filter items based on the selected price range
      // Update 'filteredProducts' accordingly
      if (priceRange > 0) {
        // this.searchQuery =  " ";
        this.prrr = " ";
        this.filteredProducts = {};
        console.log(priceRange)
        for (const category in this.item_list) {
          const filteredCategory = this.item_list[category].filter(
            (product) => product.rate < parseInt(priceRange)
          );

          if (filteredCategory.length > 0) {
            this.filteredProducts[category] = filteredCategory;
          }
        }
      } else {
        this.filteredProducts = { ...this.item_list };
      }
      console.log('All Products:', this.item_list);
      console.log('Filtered Products:', this.filteredProducts);
      // this.searchQuery =  "";

    },

    // handleSearch(query) {
    //   if (query == null || query == "") {
    //     console.log("null returned")
    //     this.searchQuery = "";
    //     return "xdf"
    //   }
    //   else {
    //     console.log("handelSearch query = ", query);
    //     this.searchQuery = query;
    //     this.performSearch();
    //   }
    // },

    handleSearch(query) {
      // try { const query = event.target.value.trim().toLowerCase(); }
      // catch (error) { console.log(event.target) }

      // for (let prop in event) {
      //   if (event.hasOwnProperty(prop)) {
      //     console.log(`${prop}: ${event[prop]}`);
      //   }
      // }
      try {
        console.log("..............................................")
        console.log(query)
        console.log(typeof (query));
        if (query == null || query.trim() === "") {
          console.log("null returned");
          this.searchQuery = "";
          return null;
        } else {
          console.log("handleSearch query = ", query);
          this.searchQuery = query.trim();
          this.performSearch();
        }
      }
      catch (error) { console.log("error occured") }
    },

    //the new code  start
    performSearch() {

      // console.log('Search Query:', this.lowercaseSearchQuery);
      // const lowercaseSearchQuery = (this.searchQuery || "").toLowerCase(); 
      this.filteredProducts = {};
      this.searchQuery = this.searchQuery.toLowerCase()
      for (const category in this.item_list) {
        const filteredCategory = this.item_list[category].filter((product) => {
          console.log(product)
          const lowercaseItem = (product.name || "").toLowerCase();
          const lowercaseCategory = (category || "").toLowerCase();
          //   console.log('Item:', product.item.toLowerCase());
          // console.log('Category:', category.toLowerCase());
          // console.log('Match:', product.item.toLowerCase().includes(this.lowercaseSearchQuery) || category.toLowerCase().includes(this.lowercaseSearchQuery));
          return (
            lowercaseItem.includes(this.searchQuery) ||
            lowercaseCategory.includes(this.searchQuery)
          );
        });

        if (filteredCategory.length > 0) {
          this.filteredProducts[category] = filteredCategory;
        }
        // else{
        //   this.filteredProducts = { ...this.item_list };
        // }
      }
      console.log('Filtered Products:', this.filteredProducts);
      // if (this.searchQuery) {
      //   this.suggestions = this.findSuggestions();
      // } else {
      //   this.suggestions = [];
      // }
      console.log(this.searchQuery)
    },


    findSuggestions() {
      const suggestions = [];

      // Iterate over your data to find suggestions
      for (const category in this.item_list) {
        const categoryMatches = this.item_list[category].some((product) =>
          product.name.toLowerCase().includes(this.searchQuery)
        );

        if (categoryMatches) {
          suggestions.push(category);
        }

        const productMatches = this.item_list[category].filter((product) =>
          product.name.toLowerCase().includes(this.searchQuery)
        );

        suggestions.push(...productMatches.map((product) => product.name));
      }

      return suggestions;
    },

    out_of_stock(id) {

      let arr = id.split('+')
      const item_list = JSON.parse(localStorage.getItem("item_list"));
      let itemcount = document.getElementById(`itemcount${id}`).innerText;


      for (const product of item_list[arr[1]]) {
        // document.getElementById(id).innerText = 'Unavailable'
        //   document.getElementById(id).disabled = true
        if (product['name'] === arr[0]) {
          if (product['stock'] - product['quantity'] * parseInt(itemcount) >= product['quantity']) {
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

    async get_item_dashboard() {
      console.log(this.publicPath )
      await axios.get('http://127.0.0.1:5000/dashboard')
        .then((res) => {
          
          this.item_list = res.data.products;
          localStorage.setItem('item_list', JSON.stringify(this.item_list));
          slider();
        })

      const item_list = JSON.parse(localStorage.getItem("item_list"));
      console.log(item_list)

      for (const products in item_list) {
        for (const product of item_list[products]) {

          if (product['stock'] == 0) {
            let id = `${product['name']}+${products}`
            document.getElementById(id).innerText = 'Out of Stock'
            document.getElementById(id).style.backgroundColor = '#e94242'
            document.getElementById(id).style.borderColor = "#e94242"
            document.getElementById(id).disabled = true
          }
        }
      };

    },

    async button_ready() {
      try {
        await axios.get('http://127.0.0.1:5000/add_cart_item')
          .then((res) => {
            this.logged_user = res.data['user']
            this.logged_in = true
            let item_arr = res.data['message']
            // console.log(item_arr)

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

  },

  components: {
    Navbar,
  },


};

function slider() {
  $(document).ready(function () {



    var itemsMainDiv = ".MultiCarousel";
    var itemsDiv = ".MultiCarousel-inner";
    var itemWidth = "";

    $(".leftLst, .rightLst").click(function () {
      var condition = $(this).hasClass("leftLst");
      if (condition) click(0, this);
      else click(1, this);
    });

    ResCarouselSize();

    $(window).resize(function () {
      ResCarouselSize();
    });

    //this function define the size of the items
    function ResCarouselSize() {
      var incno = 0;
      var dataItems = "data-items";
      var itemClass = ".item";
      var id = 0;
      var btnParentSb = "";
      var itemsSplit = "";
      var sampwidth = $(itemsMainDiv).width();
      var bodyWidth = $("body").width();
      $(itemsDiv).each(function () {
        id = id + 1;
        var itemNumbers = $(this).find(itemClass).length;
        btnParentSb = $(this).parent().attr(dataItems);
        itemsSplit = btnParentSb.split(",");
        $(this)
          .parent()
          .attr("id", "MultiCarousel" + id);

        if (bodyWidth >= 1200) {
          incno = itemsSplit[3];
          itemWidth = sampwidth / incno;
        } else if (bodyWidth >= 992) {
          incno = itemsSplit[2];
          itemWidth = sampwidth / incno;
        } else if (bodyWidth >= 768) {
          incno = itemsSplit[1];
          itemWidth = sampwidth / incno;
        } else {
          incno = itemsSplit[0];
          itemWidth = sampwidth / incno;
        }
        $(this).css({
          transform: "translateX(0px)",
          width: itemWidth * itemNumbers,
        });
        $(this)
          .find(itemClass)
          .each(function () {
            $(this).outerWidth(itemWidth);
          });

        $(".leftLst").addClass("over");
        $(".rightLst").removeClass("over");
      });
    }

    //this function used to move the items
    function ResCarousel(e, el, s) {
      var leftBtn = ".leftLst";
      var rightBtn = ".rightLst";
      var translateXval = "";
      var divStyle = $(el + " " + itemsDiv).css("transform");
      var values = divStyle.match(/-?[\d\.]+/g);
      var xds = Math.abs(values[4]);
      if (e == 0) {
        translateXval = parseInt(xds) - parseInt(itemWidth * s);
        $(el + " " + rightBtn).removeClass("over");

        if (translateXval <= itemWidth / 2) {
          translateXval = 0;
          $(el + " " + leftBtn).addClass("over");
        }
      } else if (e == 1) {
        var itemsCondition = $(el).find(itemsDiv).width() - $(el).width();
        translateXval = parseInt(xds) + parseInt(itemWidth * s);
        $(el + " " + leftBtn).removeClass("over");

        if (translateXval >= itemsCondition - itemWidth / 2) {
          translateXval = itemsCondition;
          $(el + " " + rightBtn).addClass("over");
        }
      }
      $(el + " " + itemsDiv).css(
        "transform",
        "translateX(" + -translateXval + "px)"
      );
    }

    //It is used to get some elements from btn
    function click(ell, ee) {
      var Parent = "#" + $(ee).parent().attr("id");
      var slide = $(Parent).attr("data-slide");
      ResCarousel(ell, Parent, slide);
    }
  });

};

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Linear+B&family=Roboto:ital,wght@1,300&display=swap');




.my-btn {
  border-radius: 0px;
  justify-content: center;
  height: 29px;
  align-items: center;
  display: inline-flex;
}

.btn_3 {
  /* border: 1px solid red; */
  width: auto;
  position: relative;
  left: 33px;
  display: none;
  bottom: 33px;
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
  left: 31px;
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
  color: white;
    top: 7px;
  position: relative;
  font-size: 14px;
  height: 44px;
  font-family: 'Noto Sans Linear B', sans-serif;
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
  width: 87%;
  position: relative;
  top: 3px;
  display: inline-block;
  align-items: center;
  height: 56%;
}

.productimage {
  width: 100%;
  /* border: 2px solid red; */
  /* background-image: url('images/Chicken/Image_1.jpg'); */
}

.container {
  max-width: 1305px;
}

.leftLst {
  width: 3%;
  height: 16%;
}

.rightLst {
  width: 3%;
  height: 16%;
}

.left-arrow {
  width: 117%;
  position: relative;
  right: 16%;
}

.right-arrow {
  width: 117%;
  position: relative;
  left: 16%;
}

.MultiCarousel {
  float: left;
  overflow: hidden;
  padding: 15px;
  width: 100%;
  position: relative;
  margin-top: 45px;
  height: 272px;
  /* border: 1px solid yellow; */
}


.MultiCarousel .MultiCarousel-inner {
  transition: 1s ease all;
  float: left;
}

.MultiCarousel .MultiCarousel-inner .item {
  width: 320px;
  float: left;
  height: 265px;
  width: 216px;
  display: inline-flex;
  /* border: 1px solid blue; */
}

.MultiCarousel .MultiCarousel-inner .item>div {
  text-align: center;
  padding: 10px;
  margin: 10px;
  border-radius: 10px;
  background: #f1f1f1;
  color: #666;
}

.MultiCarousel .leftLst,
.MultiCarousel .rightLst {
  position: absolute;
  border-radius: 50%;
  top: calc(50% - 20px);
}

.MultiCarousel .leftLst {
  left: 0;
}

.MultiCarousel .rightLst {
  right: 0;
}

.MultiCarousel .leftLst.over,
.MultiCarousel .rightLst.over {
  pointer-events: none;
  background: #ccc;
}

.pad15 {
  width: 190px;
  /* border: 1px solid red; */
}
</style>

