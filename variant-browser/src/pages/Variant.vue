<template>
    <div class="container-fluid"> 

        <div class="row justify-content-center">
            <div class="col-12 col-sm-11 col-md-11" >
                <div class="child-component" id="center"> 
                    <h1> HLA-{{ variant }}  </h1>
                    <a :href="'https://www.ebi.ac.uk/ipd/imgt/hla/alleles/?query=or(startsWith(name,%22'+this.variant+'%22),contains(previous_nomenclature,%22'+this.variant+'%22),%20eq(accession,%20%22'+this.variant+'%22),startsWith(wmda.G_group.name,'+ this.variant+'))#panelAdvancedQuery'" style="color: black; font-style: italic;" target="_blank"> IPD-IMGT/HLA Accession </a>
                    <p></p>
                    <PharmTable :variant="variant" :annType="clinical_ann"/>
                    <PharmTable :variant="variant" :annType="variant_ann"/>
                </div>
            </div>
        </div>
    </div>
   
</template>
<script>
import PharmTable from '@/components/PharmTable.vue'

export default {
    name: "Variant",
    data: function() {
        return {
            tabulator: null,
            clinical_ann: "Clinical",
            variant_ann: "Variant"
        }
    },
    components: {
        PharmTable
    },
    props: {
        variant: String
    },
    mounted: function() {

    },
    methods: {
       
    },
  
}
</script>