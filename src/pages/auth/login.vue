<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from 'axios'; // Import axios

const router = useRouter();
const username = ref("");
const password = ref("");
const isUsernameEmpty = ref(false);
const isPasswordEmpty = ref(false);
const loginError = ref(""); // Error message for login failure
const showModal = ref(false); // For showing the modal when login is successful

const login = async () => {
  isUsernameEmpty.value = !username.value;
  isPasswordEmpty.value = !password.value;

  if (!isUsernameEmpty.value && !isPasswordEmpty.value) {
    try {
      // Mengirim data login ke API Flask
      const response = await axios.post("https://api-ticketconcert.vercel.app/login", {
        username: username.value,
        password: password.value
      });

      // Jika login berhasil, simpan data ke localStorage
      if (response.status === 200) {
        // Simpan data login ke localStorage
        localStorage.setItem("user_id", response.data.user_id);  // Menyimpan user_id
        localStorage.setItem("username", username.value);  // Menyimpan username

        showModal.value = true; // Show the modal
        setTimeout(() => {
          router.push("/home"); // Redirect to home after modal closes
        }, 1500); // Delay before redirecting
      } else {
        loginError.value = "Invalid credentials. Please try again.";
      }
    } catch (error) {
      console.error(error);
      loginError.value = "An error occurred. Please try again.";
    }
  }
};




const closeModal = () => {
  console.log("Closing modal...");
  showModal.value = false;
  router.push("/home"); // Redirect to home after closing modal
};


const isVisible = ref(false);
onMounted(() => {
  isVisible.value = true;
});

// Modal transition effects
const beforeEnter = (el) => {
  el.style.opacity = 0;
};

const enter = (el, done) => {
  el.offsetHeight; // trigger reflow
  el.style.transition = "opacity 0.5s";
  el.style.opacity = 1;
  done();
};

const leave = (el, done) => {
  el.style.transition = "opacity 0.5s";
  el.style.opacity = 0;
  done();
};

let showPassword = ref(false);
</script>

<template>
  <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
    <main v-if="isVisible" class="p-10 w-full flex justify-center items-center h-screen">
      <div class="w-full max-w-xs">
        <div class="flex items-center mb-5">
          <button @click="$router.push('/')" class="btn flex items-center mr-3">
            <i class="fas fa-arrow-left"></i>
          </button>
          <h1 class="text-2xl font-sans2">Login</h1>
        </div>

        <label class="form-control w-full max-w-xs mt-3">
          <div class="label">
            <span class="label-text">Username</span>
          </div>
          <label :class="[ 'input input-bordered flex items-center gap-2', isUsernameEmpty ? 'border-red-500' : '' ]">
            <i class="fas fa-user-circle opacity-70"></i>
            <input v-model="username" type="text" class="grow" placeholder="Username" required />
          </label>
          <span v-if="isUsernameEmpty" class="text-red-500 text-sm mt-1">Username is required</span>
        </label>

        <label class="form-control w-full max-w-xs mt-3">
          <div class="label">
            <span class="label-text">Password</span>
          </div>
          <label :class="[ 'input input-bordered flex items-center gap-2', isPasswordEmpty ? 'border-red-500' : '' ]">
            <i class="fas fa-lock opacity-70"></i>
            <input v-model="password" :type="showPassword ? 'text' : 'password'" class="grow" placeholder="Password" required />
          </label>
          <span v-if="isPasswordEmpty" class="text-red-500 text-sm mt-1">Password is required</span>

          <div class="flex items-center mt-2">
            <input type="checkbox" id="showPassword" class="form-checkbox mr-2" v-model="showPassword" />
            <label for="showPassword" class="label-text cursor-pointer">Show Password</label>
          </div>
        </label>

        <div class="text-sm mt-3">
          Don't have an account? <a class="link" @click="$router.push('/register')">Register</a>
        </div>

        <!-- Error Message -->
        <div v-if="loginError" class="mt-3 text-red-500 text-sm">
          {{ loginError }}
        </div>

        <div class="flex justify-end mt-5">
          <button class="btn bg-secondary" @click="login">Login</button>
        </div>
      </div>
    </main>
  </transition>

  <!-- Modal for successful login -->
    <transition name="fade">
    <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-gray-600 bg-opacity-50">
      <div class="bg-white p-6 rounded shadow-lg px-6 sm:px-8">
        <h2 class="text-lg font-semibold">Login Successful!</h2>
        <p class="mt-2">You have successfully logged in. Redirecting to home...</p>
        <div class="mt-4 flex justify-end">
          <button @click="closeModal" class="btn bg-secondary">Close</button>
        </div>
      </div>
    </div>
  </transition>

</template>

<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
.border-red-500 {
  border-color: #f56565;
}
.text-red-500 {
  color: #f56565;
}
</style>
