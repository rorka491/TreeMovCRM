import { useEffect, useState } from 'react'
import { FilterBar } from '../../../components/page/FilterBar'
import { Employee } from '../../../api/api'
import { api } from '../../../api'
import { Table } from '../../../components/Table'
import { useNavigate } from 'react-router-dom'

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

const departments = [{}]

export function EmployeesMain() {
    // const [departments, setDepartments] = useState<Department[]>([])
    const navigate = useNavigate()

    // useEffect(() => {
    //     api.department.getAllDepartments().then(setDepartments)
    // }, [])

    return (
        <>
            <FilterBar filterData={filterData} />
            <Table
                data={departments}
                keys={{
                    department: 'Все отделы',
                    countOfEmployees: 'Кол-во сотрудников',
                    access: 'Права доступа',
                    countOfEmployeesOnShift: 'Сейчас на смене',
                    id: 'Код отдела',
                }}
                showSkeleton={departments.length === 0}
                skeletonAmount={18}
                rowActions={{
                    Открыть: (department) =>
                        navigate('/department/' + department.id),
                    Изменить: (department) =>
                        navigate('/department/' + department.id + '/edit'),
                    'В архив': () => {
                        //TODO!
                    },
                    Удалить: () => {
                        //TODO!
                    },
                }}
            />
        </>
    )
}

export default EmployeesMain
