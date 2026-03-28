<template>
  <div class="app-container">
    <div class="toolbar">
      <el-button type="primary" @click="createOne">新增课程</el-button>
    </div>
    <el-table :data="list" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="course_code" label="课程代码" />
      <el-table-column prop="course_name" label="课程名称" />
      <el-table-column prop="credit" label="学分" />
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
import { listCourses, createCourse, updateCourse, deleteCourse } from '@/api/edu'

export default {
  name: 'CoursesView',
  data() {
    return { list: [] }
  },
  created() {
    this.load()
  },
  methods: {
    async load() {
      const { data } = await listCourses()
      this.list = data || []
    },
    async createOne() {
      await createCourse({ course_code: `C${Date.now()}`, course_name: '新课程' })
      this.$message.success('新增成功')
      this.load()
    },
    async updateOne(row) {
      await updateCourse(row.id, { course_name: `${row.course_name}-已更新` })
      this.$message.success('更新成功')
      this.load()
    },
    async deleteOne(row) {
      await deleteCourse(row.id)
      this.$message.success('删除成功')
      this.load()
    }
  }
}
</script>
