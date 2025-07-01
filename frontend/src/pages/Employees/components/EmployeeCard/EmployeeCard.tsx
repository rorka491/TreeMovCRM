import React from "react";

type EmployeeCardProps {
    name: string;
    department: string;
    position: string;
    leaveType: string;
    leaveDays: number;
    leaveFrom: string;
    leaveTo: string;
    approvedBy: string;
    status: string;
}

function EmployeeCar({
    name,
    department,
    position,
    leaveType,
    leaveDays,
    leaveFrom,
    leaveTo,
    approvedBy,
    status,
}:EmployeeCardProps) {
    return (
        <li className="grid employee-card">
            {/* Avatar */}
            <div className="employee-card__avatar" />
            {/* Name */}
            <div className="employee-card__name">{name}</div>
            {/* Department */}
            <div className="employee-card__department">
                <span>Отдел</span>
                <span>{department}</span>
            </div>
            {/* Position */}
            <div className="employee-card__position">
                <span>Должность</span>
                <span>{position}</span>
            </div>
            {/* Leave Type */}
            <div className="employee-card__leave-type">{leaveType}</div>
            {/* Leave Days */}
            <div className="employee-card__leave-days">{leaveDays} дней</div>
            {/* Leave Dates */}
            <div className="employee-card__leave-dates">
                <span>Отпуск</span>
                <span>с {leaveFrom} по {leaveTo}</span>
            </div>
            {/* Approved By */}
            <div className="employee-card__approved-by">
                <span>Кем</span>
                <span>{approvedBy}</span>
            </div>
            {/* Status */}
            <div className="employee-card__status">{status}</div>
        </li>
    );
};

export default EmployeeCard;
