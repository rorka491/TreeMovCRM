import { Grade, Student } from './api'

export { Student }

let baseLatency = parseFloat(localStorage.getItem('fakeApi:fakeLatency') ?? '0')
let latencyVariance = parseFloat(
    localStorage.getItem('fakeApi:latencyVariance') ?? '0'
)

// в консоли браузера можно контролировать задержку у фейкового апи
// просто пишешь:
// setFakeLatency(<Тут задержка нужная>)
// @ts-ignore
globalThis.setFakeLatency = (base: number, variance = 0) => {
    baseLatency = base
    localStorage.setItem('fakeApi:fakeLatency', base + '')
    latencyVariance = variance
    localStorage.setItem('fakeApi:latencyVariance', variance + '')
}

const baseApi = {
    students: {
        getAll(): Student[] {
            const students: Student[] = [
                {
                    id: 1,
                    fullName: 'Иванов Иван',
                    img: null,
                    dateOfBirth: '2010-05-15',
                    groups: ['math-club', 'science-lab'],
                    phone: '+7 900 123-45-67',
                    email: 'ivanov@example.com',
                    parentFullName: 'Иванов Сергей',
                    parentPhone: '+7 900 987-65-43',
                    grades: [],
                    studies: [
                        {
                            id: 'study-1',
                            subject: 'Математика',
                            startDate: '2024-09-01',
                        },
                    ],
                    payments: [
                        {
                            id: 'p-1',
                            amount: 5000,
                            for: 'Сентябрь 2024',
                            debt: 0,
                            status: 'Успешно',
                            date: '2024-09-05',
                            group: 'math-club',
                        },
                    ],
                    subscriptionActive: true,
                },
                {
                    id: 2,
                    fullName: 'Петрова Мария',
                    img: null,
                    dateOfBirth: '2011-03-22',
                    groups: ['english-club'],
                    phone: '+7 901 555-66-77',
                    email: 'petrova@example.com',
                    parentFullName: 'Петрова Анна',
                    parentPhone: '+7 901 444-33-22',
                    grades: [],
                    studies: [
                        {
                            id: 'study-2',
                            subject: 'Английский язык',
                            startDate: '2024-09-01',
                        },
                    ],
                    payments: [
                        {
                            id: 'p-2',
                            amount: 4800,
                            for: 'Сентябрь 2024',
                            debt: 200,
                            status: 'Ошибка',
                            date: '2024-09-06',
                            group: 'english-club',
                        },
                    ],
                    subscriptionActive: false,
                },
            ]

            const grades: Grade[] = [
                {
                    student: students[0],
                    comment: 'Хорошо справился с задачами.',
                    created_at: '2025-01-10',
                    updated_at: '2025-01-10',
                    lesson: 1,
                    value: 4,
                },
                {
                    student: students[1],
                    comment: 'Отличная работа на уроке.',
                    created_at: '2025-01-11',
                    updated_at: '2025-01-11',
                    lesson: 1,
                    value: 5,
                },
            ]

            students[0].grades.push(grades[0])
            students[1].grades.push(grades[1])

            return students
        },
        getById(id: any) {
            return baseApi.students
                .getAll()
                .find((student) => student.id === id || student.id + '' === id)
        },
        getAllGroups() {
            // @ts-ignore
            return Array.from(
                new Set(
                    baseApi.students
                        .getAll()
                        .reduce(
                            (result, current) => [...result, ...current.groups],
                            [] as string[]
                        )
                )
            )
        },
    },
}

type SpecialObject = {
    [k: string]: SpecialObject | ((...args: any[]) => any)
}

function goThroughKeys(obj: SpecialObject) {
    const result: SpecialObject = {}

    for (const key in obj) {
        const val = obj[key]

        if (typeof val === 'function') {
            result[key] = (...args) =>
                new Promise((resolve) => {
                    const result = val(...args)
                    const timeout =
                        baseLatency + Math.random() * latencyVariance

                    setTimeout(() => resolve(result), timeout)
                })
        } else {
            result
            result[key] = goThroughKeys(val)
        }
    }

    return result
}

type MapToAsync<T> = {
    [key in keyof T]: T[key] extends (...args: infer A) => infer R
        ? (...args: A) => Promise<R>
        : MapToAsync<T[key]>
}

export const fakeApi = goThroughKeys(baseApi) as MapToAsync<typeof baseApi>
