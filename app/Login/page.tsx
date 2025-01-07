import React from "react";
import Image from "next/image";

const LoginPage = () => {
  return (
    <section className="bg-gray-800 h-screen pt-[10%] relative flex items-center justify-center">
      {/* Decorative Circles */}
      <div className="top-blue w-[250px] h-[250px] bg-blue-400 rounded-full absolute top-[10%] left-[50%]"></div>
      <div className="bottom-pink w-[280px] h-[280px] bg-pink-400 rounded-full absolute top-[50%] left-[12%] lg:left-[30%]"></div>
      <div className="top-orange w-[300px] h-[300px] bg-orange-400 rounded-full absolute top-[5%] left-[5%] md:left-[23%] lg:left-[30%]"></div>

      {/* Main Content */}
      <div
        className="container w-[350px] sm:w-[350px] m-auto text-center p-8 text-white z-10"
        style={{ backdropFilter: "blur(20px)" }}
      >
        {/* Avatar/Logo */}
        <img
          id="passport"
          src="/User_Avatar.png"
          alt="User Avatar"
          className="mx-auto w-32 h-32 rounded-full border-4 border-white"
        />

        {/* Welcome Text */}
        <p className="mt-4">
          <span className="text-xl sm:text-2xl font-bold">Login Here</span>
        </p>

        <hr className="my-4 border-gray-400" />

        {/* Login Form */}
        <form method="POST">
          <input
            type="text"
            id="username"
            placeholder="Username..."
            className="w-full p-2 mx-auto text-base sm:text-lg bg-gray-700 rounded-md mb-4"
          />
          <input
            type="password"
            id="password"
            placeholder="Password..."
            className="w-full p-2 mx-auto text-base sm:text-lg bg-gray-700 rounded-md mb-4"
          />
          <button
            type="submit"
            className="p-2 sm:text-lg bg-blue-500 rounded-2xl m-8 w-36 mx-auto sm:w-48 hover:bg-gradient-to-r hover:from-orange-500 hover:via-pink-500 hover:to-pink-700"
          >
            Login
          </button>
        </form>

        {/* SignUp Link */}
        <p className="mt-4">
          If you're new here, click to{" "}
          <a href="#" className="underline hover:text-pink-300">
            SignUp
          </a>
        </p>
      </div>
    </section>
  );
};

export default LoginPage;
