import React from 'react'
import Image from 'next/image';
import { IoHomeOutline } from "react-icons/io5";
import { IoCarSportOutline } from 'react-icons/io5';
import { GoCodeReview } from "react-icons/go";
import { IoMdLogIn } from "react-icons/io";
import Background1 from './_background/Background2.jpg';
import Link from 'next/link';
import { useState, useEffect } from 'react';


function Dealerships() {
    const [dealerships, setDealerships] = useState([]);

    useEffect(() => {
        const fetchDealerships = async () => {
            const res = await fetch('http://localhost:5555/dealerships');
            const data = await res.json();
            setDealerships(data);
        }
        fetchDealerships();
    }, []);



    return (
        <div className='dealerships'>
            <div className='body__image'>
                <Image
                    src={Background1}
                    alt="Background Image"
                    layout="fill"
                    objectFit="cover"
                    quality={100}
                />
            </div>
            <div className='nav__links'>
                <div className='search__bar'>
                    <div className='select__brands'>
                        <select name="cars" id="cars">
                            <option value="select">Select Brand</option>
                            <option value="cadillac">Cadillac</option>
                            <option value="toyota">Toyota</option>
                            <option value="mercedes">Mercedes</option>
                            <option value="porshe">Porshe</option>
                            <option value="chevrolet">Chevrolet</option>
                            <option value="nissan">Nissan</option>
                            <option value="jeep">Jeep</option>
                            <option value="rolls-royce">Rolls-Royce</option>
                            <option value="bmw">BMW</option>
                        </select>
                    </div>
                </div>
                <Link href='/' className='nav__links__container'>
                    <div className='nav__links__container__icon'>
                        <IoHomeOutline size={30} />
                    </div>
                    <div className='nav__links__container__text'>
                        <h3>Home</h3>
                    </div>
                </Link>
                <Link href='/cars' className='nav__links__container'>
                    <div className='nav__links__container__icon'>
                        <IoCarSportOutline size={30} />
                    </div>
                    <div className='nav__links__container__text'>
                        <h3>Cars on Sale</h3>
                    </div>
                </Link>
                <Link href='/reviews' className='nav__links__container'>
                    <div className='nav__links__container__icon'>
                        <GoCodeReview size={30} />
                    </div>
                    <div className='nav__links__container__text'>
                        <h3>Car Reviews</h3>
                    </div>
                </Link>
                <Link href='/dashboard' className='nav__links__container'>
                    <div className='nav__links__container__icon'>
                        <IoMdLogIn size={30} />
                    </div>
                    <div className='nav__links__container__text'>
                        <h3>Login | Sign Up</h3>
                    </div>
                </Link>
            </div>

            <div className='body__container'>
                <div className='body__container__text'>
                    <h1>Available Dealerships</h1>
                    <div className='body__container__dealerships'>
                        {dealerships.map((dealership) => (
                            <div className='body__container__dealerships__card'>
                                <div className='body__container__dealerships__card__text'>
                                    <h3>{dealership.name}</h3>
                                    <p>{dealership.location}</p>
                                    <p>{dealership.contact}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div >
    )
}

export default Dealerships