

const CategoryBar = ({ activeSection }) => {
    // список категорий для удобства
    const categories = [
        { key: 'teacher', label: 'По преподавателям', href: '#' },
        { key: 'group', label: 'По группам', href: '#' },
        { key: 'classroom', label: 'По аудиториям', href: '#' },
        { key: 'edit', label: 'Редактировать расписание', href: '#' },
    ];

    return (
        <div className="border-b border-t border-gray-300 py-2">
            <ul className="flex space-x-5">
                {categories.map(({ key, label, href }) => (
                    <li
                        key={key}
                        className={`border-b-2 ${
                            activeSection === key
                                ? 'border-[7816db]'
                                : 'border-transparent hover:border-[7816db]'
                        }`}
                    >
                        <a href={href}>{label}</a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CategoryBar;
