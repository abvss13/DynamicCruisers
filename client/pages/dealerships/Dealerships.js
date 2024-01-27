import React from 'react'
import Image from 'next/image';
import { IoHomeOutline } from "react-icons/io5";
import { IoCarSportOutline } from 'react-icons/io5';
import { GoCodeReview } from "react-icons/go";
import { IoMdLogIn } from "react-icons/io";
import { PiWarehouseBold } from 'react-icons/pi';
import { MdDeleteOutline } from "react-icons/md";
import Background1 from './_background/Background1.jpg';
import { FiEdit3 } from "react-icons/fi";
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

    const deleteDealership = async (id) => {
        try {
            const response = await fetch(`http://localhost:5555/dealerships/${id}`, {
                method: 'DELETE',
            });
            if (!response.ok) {
                throw new Error('Something went wrong!');
            }
            // Refresh the list of dealerships after a successful delete
            setDealerships(dealerships.filter(dealership => dealership.id !== id));
        } catch (error) {
            console.error(error);
        }
    };


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
                <Link href='/dealerships' className='nav__links__container'>
                    <div className='nav__links__container__icon'>
                        <PiWarehouseBold size={30} />
                    </div>
                    <div className='nav__links__container__text'>
                        <h3>Dealerships</h3>
                    </div>
                </Link>
                <Link href='/cars' className='nav__links__container'>
                    <div className='nav__links__container__icon'>
                        <IoCarSportOutline size={30} />
                    </div>
                    <div className='nav__links__container__text'>
                        <h3>Cars</h3>
                    </div>
                </Link>
                <Link href='/reviews' className='nav__links__container'>
                    <div className='nav__links__container__icon'>
                        <GoCodeReview size={30} />
                    </div>
                    <div className='nav__links__container__text'>
                        <h3>Reviews</h3>
                    </div>
                </Link>
                <Link href='/dashboard' className='nav__links__container'>
                    <div className='nav__links__container__icon'>
                        <IoMdLogIn size={30} />
                    </div>
                    <div className='nav__links__container__text'>
                        <h3>Login</h3>
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
                                    <h2>{dealership.name}</h2>
                                    <h3>Address: {dealership.address}</h3>
                                    <p>Website: {dealership.website}</p>
                                    <p>Rating: {dealership.rating}</p>
                                    <div className='buttons'>
                                        <button onClick={() => deleteDealership(dealership.id)}><MdDeleteOutline size={20} /></button>
                                        <button><FiEdit3 size={20} /></button>
                                    </div>
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