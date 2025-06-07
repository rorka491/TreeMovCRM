import { useRef, useEffect } from 'react'

export function PopUpMenu({ open, setOpen, onClose, children, className }) {
    const ref = useRef(null)

    useEffect(() => {
        function handleClickOutside(e) {
            if (ref.current && !ref.current.parentNode.contains(e.target)) {
                setOpen?.(false)
                
                if (open) {
                    onClose?.()
                }
            }
        }

        document.addEventListener('click', handleClickOutside)
        return () => document.removeEventListener('click', handleClickOutside)
    }, [open])

    return (
        <>
            {open && (
                <div ref={ref} className={className + " absolute top-[100%] z-10"}>
                    {children}
                </div>
            )}
        </>
    )
}
