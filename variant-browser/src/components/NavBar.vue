<template>
<div >   
    <nav class="navbar navbar-expand-lg bg-white">
        <div class="container-fluid">
            <a class="navbar-brand" >
                <router-link :to="{ name: 'Home'}" style="color: black; text-decoration: none;"> 
                    <img src="/src/components/icons/hla_logo_round.png" height="40px">    Variant Browser 
                </router-link>
            </a>
            <span class="navbar-text"> 
                <router-link :to="{ name: 'About'}" style="color: slategray; text-decoration: none;"> About </router-link>
            </span>
        </div>
    </nav>
</div>


</template>

<script>

import SearchBar from '@/components/SearchBar.vue'

export default {
    name: "NavBar",
    components: {
        SearchBar,
    },
    methods: {
        search(event) {
            let entry = event.target.elements.name.value
            
        },
    }
}

</script>

<style scoped>
.btn {
    height: 20px;
    font-size: 6px;
}
.navbar-brand {
    color: #000;
}
</style>