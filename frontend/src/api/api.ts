import { formatDate } from '../lib/formatDate'
import axios, { AxiosResponse } from 'axios'
import { mapResult, Result } from '../lib/Result'

axios.defaults.baseURL = 'http://127.0.0.1:8000/api'

axios.interceptors.request.use((config) => {
    config.params ??= {}
    config.params.timezone_offset = -new Date().getTimezoneOffset() / 60
    config.params.test = true

    return config
})

export type Schedule = {
    org?: string
    title?: string
    start_time?: string
    end_time?: string
    date?: Date
    teacher?: string
    week_day?: string
    classroom?: string
    group?: string
    subject?: string
    is_canceled?: boolean
    is_completed?: boolean
    lesson?: string
    start_date?: Date
    end_date?: Date
}

export type Student = {
    id: string | number
    fullName: string
    img: string | null
    dateOfBirth: string
    groups: string[]
    phone: string
    email: string
    parentFullName: string
    parentPhone: string
    grades: Grade[]
    studies: {
        id: string
        subject: string
        startDate: string
    }[]
    payments: {
        id: string | number
        amount: number
        for: string
        debt: number
        status: 'Ошибка' | 'Успешно'
        date: string
        group: string
    }[]
    subscriptionActive: boolean
}

export type Grade = {
    student: Student
    comment: string
    created_at: string
    updated_at: string
    lesson: number
    value: number
}

export type Employee = {
    id: number
    name: string
    surname: string
    patronymic: string
    birthday: string
    email: string
    passport_series: string
    passport_num: string
    inn: string
    department: number
}

type PreStudent = {
    id: number
    name: string
    surname: string
    email: string
    phone_number: string
    birthday: string
    avatar: string | null
    groups: { id: number; name: string }[]
}

type PreGroup = {
    id: number
    name: string
    org: number
    students: number[]
}

type PreGrade = {
    student: PreStudent
    comment: string
    created_at: string
    updated_at: string
    lesson: 1
    value: 4
}

function preStudentToStudent(preStudent: PreStudent) {
    const result: Student = {
        id: preStudent.id,
        fullName: `${preStudent.surname} ${preStudent.name}`,
        phone: preStudent.phone_number,
        email: preStudent.email,
        dateOfBirth: preStudent.birthday,
        img: preStudent.avatar,
        groups: preStudent.groups.map((x) => x.name),
        parentFullName: '',
        parentPhone: '',
        grades: [],
        studies: [],
        payments: [],
        subscriptionActive: true,
    }

    result.dateOfBirth = formatDate(new Date(result.dateOfBirth), 'DD-MM-YYYY')

    return result
}

export const realApi = {
    isOk<T = any>(res: AxiosResponse<T>): Result<T, string> {
        if (199 < res.status && res.status < 300) {
            return [res.data as Exclude<T, null>, null]
        }

        return [null, `Ошибка ${res.status} ${res.data}`]
    },

    students: {
        async getAll() {
            const [preStudents, error] = await axios
                .get(`/students/students/?test=true`, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then((res) => realApi.isOk<PreStudent[]>(res))

            if (error !== null) {
                return []
            }

            return preStudents.map(preStudentToStudent)
        },
        async getAllGroups() {
            const [preGroups, error] = await axios
                .get(`/students/student_groups/?test=true`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then((res) => realApi.isOk<PreGroup[]>(res))

            if (error !== null) {
                return []
            }

            return preGroups.map((preGroup) => preGroup.name)
        },
        async getAllGrades(): Promise<Grade[]> {
            const [preGrades, error] = await axios
                .get(`/schedules/grades/?test=true`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then((res) => realApi.isOk<PreGrade[]>(res))

            if (error !== null) {
                return []
            }

            return preGrades.map((preGrade) => ({
                ...preGrade,
                student: preStudentToStudent(preGrade.student),
            }))
        },
        async getById(id: number) {
            const [preStudent, error] = await axios
                .get(`/students/students/${id}/?test=true`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then((res) => realApi.isOk<PreStudent>(res))

            if (error !== null) {
                return
            }

            const student = preStudentToStudent(preStudent)

            const grades: Grade[] = mapResult(
                await axios
                    .get(`/schedules/grades/?test=true&student=${id}`, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    })
                    .then((res) => realApi.isOk<PreGrade[]>(res)),
                (grades) =>
                    grades.map((preGrade) => ({
                        ...preGrade,
                        student: preStudentToStudent(preGrade.student),
                    })),
                () => []
            )

            student.grades = grades

            return student
        },
    },

    schedules: {
        async getSubjectsRequest() {
            return await axios
                .get(`/schedules/subjects/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then((res) => realApi.isOk(res))
        },

        async getClassroomsRequest() {
            return await axios
                .get(`/schedules/classrooms/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then((res) => realApi.isOk(res))
        },

        async getShedulesByClassrooms(query: Schedule) {
            return await axios
                .get(`/schedules/classrooms/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    params: query,
                })
                .then((res) => realApi.isOk(res))
        },

        async getGroupsRequest() {
            return await axios
                .get(`/schedules/student_groups/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then((res) => realApi.isOk(res))
        },

        async getTeachersRequest() {
            return await axios
                .get(`/schedules/teachers/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then((res) => realApi.isOk(res))
        },

        async getSearchRequest(query: string) {
            return await axios
                .get(`/schedules/search/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    params: query,
                })
                .then((res) => realApi.isOk(res))
        },

        async tokenRequest() {
            return await axios
                .post(`/token`, {
                    token: localStorage.getItem('refreshToken'),
                })
                .then((res) => realApi.isOk(res))
        },
    },

    employees: {
        async getAllEmployees(): Promise<Employee[]> {
            return mapResult(
                await axios
                    .get(`/schedules/search/`, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    })
                    .then((res) => realApi.isOk<Employee[]>(res)),
                (employees) => employees,
                () => []
            )
        },
    },
}
