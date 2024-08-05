<template>
    <p> HLA-{{ gene }}</p>
    <div class="row justify-content-center">
        <div class="col-12 col-sm-11 col-md-11" >
            <div class="child-component" id="center">
                <div v-if="loading">Loading...</div>
                <div v-if="error">{{ error }}</div>
                <div v-else>
                    <AlleleVisual v-if="start" :start="start" :stop="stop" :exons="exons" :gene="gene" />
                    <SequencingDepth v-if="gene" :view="gene"/>
                    <Table :gene="gene"/>
                </div>
            </div>
        </div>
    </div>   
</template>

<script>
import AlleleVisual from '@/components/AlleleVisual.vue';
import Table from '@/components/Table.vue';
import SequencingDepth from '@/components/SequencingDepth.vue';
import axios from "axios";


export default {
    components: {
    AlleleVisual,
    Table,
    SequencingDepth,
    },
    data: function() {
        return {
            start: null,
            stop: null,
            exons: null,
            loading: true,
            error: null,
        }
    },
    props: {
        gene: String,
    },
    created() {
        console.log(this.gene)
        this.loadData()
    },
    methods: {
        async loadData() {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/genes/${this.gene}`)   
                for (const d of response.data) {
                    this.start = d.txstart
                    this.stop = d.txend
                    this.exons = d.exons
                } 
                       
            }
            catch (error) {
                this.error = 'Error fetching data';
                console.error('Error fetching data:', error);
            } 
            finally {
                this.loading = false;
            }
            
        }
    }
 
}

</script>