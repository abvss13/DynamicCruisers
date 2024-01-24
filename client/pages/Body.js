import React from 'react'
import { PiWarehouseBold } from "react-icons/pi";
import { IoCarSportOutline } from "react-icons/io5";
import Link from 'next/link'

function Body() {
    return (
        <div className='body'>
            <h1>Welcome to the no. 1 care dealership website!!</h1>
            <h2>Here you can find the best car that suits your needs</h2>
            <h3>Let us start by visiting our delership options or view available cars...</h3>
            <br />
            <br />
            <div className="navlinks" >
                <Link href='/dealerships' className="dealers">
                    <PiWarehouseBold size={60} />
                    <h4>Dealers</h4>
                </Link>

                <Link href='/vehicles' className="cars">
                    <IoCarSportOutline size={60} />
                    <h4>Cars</h4>
                </Link>
            </div>
        </div>
    )
}

export default Body