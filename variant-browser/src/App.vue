
<script>
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
import NavBar from '@/components/NavBar.vue';

export default {
  components: {
    NavBar
  }
}
</script>

<template>
  <main>
    <NavBar />

    <router-view>

    </router-view>
  </main>

</template> 

