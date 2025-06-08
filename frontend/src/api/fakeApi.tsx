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

type Students = {
    id: string | number
    fullName: number
    img: number
    dateOfBirth: number
    groups: string[]
    phone: string
    email: string
    parentFullName: string
    parentPhone: string
    grades: {
        subject: string
        group: string
        score: string
    }[]
    studies: {
        subject: string
        startDate: string
    }[]
    subscriptionActive: boolean
    debt: number
    nextPaymentDate: string
}

const baseApi = {
    students: {
        getAll(): Students[] {
            return [
                {
                    id: 1,
                    fullName: 'Степанов Максим Антонович',
                    img: '/maloy.png',
                    dateOfBirth: '11.10.2011',
                    groups: ['B21111', 'C61113'],
                    phone: '8 900 000 00 00',
                    email: 'minmaxmail@mail.com',
                    parentFullName: 'Степанова Анастасия Александровна',
                    parentPhone: '8 999 000 00 00',
                    grades: [
                        {
                            subject: 'Программирование',
                            group: 'C61114',
                            score: 'Отлично',
                        },
                        {
                            subject: 'Акробатика',
                            group: 'B21111',
                            score: 'Удовлетворительно',
                        },
                        {
                            subject: 'Финансовое воспитание',
                            group: 'B21111',
                            score: 'Плохо',
                        },
                        {
                            subject: 'Английский язык',
                            group: 'B21111',
                            score: 'Отлично',
                        },
                        {
                            subject: 'Английский язык',
                            group: 'B21111',
                            score: 'Удовлетворительно',
                        },
                        {
                            subject: 'Пение',
                            group: 'C21153',
                            score: 'Хорошо',
                        },
                        {
                            subject: 'Плавание',
                            group: 'C21153',
                            score: 'Хорошо',
                        },
                        {
                            subject: 'Английский язык',
                            group: 'B21111',
                            score: 'Отлично',
                        },
                        {
                            subject: 'Окружающий мир',
                            group: 'B21111',
                            score: 'Плохо',
                        },
                        {
                            subject: 'Музыка',
                            group: 'B21111',
                            score: 'Отлично',
                        },
                        {
                            subject: 'Музыка',
                            group: 'B21111',
                            score: 'Отлично',
                        },
                        {
                            subject: 'Акробатика',
                            group: 'B21111',
                            score: 'Удовлетворительно',
                        },
                    ],
                    studies: [
                        {
                            subject: 'Программирование',
                            startDate: '01.05.2024',
                        },
                        {
                            subject: 'Акробатика',
                            startDate: '01.09.2023',
                        },
                        {
                            subject: 'Английский язык',
                            startDate: '25.04.2021',
                        },
                        {
                            subject: 'Плавание',
                            startDate: '05.04.2022',
                        },
                        {
                            subject: 'Финансовое воспитание 2',
                            startDate: '11.10.2023',
                        },
                        {
                            subject: 'Финансовое воспитание',
                            startDate: '11.10.2023',
                        },
                    ],
                    subscriptionActive: true,
                    debt: 2460,
                    nextPaymentDate: '',
                },
                {
                    id: 2,
                    fullName: 'Иванова София Дмитриевна',
                    img: '/student2.png',
                    dateOfBirth: '05.03.2002',
                    groups: ['B21111', 'A31115'],
                    phone: '8 900 111 11 11',
                    email: 'sofia.ivanova@mail.com',
                    parentFullName: 'Иванов Дмитрий Сергеевич',
                    parentPhone: '8 999 111 11 11',
                    grades: [
                        {
                            subject: 'Математика',
                            group: 'B21111',
                            score: 'Хорошо',
                        },
                        {
                            subject: 'Английский язык',
                            group: 'A31115',
                            score: 'Отлично',
                        },
                    ],
                    studies: [
                        {
                            subject: 'Математика',
                            startDate: '10.01.2024',
                        },
                        {
                            subject: 'Английский язык',
                            startDate: '15.02.2024',
                        },
                    ],
                    subscriptionActive: true,
                    debt: 0,
                    nextPaymentDate: '15.07.2024',
                },
                {
                    id: 3,
                    fullName: 'Петров Артём Игоревич',
                    img: '/student3.png',
                    dateOfBirth: '22.07.2010',
                    groups: ['D51112', 'C61113'],
                    phone: '8 900 222 22 22',
                    email: 'artem.petrov@mail.com',
                    parentFullName: 'Петрова Елена Викторовна',
                    parentPhone: '8 999 222 22 22',
                    grades: [
                        {
                            subject: 'Физика',
                            group: 'D51112',
                            score: 'Удовлетворительно',
                        },
                    ],
                    studies: [
                        {
                            subject: 'Физика',
                            startDate: '03.03.2024',
                        },
                        {
                            subject: 'Программирование',
                            startDate: '20.04.2024',
                        },
                    ],
                    subscriptionActive: false,
                    debt: 5400,
                    nextPaymentDate: '',
                },
                {
                    id: 4,
                    fullName: 'Смирнова Алиса Кирилловна',
                    img: '/student4.png',
                    dateOfBirth: '18.09.2011',
                    groups: ['A31115', 'E71116'],
                    phone: '8 900 333 33 33',
                    email: 'alisa.smirnova@mail.com',
                    parentFullName: 'Смирнов Кирилл Александрович',
                    parentPhone: '8 999 333 33 33',
                    grades: [
                        {
                            subject: 'Литература',
                            group: 'A31115',
                            score: 'Отлично',
                        },
                        {
                            subject: 'Биология',
                            group: 'E71116',
                            score: 'Хорошо',
                        },
                    ],
                    studies: [
                        {
                            subject: 'Литература',
                            startDate: '12.01.2024',
                        },
                        {
                            subject: 'Биология',
                            startDate: '25.02.2024',
                        },
                    ],
                    subscriptionActive: true,
                    debt: 1200,
                    nextPaymentDate: '05.07.2024',
                },
                {
                    id: 5,
                    fullName: 'Кузнецов Даниил Романович',
                    img: '/student5.png',
                    dateOfBirth: '30.01.2012',
                    groups: ['B21111', 'F81117'],
                    phone: '8 900 444 44 44',
                    email: 'daniel.kuznetsov@mail.com',
                    parentFullName: 'Кузнецова Ольга Игоревна',
                    parentPhone: '8 999 444 44 44',
                    grades: [
                        {
                            subject: 'Химия',
                            group: 'F81117',
                            score: 'Хорошо',
                        },
                    ],
                    studies: [
                        {
                            subject: 'Химия',
                            startDate: '08.03.2024',
                        },
                    ],
                    subscriptionActive: true,
                    debt: 0,
                    nextPaymentDate: '20.07.2024',
                },
                {
                    id: 6,
                    fullName: 'Васильева Виктория Максимовна',
                    img: '/student6.png',
                    dateOfBirth: '14.05.2011',
                    groups: ['C61113', 'G91118'],
                    phone: '8 900 555 55 55',
                    email: 'viktoria.vasilieva@mail.com',
                    parentFullName: 'Васильев Максим Андреевич',
                    parentPhone: '8 999 555 55 55',
                    grades: [
                        {
                            subject: 'История',
                            group: 'G91118',
                            score: 'Отлично',
                        },
                    ],
                    studies: [
                        {
                            subject: 'История',
                            startDate: '17.04.2024',
                        },
                    ],
                    subscriptionActive: false,
                    debt: 3200,
                    nextPaymentDate: '',
                },
                {
                    id: 7,
                    fullName: 'Новиков Александр Павлович',
                    img: '/student7.png',
                    dateOfBirth: '27.11.2010',
                    groups: ['D51112', 'H01119'],
                    phone: '8 900 666 66 66',
                    email: 'alex.novikov@mail.com',
                    parentFullName: 'Новикова Татьяна Владимировна',
                    parentPhone: '8 999 666 66 66',
                    grades: [
                        {
                            subject: 'География',
                            group: 'H01119',
                            score: 'Хорошо',
                        },
                    ],
                    studies: [
                        {
                            subject: 'География',
                            startDate: '22.02.2024',
                        },
                    ],
                    subscriptionActive: true,
                    debt: 0,
                    nextPaymentDate: '10.08.2024',
                },
                {
                    id: 8,
                    fullName: 'Морозова Елизавета Артёмовна',
                    img: '/student8.png',
                    dateOfBirth: '03.08.2012',
                    groups: ['A31115', 'I11120'],
                    phone: '8 900 777 77 77',
                    email: 'liza.morozova@mail.com',
                    parentFullName: 'Морозов Артём Дмитриевич',
                    parentPhone: '8 999 777 77 77',
                    grades: [
                        {
                            subject: 'Информатика',
                            group: 'I11120',
                            score: 'Отлично',
                        },
                    ],
                    studies: [
                        {
                            subject: 'Информатика',
                            startDate: '05.01.2024',
                        },
                    ],
                    subscriptionActive: true,
                    debt: 1800,
                    nextPaymentDate: '25.06.2024',
                },
                {
                    id: 9,
                    fullName: 'Фёдоров Михаил Сергеевич',
                    img: '/student9.png',
                    dateOfBirth: '19.04.2011',
                    groups: ['B21111', 'J21121'],
                    phone: '8 900 888 88 88',
                    email: 'mikhail.fedorov@mail.com',
                    parentFullName: 'Фёдорова Анна Михайловна',
                    parentPhone: '8 999 888 88 88',
                    grades: [
                        {
                            subject: 'Физическая культура',
                            group: 'J21121',
                            score: 'Хорошо',
                        },
                    ],
                    studies: [
                        {
                            subject: 'Физическая культура',
                            startDate: '14.03.2024',
                        },
                    ],
                    subscriptionActive: false,
                    debt: 4200,
                    nextPaymentDate: '',
                },
                {
                    id: 10,
                    fullName: 'Антонова Дарья Евгеньевна',
                    img: '/student10.png',
                    dateOfBirth: '07.12.2012',
                    groups: ['C61113', 'K31122'],
                    phone: '8 900 999 99 99',
                    email: 'darya.antonova@mail.com',
                    parentFullName: 'Антонов Евгений Валерьевич',
                    parentPhone: '8 999 999 99 99',
                    grades: [
                        {
                            subject: 'Музыка',
                            group: 'K31122',
                            score: 'Отлично',
                        },
                    ],
                    studies: [
                        {
                            subject: 'Музыка',
                            startDate: '28.04.2024',
                        },
                    ],
                    subscriptionActive: true,
                    debt: 0,
                    nextPaymentDate: '30.06.2024',
                },
                {
                    id: 11,
                    fullName: 'Тимофеев Иван Алексеевич',
                    img: '/student11.png',
                    dateOfBirth: '25.02.2010',
                    groups: ['D51112', 'L41123'],
                    phone: '8 900 123 45 67',
                    email: 'ivan.timofeev@mail.com',
                    parentFullName: 'Тимофеева Светлана Петровна',
                    parentPhone: '8 999 123 45 67',
                    grades: [
                        {
                            subject: 'Рисование',
                            group: 'L41123',
                            score: 'Хорошо',
                        },
                    ],
                    studies: [
                        {
                            subject: 'Рисование',
                            startDate: '11.01.2024',
                        },
                    ],
                    subscriptionActive: true,
                    debt: 900,
                    nextPaymentDate: '15.07.2024',
                },
                {
                    id: 12,
                    fullName: 'Тимофеев Иван Алексеевич',
                    img: '/student11.png',
                    dateOfBirth: '25.02.2010',
                    groups: ['D51112', 'L41123'],
                    phone: '8 900 123 45 67',
                    email: 'ivan.timofeev@mail.com',
                    parentFullName: 'Тимофеева Светлана Петровна',
                    parentPhone: '8 999 123 45 67',
                    grades: [
                        {
                            subject: 'Рисование',
                            group: 'L41123',
                            score: 'Хорошо',
                        },
                    ],
                    studies: [
                        {
                            subject: 'Рисование',
                            startDate: '11.01.2024',
                        },
                    ],
                    subscriptionActive: true,
                    debt: 900,
                    nextPaymentDate: '15.07.2024',
                },
                {
                    id: 13,
                    fullName: 'Тимофеев Иван Алексеевич',
                    img: '/student11.png',
                    dateOfBirth: '25.02.2010',
                    groups: ['D51112', 'L41123'],
                    phone: '8 900 123 45 67',
                    email: 'ivan.timofeev@mail.com',
                    parentFullName: 'Тимофеева Светлана Петровна',
                    parentPhone: '8 999 123 45 67',
                    grades: [
                        {
                            subject: 'Рисование',
                            group: 'L41123',
                            score: 'Хорошо',
                        },
                    ],
                    studies: [
                        {
                            subject: 'Рисование',
                            startDate: '11.01.2024',
                        },
                    ],
                    subscriptionActive: true,
                    debt: 900,
                    nextPaymentDate: '15.07.2024',
                },
            ]
        },
        getById(id) {
            return this.getAll().find(
                (student) => student.id === id || student.id + '' === id
            )
        },
        getAllGroups() {
            return Array.from(
                new Set(
                    this.getAll().reduce(
                        (result, current) => [...result, ...current.groups],
                        []
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
        : T[key]
}

export const fakeApi = goThroughKeys(baseApi) as MapToAsync<typeof baseApi>
