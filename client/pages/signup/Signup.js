import React, { useState } from 'react'
import { FaArrowRight } from "react-icons/fa";
import { FaUserPlus } from "react-icons/fa";
import { RiLockPasswordFill } from "react-icons/ri";
import Image from 'next/image';
import Background1 from '../../Public/_background/Background2.jpg';
import { CiHome } from "react-icons/ci";
import Link from 'next/link';
import { useForm } from 'react-hook-form'
import { useRouter} from 'next/router';

function Signup() {
    const router = useRouter();
    const { register, handleSubmit, setError, formState } = useForm();

    const [errorMessage, setErrorMessage] = useState('');

    const handleSignUp = async (data) => {
        try {
            const response = await fetch('http://127.0.0.1:5555/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const responseData = await response.json();
            if (response.ok) {
                // SignUp successful
                router.push('/login'); // Redirect to login page after successful sign-up
            } else {
                // SignUp failed
                setError('email', {
                    type: 'manual',
                    message: responseData.error || 'Sign-up failed. Please check your information.',
                });
            }
        } catch (error) {
            console.error('Error during sign-up:', error);
            setErrorMessage('An error occurred during sign-up. Please try again.');
        }
    };


    return (
        <div className='signup'>
            <div className='left__pane'>
                <div className='left__pane__container'>
                    <div className='left__pane__container__image'>
                    </div>
                    <div className='left__pane__container__text'>
                        <div className='left__pane__icon'>
                            <FaUserPlus size={200} color='green' />
                        </div>
                        <h1>Dynamic Cruisers</h1>
                    </div>
                    <div className='right__pane__container__text__form__input'>
                        <p>Have an account? <Link href='/login'>Sign In</Link></p>
                    </div>
                </div>
            </div>
            <div className='right__pane'>
                <div className='right__pane__container'>
                    <div className='right__pane__container__text'>
                        <h1>Welcome!</h1>
                        <p>Sign up for Greatness!!</p>
                        <form className='right__pane__container__text__form' onSubmit={handleSubmit(handleSignUp)}>
                        <div className='right__pane__container__text__form__input'>
                                <input {...register('firstname')} type='text' placeholder='First Name...' />
                            </div>
                            <div className='right__pane__container__text__form__input'>
                                <input {...register('lastname')} type='text' placeholder='Last Name...' />
                            </div>
                            <div className='right__pane__container__text__form__input'>
                                <input {...register('email')} type='text' placeholder='Email...' />
                            </div>
                            <div className='right__pane__container__text__form__input'>
                                <input {...register('password')} type='password' placeholder='Password...' />
                            </div>
                            <div className='right__pane__container__text__form__input'>
                                <input {...register('repeatPassword')} type='password' placeholder='Repeat Password...' />
                            </div>
                            <div className='right__pane__container__text__form__input'>
                                <button type='submit'>Sign Up <FaArrowRight size={15} /></button>
                            </div>
                        </form>
                        <div className='back__home'>
                            <Link href='/'> <CiHome size={50} color='white' strokeWidth={2} /></Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Signup