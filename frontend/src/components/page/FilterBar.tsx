import { Select, SelectProps } from '../Select'
import { useEffect, useState } from 'react'

type FilterPart = {
    type?: 'select' | undefined
    id: string
    label: string
    setSelected?: (o: any) => void
    selected?: any
    default?: any
    removeButton?: boolean
} & Omit<SelectProps<any>, ''>

function getSelectedFromParams(filterData: FilterPart[]) {
    const url = new URL(window.location.href)

    const selectedRes = Object.fromEntries(
        filterData.map((filter) => [filter.id, filter.default])
    )

    for (const key of url.searchParams.keys()) {
        const value = JSON.parse(url.searchParams.get(key) ?? "null")
        
        if (!value) {
            continue
        }

        selectedRes[key] = value
    }

    return selectedRes
}

export function FilterBar({
    filterData,
    selectedChange,
    disableAddButton
}: {
    filterData: FilterPart[]
    selectedChange?: (r: { [k: string]: any | undefined }) => void
    disableAddButton?: boolean
}) {
    const [selected, setSelected] = useState<{ [k: string]: any | undefined }>(
        getSelectedFromParams(filterData)
    )

    // Изменение ссылки вместе с фильтрами
    useEffect(() => {
        const url = new URL(window.location.href)

        for (const key in selected) {
            if (!selected[key]) {
                url.searchParams.delete(key)
                continue
            }

            url.searchParams.set(key, JSON.stringify(selected[key]))
        }

        history.pushState(null, '', url.toString())
    }, [selected])

    useEffect(() => {
        selectedChange?.(selected)
    }, [selected])

    return (
        <div className="flex items-end gap-x-2.5 w-full bg-white p-4 rounded-[12.5px] *:rounded-[12.5px]">
            {!disableAddButton && <button className="grid w-10 text-base text-center duration-100 border place-items-center aspect-square hover:bg-gray-50">
                <span className="flex w-min h-min">+</span>
            </button>}

            {filterData.map((props, index) => (
                <label
                    key={props.id}
                    className="flex flex-auto max-w-[400px] min-w-0 gap-2 flex-col h-[100%] m-0 justify-between text-xs text-[#616161]"
                >
                    <span className="pl-2 text-[14px] font-[700]">
                        {props.label}
                    </span>
                    <Select
                        {...(props as any)}
                        {...(props.removeButton
                            ? {
                                  top: 'Убрать фильтр',
                                  topButton: true,
                                  onTopButtonClick: () => {
                                      selected[filterData[index].id] = undefined
                                      setSelected({ ...selected })
                                  },
                              }
                            : {})}
                        className={'text-black text-sm'}
                        onSelected={(newSelected) => {
                            selected[filterData[index].id] = newSelected
                            setSelected({ ...selected })
                        }}
                        selected={selected[filterData[index].id]}
                    />
                </label>
            ))}
            <button className="text-xs px-3 font-medium text-purple-600 duration-200 border border-purple-600 rounded-lg py-2.5 hover:bg-purple-100">
                Экспорт
            </button>
        </div>
    )
}
