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

export type Student = {
    id: string | number
    fullName: string
    img: string
    dateOfBirth: string
    groups: string[]
    phone: string
    email: string
    parentFullName: string
    parentPhone: string
    grades: {
        id: string | number
        subject: string
        group: string
        score: string
        date: string
        teacherFullName: string
        teachersComment?: string
    }[]
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

const baseApi = {
    students: {
        getAll(): Student[] {
            return [
                {
                    id: 1,
                    fullName: 'Иванов Алексей Дмитриевич',
                    img: 'https://randomuser.me/api/portraits/men/32.jpg',
                    dateOfBirth: '12.03.2010',
                    groups: ['А12345', 'В34567'],
                    phone: '+7 (912) 123-45-67',
                    email: 'ivanov.alexey@example.com',
                    parentFullName: 'Иванова Мария Петровна',
                    parentPhone: '+7 (912) 765-43-21',
                    grades: [
                        {
                            id: 101,
                            subject: 'Математика',
                            group: 'А12345',
                            score: 'Хорошо',
                            date: '10.06.2025',
                            teacherFullName: 'Петров Сергей Иванович',
                        },
                        {
                            id: 115,
                            subject: 'Физика',
                            group: 'В34567',
                            score: 'Отлично',
                            date: '12.06.2025',
                            teacherFullName: 'Воронов Роман Павлович',
                        },
                    ],
                    studies: [
                        {
                            id: 's101',
                            subject: 'Математика',
                            startDate: '01.09.2024',
                        },
                        {
                            id: 's115',
                            subject: 'Физика',
                            startDate: '01.02.2025',
                        },
                    ],
                    payments: [
                        {
                            id: 201,
                            amount: 3000,
                            for: 'Июнь 2025',
                            debt: 0,
                            status: 'Успешно',
                            date: '05.06.2025',
                            group: 'А12345',
                        },
                        {
                            id: 215,
                            amount: 3100,
                            for: 'Июнь 2025',
                            debt: 100,
                            status: 'Ошибка',
                            date: '06.06.2025',
                            group: 'В34567',
                        },
                    ],
                    subscriptionActive: true,
                },
                {
                    id: 2,
                    fullName: 'Петрова Дарья Андреевна',
                    img: 'https://randomuser.me/api/portraits/women/44.jpg',
                    dateOfBirth: '21.07.2011',
                    groups: ['Б23456', 'Г45678'],
                    phone: '+7 (999) 456-78-90',
                    email: 'petrova.darya@example.com',
                    parentFullName: 'Петров Андрей Сергеевич',
                    parentPhone: '+7 (999) 654-32-10',
                    grades: [
                        {
                            id: 102,
                            subject: 'Русский язык',
                            group: 'Б23456',
                            score: 'Отлично',
                            date: '09.06.2025',
                            teacherFullName: 'Сидорова Анна Васильевна',
                        },
                        {
                            id: 116,
                            subject: 'История',
                            group: 'Г45678',
                            score: 'Хорошо',
                            date: '11.06.2025',
                            teacherFullName: 'Синицина Наталья Аркадьевна',
                        },
                    ],
                    studies: [
                        {
                            id: 's102',
                            subject: 'Русский язык',
                            startDate: '01.09.2024',
                        },
                        {
                            id: 's116',
                            subject: 'История',
                            startDate: '01.03.2025',
                        },
                    ],
                    payments: [
                        {
                            id: 202,
                            amount: 2800,
                            for: 'Июнь 2025',
                            debt: 200,
                            status: 'Ошибка',
                            date: '04.06.2025',
                            group: 'Б23456',
                        },
                        {
                            id: 216,
                            amount: 2900,
                            for: 'Июнь 2025',
                            debt: 0,
                            status: 'Успешно',
                            date: '06.06.2025',
                            group: 'Г45678',
                        },
                    ],
                    subscriptionActive: true,
                },
                {
                    id: 3,
                    fullName: 'Смирнов Никита Алексеевич',
                    img: 'https://randomuser.me/api/portraits/men/55.jpg',
                    dateOfBirth: '30.10.2009',
                    groups: ['А12345', 'Г45678'],
                    phone: '+7 (913) 222-33-44',
                    email: 'smirnov.nikita@example.com',
                    parentFullName: 'Смирнова Ольга Владимировна',
                    parentPhone: '+7 (913) 333-44-55',
                    grades: [
                        {
                            id: 103,
                            subject: 'Информатика',
                            group: 'А12345',
                            score: 'Удовлетворительно',
                            date: '07.06.2025',
                            teacherFullName: 'Федоров Иван Сергеевич',
                        },
                    ],
                    studies: [
                        {
                            id: 's103',
                            subject: 'Информатика',
                            startDate: '01.09.2024',
                        },
                    ],
                    payments: [
                        {
                            id: 203,
                            amount: 3100,
                            for: 'Июнь 2025',
                            debt: 100,
                            status: 'Ошибка',
                            date: '06.06.2025',
                            group: 'А12345',
                        },
                    ],
                    subscriptionActive: false,
                },
                {
                    id: 4,
                    fullName: 'Кузнецова Мария Игоревна',
                    img: 'https://randomuser.me/api/portraits/women/67.jpg',
                    dateOfBirth: '05.01.2012',
                    groups: ['Б23456'],
                    phone: '+7 (908) 111-22-33',
                    email: 'kuznetsova.maria@example.com',
                    parentFullName: 'Кузнецов Игорь Владимирович',
                    parentPhone: '+7 (908) 333-22-11',
                    grades: [
                        {
                            id: 104,
                            subject: 'Литература',
                            group: 'Б23456',
                            score: 'Плохо',
                            date: '06.06.2025',
                            teacherFullName: 'Алексеева Татьяна Юрьевна',
                            teachersComment: 'Не выполнила домашние задания',
                        },
                    ],
                    studies: [
                        {
                            id: 's104',
                            subject: 'Литература',
                            startDate: '01.09.2024',
                        },
                    ],
                    payments: [
                        {
                            id: 204,
                            amount: 2700,
                            for: 'Июнь 2025',
                            debt: 300,
                            status: 'Ошибка',
                            date: '02.06.2025',
                            group: 'Б23456',
                        },
                    ],
                    subscriptionActive: true,
                },
                {
                    id: 5,
                    fullName: 'Орлова Екатерина Андреевна',
                    img: 'https://randomuser.me/api/portraits/women/38.jpg',
                    dateOfBirth: '10.01.2010',
                    groups: ['Б23456'],
                    phone: '+7 (918) 221-66-00',
                    email: 'orlova.katya@example.com',
                    parentFullName: 'Орлов Андрей Васильевич',
                    parentPhone: '+7 (918) 443-21-98',
                    grades: [
                        {
                            id: 105,
                            subject: 'Английский язык',
                            group: 'Б23456',
                            score: 'Хорошо',
                            date: '05.06.2025',
                            teacherFullName: 'Беляева Лидия Викторовна',
                        },
                    ],
                    studies: [
                        {
                            id: 's105',
                            subject: 'Английский язык',
                            startDate: '01.09.2024',
                        },
                    ],
                    payments: [
                        {
                            id: 205,
                            amount: 3000,
                            for: 'Май 2025',
                            debt: 300,
                            status: 'Ошибка',
                            date: '05.05.2025',
                            group: 'Б23456',
                        },
                    ],
                    subscriptionActive: true,
                },
                {
                    id: 6,
                    fullName: 'Лебедев Никита Ильич',
                    img: 'https://randomuser.me/api/portraits/men/55.jpg',
                    dateOfBirth: '16.11.2010',
                    groups: ['В34567'],
                    phone: '+7 (930) 888-77-66',
                    email: 'lebedev.001@example.com',
                    parentFullName: 'Лебедева Ольга Васильевна',
                    parentPhone: '+7 (930) 123-45-67',
                    grades: [
                        {
                            id: 106,
                            subject: 'Физика',
                            group: 'В34567',
                            score: 'Удовлетворительно',
                            date: '10.06.2025',
                            teacherFullName: 'Воронов Роман Павлович',
                        },
                    ],
                    studies: [
                        {
                            id: 's106',
                            subject: 'Физика',
                            startDate: '01.09.2024',
                        },
                    ],
                    payments: [
                        {
                            id: 206,
                            amount: 3000,
                            for: 'Июнь 2025',
                            debt: 1000,
                            status: 'Ошибка',
                            date: '01.06.2025',
                            group: 'В34567',
                        },
                    ],
                    subscriptionActive: true,
                },
                {
                    id: 7,
                    fullName: 'Егорова София Владимировна',
                    img: 'https://randomuser.me/api/portraits/women/12.jpg',
                    dateOfBirth: '08.04.2011',
                    groups: ['В34567'],
                    phone: '+7 (921) 456-78-90',
                    email: 'egorova.sofia@example.com',
                    parentFullName: 'Егоров Владимир Сергеевич',
                    parentPhone: '+7 (921) 654-32-10',
                    grades: [
                        {
                            id: 107,
                            subject: 'Физика',
                            group: 'В34567',
                            score: 'Хорошо',
                            date: '12.06.2025',
                            teacherFullName: 'Воронов Роман Павлович',
                        },
                    ],
                    studies: [
                        {
                            id: 's107',
                            subject: 'Физика',
                            startDate: '01.09.2024',
                        },
                    ],
                    payments: [
                        {
                            id: 207,
                            amount: 2900,
                            for: 'Июнь 2025',
                            debt: 0,
                            status: 'Успешно',
                            date: '03.06.2025',
                            group: 'В34567',
                        },
                    ],
                    subscriptionActive: true,
                },
                {
                    id: 8,
                    fullName: 'Васильев Артём Сергеевич',
                    img: 'https://randomuser.me/api/portraits/men/78.jpg',
                    dateOfBirth: '14.02.2012',
                    groups: ['Г45678'],
                    phone: '+7 (931) 101-20-30',
                    email: 'vasiliev.artem@example.com',
                    parentFullName: 'Васильева Елена Викторовна',
                    parentPhone: '+7 (931) 202-30-40',
                    grades: [
                        {
                            id: 108,
                            subject: 'География',
                            group: 'Г45678',
                            score: 'Плохо',
                            date: '09.06.2025',
                            teacherFullName: 'Синицина Наталья Аркадьевна',
                            teachersComment: 'Не сдал итоговый проект',
                        },
                    ],
                    studies: [
                        {
                            id: 's108',
                            subject: 'География',
                            startDate: '01.09.2024',
                        },
                    ],
                    payments: [
                        {
                            id: 208,
                            amount: 2700,
                            for: 'Июнь 2025',
                            debt: 800,
                            status: 'Ошибка',
                            date: '05.06.2025',
                            group: 'Г45678',
                        },
                    ],
                    subscriptionActive: false,
                },
                {
                    id: 9,
                    fullName: 'Морозова Ксения Павловна',
                    img: 'https://randomuser.me/api/portraits/women/23.jpg',
                    dateOfBirth: '23.09.2010',
                    groups: ['Г45678'],
                    phone: '+7 (999) 111-22-33',
                    email: 'morozova.kseniya@example.com',
                    parentFullName: 'Морозов Павел Владимирович',
                    parentPhone: '+7 (999) 333-22-11',
                    grades: [
                        {
                            id: 109,
                            subject: 'Биология',
                            group: 'Г45678',
                            score: 'Отлично',
                            date: '08.06.2025',
                            teacherFullName: 'Тарасова Юлия Игоревна',
                        },
                    ],
                    studies: [
                        {
                            id: 's109',
                            subject: 'Биология',
                            startDate: '01.09.2024',
                        },
                    ],
                    payments: [
                        {
                            id: 209,
                            amount: 3000,
                            for: 'Июнь 2025',
                            debt: 0,
                            status: 'Успешно',
                            date: '04.06.2025',
                            group: 'Г45678',
                        },
                    ],
                    subscriptionActive: true,
                },
                {
                    id: 10,
                    fullName: 'Соколов Илья Олегович',
                    img: 'https://randomuser.me/api/portraits/men/21.jpg',
                    dateOfBirth: '18.05.2009',
                    groups: ['Г45678'],
                    phone: '+7 (921) 765-43-21',
                    email: 'sokolov.ilya@example.com',
                    parentFullName: 'Соколова Ирина Михайловна',
                    parentPhone: '+7 (921) 765-43-00',
                    grades: [
                        {
                            id: 110,
                            subject: 'Физкультура',
                            group: 'Г45678',
                            score: 'Хорошо',
                            date: '06.06.2025',
                            teacherFullName: 'Сидоров Андрей Евгеньевич',
                        },
                    ],
                    studies: [
                        {
                            id: 's110',
                            subject: 'Физкультура',
                            startDate: '01.09.2024',
                        },
                    ],
                    payments: [
                        {
                            id: 210,
                            amount: 2500,
                            for: 'Июнь 2025',
                            debt: 500,
                            status: 'Ошибка',
                            date: '05.06.2025',
                            group: 'Г45678',
                        },
                    ],
                    subscriptionActive: true,
                },
                {
                    id: 11,
                    fullName: 'Тихонов Алексей Викторович',
                    img: 'https://randomuser.me/api/portraits/men/61.jpg',
                    dateOfBirth: '07.07.2011',
                    groups: ['Д56789'],
                    phone: '+7 (912) 333-22-44',
                    email: 'tikhonov.aleksey@example.com',
                    parentFullName: 'Тихонова Марина Валерьевна',
                    parentPhone: '+7 (912) 777-66-55',
                    grades: [
                        {
                            id: 111,
                            subject: 'Информатика',
                            group: 'Д56789',
                            score: 'Отлично',
                            date: '11.06.2025',
                            teacherFullName: 'Федоров Иван Сергеевич',
                        },
                    ],
                    studies: [
                        {
                            id: 's111',
                            subject: 'Информатика',
                            startDate: '01.09.2024',
                        },
                    ],
                    payments: [
                        {
                            id: 211,
                            amount: 3500,
                            for: 'Июнь 2025',
                            debt: 0,
                            status: 'Успешно',
                            date: '04.06.2025',
                            group: 'Д56789',
                        },
                    ],
                    subscriptionActive: true,
                },
                {
                    id: 12,
                    fullName: 'Андреева Валерия Романовна',
                    img: 'https://randomuser.me/api/portraits/women/36.jpg',
                    dateOfBirth: '29.01.2010',
                    groups: ['Д56789'],
                    phone: '+7 (904) 123-33-44',
                    email: 'andreeva.valeria@example.com',
                    parentFullName: 'Андреев Роман Васильевич',
                    parentPhone: '+7 (904) 555-66-77',
                    grades: [
                        {
                            id: 112,
                            subject: 'Технология',
                            group: 'Д56789',
                            score: 'Удовлетворительно',
                            date: '10.06.2025',
                            teacherFullName: 'Шестакова Лидия Дмитриевна',
                        },
                    ],
                    studies: [
                        {
                            id: 's112',
                            subject: 'Технология',
                            startDate: '01.09.2024',
                        },
                    ],
                    payments: [
                        {
                            id: 212,
                            amount: 3300,
                            for: 'Июнь 2025',
                            debt: 200,
                            status: 'Ошибка',
                            date: '05.06.2025',
                            group: 'Д56789',
                        },
                    ],
                    subscriptionActive: true,
                },
                {
                    id: 13,
                    fullName: 'Григорьев Артём Николаевич',
                    img: 'https://randomuser.me/api/portraits/men/43.jpg',
                    dateOfBirth: '03.12.2011',
                    groups: ['Е67890'],
                    phone: '+7 (906) 678-90-12',
                    email: 'grigoryev.artem@example.com',
                    parentFullName: 'Григорьева Наталья Юрьевна',
                    parentPhone: '+7 (906) 987-65-43',
                    grades: [
                        {
                            id: 113,
                            subject: 'ОБЖ',
                            group: 'Е67890',
                            score: 'Хорошо',
                            date: '08.06.2025',
                            teacherFullName: 'Власов Аркадий Александрович',
                        },
                    ],
                    studies: [
                        {
                            id: 's113',
                            subject: 'ОБЖ',
                            startDate: '01.09.2024',
                        },
                    ],
                    payments: [
                        {
                            id: 213,
                            amount: 3100,
                            for: 'Июнь 2025',
                            debt: 0,
                            status: 'Успешно',
                            date: '03.06.2025',
                            group: 'Е67890',
                        },
                    ],
                    subscriptionActive: true,
                },
                {
                    id: 14,
                    fullName: 'Полякова Алиса Денисовна',
                    img: 'https://randomuser.me/api/portraits/women/66.jpg',
                    dateOfBirth: '15.08.2010',
                    groups: ['Е67890'],
                    phone: '+7 (999) 333-22-11',
                    email: 'polyakova.alisa@example.com',
                    parentFullName: 'Поляков Денис Александрович',
                    parentPhone: '+7 (999) 123-45-67',
                    grades: [
                        {
                            id: 114,
                            subject: 'Музыка',
                            group: 'Е67890',
                            score: 'Отлично',
                            date: '06.06.2025',
                            teacherFullName: 'Ларионова Ирина Дмитриевна',
                        },
                    ],
                    studies: [
                        {
                            id: 's114',
                            subject: 'Музыка',
                            startDate: '01.09.2024',
                        },
                    ],
                    payments: [
                        {
                            id: 214,
                            amount: 2950,
                            for: 'Июнь 2025',
                            debt: 150,
                            status: 'Ошибка',
                            date: '05.06.2025',
                            group: 'Е67890',
                        },
                    ],
                    subscriptionActive: true,
                },
            ]
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
