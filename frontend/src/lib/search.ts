export type SearchParams<T> = Partial<{
    [k in keyof T]:
        | (
              | {
                    type: 'array'
                    forAll: SearchParams<T[k] extends (infer R)[] ? R : never>
                    multiplier?: number
                }
              | {
                    type: 'subs'
                    subs: SearchParams<T[k]>
                    multiplier?: number
                }
              | {
                    type: 'string'
                    perCase?: {
                        add?: number
                        multiple?: number
                    }
                    minCases?: number
                    stopAtCases?: number
                }
          )
        | 'string'
}>

function fillSearchParams<T extends { [k: string]: any }>(
    obj: T,
    searchOptions: SearchParams<T>
): SearchParams<T> {
    const newSearchOptions: SearchParams<T> = {}

    for (const key in obj) {
        const val = obj[key]
        if (searchOptions[key]) {
            newSearchOptions[key] = searchOptions[key]
            continue
        }

        if (typeof val === 'object' && val) {
            newSearchOptions[key] = {
                type: 'subs',
                subs: fillSearchParams(obj, {}),
            } as SearchParams<T>[typeof key]
            continue
        }

        if (Array.isArray(val)) {
            newSearchOptions[key] = {
                type: 'array',
                forAll: fillSearchParams(val[0], {}),
            } as SearchParams<T>[typeof key]
            continue
        }

        newSearchOptions[key] = 'string'
    }

    return newSearchOptions
}

export function getSearchScore<T extends { [k: string]: any }>(
    obj: T,
    searchOptions: SearchParams<T>,
    str: string,
    goThroughAllKeys?: boolean
) {
    let cases = 0
    let score = 0

    if (goThroughAllKeys) {
        searchOptions = fillSearchParams(obj, searchOptions)
    }

    for (const key in searchOptions) {
        const setting = searchOptions[key]!

        if (setting === 'string') {
            const val = obj[key].toString?.() ?? obj[key] + ''

            const occurancies = val.split(str).length
            cases += occurancies
            score += occurancies
            continue
        }

        switch (setting.type) {
            case 'string': {
                const val = obj[key].toString?.() ?? obj[key] + ''
                let occurancies = val.split(str).length

                cases += occurancies

                if (occurancies < (setting?.minCases ?? 0)) {
                    break
                }

                occurancies = Math.max(
                    0,
                    Math.min(occurancies, setting.stopAtCases ?? Infinity)
                )

                score += occurancies * (setting.perCase?.add ?? 1)
                score *= (setting.perCase?.multiple ?? 1) ** occurancies
                break
            }
            case 'subs': {
                let [subScore, subCases] = getSearchScore(
                    obj[key],
                    setting.subs,
                    str,
                    goThroughAllKeys
                )

                subScore *= setting.multiplier ?? 1

                score += subScore
                cases += subCases
                break
            }
            case 'array': {
                const val = obj[key] as any[]

                if (!Array.isArray(val)) {
                    break
                }

                let [subScore, subCases] = val.reduce<[number, number]>(
                    (result, current) => {
                        const [subScore, subCases] = getSearchScore(
                            current,
                            setting.forAll,
                            str,
                            goThroughAllKeys
                        )

                        return [result[0] + subScore, result[1] + subCases]
                    },
                    [0, 0]
                )

                cases += subCases
                score += subScore * (setting.multiplier ?? 1)
                break
            }
        }
    }

    return [score, cases] as const
}
