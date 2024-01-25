import React from 'react'
import Link from 'next/link'
import { IoCarSportSharp } from "react-icons/io5";

function Header() {
    return (
        <div className='header' >
            <div className="logo">
                <Link href="/">
                    <IoCarSportSharp size={80} color='white' />
                </Link>
            </div>
            <Link className='header_tag' href="/" >
                <h1>Dynamic Cruisers</h1>
                <p>...find your dream car today!!!</p>
            </Link>
        </div>
    )
}

export default Header