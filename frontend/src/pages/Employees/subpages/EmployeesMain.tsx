import { useEffect, useState } from 'react'
import { FilterBar } from '../../../components/page/FilterBar'
import { Employee } from '../../../api/api'
import { api } from '../../../api'
import { Table } from '../../../components/Table'

const filterData = [
    {
        id: 'department',
        label: 'Отдел',
        options: ['Отдел продаж', 'Бухгалтерия', 'IT', 'HR'],
        top: 'Все',
        multiple: true,
        placeholder: 'Все',
    },
    {
        id: 'employees',
        label: 'Сотрудник',
        options: ['Иванов И.И.', 'Петров П.П.', 'Сидоров С.С.'],
        placeholder: 'Все',
    },
    {
        id: 'filters',
        label: 'Фильтр',
        options: ['Активные', 'Неактивные'],
    },
    {
        id: 'exportTypes',
        label: 'Экспорт',
        options: ['xlsx', 'csv', 'pdf'],
        default: 'xlsx',
    },
]

export function EmployeesMain() {
    const [employees, setEmployees] = useState<Employee[]>([])

    useEffect(() => {
        api.employees.getAllEmployees().then(setEmployees)
    }, [])

    return (
        <>
            <FilterBar filterData={filterData} />
            <Table data={employees.map(employee => ({...employee, fullName: `${employee.surname} ${employee.name} ${employee.patronymic}`}))} keys={{
                id: "№",
                fullName: "ФИО",

            }} />
        </>
    )
}

export default EmployeesMain
