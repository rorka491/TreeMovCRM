let baseLatency = parseFloat(localStorage.getItem('fakeApi:fakeLatency') ?? 0)
let latencyVariance = parseFloat(
    localStorage.getItem('fakeApi:latencyVariance') ?? 0
)

// в консоли браузера можно контролировать задержку у фейкового апи
// просто пишешь:
// setFakeLatency(<Тут задержка нужная>)
globalThis.setFakeLatency = (base, variance = 0) => {
    baseLatency = base
    localStorage.setItem('fakeApi:fakeLatency', base + '')
    latencyVariance = variance
    localStorage.setItem('fakeApi:latencyVariance', variance + '')
}

const baseApi = {
    students: {
        getAll() {
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
                    ],
                    subscriptionActive: true,
                    debt: 2460,
                    nextPaymentDate: '',
                },
                {
                    id: 2,
                    fullName: 'Иванова Мария Сергеевна',
                    img: '/maria',
                    dateOfBirth: '05.03.2012',
                    groups: ['B21111', 'A51112'],
                    phone: '8 900 111 11 11',
                    email: 'maria.ivanova@mail.com',
                    parentFullName: 'Иванов Сергей Петрович',
                    parentPhone: '8 999 111 11 11',
                    grades: [
                        {
                            subject: 'Математика',
                            group: 'A51112',
                            score: 'Хорошо',
                        },
                        {
                            subject: 'Физика',
                            group: 'B21111',
                            score: 'Отлично',
                        },
                    ],
                    subscriptionActive: true,
                    debt: 0,
                    nextPaymentDate: '15.07.2024',
                },
                {
                    id: 3,
                    fullName: 'Петров Артём Дмитриевич',
                    img: '/artem',
                    dateOfBirth: '22.07.2010',
                    groups: ['D31115'],
                    phone: '8 900 222 22 22',
                    email: 'artem.petrov@mail.com',
                    parentFullName: 'Петрова Ольга Викторовна',
                    parentPhone: '8 999 222 22 22',
                    grades: [
                        {
                            subject: 'Английский язык',
                            group: 'D31115',
                            score: 'Удовлетворительно',
                        },
                    ],
                    subscriptionActive: false,
                    debt: 5000,
                    nextPaymentDate: '01.06.2024',
                },
            ]
        },
        getById(id) {
            return this.getAll().find((student) => student.id === id || (student.id + "") === id)
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

function goThroughKeys(obj) {
    const result = {}

    for (const key in obj) {
        if (typeof obj[key] === 'function') {
            result[key] = (...args) =>
                new Promise((resolve, reject) => {
                    const result = obj[key](...args)
                    const timeout =
                        baseLatency + Math.random() * latencyVariance

                    setTimeout(() => resolve(result), timeout)
                })
        } else {
            result[key] = goThroughKeys(obj[key])
        }
    }

    return result
}

export const fakeApi = goThroughKeys(baseApi)
