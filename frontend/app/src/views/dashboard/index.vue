<template>
  <div class="dashboard-container">
    <div class="dashboard-text">Welcome {{ name }}</div>
    <br>
    <div class="dashboard-text">
      permissions: [<br>
      <ul v-for="principal in principals" :key="principal">{{ principal }}</ul>
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
      'principals'
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
