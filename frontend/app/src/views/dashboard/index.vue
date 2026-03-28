<template>
  <div class="dashboard-container">
    <div class="dashboard-text">欢迎，{{ name }}</div>
    <br>
    <div class="dashboard-text">
      权限列表: [<br>
      <ul v-for="principal in scopes" :key="principal">{{ principal }}</ul>
      ]
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name',
      'scopes'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
