import { useEffect, useRef, useState } from 'react'

export type SelectOption =
    | {
          key: string
          value: string
      }
    | string

function optionValue(option: SelectOption) {
    return typeof option === 'object' && option !== null && 'value' in option
        ? option.value
        : option + ''
}
function optionKey(option: SelectOption) {
    return typeof option === 'object' && option !== null && 'key' in option
        ? option.key
        : option + ''
}

export function RadioButton({
    onChange,
    checked,
    avoidButton,
}: {
    onChange?: (b: boolean) => void
    checked?: boolean
    avoidButton?: boolean
}) {
    const inner = (
        <svg
            width="17"
            height="17"
            viewBox="0 0 17 17"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            xmlnsXlink="http://www.w3.org/1999/xlink"
        >
            <rect
                x="0.5"
                y="0.5"
                width="16"
                height="16"
                rx="4.5"
                stroke="#616161"
            />
            <rect
                x="2"
                y="2.5"
                width="12"
                height="12"
                fill="url(#pattern0_2222_3012)"
            />
            {checked && (
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    viewBox="0 0 16 16"
                >
                    <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425z" />
                </svg>
            )}
        </svg>
    )

    return avoidButton ? (
        <div>{inner}</div>
    ) : (
        <button
            onClick={() => onChange?.(!checked)}
            onKeyDown={() => onChange?.(!checked)}
        >
            {inner}
        </button>
    )
}

export function Option({
    option,
    selected,
    checkMark,
    onClick,
}: {
    option: SelectOption
    selected?: boolean
    checkMark?: 'square' | 'circle' | boolean
    onClick: React.MouseEventHandler<HTMLButtonElement>
}) {
    const value = optionValue(option)
    //const key = optionKey(option)

    if (!checkMark) {
        return (
            <button
                onClick={onClick}
                className="cursor-pointer text-left px-3 py-2 hover:bg-gray-200"
            >
                {value}
            </button>
        )
    }

    // TODO!!!!
    if (checkMark === 'circle') {
        return (
            <div className="text-left px-3 py-2 hover:bg-gray-200">
                <button onClick={onClick}>{value}</button>
            </div>
        )
    }

    if (checkMark === 'square') {
        return (
            <button
                onClick={onClick}
                className="flex items-center gap-2 text-left px-3 py-2 hover:bg-gray-200"
            >
                <RadioButton avoidButton={true} checked={selected} />
                {value}
            </button>
        )
    }

    return (
        <button
            onClick={onClick}
            className="text-left px-3 py-1 hover:bg-gray-200"
        >
            {value}
        </button>
    )
}

// types of selections
// by amount
// single, multiple, n
//
// styles
// top = bool | string
export function Select({
    options,
    setSelected,
    top,
    placeholder,
    multiple,
    selected,
    checkMarks,
    className,
}: {
    options: SelectOption[]
    setSelected?: (o: SelectOption | SelectOption[]) => void
    top?: string | boolean
    placeholder?: string
    multiple?: boolean
    selected?: SelectOption | SelectOption[]
    checkMarks?: 'square' | 'circle' | boolean
    className?: string
}) {
    const [open, setOpen] = useState(false)

    const optionsRef = useRef<HTMLDivElement>(null)

    if (multiple && !selected) {
        selected = []
    }

    if (multiple && selected && Array.isArray(selected) === false) {
        selected = [selected]
    }

    function onOptionClick(option: SelectOption) {
        if (!setSelected) {
            return
        }

        if (!selected) {
            setSelected(multiple ? [option] : option)
            return
        }

        if (multiple && Array.isArray(selected)) {
            const index = selected.indexOf(option)

            if (index !== -1) {
                const newSelected = [...selected]
                newSelected.splice(index, 1)
                setSelected(newSelected)
            } else {
                setSelected([...selected, option])
            }

            return
        }

        setSelected(multiple ? [option] : option)
        setOpen(false)
    }

    function isOptionSelected(option: SelectOption) {
        if (!selected) {
            return
        }

        const key = optionKey(option)
        const value = optionValue(option)

        if (Array.isArray(selected)) {
            return (
                selected.indexOf(key) !== -1 || selected.indexOf(value) !== -1
            )
        }

        return selected === key || selected === value
    }

    useEffect(() => {
        function handleClickOutside(e: MouseEvent) {
            if (optionsRef.current && !optionsRef.current.contains(e.target as Node)) {
                setOpen(false)
            }
        }

        document.addEventListener('click', handleClickOutside)
        return () => document.removeEventListener('click', handleClickOutside)
    }, [])

    return (
        <div
            ref={optionsRef}
            className={
                'width-100 min-w-[100px] relative max-width-[none] ' +
                (className ?? '')
            }
        >
            <button
                onClick={() => {
                    setOpen(true)
                }}
                className="min-w-0 w-full max-w-[none] border-2 border-solid p-2 rounded-2xl flex items-center justify-between gap-3"
            >
                <span className="min-w-0 w-[calc(90%)] text-left truncate">
                    {Array.isArray(selected)
                        ? selected.length !== 0
                            ? selected.join(', ')
                            : (placeholder ?? 'Выберите')
                        : ((selected as any)?.key ??
                          selected ??
                          placeholder ??
                          'Выберите')}
                </span>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    viewBox="0 0 16 16"
                >
                    <path
                        fillRule="evenodd"
                        d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708"
                    />
                </svg>
            </button>
            {open && (
                <div
                    className={
                        (top ? 'pb-1' : 'py-1') +
                        ' overflow-hidden border-2 border-solid flex flex-col text-left min-w-min max-width-[none] absolute bg-white rounded-xl top-[100%] left-0 right-0'
                    }
                >
                    {top && (
                        <div className="px-3 py-2 bg-[#D8B4FE] text-white">
                            {typeof top === 'string'
                                ? top
                                : (placeholder ?? 'Выберите')}
                        </div>
                    )}
                    {options.map((option) => (
                        <Option
                            selected={isOptionSelected(option)}
                            checkMark={multiple ? 'square' : checkMarks}
                            onClick={(e) => {
                                e.preventDefault()
                                e.stopPropagation()
                                onOptionClick(option)
                            }}
                            key={optionKey(option)}
                            option={option}
                        />
                    ))}
                </div>
            )}
        </div>
    )
}

export default Select
