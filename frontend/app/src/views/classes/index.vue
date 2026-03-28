<template>
  <div class="app-container">
    <div class="toolbar">
      <el-button type="primary" @click="createOne">新增班级</el-button>
    </div>
    <el-table :data="list" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="class_code" label="班级代码" />
      <el-table-column prop="class_name" label="班级名称" />
      <el-table-column prop="grade" label="年级" />
      <el-table-column label="操作" width="240">
        <template slot-scope="scope">
          <el-button size="mini" @click="updateOne(scope.row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="deleteOne(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { listClasses, createClass, updateClass, deleteClass } from '@/api/edu'

export default {
  name: 'ClassesView',
  data() {
    return { list: [] }
  },
  created() {
    this.load()
  },
  methods: {
    async load() {
      const { data } = await listClasses()
      this.list = data || []
    },
    async createOne() {
      await createClass({ class_code: `CL${Date.now()}`, class_name: '新班级', grade: '七年级' })
      this.$message.success('新增成功')
      this.load()
    },
    async updateOne(row) {
      await updateClass(row.id, { class_name: `${row.class_name}-已更新` })
      this.$message.success('更新成功')
      this.load()
    },
    async deleteOne(row) {
      await deleteClass(row.id)
      this.$message.success('删除成功')
      this.load()
    }
  }
}
</script>
