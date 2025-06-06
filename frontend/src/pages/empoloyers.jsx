import { useLocation } from 'react-router-dom'
import CategoryBar from '../components/empoloyers/category-bar'
import DepartmentsTable from '../components/empoloyers/departments-table'
import FilterBar from '../components/empoloyers/filter-bar'
import KpiCard from '../components/empoloyers/kpi-card'
import StatsCards from '../components/empoloyers/stats-cards'
import EmployeesTable from '../components/empoloyers/employees-table'

function EmpoloyersPage() {
    const location = useLocation()
    return (
        <section className="grid gap-y-5">
            <CategoryBar />
            <FilterBar />
            {/* <div className="grid grid-rows-[1fr_max-content] grid-cols-[4fr_1fr] gap-x-5 gap-y-8">
                <DepartmentsTable />
                <KpiCard />
                <StatsCards />
            </div> */}
            <EmployeesTable />
        </section>
    )
}

export default EmpoloyersPage
