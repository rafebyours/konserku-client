<template>
  <div class="btm-nav bg-white z-50 fixed bottom-0 mt-auto w-full">
    <button 
      :class="routePath === '/home' ? 'active' : ''" 
      @click="$router.push('/home')">
      <i class="fas fa-home h-5 w-5"></i>
      <span class="btm-nav-label">Home</span>
    </button>
    <button 
      :class="routePath === '/search' ? 'active' : ''" 
      @click="$router.push('/search')">
      <i class="fas fa-search h-5 w-5"></i>
      <span class="btm-nav-label">Search</span>
    </button>
    <button 
      :class="routePath === '/myTicket' ? 'active' : ''" 
      @click="$router.push('/myTicket')">
      <i class="fas fa-ticket-alt h-5 w-5"></i>
      <span class="btm-nav-label">MyTicket</span>
    </button>
    <button 
      :class="routePath === '/profile' ? 'active' : ''" 
      @click="$router.push('/profile')">
      <i class="fas fa-user h-5 w-5"></i>
      <span class="btm-nav-label">Profile</span>
    </button>

    <button 
  :class="routePath === '/about' ? 'active' : ''" 
  @click="$router.push('/about')">
  <i class="fa-solid fa-info-circle fa-bounce"></i>
  <span class="btm-nav-label">About</span>
</button>

    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const activeButton = ref('home'); 

// get route path
const routePath = router.currentRoute.value.path;
console.log(routePath);

</script>
