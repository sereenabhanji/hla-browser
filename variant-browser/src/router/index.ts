import { createRouter, createWebHistory, RouterLink } from "vue-router"
import Home from '@/pages/Home.vue'
import Gene from '@/pages/Gene.vue'
import Test from '@/pages/Test.vue'
import About from '@/pages/About.vue'
import Variant from '@/pages/Variant.vue'

const routes = [
    {path: '/', name: 'Home', component: Home},
    //{path: '/:gene', name: 'Gene', component: Gene, props: true},
    {path: '/test', name: 'Test', component: Test},
    {path: '/about', name: 'About', component: About},
    {path: '/:variant', name: 'Variant', component: Variant, props: true}
]

const router = createRouter( {
    history: createWebHistory(),
    routes: routes
})

export default router