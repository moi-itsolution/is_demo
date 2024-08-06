<template>
  <v-app>
    <v-main>
      <h1>Vue __ </h1>
      <h2>ID: {{ profile.ID }}</h2>
      <h2>ADMIN: {{ profile.ADMIN }}</h2>
      <h2 class="ml-5">{{ profile.NAME }} {{ profile.LAST_NAME }}</h2>
      <v-img :src="profile.PERSONAL_PHOTO" width="100" class="mx-auto"></v-img>
      <br>
      <p v-for="task in tasks">
        {{ task.title }}
      </p>
      <br>

    </v-main>
  </v-app>
</template>

<script setup>
  import {bxCall} from "@/bitrix";
  import {onMounted, ref} from "vue";

  const profile = ref({})
  const tasks = ref({})

  onMounted(async () => {
    let result;
    result = await bxCall('profile')
    profile.value = result

    let curUserId = result['ID']

    result = await bxCall('tasks.task.list', {
      "filter": {"RESPONSIBLE_ID": curUserId, "!STATUS": ["5"]}
    })

    window.debvar = result
    tasks.value = result['tasks']

  })
</script>
