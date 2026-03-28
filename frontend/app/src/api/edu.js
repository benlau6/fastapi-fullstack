import request from '@/utils/request'

export function listStudents() {
  return request({ url: '/students', method: 'get' })
}

export function createStudent(data) {
  return request({ url: '/students', method: 'post', data })
}

export function updateStudent(id, data) {
  return request({ url: `/students/${id}`, method: 'put', data })
}

export function deleteStudent(id) {
  return request({ url: `/students/${id}`, method: 'delete' })
}

export function listTeachers() {
  return request({ url: '/teachers', method: 'get' })
}

export function createTeacher(data) {
  return request({ url: '/teachers', method: 'post', data })
}

export function updateTeacher(id, data) {
  return request({ url: `/teachers/${id}`, method: 'put', data })
}

export function deleteTeacher(id) {
  return request({ url: `/teachers/${id}`, method: 'delete' })
}

export function listCourses() {
  return request({ url: '/courses', method: 'get' })
}

export function createCourse(data) {
  return request({ url: '/courses', method: 'post', data })
}

export function updateCourse(id, data) {
  return request({ url: `/courses/${id}`, method: 'put', data })
}

export function deleteCourse(id) {
  return request({ url: `/courses/${id}`, method: 'delete' })
}

export function listClasses() {
  return request({ url: '/classes', method: 'get' })
}

export function createClass(data) {
  return request({ url: '/classes', method: 'post', data })
}

export function updateClass(id, data) {
  return request({ url: `/classes/${id}`, method: 'put', data })
}

export function deleteClass(id) {
  return request({ url: `/classes/${id}`, method: 'delete' })
}
