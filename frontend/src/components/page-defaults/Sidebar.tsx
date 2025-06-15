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
        { path: '/settings', label: 'Настройки' },
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

                <div className="px-6 py-4 flex justify-center items-center bg-[#2f213E]">
                    <button className="flex items-center gap-2 text-white hover:text-gray-300">
                        <span className="text-[16px] font-bold">Выйти</span>
                        <svg
                            width="24"
                            height="23"
                            viewBox="0 0 24 23"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M4 11.4991C4 11.7364 4.10536 11.964 4.29289 12.1318C4.48043 12.2996 4.73478 12.3939 5 12.3939H12.59L10.29 14.4428C10.1963 14.526 10.1219 14.6249 10.0711 14.734C10.0203 14.843 9.9942 14.96 9.9942 15.0781C9.9942 15.1962 10.0203 15.3131 10.0711 15.4222C10.1219 15.5312 10.1963 15.6302 10.29 15.7133C10.383 15.7972 10.4936 15.8638 10.6154 15.9092C10.7373 15.9546 10.868 15.978 11 15.978C11.132 15.978 11.2627 15.9546 11.3846 15.9092C11.5064 15.8638 11.617 15.7972 11.71 15.7133L15.71 12.1344C15.801 12.0493 15.8724 11.949 15.92 11.8391C16.02 11.6213 16.02 11.377 15.92 11.1591C15.8724 11.0493 15.801 10.949 15.71 10.8639L11.71 7.28492C11.6168 7.20149 11.5061 7.13532 11.3842 7.09017C11.2624 7.04502 11.1319 7.02178 11 7.02178C10.8681 7.02178 10.7376 7.04502 10.6158 7.09017C10.4939 7.13532 10.3832 7.20149 10.29 7.28492C10.1968 7.36834 10.1228 7.46738 10.0723 7.57638C10.0219 7.68538 9.99591 7.8022 9.99591 7.92018C9.99591 8.03816 10.0219 8.15498 10.0723 8.26398C10.1228 8.37298 10.1968 8.47202 10.29 8.55544L12.59 10.6044H5C4.73478 10.6044 4.48043 10.6987 4.29289 10.8665C4.10536 11.0342 4 11.2618 4 11.4991ZM17 2.55176H7C6.20435 2.55176 5.44129 2.83456 4.87868 3.33794C4.31607 3.84133 4 4.52407 4 5.23597V7.92018C4 8.15748 4.10536 8.38506 4.29289 8.55285C4.48043 8.72065 4.73478 8.81492 5 8.81492C5.26522 8.81492 5.51957 8.72065 5.70711 8.55285C5.89464 8.38506 6 8.15748 6 7.92018V5.23597C6 4.99867 6.10536 4.77109 6.29289 4.60329C6.48043 4.4355 6.73478 4.34123 7 4.34123H17C17.2652 4.34123 17.5196 4.4355 17.7071 4.60329C17.8946 4.77109 18 4.99867 18 5.23597V17.7623C18 17.9996 17.8946 18.2272 17.7071 18.395C17.5196 18.5628 17.2652 18.657 17 18.657H7C6.73478 18.657 6.48043 18.5628 6.29289 18.395C6.10536 18.2272 6 17.9996 6 17.7623V15.0781C6 14.8408 5.89464 14.6132 5.70711 14.4454C5.51957 14.2776 5.26522 14.1833 5 14.1833C4.73478 14.1833 4.48043 14.2776 4.29289 14.4454C4.10536 14.6132 4 14.8408 4 15.0781V17.7623C4 18.4742 4.31607 19.1569 4.87868 19.6603C5.44129 20.1637 6.20435 20.4465 7 20.4465H17C17.7957 20.4465 18.5587 20.1637 19.1213 19.6603C19.6839 19.1569 20 18.4742 20 17.7623V5.23597C20 4.52407 19.6839 3.84133 19.1213 3.33794C18.5587 2.83456 17.7957 2.55176 17 2.55176Z"
                                fill="currentColor"
                            />
                            <path
                                d="M4.29265 12.1325C4.10511 11.9647 3.99976 11.7371 3.99976 11.4998C3.99976 11.2625 4.10511 11.0349 4.29265 10.8671C4.48019 10.6993 4.73454 10.6051 4.99976 10.6051H12.5898L10.2898 8.55612C10.1965 8.4727 10.1226 8.37366 10.0721 8.26466C10.0216 8.15566 9.99567 8.03884 9.99567 7.92086C9.99567 7.80288 10.0216 7.68606 10.0721 7.57706C10.1226 7.46806 10.1965 7.36902 10.2898 7.2856C10.383 7.20217 10.4937 7.136 10.6155 7.09085C10.7373 7.0457 10.8679 7.02246 10.9998 7.02246C11.1316 7.02246 11.2622 7.0457 11.384 7.09085C11.5058 7.136 11.6165 7.20217 11.7098 7.2856L15.7098 10.8645C15.8008 10.9496 15.8722 11.05 15.9198 11.1598C16.0198 11.3776 16.0198 11.622 15.9198 11.8398C15.8722 11.9496 15.8008 12.05 15.7098 12.1351L11.7098 15.714C11.6168 15.7979 11.5062 15.8644 11.3843 15.9099C11.2625 15.9553 11.1318 15.9787 10.9998 15.9787C10.8677 15.9787 10.737 15.9553 10.6152 15.9099C10.4933 15.8644 10.3827 15.7979 10.2898 15.714C10.196 15.6308 10.1216 15.5319 10.0709 15.4228C10.0201 15.3138 9.99396 15.1969 9.99396 15.0788C9.99396 14.9606 10.0201 14.8437 10.0709 14.7347C10.1216 14.6256 10.196 14.5267 10.2898 14.4435L12.5898 12.3945H4.99976C4.73454 12.3945 4.48019 12.3003 4.29265 12.1325Z"
                                fill="currentColor"
                            />
                        </svg>
                    </button>
                </div>

                <button
                    id="hideBtn"
                    onClick={() => setIsVisible(false)}
                    className="absolute top-1/2 right-0 transform -translate-y-1/2 bg-[#FFFFFF33] hover:bg-[#ffffff59] transition text-white py-2 rounded-l-[15px] h-[130px]"
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
                    id="showBtn"
                    onClick={() => setIsVisible(true)}
                    className="fixed top-1/2 left-0 transform -translate-y-1/2 bg-[#7816db] text-white p-2 rounded-r-[15px] h-[130px]"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="w-6 h-16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="3"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M9 5l7 7-7 7"
                        />
                    </svg>
                </button>
            )}
        </div>
    )
}

export default Sidebar
