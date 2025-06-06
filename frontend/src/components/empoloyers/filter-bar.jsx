import DropDown from './drop-down'

const filterData = [
    {
        id: 'department',
        label: 'Отдел',
        data: ['Все', 'Отдел продаж', 'Бухгалтерия', 'IT', 'HR'],
    },
    {
        id: 'employees',
        label: 'Сотрудник',
        data: ['Все', 'Иванов И.И.', 'Петров П.П.', 'Сидоров С.С.'],
    },
    {
        id: 'filters',
        label: 'Фильтр',
        data: ['Все', 'Активные', 'Неактивные'],
    },
    {
        id: 'exportTypes',
        label: 'Экспорт',
        data: ['xlsx', 'csv', 'pdf'],
    },
]

const FilterBar = () => {
    return (
        <div className="grid grid-flow-col items-end gap-x-2.5 grid-cols-[min-content_5fr_7fr_3fr_2fr_2fr] w-full bg-white p-4 rounded-[12.5px] *:rounded-[12.5px]">
            <button className="grid w-10 text-base text-center duration-100 border place-items-center aspect-square hover:bg-gray-50">
                <span className="flex w-min h-min">+</span>
            </button>

            {filterData.map((props) => {
                return <DropDown props={props} key={props.id} />
            })}

            <button className="text-xs font-medium text-purple-600 duration-200 border border-purple-600 rounded-lg py-2.5 hover:bg-purple-100">
                Экспорт
            </button>
        </div>
    )
}

export default FilterBar
