import React from 'react'
import { FaArrowRight } from "react-icons/fa";
import { FaUserPlus } from "react-icons/fa";
import { RiLockPasswordFill } from "react-icons/ri";

function Login() {
    return (
        <div className='login'>
            <div className='left__pane'>
                <div className='left__pane__container'>
                    <div className='left__pane__container__text'>
                        <h1>Dynamic Cruisers</h1>
                        <p>...find your dream car today!!!</p>
                    </div>
                    <div className='right__pane__container__text__form__input'>
                        <p>Don't have an account? <a href='/signup'>Sign Up</a></p>
                    </div>
                </div>
            </div>
            <div className='right__pane'>
                <div className='right__pane__container'>
                    <div className='right__pane__container__text'>
                        <h1>Welcome Back!</h1>
                        <p>Sign in to your account to continue</p>
                        <form className='right__pane__container__text__form'>
                            <div className='right__pane__container__text__form__input'>
                                <input type='text' placeholder='<FaUserPlus /> Email' />
                            </div>
                            <div className='right__pane__container__text__form__input'>
                                <input type='password' placeholder='<RiLockPasswordFill /> Password' />
                            </div>
                            <div className='right__pane__container__text__form__input'>
                                <button type='submit'>Login <FaArrowRight size={30} /></button>
                            </div>
                            <div className='right__pane__container__text__form__input'>
                                <a href='/forgotpassword'>Forgot Password?</a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login