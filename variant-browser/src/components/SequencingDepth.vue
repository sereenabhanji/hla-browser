<template>
   <div class="svg-container">
        <svg ref="depth" class="chart">
            <g ref="axes" class="chart-axes">
            </g>
        </svg>
    </div>
</template>

<script>
import * as d3 from "d3";
import axios from "axios";

export default {
    name: "SequencingDepth",
    
    data () {
        return {
            length: 0,
            chromData: null,
            hoveredPos: "null",
            margin: {top: 20, right: 10, bottom: 20, left: 12},
            start: 0,
            stop: 0,
        }
    },
    props: {
        view: String,
    },
    watch: {
        view: function() {
            this.loadData();
        }

    },
    mounted: function() {
        
        //d3.selectAll("svg > *").remove()

        
        this.loadData();
        
        
        
    },
    methods:  {
        loadData() {
           
            axios.get(`http://127.0.0.1:5000/depths/${this.view}`)
                .then(response => {
                    console.log(response.data)
                    this.start = response.data.txstart;
                    this.stop = response.data.txend;
                    this.initializeSvg();
                    this.scale_y.domain([response.data.max.cov, 0]).range([0, this.height])
                    let coords = []
                    for (const e of response.data.points) {
                        //console.log(e)
                        let point = [this.scale_x(e.pos), this.scale_y(e.cov)]
                        coords.push(point)
                    }
                    this.gy = this.svg.append("g")
                        .attr("transform", "translate(-1,0)")                
                        .call(d3.axisLeft(this.scale_y).tickSizeInner(3)).style("font-size", "3px")
                        
                    
                    this.svg
                        .append("path")
                        .attr("d", this.curve(coords))
                        .attr("stroke", "#b1d4e0")
                        .attr('fill', '#b1d4e0');
                    this.gx = this.svg.append("g")
                        .attr("transform", "translate(0,40)")                      
                        .call(d3.axisBottom(this.scale_x).tickSizeInner(3)).style("font-size", "3px")
                    /*this.svg.append("text")
                        .attr("class", "x-label")
                        .attr("text-anchor", "end")
                        .attr("x", this.width/2)
                        .attr("y", this.height+this.margin.bottom)
                        .text("locus")
                        .style("font-size", "6px");*/
                    })
                   
  
        },
        initializeSvg() {
            this.width = 500 - this.margin.left - this.margin.right;
            this.height = 75 - this.margin.top - this.margin.bottom;
            this.length = this.stop - this.start;
            this.scale_x = d3.scaleLinear()
                .domain([this.start, this.stop])
                .range([0, this.width])
            this.scale_y = d3.scaleLinear()
                
            this.svg = d3.select(this.$refs.depth)
                .attr("viewBox", `0 0 500 80`)
                .append("g")
                .attr("transform", "translate(" + this.margin.left + "," + this.margin.bottom + ")");
            this.curve = d3.area().y0(this.height)//.curve(d3.curveBasis);

        },
     
    }
}

</script>

