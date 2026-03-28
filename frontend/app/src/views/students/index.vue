<template>
  <div class="app-container">
    <div class="toolbar">
      <el-button type="primary" @click="createOne">新增学生</el-button>
    </div>
    <el-table :data="list" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="student_no" label="学号" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="gender" label="性别" />
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
import { listStudents, createStudent, updateStudent, deleteStudent } from '@/api/edu'

export default {
  name: 'StudentsView',
  data() {
    return { list: [] }
  },
  created() {
    this.load()
  },
  methods: {
    async load() {
      const { data } = await listStudents()
      this.list = data || []
    },
    async createOne() {
      await createStudent({ student_no: `S${Date.now()}`, name: '新学生' })
      this.$message.success('新增成功')
      this.load()
    },
    async updateOne(row) {
      await updateStudent(row.id, { name: `${row.name}-已更新` })
      this.$message.success('更新成功')
      this.load()
    },
    async deleteOne(row) {
      await deleteStudent(row.id)
      this.$message.success('删除成功')
      this.load()
    }
  }
}
</script>
