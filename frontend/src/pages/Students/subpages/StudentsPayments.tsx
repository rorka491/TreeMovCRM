import { FilterBar } from '../../../components/page/FilterBar'
import { api } from '../../../api'
import { useEffect, useState } from 'react'
import { Table } from '../../../components/Table'
import { useNavigate } from 'react-router-dom'
import { Student } from '../../../api/fakeApi'

export function StudentsPayments() {
    const [students, setStudents] = useState<Student[]>([])
    const [loaded, setLoaded] = useState(false)
    const navigate = useNavigate()

    useEffect(() => {
        ;(async () => {
            const students = await api.students.getAll()
            setStudents(students)
            setLoaded(true)
            filterData[0].options = await api.students.getAllGroups()
            filterData[1].options = students.map((student) => student.fullName)
            setFilterData([...filterData])
        })()
    }, [])

    const [filtersSelected, setFiltersSelected] = useState<{
        [k: string]: any | undefined
    }>({})

    const [filterData, setFilterData] = useState([
        {
            id: 'group',
            label: 'Группа',
            options: ['A', 'B'],
            multiple: true,
            search: true,
            removeButton: true,
        },
        {
            id: 'student',
            label: 'Ученик',
            options: ['Иванов'],
            multiple: true,
            search: true,
            removeButton: true,
        },
        {
            id: 'active',
            label: 'Фильтр',
            options: ['Активные', 'Неактивные'],
            removeButton: true,
        },
        {
            id: 'exportTypes',
            label: 'Экспорт',
            options: ['xlsx', 'csv', 'pdf'],
            default: 'xlsx',
        },
    ])

    return (
        <>
            <FilterBar
                filterData={filterData}
                selectedChange={setFiltersSelected}
            />
            <Table
                data={students
                    .filter((student) =>
                        filtersSelected.group &&
                        filtersSelected.group.length > 0
                            ? filtersSelected.group.reduce(
                                  (result, group) =>
                                      result || student.groups.includes(group),
                                  false
                              )
                            : true
                    )
                    .filter((student) =>
                        filtersSelected.student &&
                        filtersSelected.student.length > 0
                            ? filtersSelected.student.some(
                                  (fullName) => fullName === student.fullName
                              )
                            : true
                    )
                    .filter((student) =>
                        filtersSelected.active
                            ? (filtersSelected.active === 'Активные' &&
                                  student.subscriptionActive) ||
                              (filtersSelected.active === 'Неактивные' &&
                                  !student.subscriptionActive)
                            : true
                    )
                    .map((student) =>
                        student.payments.map((payment) => ({
                            id: `${student.id}-${payment.for}-${payment.date}`,
                            studentFullName: student.fullName,
                            group: payment.group,
                            status: student.subscriptionActive
                                ? 'Активен'
                                : 'Не активен',
                            date: payment.date,
                            amount: payment.amount + ' ₽',
                            for: payment.for,
                            paymentStatus: payment.status,
                            debt: payment.debt,
                        }))
                    )
                    .flat()}
                keys={{
                    studentFullName: 'Ученик',
                    group: 'Группа',
                    status: 'Статус',
                    date: 'Дата платежа',
                    amount: 'Сумма',
                    for: 'Назначение платежа',
                    paymentStatus: 'Статус оплаты',
                    debt: 'Задолженность',
                }}
                conditionalClassNames={{
                    paymentStatus: (student) =>
                        ({
                            Успешно: 'text-[#22C55E]',
                            Ошибка: 'text-[#FF1814]',
                        })[student.paymentStatus] ?? '',
                    status: (student) =>
                        ({
                            Активен: 'text-[#22C55E]',
                            'Не активен': 'text-[#FF1814]',
                        })[student.status] ?? '',
                    debt: (student) =>
                        student.debt > 0 ? 'text-[#FF1814]' : '',
                }}
                mapFields={{
                    debt: (payment) =>
                        payment.debt > 0 ? payment.debt + ' ₽' : 'нет',
                }}
                rowActions={{
                    Открыть: (student) =>
                        navigate('/students/profile/' + student.id),
                    Изменить: (student) =>
                        navigate('/students/profile/' + student.id + '/edit'),
                    Удалить: () => {
                        //TODO!
                    },
                }}
                showSkeleton={!loaded}
                skeletonAmount={18}
            />
        </>
    )
}
