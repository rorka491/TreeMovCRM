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

export function Table<T>({
    keys,
    data,
    rowActions,
    conditionalClassNames,
    showSkeleton,
    skeletonAmount,
    mapFields,
}: {
    keys:
        | (keyof T)[]
        | Partial<{
              [k in keyof T]: string
          }>
    data: T[]
    rowActions?: { [k: string]: (row: T) => void }
    conditionalClassNames?: Partial<{
        [k in keyof T]: (row: T) => string | undefined | null
    }>
    mapFields?: Partial<{
        [k in keyof T]: (row: T) => any
    }>
    showSkeleton?: boolean
    skeletonAmount?: number
}) {
    const [popupOpen, setPopupOpen] = useState<string | number>(-1)
    skeletonAmount ??= 8

    if (Array.isArray(keys)) {
        const temp: Partial<{
            [k in keyof T]: string
        }> = {}

        for (const key of keys) {
            temp[key] = key.toString()
        }

        keys = temp
    }

    return (
        <div className="w-full h-[100%] overflow-y-scroll special-scroll">
            <table className="w-full min-w-0 border-separate border-spacing-y-2">
                <thead>
                    <tr>
                        {Object.keys(keys).map((key, i) => (
                            <th
                                className={
                                    (i === 0
                                        ? 'pl-3 font-[700] text-[17px]'
                                        : 'text-gray-600 font-[500]') +
                                    ' px-2 overflow-ellipsis ttnorms max-w-[200px] text-start'
                                }
                                key={key}
                            >
                                {keys[key]}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {!showSkeleton
                        ? data.map((row, rowIndex) => (
                              <tr key={getRowId(row)}>
                                  {Object.keys(keys).map((key, i) => (
                                      <td
                                          className={
                                              (i === 0
                                                  ? 'border-l-2 pl-3 rounded-l-xl'
                                                  : '') +
                                              ' text-nowrap px-2 border-y-2 max-w-[200px] truncate py-2 ' +
                                              (conditionalClassNames
                                                  ? conditionalClassNames[
                                                        key
                                                    ]?.(row)
                                                  : '')
                                          }
                                          key={key}
                                      >
                                          {mapFields && key in mapFields
                                              ? mapFields[key]?.(row)
                                              : Array.isArray(row[key])
                                                ? row[key].join(', ')
                                                : row[key]}
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
                                              onClose={() => setPopupOpen(-1)}
                                          >
                                              {Object.keys(rowActions).map(
                                                  (actionName) => (
                                                      <button
                                                          key={actionName}
                                                          onClick={() =>
                                                              rowActions[
                                                                  actionName
                                                              ](row)
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
