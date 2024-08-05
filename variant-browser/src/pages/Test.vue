<template>
    <div class="home">
        <div class="child-component" id="center">   
            <SearchBar />
        </div>        
    </div>
</template>

<script>
import Filter from '@/components/Filter.vue'
import SearchBar from '@/components/SearchBar.vue'

export default {
    components: {
        Filter,
        SearchBar,
        
    },
    data: function() {
        return {
            filterArr: null,
        }
    },
    methods: {
        updateView(view) {
            if (view == "all") {
                this.filterArr = []
            }
            else {
                this.filterArr = [{field: "allele_id", type: "starts", value: view}]  // make this more abstract later             
            }
        }
        
    }
}
</script>

