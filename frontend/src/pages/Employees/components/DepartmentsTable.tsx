import { Link } from 'react-router-dom'

const departments = [
    {
        name: 'Отдел продаж',
        employeesCount: 43,
        accessLevel: 'Микс',
        onShift: 11,
        code: '001',
    },
    {
        name: 'Отдел закупок',
        employeesCount: 11,
        accessLevel: 'Ограничены',
        onShift: 2,
        code: '002',
    },
    {
        name: 'Кураторы',
        employeesCount: 21,
        accessLevel: 'Полный',
        onShift: 10,
        code: '003',
    },
    {
        name: 'Преподаватели',
        employeesCount: 56,
        accessLevel: 'Только свой',
        onShift: 36,
        code: '004',
    },
    {
        name: 'Бухгалтерия',
        employeesCount: 15,
        accessLevel: 'Ограничены',
        onShift: 8,
        code: '005',
    },
    {
        name: 'IT-отдел',
        employeesCount: 25,
        accessLevel: 'Полный',
        onShift: 12,
        code: '006',
    },
    {
        name: 'Маркетинг',
        employeesCount: 18,
        accessLevel: 'Микс',
        onShift: 9,
        code: '007',
    },
    {
        name: 'HR-отдел',
        employeesCount: 8,
        accessLevel: 'Ограничены',
        onShift: 4,
        code: '008',
    },
    {
        name: 'Логистика',
        employeesCount: 30,
        accessLevel: 'Только свой',
        onShift: 15,
        code: '009',
    },
    {
        name: 'Администрация',
        employeesCount: 12,
        accessLevel: 'Полный',
        onShift: 6,
        code: '010',
    },
]

const headers = [
    'Все отделы',
    'Кол-во сотрудников',
    'Права доступа',
    'Сейчас на смене',
    'Код отдела',
    '',
]

function DepartmentsTable() {
    return (
        <section>
            <div className="grid grid-cols-[2fr_repeat(5,1fr)] mb-4 text-gray-600">
                {headers.map((title, i) => {
                    return i === 0 ? (
                        <div className="text-sm font-bold text-black">
                            {title}
                        </div>
                    ) : (
                        <div
                            key={i}
                            className="text-xs font-medium text-center"
                        >
                            {title}
                        </div>
                    )
                })}
            </div>

            <ul className="max-h-[40vh] overflow-y-auto">
                {departments.map((department) => (
                    <li
                        key={department.code}
                        className="*:py-2.5 text-center text-xs text-gray-600 grid grid-cols-[2fr_repeat(5,1fr)] border border-[#D9D9D9] items-center hover:bg-gray-50 rounded-[12.5px]"
                    >
                        <Link
                            className="grid h-full p-2.5 rounded-[12.5px] font-medium text-left bg-white border w-max hover:bg-gray-200 place-items-center"
                            to={'/empoloyers/' + department.code}
                        >
                            {department.name}
                        </Link>
                        <div>{department.employeesCount}</div>
                        <div>{department.accessLevel}</div>
                        <div>{department.onShift}</div>
                        <div>{department.code}</div>
                        <button className="w-10 rounded-[12.5px] bg-white border hover:bg-gray-200 grid place-items-center">
                            <svg
                                viewBox="0 0 24 24"
                                fill="currentColor"
                                className="w-5 rotate-90 aspect-square"
                            >
                                <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z" />
                            </svg>
                        </button>
                    </li>
                ))}
            </ul>
        </section>
    )
}

export default DepartmentsTable
