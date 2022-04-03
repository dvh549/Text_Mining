<template>
  <div>
      <navbar />
      <div class="d-flex flex-column min-vh-100">
      <div class="container-sm">
        <div class="home">
          <br />
          <br />
          <h1 class="title">Generate Topic</h1>
          <br />
          <div class="input-group">
            <div class="form-outline">
                <form class="contact-form row" @submit.prevent='GenerateTopics("sentence")'>
                <div class="form-field col-lg-12 ">
                    <input id="sentence" class="input-text js-input" type="sentence" v-model.trim="sentence" required>
                    <label class="label" for="sentence" v-if="this.sentence==''">Input Sentence... </label>
                </div> 
                <div class="form-field col-lg-12">
                    <input class="submit-btn" type="submit" value="Generate">
                </div>
            </form>
            </div>
          </div>
          <br />
          <h5 >Classified Under: {{this.classified}}</h5>
          <h5 style="color:red">{{this.error}}</h5>
          <table class="table table-hover table-striped align-middle">
            <thead>
              <tr>
                <th scope="col">Category </th>
                <!-- <th scope="col">Percentage Contributed</th> -->
                <th scope="col">Keywords</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{ this.topic["dominate_topic"]}}</td>
                <!-- <td>{{ this.topic["perc_cont"] }}</td> -->
                <td>{{ this.topic["keywords"] }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      </div>
  </div>
</template>
<script>
import navbar from "../components/navbar.vue";
// import { collection, query, onSnapshot,where,orderBy } from "firebase/firestore";
import axios from "axios"
// import { db } from "../firebaseDB.js";
// import router from '@/router'

export default {
  components: {
    navbar,
  },
  data() {
    return {
      topic: {},
      classified:'',
      error:'',
      sentence: ''
    };
  },
  methods: {
    // GenerateTopics() {
    //     console.log(this.sentence)
    // },
    GenerateTopics(){
      console.log("here")
        axios.post("http://127.0.0.1:5000/orchestrator",{"sent":this.sentence })
                  .then(res=>{
                    console.log(res.data)
                    this.classified = res.data["task1"]
                    this.topic = res.data["task2"]
                    console.log( this.topic)
                  })
              .catch(()=>{
                this.error = "An Error Occured"
              })
    }, 
  }

};
</script>

<style scoped>
.title {
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 3px;
  font-size: 3.2em;
  line-height: 48px;
  padding-bottom: 48px;
  color: #5543ca;
  background: #5543ca;
  background: -moz-linear-gradient(left, #f4524d 0%, #5543ca 100%) !important;
  background: -webkit-linear-gradient(
    left,
    #f4524d 0%,
    #5543ca 100%
  ) !important;
  background: linear-gradient(to right, #f4524d 0%, #5543ca 100%) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
}


.contact-form .form-field {
  position: relative;
  margin: 32px 0;
}
.contact-form .input-text {
  display: block;
  width: 60em;
  height: 36px;
  border-width: 0 0 2px 0;
  border-color: #5543ca;
  font-size: 18px;
  line-height: 26px;
  font-weight: 400;
}
.contact-form .input-text:focus {
  outline: none;
}
.contact-form .input-text:focus + .label,
.contact-form .input-text.not-empty + .label {
  -webkit-transform: translateY(-24px);
          transform: translateY(-24px);
}
.contact-form .label {
  position: absolute;
  left: 20px;
  bottom: 11px;
  font-size: 18px;
  line-height: 26px;
  font-weight: 400;
  color: #5543ca;
  cursor: text;
  transition: -webkit-transform .2s ease-in-out;
  transition: transform .2s ease-in-out;
  transition: transform .2s ease-in-out, 
  -webkit-transform .2s ease-in-out;
}
.contact-form .submit-btn {
  display: inline-block;
  background-color: #000;
   background-image: linear-gradient(125deg,#a72879,#064497);
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 16px;
  padding: 8px 16px;
  border: none;
  width:200px;
  cursor: pointer;
}

</style>