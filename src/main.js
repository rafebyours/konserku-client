import { createApp } from 'vue';
import './assets/css/app.css';  // Your existing CSS
import router from './router';   // Your existing router
import App from './App.vue';     // Your existing App.vue

// Import Leaflet
import L from 'leaflet';
// Import Leaflet CSS (for map styling)
import 'leaflet/dist/leaflet.css';



// Create Vue app
const app = createApp(App);

// Use the router as before
app.use(router);

// Mount the Vue app
app.mount('#app');

// Now you can initialize Leaflet maps globally if needed, or do it in a specific component