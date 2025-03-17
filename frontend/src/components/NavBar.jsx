import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { Menu, X } from "lucide-react";

const NavBar = () => {
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);

  const toggleNavbar = () => {
    setMobileDrawerOpen(!mobileDrawerOpen);
  };

  return (
    <nav className='sticky top-0 x-50  py-3 backdrop-blur-lg border-b border-neutral-700/80'>
      <div className='container px-4 mx-auto relative text-md'>
        <div className='flex items-center justify-between'>
          <div className='flex items-center flex-shrink-0'>
            <span className='text-xl tracking-tight'>FitLens</span>
          </div>
          <ul className='hidden lg:flex ml-40 space-x-12'>
          <li>
              <NavLink to='/' className={({ isActive }) => isActive ? 'text-cyan-600' : ''}>
                Home
              </NavLink>
            </li>
            <li>
              <NavLink to='/learn' className={({ isActive }) => isActive ? 'text-cyan-600' : ''}>
                Learn
              </NavLink>
            </li>
            <li>
              <NavLink to='/workout' className={({ isActive }) => isActive ? 'text-cyan-600' : ''}>
                Try Exercises
              </NavLink>
            </li>
            <li>
              <NavLink to='/profile' className={({ isActive }) => isActive ? 'text-cyan-600' : ''}>
                Profile
              </NavLink>
            </li>
          </ul>
          {/* <div className='hidden lg:flex justify-center space-x-12 items-center'>
            <NavLink to='/signin' className='py-2 px-3 border rounded-md'>
              Sign In
            </NavLink>
            <NavLink to='/signup' className='bg-gradient-to-r from-cyan-600 to-cyan-900 py-2 px-3 rounded-md'>
              Create an account
            </NavLink>
          </div> */}
          <div className='lg:hidden md-flex flex-col justify-end'>
            <button onClick={toggleNavbar}>
              {mobileDrawerOpen ? <X /> : <Menu />}
            </button>
          </div>
        </div>
        {mobileDrawerOpen && (
          <div className='fixed right-0 z-20 bg-neutral-900 w-full p-12 flex flex-col justify-center items-center lg:hidden'>
            <ul>
              <li className='py-4'>
                <NavLink to='/learn' className={({ isActive }) => isActive ? 'text-cyan-600' : ''}>
                  Learn
                </NavLink>
              </li>
              <li className='py-4'>
                <NavLink to='/workout' className={({ isActive }) => isActive ? 'text-cyan-600' : ''}>
                  Try Exercises
                </NavLink>
              </li>
              <li className='py-4'>
                <NavLink to='/profile' className={({ isActive }) => isActive ? 'text-cyan-600' : ''}>
                  Profile
                </NavLink>
              </li>
            </ul>
            {/* <div className='flex space-x-6'>
              <NavLink to='/signin' className='py-2 px-3 border rounded-md'>
                Sign In
              </NavLink>
              <NavLink to='/signup' className='py-2 px-3 border rounded-md bg-gradient-to-r from-cyan-600 to-cyan-900'>
                Create an account
              </NavLink>
            </div> */}
          </div>
        )}
      </div>
    </nav>
  );
};

export default NavBar;
