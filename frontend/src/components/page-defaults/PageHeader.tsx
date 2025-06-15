import React, { useEffect, useState, useRef } from 'react'
import unknown_photo from '../../assets/images/unknown.png'
import { useLocation } from 'react-router-dom'

const headers = {
    schedule: {
        base: 'Расписание',
        sub: {
            'by-teacher': 'По преподавателям',
            'by-group': 'По группам',
            'by-classroom': 'По аудиториям',
            edit: 'Редактировать расписание',
        },
    },
    employees: {
        base: 'Сотрудники',
        sub: {
            main: 'Основное',
            vacation: 'Отпуска',
            analytics: 'Аналитика',
            archive: 'Архив',
        },
    },
    students: {
        base: 'Ученики',
        sub: {
            main: 'Основное',
            grades: 'Оценки',
            payments: 'Оплаты',
            profile: "Профиль"
        },
    },
}

export function PageHeader() {
    const [profile, setProfile] = useState({
        profilePhoto: null,
        username: 'Admin',
    })

    const path = useLocation().pathname

    const [isOpen, setIsOpen] = useState(false)
    const menuRef = useRef<HTMLButtonElement>(null)

    useEffect(() => {
        const handleClickOutside = (e) => {
            if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
                setIsOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () =>
            document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    return (
        <div className="flex justify-between items-center py-4 bg-opacity-100 relative">
            <div className="flex items-baseline gap-3 font-[700]">
                <h1 className="text-[30px] ">
                    {headers[path.split('/')[1]]?.base}
                </h1>
                {path.split('/').length > 2 && (
                    <span className="text-[25px] font-bold pt-1 text-[#616161]">
                        /
                    </span>
                )}
                {path.split('/').length > 2 && (
                    <h2 className="text-[25px] text-[#616161]">
                        {headers[path.split('/')[1]]?.sub?.[path.split('/')[2]]}
                    </h2>
                )}
            </div>

            <button
                ref={menuRef}
                className="items-center w-fit bg-white rounded-[12px] border-none flex gap-2 px-4 py-2 cursor-pointer relative"
                onClick={() => setIsOpen((prev) => !prev)}
                onKeyDown={() => setIsOpen((prev) => !prev)}
            >
                <svg
                    width="24"
                    height="25"
                    viewBox="0 0 24 25"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path
                        fillRule="evenodd"
                        clipRule="evenodd"
                        d="M12.0001 2C11.6022 2 11.2207 2.15804 10.9394 2.43934C10.6581 2.72064 10.5001 3.10218 10.5001 3.5V3.65C8.80602 3.9958 7.28348 4.91627 6.19011 6.25565C5.09675 7.59502 4.49972 9.27102 4.50007 11V17L2.69257 18.992C1.81807 19.9565 2.50207 21.5 3.80257 21.5H9.40207C9.66539 21.956 10.0441 22.3347 10.5001 22.598C10.9562 22.8613 11.4735 22.9999 12.0001 22.9999C12.5267 22.9999 13.044 22.8613 13.5 22.598C13.956 22.3347 14.3348 21.956 14.5981 21.5H20.1976C21.4981 21.5 22.1821 19.955 21.3076 18.992L19.5001 17V11C19.5004 9.27102 18.9034 7.59502 17.81 6.25565C16.7167 4.91627 15.1941 3.9958 13.5001 3.65V3.5C13.5001 3.10218 13.342 2.72064 13.0607 2.43934C12.7794 2.15804 12.3979 2 12.0001 2ZM6.75007 17.87L6.16507 18.512L5.49607 19.25H18.5041L17.8336 18.512L17.2501 17.8685V11C17.2501 10.3106 17.1143 9.62787 16.8504 8.99091C16.5866 8.35395 16.1999 7.7752 15.7124 7.28769C15.2249 6.80018 14.6461 6.41347 14.0092 6.14963C13.3722 5.8858 12.6895 5.75 12.0001 5.75C11.3106 5.75 10.6279 5.8858 9.99098 6.14963C9.35402 6.41347 8.77527 6.80018 8.28776 7.28769C7.80025 7.7752 7.41354 8.35395 7.1497 8.99091C6.88587 9.62787 6.75007 10.3106 6.75007 11V17.87Z"
                        fill="#616161"
                    />
                </svg>

                {profile.profilePhoto ? (
                    <img
                        src={profile.profilePhoto}
                        alt="Avatar"
                        className="w-10 h-10 rounded-full object-cover"
                    />
                ) : (
                    <img
                        src={unknown_photo}
                        alt="Avatar"
                        className="w-10 h-10 rounded-full object-cover"
                    />
                )}

                <p>{profile.username}</p>

                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth="1.5"
                    stroke="currentColor"
                    className="size-6"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="m19.5 8.25-7.5 7.5-7.5-7.5"
                    />
                </svg>

                {isOpen && (
                    <div className="absolute right-0 top-[60px] w-48 bg-white border rounded-lg shadow-lg z-50">
                        <ul className="py-2">
                            <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">
                                Профиль
                            </li>
                            <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">
                                Настройки
                            </li>
                            <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer text-red-500">
                                Выйти
                            </li>
                        </ul>
                    </div>
                )}
            </button>
        </div>
    )
}

export default PageHeader
