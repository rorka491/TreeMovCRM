type EmployeeCardProps = {
    fullName: string
    img: string
    department: string
    position: string
    leaveType: string
    leaveDays: number
    leaveFrom: string
    leaveTo: string
    approvedBy: string
    status: string
}

function EmployeeCard({
    fullName,
    img,
    department,
    position,
    leaveType,
    leaveDays,
    leaveFrom,
    leaveTo,
    approvedBy,
    status,
}: EmployeeCardProps) {
    return (
        <li className="grid items-center grid-cols-[max-content_max-content_1fr_max-content] gap-x-[20px] py-[15px] px-[10px] gap-y-[10px] bg-white rounded-[12.5px]">
            <div className="relative flex justify-center w-full col-start-1 col-end-2 row-start-1 row-end-3 overflow-hidden rounded-full aspect-square">
                <div className="absolute inset-0 content-placeholder"></div>
                <img
                    className="absolute object-cover block h-[100%] aspect-auto"
                    src={img}
                    alt={fullName}
                />
            </div>
            <span className="px-[10px] col-start-1 col-end-2 row-start-3 row-end-4 text-[12px] py-[4.5px] border border-[#D9D9D9] rounded-[12.5px]">
                {leaveType || 'тип отпуска'}
            </span>
            <span className="px-[10px] col-start-1 col-end-2 row-start-4 row-end-5 text-[12px] py-[4.5px] border border-[#D9D9D9] rounded-[12.5px]">
                {leaveDays || 'кол-во'} дней
            </span>
            <span className="col-start-2 col-end-4 row-start-1 row-end-2 px-[10px] py-[7.5px] border border-[#D9D9D9] rounded-[12.5px] text-[14px] font-bold">
                {fullName || 'Фамилия Имя Отчество'}
            </span>

            <span className="font-bold text-[#616161] text-[12px] col-start-2 col-end-3 row-start-2 row-end-3">
                Отдел
            </span>
            <span className="px-[10px] py-[4.5px] text-[12px] border border-[#D9D9D9] rounded-[12.5px] col-start-3 col-end-4 row-start-2 row-end-3">
                {department || 'Отдел'}
            </span>
            <span className="font-bold text-[#616161] text-[12px] col-start-2 col-end-3 row-start-3 row-end-4">
                Должность
            </span>
            <span className="px-[10px] py-[4.5px] text-[12px] border border-[#D9D9D9] rounded-[12.5px] col-start-3 col-end-4 row-start-3 row-end-4">
                {position || 'Должность'}
            </span>
            <div className="flex items-center font-bold text-[#616161] text-[12px] gap-x-[15px] col-start-2 col-end-4 row-start-4 row-end-5">
                Отпуск
                <span>с</span>
                <span className="px-[10px] text-black font-normal py-[4.5px] border border-[#D9D9D9] rounded-[12.5px]">
                    {leaveFrom || 'дата начала'}
                </span>
                по
                <span className="px-[10px] text-black font-normal py-[4.5px] border border-[#D9D9D9] rounded-[12.5px]">
                    {leaveTo || 'дата конца'}
                </span>
            </div>
            <div className="flex items-center font-bold text-[#616161] text-[12px] gap-x-[15px] col-start-2 col-end-4 row-start-5 row-end-6">
                Кем
                <span className="px-[10px] text-black font-normal py-[4.5px] border border-[#D9D9D9] rounded-[12.5px]">
                    {approvedBy || 'ФИО'}
                </span>
                по
                <span
                    className={`${status === 'одобрен' ? 'bg-blue-100' : ''} px-[10px] text-black font-normal py-[4.5px] border border-[#D9D9D9] rounded-[12.5px]`}
                >
                    {status || 'статус'}
                </span>
            </div>
            <button className="grid w-[34px] h-[27px] transition bg-white border rounded-[12.5px] hover:bg-gray-200 place-items-center">
                <svg
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    className="w-5 h-5 rotate-90"
                >
                    <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z" />
                </svg>
            </button>
        </li>
    )
}

export default EmployeeCard
