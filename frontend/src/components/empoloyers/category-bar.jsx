import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'

const categories = [
    { key: '', label: 'Основное' },
    { key: 'vacation', label: 'Отпуска' },
    { key: 'analytic', label: 'Аналитика' },
    { key: 'archive', label: 'Архив' },
]

const CategoryBar = () => {
    const location = useLocation()
    const [searchValue, setSearchValue] = useState('')

    return (
        <div className="flex justify-between border-y border-[#D9D9D9]  text-xs">
            <ul className="grid grid-flow-col grid-rows-1 w-min">
                {categories.map(({ key, label }) => (
                    <li
                        key={key}
                        className="relative flex flex-col group w-max"
                    >
                        <Link
                            to={'/empoloyers/' + key}
                            className={'cursor-pointer py-2.5 px-4'}
                        >
                            {label}
                        </Link>
                        <div
                            className={`w-full h-[1px] duration-100 bg-[#7816db] group-hover:scale-x-100 group-hover:opacity-50 absolute bottom-[-3px]
                                ${
                                    location.pathname.split('/')[2] === key
                                        ? 'scale-x-100'
                                        : 'scale-x-0'
                                }
                            `}
                        ></div>
                    </li>
                ))}
            </ul>
            <form className="grid items-center grid-rows-1 grid-cols-[1fr_repeat(2,max-content)] gap-x-2.5 px-2.5 py-[5px] bg-white rounded-[12.5px]">
                <input
                    type="text"
                    placeholder="Найти в сотрудниках..."
                    className="py-1.5 bg-inherit"
                    value={searchValue}
                    onChange={(e) => setSearchValue(e.target.value)}
                />
                <button
                    className="grid w-6 duration-100 aspect-square place-content-center rounded-[12.5px] hover:bg-gray-200"
                    type="reset"
                    onClick={(e) => {
                        e.preventDefault()
                        setSearchValue('')
                    }}
                >
                    <svg
                        fill="#000"
                        width="9"
                        height="9"
                        viewBox="0 0 16 16"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path d="M4.11 2.697L2.698 4.11 6.586 8l-3.89 3.89 1.415 1.413L8 9.414l3.89 3.89 1.413-1.415L9.414 8l3.89-3.89-1.415-1.413L8 6.586l-3.89-3.89z"></path>
                    </svg>
                </button>

                <button
                    type="submit"
                    className="rounded-[12.5px] border px-[14.5px] py-[5px] text-[#616161] hover:bg-gray-200 duration-100"
                    onClick={(e) => {
                        e.preventDefault()
                        console.log('В поиске: ' + searchValue)
                    }}
                >
                    Поиск
                </button>
            </form>
        </div>
    )
}

export default CategoryBar
