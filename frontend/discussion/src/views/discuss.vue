<template>
<div class="container">
        <div class="message-wrap">
            <div class="msg-wrap">
                <div class="media msg ">
                    <div class="media-body" v-for="(value, name) in collection" :key="name">
                        
                        <small class="pull-right time"><i class="fa fa-clock-o"></i>{{value.timestamp}}</small>
                        <h5 v-if="value.userName==null" class="media-heading">Anon</h5>
                        <h5 v-else class="media-heading">{{value.userName}}</h5>

                        <small class="col-lg-10">{{value.msg}}</small>
                    </div>
                </div>
                </div>

            <!-- <div>
               <form @submit.prevent='sendMsg'> 
                  <div class="form-group send-wrap">
                     <label for="message">message</label>
                     <input type="textarea" name="message" id="message" v-model.trim="msg" required>
                  </div>
                  <div class="CTA">
                     <input type="submit" value="login">
                  </div>
                  <div>
                    <p v-if="this.loginError !=''" style="color:red">{{this.loginError}}</p>
                  </div>
               </form>
            </div>End Login Form -->

            <div class="send-wrap ">
                <textarea class="form-control send-message" rows="3" placeholder="Write a reply..." v-model.trim="msg" required></textarea>
            </div>
            <form @submit.prevent='sendMsg'>
            <div class="btn-panel">
                <button onclick="sendMsg" class=" col-lg-12 btn btn-success send-message-btn " role="button"> Send </button>
            </div>
            </form>
        </div>
 
</div>
</template>
<script>
import axios from "axios"
import { collection, query, onSnapshot,orderBy } from "firebase/firestore";
import { db } from "../firebaseDB.js";

export default {
  data(){
    return{
        username:'',
        msg:'',
        collection:{}
    }
  },
  methods:{
    retrieveData() {
        const q = query(collection(db, "discussMsg"), orderBy("raw_timestamp"));
        onSnapshot(q, (querySnapshot) => {
            querySnapshot.forEach((doc) => {

            var document = doc.data()   
            document["id"] = doc.id
            this.collection[doc.id] = doc.data();
            
            });

        });
    },
    sendMsg(){
        axios.post("http://127.0.0.1:5000/",{"userName":this.username, "msg":this.msg})
                  .then(()=>{
                    this.msg = ''
                
              }).catch(()=>{
              });
    }
  },
  
  mounted(){
        this.username = this.$store.getters.getUsername
        if (this.username ==''){
            this.username == "Anon"
        }
        this.retrieveData()
        console.log(this.collection)
  }
}

</script>
<style scoped>
    .conversation-wrap
    {
        box-shadow: -2px 0 3px #ddd;
        padding:0;
        max-height: 400px;
        overflow: auto;
    }
    .conversation
    {
        padding:5px;
        border-bottom:1px solid #ddd;
        margin:0;

    }

    .message-wrap
    {
        box-shadow: 0 0 3px #ddd;
        padding:0;

    }
    .msg
    {
        padding:5px;
        /*border-bottom:1px solid #ddd;*/
        margin:0;
    }
    .msg-wrap
    {
        padding:10px;
        max-height: 400px;
        overflow: auto;

    }

    .time
    {
        color:#bfbfbf;
    }

    .send-wrap
    {
        border-top: 1px solid #eee;
        border-bottom: 1px solid #eee;
        padding:10px;
        /*background: #f8f8f8;*/
    }

    .send-message
    {
        resize: none;
    }

    .highlight
    {
        background-color: #f7f7f9;
        border: 1px solid #e1e1e8;
    }

    .send-message-btn
    {
        border-top-left-radius: 0;
        border-top-right-radius: 0;
        border-bottom-left-radius: 0;

        border-bottom-right-radius: 0;
    }
    .btn-panel
    {
        background: #f7f7f9;
    }

    .btn-panel .btn
    {
        color:white;

        transition: 0.2s all ease-in-out;
    }

    .btn-panel .btn:hover
    {
        color:#666;
        background: #f8f8f8;
    }
    .btn-panel .btn:active
    {
        background: #f8f8f8;
        box-shadow: 0 0 1px #ddd;
    }

    .btn-panel-conversation .btn,.btn-panel-msg .btn
    {

        background: #f8f8f8;
    }
    .btn-panel-conversation .btn:first-child
    {
        border-right: 1px solid #ddd;
    }

    .msg-wrap .media-heading
    {
        color:#003bb3;
        font-weight: 700;
    }


    .msg-date
    {
        background: none;
        text-align: center;
        color:#aaa;
        border:none;
        box-shadow: none;
        border-bottom: 1px solid #ddd;
    }


    body::-webkit-scrollbar {
        width: 12px;
    }
 
    
    /* Let's get this party started */
    ::-webkit-scrollbar {
        width: 6px;
    }

    /* Track */
    ::-webkit-scrollbar-track {
        -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3); 
/*        -webkit-border-radius: 10px;
        border-radius: 10px;*/
    }

    /* Handle */
    ::-webkit-scrollbar-thumb {
/*        -webkit-border-radius: 10px;
        border-radius: 10px;*/
        background:#ddd; 
        -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.5); 
    }
    ::-webkit-scrollbar-thumb:window-inactive {
        background: #ddd; 
    }

</style>
