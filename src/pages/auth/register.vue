<template>
    
    <main class="p-10 flex justify-center items-center h-screen w-screen">
        <button @click="$router.go(-1)" class="btn btn-square btn-outline absolute top-5 left-5 flex items-center">
            <i class="fas fa-arrow-left"></i>
        </button>
        <div>
            <h1 class="text-2xl font-bold">Register</h1>

            <label class="form-control w-full max-w-xs">
            <div class="label">
                <span class="label-text">Name</span>
            </div>
            <input type="text" placeholder="Name" class="input input-bordered w-full max-w-xs" />
            </label>

            <label class="form-control w-full max-w-xs">
            <div class="label">
                <span class="label-text">Username</span>
            </div>
            <input type="text" placeholder="Username" class="input input-bordered w-full max-w-xs" />
            </label>

            <label class="form-control w-full max-w-xs">
            <div class="label">
                <span class="label-text">Password</span>
            </div>
            <input type="Password" placeholder="Password" class="input input-bordered w-full max-w-xs" />
            </label>

            <label class="form-control w-full max-w-xs">
            <div class="label">
                <span class="label-text">Confirm Password</span>
            </div>
            <input type="Password" placeholder="Confirm Password" class="input input-bordered w-full max-w-xs" />
            </label>

            <div class="text-sm mt-2">have any account? <a class="link" @click="$router.push('/login')">Login</a></div>
            <div class="flex justify-end mt-5">
                <button class="btn btn-primary">Register</button>
            </div>
        </div>
    </main>
</template>

<script setup>

</script>

<style lang="scss" scoped>

</style>