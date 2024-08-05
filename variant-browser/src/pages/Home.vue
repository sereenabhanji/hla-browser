<template>
    <div class="home">
        <div class="container-fluid">

        <div class="row justify-content-center">
            <div class="col-12 col-sm-11 col-md-11" >
                <div class="child-component" id="center"> 
                    <Summary :view="view"  />                
                    <AlleleVisual :gene="view" />
                    <SequencingDepth :view="view"/>                       
                    <Filter @view="updateView"/>
                    <GeneTable @hover="tableHover" :view="view" />

                </div>
            </div>
        </div>
    </div>

        
    </div>
</template>

<script>
import GeneTable from '@/components/GeneTable.vue'
import Summary from '@/components/Summary.vue'
import Filter from '@/components/Filter.vue'
import AlleleVisual from '@/components/AlleleVisual.vue'
import SequencingDepth from '@/components/SequencingDepth.vue'

export default {
    components: {
        GeneTable,
        Summary,
        Filter,
        AlleleVisual,
        SequencingDepth
    },
    data: function() {
        return {
            hoveredGene: null,
            view: "all",
            start: null,
            stop: null,
            regions: null,
            loading: true,
            error: null,
            loaded: false
        }
    },

    methods: {
        tableHover(name) {
            //console.log(name)
            this.hoveredGene = name
        },
        updateView(view) {
            console.log(view)
            this.view = view  // make this more abstract later 
            
        },    
    }
}


</script>
