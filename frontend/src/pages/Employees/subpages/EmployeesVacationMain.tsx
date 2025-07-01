import { useEffect, useState } from 'react'
import { FilterBar } from '../../../components/page/FilterBar'
import { Employee } from '../../../api/api'
import { api } from '../../../api'
import { Table } from '../../../components/Table'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import StatisticsCard from '../components/StatisticsCard'

export function EmployeesVacationMain() {
    const navigate = useNavigate()
    // const [employees, setEmployees] = useState<Employee[]>([])
    const employees = [{}, {}, {}, {}]
    const statistics = [{}, {}, {}]
    const route = useLocation()
    const dataView = {
        Таблица: '',
        Карточки: 'by-cards',
        Календарь: 'by-calendar',
    }

    const filterData = [
        {
            id: 'view',
            label: 'Вид',
            options: ['Таблица', 'Карточки', 'Календарь'],
            setSelected: (o) => {
                navigate('/employees/vacation/' + dataView[o])
            },
            default: 'Таблица',
        },
        {
            id: 'department',
            label: 'Отдел',
            multiple: true,
            options: ['Преподователи', 'Менеджеры'],
        },
        {
            id: 'date',
            label: 'Дата',
            multiple: true,
            options: ['11.22.3333', '44.55.6666'],
        },
        {
            id: 'status',
            label: 'Статус',
            options: ['Запрошен', 'Утвержден'],
            multiple: true,
            placeholder: 'Все',
        },
        {
            id: 'filters',
            label: 'Фильтр',
            multiple: true,
            options: ['Активные', 'Неактивные'],
        },
        {
            id: 'exportTypes',
            label: 'Экспорт',
            options: ['xlsx', 'csv', 'pdf'],
            default: 'xlsx',
        },
    ]

    // useEffect(() => {
    //     api.employees.getAllEmployees().then(setEmployees)
    // }, [])

    return (
        <>
            <FilterBar filterData={filterData} />

            {route.pathname.split('/')[3] === '' ||
            route.pathname.split('/')[3] === undefined ? (
                <Table
                    data={employees.map((employee) => ({
                        ...employee,
                        fullName: `${employee.surname} ${employee.name} ${employee.patronymic}`,
                    }))}
                    keys={{
                        id: '№',
                        fullName: 'ФИО',
                        position: 'Должность',
                        department: 'Отдел',
                        vacationType: 'Тип отпуска',
                        startDate: 'Дата начала',
                        endDate: 'Дата окончания',
                        vacationStatus: 'Статус',
                    }}
                    showSkeleton={employees.length === 0}
                    skeletonAmount={18}
                    rowActions={{
                        Открыть: (employee) =>
                            navigate('/employees/vacation/' + employee.id),
                        Изменить: (employee) =>
                            navigate(
                                '/employees/vacation/' + employee.id + '/edit'
                            ),
                        Удалить: () => {
                            //TODO!
                        },
                    }}
                />
            ) : (
                <Outlet context={employees} />
            )}
            {route.pathname.split('/')[3] === '' ||
            route.pathname.split('/')[3] === undefined ||
            route.pathname.split('/')[3] === 'by-cards' ? (
                <ul className="flex gap-[20px]">
                    {statistics.map((card, i) => {
                        return <StatisticsCard {...card} key={i} />
                    })}
                </ul>
            ) : null}
        </>
    )
}

export default EmployeesVacationMain
