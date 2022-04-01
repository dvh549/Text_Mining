<template>
    <nav class="navbar navbar-dark justify-content-between navbar-main">
        <a class="navbar-brand" href='' @click="goHome()" style="margin-left:100px">Text Mining</a>
        <div class="d-flex" style="margin-right:100px">
            <div class="navmenu-div d-flex">
                <a class="nav-item nav-link" v-bind:class="{ 'active': this.$route.path === '/addUser'}" @click="goHome()" href="">Generate</a>
                <a class="nav-item nav-link" v-bind:class="{ 'active': this.$route.path === '/addUser'}" @click="goRace()" href="">Race</a>
                <a class="nav-item nav-link" v-bind:class="{ 'active': this.$route.path === '/expiry'}" @click="goReligion()" href="">Religion</a>
                <a class="nav-item nav-link" v-bind:class="{ 'active': this.$route.path === '/editCom'}" @click="goGender()" href="" >Gender</a>
                <a class="nav-item nav-link" v-bind:class="{ 'active': this.$route.path === '/editCom'}" @click="goDisability()" href="" >Disability</a>
                <a class="nav-item nav-link" v-bind:class="{ 'active': this.$route.path === '/editCom'}" @click="goNone()" href="" >None</a>


            </div>
        </div>
    </nav>

</template>
<script>
import router from '@/router'


    export default{
        // setup(){
        //     const route = useRoute();
        //     const id = route.params.id;
        // }, 
        date(){
            return{
            }
        },
        methods:{
            goHome(){
                router.push("/")
            },
            goNone(){
                router.push("/None")
            },
            goRace(){
                router.push("/Race")
            },
            goReligion(){
                router.push("/Religion")
            },
            goDisability(){
                router.push("/Disability")
            },
            goGender(){
                router.push("/Gender")
            },
         
        }
    }
</script>

<style scoped>
.navbar-main {
    padding: 30px 0;
}

.navbar-brand {
    color: #000000 !important;
    font-size: 16px;
    font-weight: 700;
    text-transform: uppercase;
}

.nav-link {
    color: #898989;
}

.navbar {
    border-bottom: 2px solid rgba(0,0,0,0.05);
}

.navmenu-div a {
    color: rgba(0,0,0,0.5) ;
    font-size: 16px;
    font-weight: 700;
    text-transform: uppercase;
    transition: 0.5s
}

.navmenu-div a:hover, .active {
    color: #000000 !important;
}




</style>