import { useState } from 'react'
import { Navigate, useParams } from 'react-router-dom'
import { api } from '../../../api'

const listKeys = {
    dateOfBirth: 'Дата рождения',
    email: 'Почта',
    phone: 'Телефон',
    parentFullName: 'Родитель',
    parentPhone: 'Телефон родителя',
}

export function StudentProfile() {
    const { studentId } = useParams()
    const [student, setStudent] = useState(null)

    let age = 0
    if (student) {
        const today = new Date()
        const parts = student.dateOfBirth.split(/[/.-]/)
        const birthDate = new Date(
            parseInt(parts[2], 10),
            parseInt(parts[1], 10) - 1,
            parseInt(parts[0], 10)
        )
        console.log(today, birthDate)
        age = today.getFullYear() - birthDate.getFullYear()
        const m = today.getMonth() - birthDate.getMonth()
        if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
            age--
        }
    }

    console.log(age)

    useState(() => {
        api.students.getById(studentId).then(setStudent)
    }, [])

    if (!studentId) {
        return <Navigate to="../" />
    }

    return (
        <div className="border-t-2 h-[100%] p-4 grid gap-[20px] grid-cols-[10fr_9fr] grid-rows-[0.56fr_0.72fr_1fr_50px]">
            <div className="p-3 flex flex-col bg-white rounded-3xl row-start-1 row-end-3">
                <div className="flex gap-5">
                    <div className="relative min-w-[170px] rounded-full overflow-hidden w-[170px] h-[170px]">
                        <div className="absolute content-placeholder inset-0"></div>
                        <img
                            className="absolute object-cover block h-[100%] aspect-auto"
                            src={student?.img}
                            alt={student?.fullName}
                        />
                    </div>
                    <div className="w-[100%] flex flex-col gap-3">
                        {student?.fullName ? (
                            <div>
                                <h3 className="inline font-[900] text-3xl">
                                    {student?.fullName},{' '}
                                    <span className="font-normal">
                                        {age} лет
                                    </span>
                                </h3>
                            </div>
                        ) : (
                            <>
                                <div
                                    style={{ animationDelay: '0.8s' }}
                                    className="content-placeholder rounded-lg max-w-[none] w-[100%] h-8"
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
                                ' flex py-3 justify-between'
                            }
                            key={key}
                        >
                            <div className="text-nowrap">{listKeys[key]}</div>
                            <div className="text-[#6B7280] flex items-end text-right w-[100%]">
                                {student?.[key] ? (
                                    <div className="ml-auto">
                                        {student[key]}
                                    </div>
                                ) : (
                                    <div className="ml-auto w-[30%] h-[100%] content-placeholder"></div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            <div className="bg-white rounded-3xl p-3">
                <div className="flex items-center justify-between">
                    <div className="text-[24px] font-[900]">
                        Абонементы и оплаты
                    </div>
                    <button className='bg-[#7A75FF] w-[30px] h-[30px] flex items-center justify-center rounded-full'>
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
                <div className="ttnorms">
                    <div className="border-b flex py-3 justify-between">
                        <div className="text-nowrap">Статус абонемента</div>
                        <div className="flex items-end text-right w-[100%]">
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
                                <div className="ml-auto w-[30%] h-[100%] content-placeholder"></div>
                            )}
                        </div>
                    </div>
                    <div className="border-b flex py-3 justify-between">
                        <div className="text-nowrap">Задолженность</div>
                        <div className="flex items-end text-right w-[100%]">
                            {typeof student?.debt !== 'undefined' ? (
                                <div className="ml-auto text-[#FF0000]">
                                    {student.debt} р
                                </div>
                            ) : (
                                <div className="ml-auto w-[30%] h-[100%] content-placeholder"></div>
                            )}
                        </div>
                    </div>
                    <div className="flex py-3 justify-between">
                        <div className="text-nowrap">Дата следующей оплаты</div>
                        <div className="flex items-end text-right w-[100%]">
                            {typeof student?.nextPaymentDate === 'string' ? (
                                <div className="ml-auto">
                                    {student.nextPaymentDate.length === 0
                                        ? 'нет'
                                        : student.nextPaymentDate}
                                </div>
                            ) : (
                                <div className="ml-auto w-[30%] h-[100%] content-placeholder"></div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
            <div className="bg-white rounded-3xl p-3">
                <div className="flex items-center justify-between">
                    <div className="text-[24px] font-[900]">
                        Период обучения
                    </div>
                </div>
            </div>
            <div className="bg-white rounded-3xl row-start-2 row-end-4 p-3">
                <div className="flex items-center justify-between">
                    <div className="text-[24px] font-[900]">
                        Последние оценки
                    </div>
                    <button className='bg-[#7A75FF] w-[30px] h-[30px] flex items-center justify-center rounded-full'>
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
            </div>
        </div>
    )
}
