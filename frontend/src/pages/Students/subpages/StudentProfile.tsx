import { useEffect, useState } from 'react'
import { Link, Navigate, useParams } from 'react-router-dom'
import { api } from '../../../api'
import { russianPlural } from '../../../lib/russianPlural'
import { formatDate } from '../../../lib/formatDate'
import { getDifferenceMonthsAndYears } from '../../../lib/getDifferenceMonthsAndYears'
import { Student } from '../../../api/fakeApi'
import { parseDate } from '../../../lib/parseDate'

const listKeys = {
    dateOfBirth: 'Дата рождения',
    email: 'Почта',
    phone: 'Телефон',
    parentFullName: 'Родитель',
    parentPhone: 'Телефон родителя',
}

const gradeToColor = {
    Хорошо: '#22C55E',
    Отлично: '#22C55E',
    Удовлетворительно: '#FFAB25',
    Плохо: '#FF1814',
}

function formatDateDifference(months, years) {
    let result = ''

    if (years > 0) {
        result += `${years} ${russianPlural(years, 'год', 'года', 'лет')} `
    }

    if (months > 0) {
        result += `${months} ${russianPlural(months, 'месяц', 'месяца', 'месяцев')}`
    }

    if (result.length === 0) {
        result = 'меньше месяца'
    }

    return result
}

export function StudentProfile() {
    const { studentId } = useParams()
    const [student, setStudent] = useState<Student | undefined>(undefined)

    let age = 0

    if (student) {
        ;[, age] = getDifferenceMonthsAndYears(
            parseDate(student.dateOfBirth),
            new Date()
        )
    }

    useEffect(() => {
        api.students.getById(studentId).then(setStudent)
    }, [])

    if (!studentId) {
        return <Navigate to="../" />
    }

    const debt = student?.payments?.reduce(
        (result, cur) => result + cur.debt,
        0
    )

    return (
        <div className="border-t-2 h-[100%] p-4 grid gap-[20px] grid-cols-[10fr_9fr] grid-rows-[0.56fr_0.72fr_1fr_50px]">
            <div className="min-h-0 overflow-hidden p-3 flex flex-col bg-white rounded-3xl row-start-1 row-end-3">
                <div className="flex gap-5">
                    <div className="relative min-w-[170px] rounded-full overflow-hidden w-[170px] h-[170px]">
                        <div className="absolute content-placeholder inset-0"></div>
                        <img
                            className="absolute object-cover block h-[100%] aspect-auto"
                            src={student?.img}
                            alt={student?.fullName}
                        />
                    </div>
                    <div className="w-full flex flex-col gap-3">
                        {student?.fullName ? (
                            <div className="max-h-[112px] overflow-hidden">
                                <h3 className="inline font-[900] text-3xl">
                                    {student?.fullName},{' '}
                                    <span className="font-normal">
                                        {age}
                                        {russianPlural(
                                            age,
                                            'год',
                                            'года',
                                            'лет'
                                        )}
                                    </span>
                                </h3>
                            </div>
                        ) : (
                            <>
                                <div
                                    style={{ animationDelay: '0.8s' }}
                                    className="content-placeholder rounded-lg max-w-[none] w-full h-8"
                                />
                                <div className="flex gap-2">
                                    <div
                                        style={{ animationDelay: '0.9s' }}
                                        className="content-placeholder rounded-lg max-w-[none] w-[40%] h-8"
                                    />
                                    <div
                                        style={{ animationDelay: '1.3s' }}
                                        className="content-placeholder rounded-lg max-w-[none] w-[40%] h-8"
                                    />
                                </div>
                            </>
                        )}
                        <div className="flex gap-2">
                            {student?.groups?.map((group) => (
                                <div
                                    className="flex-auto text-center max-w-[109px] bg-[#7A75FF] text-white px-5 py-1 rounded-full"
                                    key={group}
                                >
                                    {group}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
                <div className="flex ttnorms flex-col h-[100%]">
                    {Object.keys(listKeys).map((key, i, arr) => (
                        <div
                            className={
                                (i !== arr.length - 1 ? 'border-b' : '') +
                                ' flex h-[100%] items-center justify-between'
                            }
                            key={key}
                        >
                            <div className="text-nowrap">{listKeys[key]}</div>
                            <div className="text-[#6B7280] flex items-end text-right w-full">
                                {student && key in student ? (
                                    <div className="ml-auto">
                                        {student[key]}
                                    </div>
                                ) : (
                                    <div className="ml-auto w-[30%] h-[1.2em] content-placeholder"></div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            <div className="min-h-0 overflow-hidden bg-white rounded-3xl p-3 flex flex-col">
                <div className="flex items-center justify-between">
                    <div className="text-[24px] font-[900]">
                        Абонементы и оплаты
                    </div>
                    <button className="bg-[#7A75FF] w-[30px] h-[30px] flex items-center justify-center rounded-full">
                        <svg
                            width="16"
                            height="16"
                            viewBox="0 0 16 16"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M12.175 9H0V7H12.175L6.575 1.4L8 0L16 8L8 16L6.575 14.6L12.175 9Z"
                                fill="white"
                            />
                        </svg>
                    </button>
                </div>
                <div className="ttnorms flex flex-col h-[100%]">
                    <div className="border-b flex h-[100%] items-center justify-between">
                        <div className="text-nowrap">Статус абонемента</div>
                        <div className="flex items-end text-right w-full">
                            {typeof student?.subscriptionActive ===
                            'boolean' ? (
                                <div className="ml-auto flex items-center gap-1">
                                    <svg
                                        width="8"
                                        height="9"
                                        viewBox="0 0 8 9"
                                        fill="none"
                                        xmlns="http://www.w3.org/2000/svg"
                                    >
                                        <circle
                                            cx="4"
                                            cy="4.5"
                                            r="4"
                                            fill={
                                                student.subscriptionActive
                                                    ? '#0FEA1D'
                                                    : '#990000'
                                            }
                                        />
                                    </svg>
                                    {student.subscriptionActive
                                        ? 'активен'
                                        : 'неактивен'}
                                </div>
                            ) : (
                                <div className="ml-auto w-[30%] h-[1.2em] content-placeholder"></div>
                            )}
                        </div>
                    </div>
                    <div className="border-b flex h-[100%] items-center justify-between">
                        <div className="text-nowrap">Задолженность</div>
                        <div className="flex items-end text-right w-full">
                            {typeof debt !== 'undefined' ? (
                                <div
                                    className={
                                        'ml-auto ' +
                                        (debt > 0
                                            ? 'text-[#FF0000]'
                                            : 'text-black')
                                    }
                                >
                                    {debt} р
                                </div>
                            ) : (
                                <div className="ml-auto w-[30%] h-[1.2em] content-placeholder"></div>
                            )}
                        </div>
                    </div>
                    <div className="flex h-[100%] items-center justify-between">
                        <div className="text-nowrap">Дата следующей оплаты</div>
                        <div className="flex items-end text-right w-full">
                            {student?.payments ? (
                                <div className="ml-auto">
                                    {student.payments.length === 0
                                        ? 'нет'
                                        : parseDate(
                                                student.payments[
                                                    student.payments.length - 1
                                                ].date
                                            ) > new Date()
                                          ? student.payments[
                                                student.payments.length - 1
                                            ].date
                                          : 'Нет'}
                                </div>
                            ) : (
                                <div className="ml-auto w-[30%] h-[1.2em] content-placeholder"></div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
            <div className="min-h-0 overflow-hidden bg-white rounded-3xl p-3 flex flex-col">
                <div className="flex items-center justify-between">
                    <div className="text-[24px] pb-1 font-[900]">
                        Период обучения
                    </div>
                </div>
                <div className="h-[100%] min-w-0 flex flex-col overflow-y-auto special-scroll">
                    <table
                        className="w-full h-[100%] min-w-0 text-left ttnorms text-[14px]"
                        style={{
                            maxHeight:
                                30 + 40 * (student?.studies?.length ?? 13),
                        }}
                    >
                        <thead>
                            <tr className="font-[700]">
                                <th>Предмет</th>
                                <th>Начало занятий</th>
                                <th>Прошло с начала</th>
                            </tr>
                        </thead>
                        <tbody className="font-[400]">
                            {student?.studies
                                ? student?.studies.map((study, i) => (
                                      <tr
                                          className={
                                              i !== student.studies.length - 1
                                                  ? 'border-y'
                                                  : ''
                                          }
                                          key={study.subject + study.startDate}
                                      >
                                          <td>{study.subject}</td>
                                          <td className="py-1">
                                              {formatDate(
                                                  parseDate(study.startDate),
                                                  'dd m_short yyyy',
                                                  { padDay: false }
                                              )}
                                          </td>
                                          <td className="text-[#6B7280]">
                                              {formatDateDifference(
                                                  ...getDifferenceMonthsAndYears(
                                                      parseDate(
                                                          study.startDate
                                                      ),
                                                      new Date()
                                                  )
                                              )}
                                          </td>
                                      </tr>
                                  ))
                                : Array.from({ length: 13 }).map((_, i) => (
                                      <tr key={i}>
                                          <td className="max-h-[60px] min-h-0">
                                              <div className="mr-auto w-[170px] h-[1.6em] content-placeholder"></div>
                                          </td>
                                          <td className="py-1 flex h-[100%] items-center justify-center text-[12px] text-center">
                                              <div className="my-auto w-[60%] h-[1.6em] content-placeholder"></div>
                                          </td>
                                          <td className={`text-center`}>
                                              <div className="ml-auto mr-7 w-[90%] h-[1.6em] content-placeholder"></div>
                                          </td>
                                      </tr>
                                  ))}
                        </tbody>
                    </table>
                </div>
            </div>
            <div className="min-h-0 overflow-hidden bg-white flex flex-col rounded-3xl row-start-2 row-end-4 p-3">
                <div className="flex items-center justify-between">
                    <div className="text-[24px] font-[900]">
                        Последние оценки
                    </div>
                    <button className="bg-[#7A75FF] w-[30px] h-[30px] flex items-center justify-center rounded-full">
                        <svg
                            width="16"
                            height="16"
                            viewBox="0 0 16 16"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M12.175 9H0V7H12.175L6.575 1.4L8 0L16 8L8 16L6.575 14.6L12.175 9Z"
                                fill="white"
                            />
                        </svg>
                    </button>
                </div>

                <div className="h-[100%] min-w-0 flex flex-col overflow-y-auto special-scroll">
                    <table
                        className={`w-full h-[100%] text-left ttnorms text-[14px]`}
                        style={{
                            maxHeight:
                                30 + 35 * (student?.grades?.length ?? 90),
                        }}
                    >
                        <thead>
                            <tr className="font-[700]">
                                <th>Предмет</th>
                                <th className="text-center">Группа</th>
                                <th className="text-center">Оценка</th>
                            </tr>
                        </thead>
                        <tbody className="font-[400]">
                            {student?.grades
                                ? student?.grades.map((study, i) => (
                                      <tr
                                          className={
                                              (i !== student.studies.length - 1
                                                  ? 'border-y'
                                                  : '') +
                                              ' min-h-0 max-h-[60px]'
                                          }
                                          key={i}
                                      >
                                          <td className="max-h-[60px] py-1 min-h-0">
                                              {study.subject}
                                          </td>
                                          <td className="text-[12px] py-1 text-center">
                                              {study.group}
                                          </td>
                                          <td
                                              className={`text-[${gradeToColor[study.score]}] py-1 text-center`}
                                          >
                                              {study.score}
                                          </td>
                                      </tr>
                                  ))
                                : Array.from({ length: 90 }).map((_, i) => (
                                      <tr key={i}>
                                          <td className="max-h-[60px] py-1 min-h-0">
                                              <div className="mr-auto w-[90%] h-[1.6em] content-placeholder"></div>
                                          </td>
                                          <td className="flex h-[100%] items-center justify-center text-[12px] text-center">
                                              <div className="my-auto w-[60%] h-[1.6em] content-placeholder"></div>
                                          </td>
                                          <td className={`text-center`}>
                                              <div className="ml-auto w-[90%] h-[1.6em] content-placeholder"></div>
                                          </td>
                                      </tr>
                                  ))}
                        </tbody>
                    </table>
                </div>
            </div>
            <div className="min-h-0 overflow-hidden flex justify-between col-start-1 col-end-3">
                <Link
                    className="bg-[#5810A1] flex items-center justify-center text-white rounded-2xl flex-auto max-w-[270px]"
                    to={'./edit'}
                >
                    <span>Изменить профиль</span>
                </Link>
                <button className="bg-[#2F213E] self-right rounded-2xl px-3.5 flex-auto text-white max-w-[200px] flex justify-between items-center">
                    <svg
                        width="16"
                        height="18"
                        viewBox="0 0 16 18"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M3 18C2.45 18 1.97934 17.8043 1.588 17.413C1.19667 17.0217 1.00067 16.5507 1 16V3C0.71667 3 0.479337 2.904 0.288004 2.712C0.0966702 2.52 0.000670115 2.28267 3.44827e-06 2C-0.000663218 1.71733 0.0953369 1.48 0.288004 1.288C0.48067 1.096 0.718003 1 1 1H5C5 0.716667 5.096 0.479333 5.288 0.288C5.48 0.0966668 5.71734 0.000666667 6 0H10C10.2833 0 10.521 0.0960001 10.713 0.288C10.905 0.48 11.0007 0.717333 11 1H15C15.2833 1 15.521 1.096 15.713 1.288C15.905 1.48 16.0007 1.71733 16 2C15.9993 2.28267 15.9033 2.52033 15.712 2.713C15.5207 2.90567 15.2833 3.00133 15 3V16C15 16.55 14.8043 17.021 14.413 17.413C14.0217 17.805 13.5507 18.0007 13 18H3ZM13 3H3V16H13V3ZM6 14C6.28334 14 6.521 13.904 6.713 13.712C6.905 13.52 7.00067 13.2827 7 13V6C7 5.71667 6.904 5.47933 6.712 5.288C6.52 5.09667 6.28267 5.00067 6 5C5.71734 4.99933 5.48 5.09533 5.288 5.288C5.096 5.48067 5 5.718 5 6V13C5 13.2833 5.096 13.521 5.288 13.713C5.48 13.905 5.71734 14.0007 6 14ZM10 14C10.2833 14 10.521 13.904 10.713 13.712C10.905 13.52 11.0007 13.2827 11 13V6C11 5.71667 10.904 5.47933 10.712 5.288C10.52 5.09667 10.2827 5.00067 10 5C9.71734 4.99933 9.48 5.09533 9.288 5.288C9.096 5.48067 9 5.718 9 6V13C9 13.2833 9.096 13.521 9.288 13.713C9.48 13.905 9.71734 14.0007 10 14Z"
                            fill="white"
                        />
                    </svg>
                    <span>Удалить профиль</span>
                </button>
            </div>
        </div>
    )
}
