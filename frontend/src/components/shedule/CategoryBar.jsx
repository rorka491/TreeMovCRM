const CategoryBar = ({ activeSection, setActiveSection }) => {
    const categories = [
        { key: 'teacher', label: 'По преподавателям' },
        { key: 'group', label: 'По группам' },
        { key: 'classroom', label: 'По аудиториям' },
        { key: 'edit', label: 'Редактировать расписание' },
    ];

    return (
        <div className="border-b border-t border-black py-2">
            <ul className="flex space-x-5">
                {categories.map(({ key, label }) => (
                    <li
                        key={key}
                        className={`cursor-pointer border-b-2 ${
                            activeSection === key
                                ? 'border-[#7816db]'
                                : 'border-transparent hover:border-[#7816db]'
                        }`}
                        onClick={() => setActiveSection(key)}
                    >
                        {label}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CategoryBar;
