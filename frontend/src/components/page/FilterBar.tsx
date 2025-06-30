import { Select, SelectProps } from '../Select'
import { useEffect, useState } from 'react'

export type FilterPart = {
    id: string
    label: string
    setSelected?: (o: any) => void
    selected?: any
} & (
    | ({
          type?: 'select' | undefined
          default?: any
          removeButton?: boolean
      } & Omit<SelectProps<any>, ''>)
    | {
          type: 'date'
      }
)

function getSelectedFromParams(filterData: FilterPart[]) {
    const url = new URL(window.location.href)

    const selectedRes = Object.fromEntries(
        filterData.map((filter) => [filter.id, (filter as any).default])
    )

    for (const key of url.searchParams.keys()) {
        const value = JSON.parse(url.searchParams.get(key) ?? 'null')

        if (!value) {
            continue
        }

        selectedRes[key] = value
    }

    return selectedRes
}

export type FilterSettings<T> = {
    [k in keyof T]?:
        | {
              filterId?: string
              type?:
                  | 'array-vs-array'
                  | 'includes'
                  | 'equal'
                  | 'auto'
                  | undefined
              mapValue?: (val: T[k]) => any
          }
        | { keys: FilterSettings<T[k]> }
}

function fitsFilter<T extends { [k: string]: any }>(
    obj: T,
    filterSettings: FilterSettings<T>,
    filtersSelected: { [k: string]: any }
) {
    for (const key in obj) {
        const setting = filterSettings[key]

        if (!setting) {
            continue
        }

        if (!('keys' in setting)) {
            const value = setting.mapValue
                ? setting.mapValue(obj[key])
                : obj[key]

            const selectedFilter = filtersSelected[setting.filterId ?? key]

            if (!selectedFilter) {
                continue
            }

            switch (setting.type) {
                case undefined:
                case 'auto':
                    if (Array.isArray(selectedFilter) && Array.isArray(value)) {
                        if (
                            selectedFilter.length > 0 &&
                            !selectedFilter.some(
                                (fil) => value.indexOf(fil) !== -1
                            )
                        ) {
                            return false
                        }
                    } else if (
                        Array.isArray(selectedFilter) &&
                        selectedFilter.length > 0 &&
                        !selectedFilter.includes(value)
                    ) {
                        return false
                    } else if (
                        (selectedFilter + '')
                            .toLowerCase()
                            .indexOf((value + '').toLowerCase()) === -1
                    ) {
                        return false
                    }
                    break
                case 'includes':
                    if (
                        Array.isArray(selectedFilter) &&
                        selectedFilter.length > 0 &&
                        !selectedFilter.includes(value)
                    ) {
                        return false
                    } else if (
                        !Array.isArray(selectedFilter) &&
                        (selectedFilter + '')
                            .toLowerCase()
                            .indexOf((value + '').toLowerCase()) === -1
                    ) {
                        return false
                    }

                    break
                case 'array-vs-array':
                    if (Array.isArray(selectedFilter) && Array.isArray(value)) {
                        if (
                            selectedFilter.length > 0 &&
                            !selectedFilter.some(
                                (fil) => value.indexOf(fil) !== -1
                            )
                        ) {
                            return false
                        }
                    }
                    break
                case 'equal':
                    if (selectedFilter === undefined) {
                        continue
                    }
                    if (selectedFilter !== value) {
                        return false
                    }
            }
            continue
        }

        const value = obj[key]

        if (!fitsFilter(value, setting.keys, filtersSelected)) {
            return false
        }
    }

    return true
}

export function filter<T extends { [k: string]: any }>(
    arr: T[],
    filterSettings: FilterSettings<T>,
    filtersSelected: { [k: string]: any }
) {
    return arr.filter((value) =>
        fitsFilter(value, filterSettings, filtersSelected)
    )
}

export function FilterInput({
    part,
    setSelected,
    selected,
}: {
    part: FilterPart
    setSelected?: (o: any) => void
    selected?: any
}) {
    if (part.type === 'select' || part.type === undefined) {
        return (
            <label
                key={part.id}
                className="flex flex-auto max-w-[400px] min-w-0 gap-2 flex-col h-[100%] m-0 justify-between text-xs text-[#616161]"
            >
                <span className="pl-2 text-[14px] font-[700]">
                    {part.label}
                </span>

                <Select
                    {...(part as any)}
                    {...(part.removeButton
                        ? {
                              top: 'Убрать фильтр',
                              topButton: true,
                              onTopButtonClick: () => {
                                  setSelected?.(undefined)
                              },
                          }
                        : {})}
                    className={'text-black text-sm'}
                    onSelected={(newSelected) => {
                        setSelected?.(newSelected)
                        part.onSelected?.(newSelected as any)
                        part.setSelected?.(newSelected)
                    }}
                    selected={selected}
                />
            </label>
        )
    }

    if (part.type == 'date') {
        return (
            <label
                key={part.id}
                className="flex flex-auto max-w-[400px] min-w-0 gap-2 flex-col h-[100%] m-0 justify-between text-xs text-[#616161]"
            >
                <span className="pl-2 text-[14px] font-[700]">
                    {part.label}
                </span>

                <input
                    type="date"
                    className="border-2 border-solid p-2 rounded-2xl bg-white"
                    onChange={(e) => {
                        setSelected?.(e.target.value)
                    }}
                    onFocus={(e) => {
                        e.target.showPicker()
                    }}
                    value={selected + ''}
                />
            </label>
        )
    }

    return <div>Huy</div>
}

export function FilterBar({
    filterData,
    selectedChange,
    disableAddButton,
    disableExportButton,
}: {
    filterData: FilterPart[]
    selectedChange?: (r: { [k: string]: any | undefined }) => void
    disableAddButton?: boolean
    disableExportButton?: boolean
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
            {!disableAddButton && (
                <button className="grid w-10 text-base text-center duration-100 border place-items-center aspect-square hover:bg-gray-50">
                    <span className="flex w-min h-min">+</span>
                </button>
            )}

            {filterData.map((part) => (
                <FilterInput
                    key={part.id}
                    part={part}
                    setSelected={(val) => {
                        setSelected({ ...selected, [part.id]: val })
                    }}
                    selected={selected[part.id]}
                />
            ))}
            {!disableExportButton && (
                <button className="text-xs px-3 font-medium text-purple-600 duration-200 border border-purple-600 rounded-lg py-2.5 hover:bg-purple-100">
                    Экспорт
                </button>
            )}
        </div>
    )
}
