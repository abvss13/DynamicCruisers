import React from 'react'
import Image from 'next/image'
import Background1 from '../Public/Background/Background1.jpg'


function Body() {
    return (
        <div className='body'>
            <div className='body__image'>
                <Image
                    src={Background1}
                    alt="Background Image"
                    layout="fill"
                    objectFit="cover"
                    quality={100}
                />
            </div>
            <div className='body__container'>
                <div className='body__container__text'>
                    <h1>Find the best car for you</h1>
                    <p>Find the best car that suits your needs. We have a wide range of cars for you to choose from.</p>
                </div>
                <div className='body__container__icons'>
                    <div className='body__container__icons__icon'>
                        <PiWarehouseBold />
                        <p>Wide range of cars</p>
                    </div>
                    <div className='body__container__icons__icon'>
                        <IoCarSportOutline />
                        <p>Best prices</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Body