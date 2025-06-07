const CategoryBar = ({ activeSection, setActiveSection }) => {
    const categories = [
        { key: 'teacher', label: 'По преподавателям' },
        { key: 'group', label: 'По группам' },
        { key: 'classroom', label: 'По аудиториям' },
        { key: 'edit', label: 'Редактировать расписание' },
    ];

    return (
        <div className="border-b border-t border-[#D9D9D9]">
            <ul className="flex">
                {categories.map(({ key, label }) => (
                    <li
                        key={key}
                        className={`group relative flex items-center justify-center h-10 px-4 cursor-pointer`}
                        onClick={() => setActiveSection(key)}
                    >
                        <span className="text-center">{label}</span>
                        <div
                            className={`absolute bottom-0 left-0 h-[1px] w-full transition-all duration-200 ${
                                activeSection === key
                                    ? 'bg-[#7816db]'
                                    : 'bg-transparent group-hover:bg-[#7816db]'
                            }`}
                        />
                    </li>
                ))}
            </ul>
        </div>
    );
};




export default CategoryBar;


