export function russianPlural(num, singleCase, smallCase, bigCase) {
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
