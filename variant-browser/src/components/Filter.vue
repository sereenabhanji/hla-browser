<template>
   <div class="dropdown">
    <button class="btn btn-secondary btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
        Showing HLA-{{ this.currView }}
    </button>
    <ul class="dropdown-menu">
        <template v-for="gene in genes">
            <li @click="view(gene)"><a class="dropdown-item" href="#"> HLA-{{ gene }}</a></li>
        </template>
    </ul>
    
    </div>
        
</template>

<script>

export default {
    name: "Filter",
    data() {
        return {
            genes: ['all', 'A','B','C','DPA1','DPB1','DQA1','DQB1','DRB1'],
            currView: 'all'
        }
    },
    emits: ["view"],

    mounted: function() {
        this.$emit("view","all")
    },

    methods: {
        view: function(gene) {
            this.$emit("view", gene)
            //this.currView = gene

        },
       
    }
}


</script>

<style >


</style>
