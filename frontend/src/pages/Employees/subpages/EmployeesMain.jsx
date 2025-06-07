import {FilterBar} from "../../../components/page/FilterBar"
import {EmployeesTable} from "../components/EmployeesTable"

const filterData = [
	{
		id: "department",
		label: "Отдел",
		data: ["Отдел продаж", "Бухгалтерия", "IT", "HR"],
		top: "Все",
		multiple: true,
        placeholder: "Все"
	},
	{
		id: "employees",
		label: "Сотрудник",
		data: ["Иванов И.И.", "Петров П.П.", "Сидоров С.С."],
        placeholder: "Все"
	},
	{
		id: "filters",
		label: "Фильтр",
		data: ["Активные", "Неактивные"],
	},
	{
		id: "exportTypes",
		label: "Экспорт",
		data: ["xlsx", "csv", "pdf"],
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
