import { useOutletContext } from 'react-router-dom'
import EmployeeCard from '../components/EmployeeCard'

export function EmployeesVacationCards() {
    const employees = useOutletContext()
    return (
        <ul className="grid grid-cols-2 gap-x-[18px] gap-y-[20px] w-full h-[100%] overflow-y-scroll special-scroll">
            {employees.map((card, i) => {
                return <EmployeeCard {...card} key={i} />
            })}
        </ul>
    )
}

export default EmployeesVacationCards
