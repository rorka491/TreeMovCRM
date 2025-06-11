import Select, { SelectOption } from '../Select'
import { useState } from 'react'

type FilterPart = {
    type?: 'select'
    id: string
    label: string
    multiple?: boolean
    options: SelectOption[]
    top?: string
    setSelected?: (o: SelectOption | SelectOption[]) => void
    placeholder?: string
    selected?: SelectOption | SelectOption[]
    checkMarks?: 'square' | 'circle' | boolean
    default?: SelectOption
}

export function FilterBar({ filterData }: { filterData: FilterPart[] }) {
    const [selected, setSelected] = useState<{ [k: string]: SelectOption | SelectOption[] | undefined }>(
        Object.fromEntries(
            filterData.map((filter) => [filter.id, filter.default])
        )
    )

    return (
        <div className="flex grid-flow-col items-end gap-x-2.5 w-full bg-white p-4 rounded-[12.5px] *:rounded-[12.5px]">
            <button className="grid w-10 text-base text-center duration-100 border place-items-center aspect-square hover:bg-gray-50">
                <span className="flex w-min h-min">+</span>
            </button>

            {filterData.map((props, index) => (
                <label
                    key={props.id}
                    className="flex max-w-[400px] flex-auto min-w-0 gap-2 flex-col h-[100%] m-0 justify-between text-xs text-[#616161]"
                >
                    <span className="pl-2 text-[14px] font-[700]">
                        {props.label}
                    </span>
                    <Select
                        multiple={props.multiple}
                        className={'text-black text-sm'}
                        options={props.options}
                        top={props.top}
                        onSelected={(newSelected) => {
                            selected[filterData[index].id] = newSelected
                            setSelected({ ...selected })
                        }}
                        selected={selected[filterData[index].id]}
                        placeholder={props.placeholder}
                    />
                </label>
            ))}
            <button className="text-xs px-3 font-medium text-purple-600 duration-200 border border-purple-600 rounded-lg py-2.5 hover:bg-purple-100">
                Экспорт
            </button>
        </div>
    )
}
