import { formatDate } from '../lib/formatDate'

const domain = 'http://127.0.0.1:8000/api/'

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

export type Grade = {
    student: Student
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
    isOk<T = any>(res: Response): Promise<T> {
        if (res.ok) {
            return res.json()
        }
        return Promise.reject(`Ошибка ${res.status}`)
    },

    students: {
        async getAll() {
            const result = (
                await fetch(`${domain}students/students/?test=true`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }).then((res) => realApi.isOk<PreStudent[]>(res))
            ).map(preStudentToStudent)

            return result
        },
        async getAllGroups() {
            return (
                await fetch(`${domain}students/student_groups/?test=true`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }).then((res) => realApi.isOk<PreGroup[]>(res))
            ).map((preGroup) => preGroup.name)
        },
        async getAllGrades(): Promise<Grade[]> {
            return (
                await fetch(`${domain}schedules/grades/?test=true`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }).then((res) => realApi.isOk<PreGrade[]>(res))
            ).map((preGrade) => ({
                ...preGrade,
                student: preStudentToStudent(preGrade.student),
            }))
        },
        async getById(id: number) {
            const student = preStudentToStudent(
                await fetch(`${domain}students/students/${id}/?test=true`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }).then((res) => realApi.isOk<PreStudent>(res))
            )

            const grades: Grade[] = (
                await fetch(
                    `${domain}schedules/grades/?test=true&student=${id}`,
                    {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    }
                ).then((res) => realApi.isOk<PreGrade[]>(res))
            ).map((preGrade) => ({
                ...preGrade,
                student: preStudentToStudent(preGrade.student),
            }))

            student.grades = grades

            return student
        },
    },

    schedules: {
        async getSubjectsRequest() {
            return await fetch(`${domain}schedules/subjects/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then((res) => realApi.isOk(res))
        },

        async getClassroomsRequest() {
            return await fetch(`${domain}schedules/classrooms/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then((res) => realApi.isOk(res))
        },

        async getShedulesRequest(query: Schedule) {
            return await fetch(`${domain}schedules/classrooms/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(query),
            }).then((res) => realApi.isOk(res))
        },

        async getGroupsRequest() {
            return await fetch(`${domain}schedules/student_groups/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then((res) => realApi.isOk(res))
        },

        async getTeachersRequest() {
            return await fetch(`${domain}schedules/teachers/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then((res) => realApi.isOk(res))
        },

        async getSearchRequest(query: string) {
            return await fetch(`${domain}schedules/search/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(query),
            }).then((res) => realApi.isOk(res))
        },

        async tokenRequest() {
            return await fetch(`${domain}token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    token: localStorage.getItem('refreshToken'),
                }),
            }).then((res) => realApi.isOk(res))
        },
    },
}
