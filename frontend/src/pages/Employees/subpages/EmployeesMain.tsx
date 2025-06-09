import {FilterBar} from "../../../components/page/FilterBar"
import {EmployeesTable} from "../components/EmployeesTable"

const filterData = [
	{
		id: "department",
		label: "Отдел",
		options: ["Отдел продаж", "Бухгалтерия", "IT", "HR"],
		top: "Все",
		multiple: true,
        placeholder: "Все"
	},
	{
		id: "employees",
		label: "Сотрудник",
		options: ["Иванов И.И.", "Петров П.П.", "Сидоров С.С."],
        placeholder: "Все"
	},
	{
		id: "filters",
		label: "Фильтр",
		options: ["Активные", "Неактивные"],
	},
	{
		id: "exportTypes",
		label: "Экспорт",
		options: ["xlsx", "csv", "pdf"],
		default: "xlsx",
	},
]

export function EmployeesMain() {
	return (
		<>
            <FilterBar filterData={filterData} />
			<EmployeesTable />
		</>
	)
}

export default EmployeesMain
