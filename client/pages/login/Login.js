import React from 'react'
import { FaArrowRight } from "react-icons/fa";
import { FaUserPlus } from "react-icons/fa";
import { RiLockPasswordFill } from "react-icons/ri";
import Image from 'next/image';
import { CiHome } from "react-icons/ci";
import Link from 'next/link';


function Login() {


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
                        <form className='right__pane__container__text__form' >
                            <div className='right__pane__container__text__form__input'>
                                <input type='text' placeholder='Email...' />
                            </div>
                            <div className='right__pane__container__text__form__input'>
                                <input type='password' placeholder='Password...' />
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