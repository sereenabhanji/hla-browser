<template>
    <div class="row search-box" >       
        <form class="d-flex" role="search">
            <input class="form-control me-2 h-25" type="search" placeholder="Search" aria-label="Search" name="name" @change="handleChange" autocomplete="off">
            <button class="btn btn-outline-success h-25" type="submit">Search</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "SearchBar",
    data: function() {
        return {
            searchEntry: "",
            showDropdown: false,
            searchMatches: [],
            loading: true,
            error: null,
        }
    },
    mounted: function() {
        $(this)
    },
    methods: {
        handleSearch(event) {
            console.log(event.target.elements.name.value)
        },
        handleChange(event) {
            console.log(event.target.value)
            $('.basicAutoComplete').autoComplete({
                resolverSettings: {
                    url: `http://127.0.0.1:5000/matches/${event.target.value}`
                }
            });

        }
    }
}

</script>

