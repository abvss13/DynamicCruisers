import React, { useState } from 'react';
import Image from 'next/image';
import { PiWarehouseBold } from 'react-icons/pi';
import { IoCarSportOutline } from 'react-icons/io5';
import { GoCodeReview } from "react-icons/go";
import { IoMdLogIn } from "react-icons/io";
import { IoHomeOutline } from "react-icons/io5";
import Background1 from './_background/Background3.jpg';
import Link from 'next/link';

function AddDealer() {
    const [dealerData, setDealerData] = useState({
        name: '',
        address: '',
        website: '',
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setDealerData({
            ...dealerData,
            [name]: value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('http://localhost:5555/dealerships', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dealerData),
            });

            if (!response.ok) {
                throw new Error('Failed to add dealer');
            }

            // Assuming the response contains the added dealer data, you can handle it here
            const addedDealer = await response.json();
            console.log('Added Dealer:', addedDealer);

            // Add logic to update state or perform any other actions based on the response
        } catch (error) {
            console.error('Error adding dealer:', error);
        }
    };


    return (
        <div>
            <div className='add__dealer'>
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
                            <h3>Dealers</h3>
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
                    <Link href='/login' className='nav__links__container'>
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
                        <h1>Add Dealer</h1>
                        <div className='body__container__form'>
                            <form onSubmit={handleSubmit}>
                                <div className='body__container__form__input'>
                                    <input
                                        type="text"
                                        name="name"
                                        id="name"
                                        placeholder='name'
                                        value={dealerData.name}
                                        onChange={handleInputChange}
                                    />
                                </div>
                                <div className='body__container__form__input'>
                                    <input
                                        type="text"
                                        name="address"
                                        id="address"
                                        placeholder='address'
                                        value={dealerData.address}
                                        onChange={handleInputChange}
                                    />
                                </div>
                                <div className='body__container__form__input'>
                                    <input
                                        type="text"
                                        name="website"
                                        id="website"
                                        placeholder='website'
                                        value={dealerData.website}
                                        onChange={handleInputChange}
                                    />
                                </div>
                                <div className='submit__button'>
                                    <button type="submit">Submit</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div >
        </div>
    );
}

export default AddDealer;
