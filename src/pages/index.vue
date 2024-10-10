<template>
    <Homelayout>
        <div class="flex flex-col h-[calc(100vh-160px)] w-screen justify-between items-center">
            <h1 class="text-2xl font-bold">Tugas</h1>
            <div class="flex flex-col justify-end items-center">
                <button @click="$router.push('/register')" class="btn btn-primary w-11/12 max-w-md">Register</button>
                <div class="text-sm mt-2">
                    already have an account? <a class="link" @click="$router.push('/login')">Login</a>
                </div>
            </div>
        </div>
    </Homelayout>
</template>

<script setup>
import Homelayout from "@/layouts/Homelayout.vue"
</script>

<style lang="scss" scoped>
</style>