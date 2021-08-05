<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="Email">
        <template slot-scope="scope">
          {{ scope.row.email }}
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="Activated" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.is_active | statusFilter">{{ scope.row.is_active }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="Verified" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.is_verified | statusFilter">{{ scope.row.is_verified }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="Superuser" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.is_superuser | statusFilter">{{ scope.row.is_superuser }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getUsers } from '@/api/user'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        // success as green, grey as blue, danger as red
        true: 'grey',
        false: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      listLoading: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getUsers().then(response => {
        this.list = response.data
        this.listLoading = false
      })
    }
  }
}
</script>
