import { createContext, useState } from 'react'
import { Link } from 'react-router-dom'
import { SearchParams } from '../../lib/search'
import { PopUpMenu } from '../PopUpMenu'

export const categoryBarContext = createContext({
    searchValue: undefined,
})

export type SearchOption<T> = {
    id: string | number
    title?: string
    onSelect: (s: T) => void
    object: T
    searchOptions?: SearchParams<T>
}

export function CategoryBar({
    activeSection,
    categories,
    search,
    searchPlaceholder,
    searchButtonLabel,
    onSearch,
    onSearchInputChange,
    searchOptions,
}: {
    activeSection?: string
    categories: { url: string; label: string }[]
    search?: boolean
    searchPlaceholder?: string
    searchButtonLabel?: string
    onSearch?: (s: string) => void
    onSearchInputChange?: (s: string) => void
    searchOptions?: SearchOption<any>[]
}) {
    const searchActive =
        search ||
        searchPlaceholder ||
        onSearch ||
        onSearchInputChange ||
        (searchOptions && searchOptions.length > 0)

    const [searchOptionsOpen, setSearchOptionsOpen] = useState(false)
    const [searchValue, setSearchValue] = useState('')

    return (
        <div className="flex text-[16px] items-center justify-between border-b border-t border-gray-300">
            <ul className="flex h-full space-x-5">
                {categories.map(({ url, label }) => (
                    <li className="h-full" key={url}>
                        <Link
                            className={`px-3 block h-full py-[10px] cursor-pointer border-b-2 ${activeSection === url || activeSection === label ? 'border-[#7816db]' : 'border-transparent hover:border-[#7816db]'}`}
                            to={url}
                        >
                            {label}
                        </Link>
                    </li>
                ))}
            </ul>
            {searchActive && (
                <>
                    <div
                        onSubmit={(e) => {
                            alert('div')
                            e.preventDefault()
                        }}
                        className="flex h-[100%] items-center gap-2.5 px-3 py-[5px] bg-white rounded-[12.5px]"
                    >
                        <PopUpMenu
                            className="bg-white rounded-2xl min-w-[300px]"
                            open={searchOptionsOpen}
                            onClose={() => setSearchOptionsOpen(false)}
                        >
                            <div className="flex flex-col">
                                {searchOptions && searchOptions.length > 0 ? (
                                    searchOptions.map((option) => (
                                        <button
                                            key={option.id}
                                            onClick={(e) => {
                                                e.preventDefault()
                                                option.onSelect(option.object)
                                            }}
                                            type="button"
                                            className="p-3 hover:bg-gray-100"
                                        >
                                            {option.title}
                                        </button>
                                    ))
                                ) : (
                                    <div className="p-3 border-1 text-center">Ничего</div>
                                )}
                            </div>
                        </PopUpMenu>
                        <input
                            placeholder={searchPlaceholder ?? 'Введите'}
                            value={searchValue}
                            onChange={(e) => {
                                setSearchValue(e.target.value)
                                onSearchInputChange?.(e.target.value)
                            }}
                            onFocus={() => setSearchOptionsOpen(true)}
                        />
                        <button onClick={() => setSearchValue('')}>
                            <svg
                                width="26"
                                height="26"
                                viewBox="5 5 16 16"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    d="M9.81288 15.1365L11.8948 13.0546L9.82842 10.9881L10.6985 10.1181L12.7649 12.1845L14.8313 10.1181L15.7118 10.9985L13.6453 13.0649L15.7118 15.1313L14.8417 16.0014L12.7753 13.935L10.6933 16.0169L9.81288 15.1365Z"
                                    fill="#616161"
                                />
                            </svg>
                        </button>
                        <input
                            onClick={() => onSearch?.(searchValue)}
                            className="rounded-[12.5px] border px-[14.5px] py-[5px] text-[#616161] hover:bg-gray-200 duration-100"
                            type="submit"
                            value={searchButtonLabel ?? 'Поиск'}
                        />
                    </div>
                </>
            )}
        </div>
    )
}

export default CategoryBar
