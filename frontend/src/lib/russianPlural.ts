/**
 *
 * @param num - число
 * @param singleCase - единственный случай
 * @param smallCase - мало
 * @param bigCase - много
 * @returns singleCase | smallCase | bigCase
 * @example
 * russianPlural(1, 'год', 'года', 'лет') === 'год'
 * russianPlural(2, 'год', 'года', 'лет') === 'года'
 * russianPlural(4, 'год', 'года', 'лет') === 'года'
 * russianPlural(5, 'год', 'года', 'лет') === 'лет'
 * russianPlural(11, 'год', 'года', 'лет') === 'лет'
 * russianPlural(21, 'год', 'года', 'лет') === 'год'
 */
export function russianPlural(
    num: number,
    singleCase: string,
    smallCase: string,
    bigCase: string
): string {
    const lastDigit = num % 10
    const lastTwoDigits = num % 100

    if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
        return bigCase
    }

    if (lastDigit === 1) {
        return singleCase
    }

    if (lastDigit >= 2 && lastDigit <= 4) {
        return smallCase
    }

    return bigCase
}
