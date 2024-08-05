<template>
    <div>
        <div v-if="loading"> Loading... </div>
        <div v-else-if="error"> Error fetching data </div>
        <div v-else>
            <div v-if="start">
                <h1 v-if="mhc"> MHC </h1>
                <h1 v-else> HLA-{{ this.view }}</h1>
                <ul class="list-unstyled">
                    <h6 v-if="mhc"> Major Histocompatibility Complex </h6>
                    <h6 v-else> Human Leukocyte Antigen {{ this.view }}</h6>
                    <li> chr6: {{this.start}} - {{ this.stop }} </li>
                </ul> 
            </div>
        </div>                 
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "Summary",
    data: function() {
        return {
            loading: true,
            error: null,
            start: null,
            stop: null,
            regions: null,
        }
    },
    props: {
        view: {
            type: String,
            default: "all"
        },
       
    }
    , 
    watch: {
        view: function() {
            this.getData();

        }
    },
    computed: {
        mhc: function() {
            if (this.view == "all") {
                return true;
            }
            return false;
        }
    },
    mounted: function() {
        this.getData()
    },
    methods: {
        async getData() {
            try {
                const response = await axios 
                .get(`http://127.0.0.1:5000/genes/${this.view}`)
                for (const d of response.data) {
                    console.log(d.txstart)
                    this.start = d.txstart 
                    this.stop = d.txend
                    this.regions = d.regions
                }
            }
            catch (error) {
                this.error = "error fetching"
                console.error('error', error)
            }
            finally {
                this.loading = false;
            }
        },
    }    

}

</script>
