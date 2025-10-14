import React, { useEffect, useState } from 'react'
import logo from '../../assets/logo/Logo.svg'
import { Link, useMatch } from 'react-router-dom'

const Sidebar = ({ isVisible, setIsVisible, setSection }) => {
    const match = useMatch('/:activeSection/*')
    const activeSection = match?.params?.activeSection ?? 'schedule'

    const links = [
        { path: '/analytics', label: 'Аналитика' },
        { path: '/schedule', label: 'Расписание' },
        { path: '/employees', label: 'Сотрудники' },
        { path: '/students', label: 'Ученики' },
        { path: '/financial_reporting', label: 'Финансовая отчётность' },
    ]

    useEffect(() => {
        const currentLink = links.find((link) => activeSection === link.path)
        if (currentLink) {
            setSection(currentLink.label)
        }
    }, [activeSection, setSection])

    return (
        <div className="relative">
            <aside
                id="sidebar"
                className={`w-72 h-screen text-white flex flex-col justify-between transition-transform duration-300 bg-[#7816db] ease-in-out top-0 left-0 ${isVisible ? '' : 'hidden'}`}
            >
                <div>
                    <div className="flex items-center justify-center gap-2 px-6 py-6">
                        <div className="rounded-full p-2">
                            <img src={logo} alt="TreeMov" />
                        </div>
                    </div>

                    <nav className="mt-2 mr-12 ml-6">
                        <ul
                            className="space-y-1"
                            style={{
                                fontFamily: 'Arial, Helvetica, sans-serif',
                                fontSize: '14pt',
                                fontWeight: 'bold',
                            }}
                        >
                            {links.map((link) => (
                                <li key={link.path}>
                                    <Link
                                        to={link.path}
                                        className={`text-[16px] block px-6 py-3 rounded-lg hover:bg-purple-600 ${'/' + activeSection === link.path ? 'bg-[#4b0096]' : ''}`}
                                    >
                                        {link.label}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </nav>
                </div>

                <button
                    onClick={() => setIsVisible(false)}
                    className="absolute top-1/2 right-0 transform -translate-y-1/2 bg-gray-100 transition text-black py-2 rounded-l-[15px] h-[130px]"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="40"
                        height="40"
                        fill="currentColor"
                        viewBox="0 0 16 16"
                    >
                        <path
                            fillRule="evenodd"
                            d="M9.224 1.553a.5.5 0 0 1 .223.67L6.56 8l2.888 5.776a.5.5 0 1 1-.894.448l-3-6a.5.5 0 0 1 0-.448l3-6a.5.5 0 0 1 .67-.223"
                        />
                    </svg>
                </button>
            </aside>

            {!isVisible && (
                <button
                    onClick={() => setIsVisible(true)}
                    className="fixed top-1/2 left-0 transform w-[40px] -translate-y-1/2 bg-[#7816db] text-white py-2 rounded-r-[15px] h-[130px]"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="40"
                        height="40"
                        fill="currentColor"
                        viewBox="0 0 16 16"
                        className="rotate-180"
                    >
                        <path
                            fillRule="evenodd"
                            d="M9.224 1.553a.5.5 0 0 1 .223.67L6.56 8l2.888 5.776a.5.5 0 1 1-.894.448l-3-6a.5.5 0 0 1 0-.448l3-6a.5.5 0 0 1 .67-.223"
                        />
                    </svg>
                </button>
            )}
        </div>
    )
}

export default Sidebar
