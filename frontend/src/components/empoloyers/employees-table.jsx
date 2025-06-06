import { Link } from 'react-router-dom'

const employees = [
    {
        id: 1,
        fullName: 'Альберт Рафаилович',
        position: 'Главный менеджер',
        profile: 'Звонки',
        phone: '8 900 000 00 00',
        email: 'antonzhuravlyuv@yopmail.com',
    },
    {
        id: 2,
        fullName: 'Менеджер',
        position: 'Главный менеджер',
        profile: 'Звонки',
        phone: '8 900 000 00 00',
        email: 'antonzhuravlyuv@yopmail.com',
    },
    {
        id: 3,
        fullName: 'Менеджер',
        position: 'Главный менеджер',
        profile: 'Звонки',
        phone: '8 900 000 00 00',
        email: 'antonzhuravlyuv@yopmail.com',
    },
    {
        id: 4,
        fullName: 'Менеджер',
        position: 'Главный менеджер',
        profile: 'Звонки',
        phone: '8 900 000 00 00',
        email: 'antonzhuravlyuv@yopmail.com',
    },
    {
        id: 5,
        fullName: 'Менеджер',
        position: 'Главный менеджер',
        profile: 'Звонки',
        phone: '8 900 000 00 00',
        email: 'antonzhuravlyuv@yopmail.com',
    },
]

const headers = ['№', 'ФИО', 'Должность', 'Профиль', 'Телефон', 'Почта', '']

const EmployeesTable = () => {
    return (
        <section>
            <div className="grid grid-cols-[1fr_5fr_3fr_3fr_4fr_5fr_1fr] mb-4 text-gray-600 gap-2">
                {headers.map((title, i) => (
                    <div
                        key={i}
                        className={
                            (i === 0 || i === 1
                                ? 'text-sm font-bold text-black'
                                : 'text-xs font-medium') + ' truncate'
                        }
                    >
                        {title}
                    </div>
                ))}
            </div>
            <ul className="max-h-[40vh] overflow-y-auto flex flex-col">
                {employees.map((employee) => (
                    <li
                        key={employee.id}
                        className="grid grid-cols-[1fr_5fr_3fr_3fr_4fr_5fr_1fr] items-center text-xs border-y border-[#D9D9D9] hover:bg-gray-100 transition *:py-2.5 *:truncate"
                    >
                        <div>{employee.id}</div>
                        <div>{employee.fullName}</div>
                        <div>{employee.position}</div>
                        <div>{employee.profile}</div>
                        <div>{employee.phone}</div>
                        <div>{employee.email}</div>
                        <button className="w-10 h-10 rounded-[12.5px] bg-white border hover:bg-gray-200 grid place-items-center transition">
                            <svg
                                viewBox="0 0 24 24"
                                fill="currentColor"
                                className="w-5 h-5 rotate-90"
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

export default EmployeesTable
