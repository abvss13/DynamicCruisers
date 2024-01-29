import React, { useState } from 'react'
import { FaArrowRight } from "react-icons/fa";
import { FaUserPlus } from "react-icons/fa";
import { RiLockPasswordFill } from "react-icons/ri";
import Image from 'next/image';
import { CiHome } from "react-icons/ci";
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useForm } from 'react-hook-form';


function Login() {
    const router = useRouter();
    const { register, handleSubmit, setError, formState } = useForm();

    const [errorMessage, setErrorMessage] = useState("")

    const handleLogin = async (data) => {
        try {

            const response = await fetch(' http://127.0.0.1:5555/login', {
                method: 'POST',
                headers: {
                    'Content-Type':'application/json',
                },
                body: JSON.stringify(data),
            });

            const responseData = await response.json();
            if (response.ok) {
                //Login successful
                router.push('/');
            } else {
                //Login failed
                setErrorMessage(responseData.error || "Login failed. Please enter the correct email and password.");
            }
        } catch (error) {
            console.error('Error during login:', error);
            setErrorMessage("An error occured during login. Please try again.");
        }
    };


    return (
        <div className='login'>
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
                        <p>Don't have an account? <Link href='/signup'>Sign Up</Link></p>
                    </div>
                </div>
            </div>
            <div className='right__pane'>
                <div className='right__pane__container'>
                    <div className='right__pane__container__text'>
                        <h1>Welcome Back!</h1>
                        <p>Sign in to your account to continue</p>
                        <form className='right__pane__container__text__form' onSubmit={handleSubmit(handleLogin)}>
                            <div className='right__pane__container__text__form__input'>
                                <input {...register('email')} type='text' placeholder='Email...' />
                            </div>
                            <div className='right__pane__container__text__form__input'>
                                <input {...register('password')} type='password' placeholder='Password...' />
                            </div>
                            <div className='right__pane__container__text__form__input'>
                                <button type='submit'>Login <FaArrowRight size={15} /></button>
                            </div>
                            <div className='right__pane__container__text__form__input'>
                                <Link href='/forgotpassword'>Forgot Password?</Link>
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

export default Login