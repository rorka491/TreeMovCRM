import { useState } from 'react'

const departments = ['Все', 'Отдел продаж', 'Бухгалтерия', 'IT', 'HR']

const DropDown = ({ props }) => {
    const { id, label, data } = props
    const [value, setValue] = useState(data[0])

    return (
        <div className="relative text-xs">
            <label htmlFor={id} className="flex mb-2.5 text-[#616161]">
                {label}
            </label>
            <div className="relative">
                <select
                    id={id}
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    className="w-full p-2.5 pr-8 border border-gray-200 rounded-[12.5px] appearance-none focus:outline-none cursor-pointer"
                >
                    {data.map((dep) => (
                        <option key={dep} value={dep}>
                            {dep}
                        </option>
                    ))}
                </select>
                <div className="absolute inset-y-0 right-0 flex items-center px-2 text-gray-400 pointer-events-none">
                    <svg className="w-4 h-4 fill-current" viewBox="0 0 20 20">
                        <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                    </svg>
                </div>
            </div>
        </div>
    )
}

export default DropDown
