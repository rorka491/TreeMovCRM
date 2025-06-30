import { useState } from 'react'
import { PopUpMenu } from '../PopUpMenu'

function getRowId(row: any) {
    if ('id' in row) {
        return row.id.toString()
    }

    if ('key' in row) {
        return row.key.toString()
    }

    return JSON.stringify(row)
}

type ObjectValue = string | number | Object

type Object = {
    [k: string]: ObjectValue | ObjectValue[]
}

function objectToRow<T extends { [k: string]: any }>(
    object: T,
    keys: KeysObject<T>
): [string, string][] {
    const result: [string, string][] = []

    for (const key in keys) {
        // @ts-ignore
        const value = object[key]
        const keyType = keys[key]!

        if (typeof keyType === 'string') {
            if (Array.isArray(value)) {
                result.push([keyType, value.join(', ')])
            } else {
                result.push([keyType, value + ''])
            }
            continue
        }

        switch (keyType.type) {
            case 'flat': {
                result.push(...objectToRow(value, keyType.keys))
                break
            }
            case 'join': {
                result.push([
                    keyType.str,
                    keyType.keys
                        .map((key) => value[key])
                        .join(keyType.sep ?? ' '),
                ])
                break
            }
            case 'map': {
                result.push([keyType.str, keyType.f(object)])
            }
        }
    }

    return result
}

type KeysObject<T extends { [k: string]: any }> = Partial<{
    [k in keyof T]:
        | string
        | {
              type: 'join'
              sep?: string // default = " "
              str: string
              keys: (keyof T[k])[]
          }
        | {
              type: 'flat'
              keys: KeysObject<T[k]>
          }
        | {
              type: 'map'
              str: string
              f: (i: T) => string
          }
}>

function getKeyLabels<T extends { [k: string]: any }>(keys: KeysObject<T>) {
    const result: string[] = []

    for (const key in keys) {
        const val = keys[key]!

        if (typeof val === 'string') {
            result.push(val)
            continue
        }

        switch (val.type) {
            case 'map':
            case 'join':
                result.push(val.str)
                break
            case 'flat':
                result.push(...getKeyLabels(val.keys))
                break
        }
    }

    return result
}

export function Table<T extends { [k: string]: any }>({
    keys,
    data,
    rowActions,
    conditionalClassNames,
    showSkeleton,
    skeletonAmount,
}: {
    keys: KeysObject<T>
    data: T[]
    rowActions?: { [k: string]: (row: T) => void }
    conditionalClassNames?: Partial<{
        [k in keyof T]: (row: T) => string | undefined | null
    }>
    showSkeleton?: boolean
    skeletonAmount?: number
}) {
    const [popupOpen, setPopupOpen] = useState<string | number>(-1)
    skeletonAmount ??= 8

    return (
        <div className="w-full h-[100%] overflow-y-scroll special-scroll">
            <table className="w-full min-w-0 border-separate border-spacing-y-2">
                <thead>
                    <tr>
                        {getKeyLabels(keys).map((key, i) => (
                            <th
                                className={
                                    (i === 0
                                        ? 'pl-3 font-[700] text-[17px]'
                                        : 'text-gray-600 font-[500]') +
                                    ' px-2 overflow-ellipsis ttnorms max-w-[200px] text-start'
                                }
                                key={key}
                            >
                                {key}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {!showSkeleton
                        ? data
                              .map((row) => ({
                                  id: getRowId(row),
                                  data: objectToRow(row, keys),
                                  row: row,
                              }))
                              .map((row, rowIndex) => (
                                  <tr key={row.id}>
                                      {row.data.map(([key, value], i) => (
                                          <td
                                              className={
                                                  (i === 0
                                                      ? 'border-l-2 pl-3 rounded-l-xl'
                                                      : '') +
                                                  ' text-nowrap px-2 border-y-2 max-w-[200px] truncate py-2 ' +
                                                  (conditionalClassNames
                                                      ? conditionalClassNames[
                                                            key
                                                        ]?.(row.row)
                                                      : '')
                                              }
                                              key={key}
                                          >
                                              {value}
                                          </td>
                                      ))}
                                      {rowActions && (
                                          <td className="border-y-2 py-2 border-r-2 pr-3 rounded-r-xl">
                                              <button
                                                  onClick={() => {
                                                      setPopupOpen(rowIndex)
                                                  }}
                                                  className="w-10 h-5 rounded-xl bg-white border hover:bg-gray-200 grid place-items-center transition"
                                              >
                                                  <svg
                                                      viewBox="0 0 24 24"
                                                      fill="currentColor"
                                                      className="w-5 h-5 rotate-90"
                                                  >
                                                      <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z" />
                                                  </svg>
                                              </button>
                                              <PopUpMenu
                                                  className="flex flex-col gap-3"
                                                  open={popupOpen === rowIndex}
                                                  onClose={() =>
                                                      setPopupOpen(-1)
                                                  }
                                              >
                                                  {Object.keys(rowActions).map(
                                                      (actionName) => (
                                                          <button
                                                              key={actionName}
                                                              onClick={() =>
                                                                  rowActions[
                                                                      actionName
                                                                  ](
                                                                      data[
                                                                          rowIndex
                                                                      ]
                                                                  )
                                                              }
                                                              className="bg-white rounded-xl p-2 border shadow-md hover:bg-[#F0E5FB]"
                                                          >
                                                              {actionName}
                                                          </button>
                                                      )
                                                  )}
                                              </PopUpMenu>
                                          </td>
                                      )}
                                  </tr>
                              ))
                        : Array.from({ length: skeletonAmount }).map((_, i) => (
                              <tr
                                  key={i}
                                  style={{ animationDelay: `${i * 0.1}s` }}
                                  className="bg-gray-300 h-[40px] content-placeholder"
                              >
                                  {Array.from({
                                      length: Object.keys(keys).length + 1,
                                  }).map((_, i) => (
                                      <td
                                          className={
                                              (i === 0
                                                  ? 'pl-3 rounded-l-xl font-200'
                                                  : '') +
                                              (i === Object.keys(keys).length
                                                  ? ' pr-3 rounded-r-xl font-200'
                                                  : '') +
                                              ' text-nowrap truncate max-w-[200px] font-normal text-start'
                                          }
                                          key={i}
                                      ></td>
                                  ))}
                              </tr>
                          ))}
                </tbody>
            </table>
        </div>
    )
}
