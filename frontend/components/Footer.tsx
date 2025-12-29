"use client";

import Link from "next/dist/client/link";

export default function Footer() {
  return (
    <footer className="m-[50px] grid grid-cols-3 grid-rows-2 h-[600px]">
      <div className="border rounded-tl-xl p-5 w-full h-full flex justify-center items-center">
        <h1 className="logo text-[64px] tracking-[-6px]">Skill Lantern</h1>
      </div>
      <div className="border-b border-r border-t p-5 w-full h-full flex flex-col justify-between">
        <h3 className="footer-h">Links</h3>
        <ul className="text-[#555551]">
          <li><Link href="/features">Features</Link></li>
          <li><Link href="/howitworks">How it Works</Link></li>
          <li><Link href="/contact">Contact</Link></li>
        </ul>
      </div>
      <div className="border-b border-r border-t rounded-tr-xl p-5 w-full h-full flex flex-col justify-between">
        <h3 className="footer-h">Sections</h3>
        <ul className="text-[#555551]">
          <li><Link href="#About">About Skill Lantern</Link></li>
          <li><Link href="#Why">Why Choose Skill Lantern</Link></li>
          <li><Link href="#Join">Join Skill Lantern Now</Link></li>
        </ul>
      </div>
      <div className="border-b border-r border-l rounded-bl-xl p-5 w-full h-full flex flex-col justify-end space-y-5 text-[#555551]">
        <div>
          <p>© 2025 Skill Lantern — Smart Career Recommendation Platform </p>
          <p> All Rights Reserved.</p>
        </div>
        <div>
          <p>(+977) 9824155271</p>
          <p>support@skilllantern.com</p>
        </div>
      </div>
      <div className="border-b border-r p-5 w-full h-full flex flex-col justify-between">
        <h3 className="footer-h">Skill Lantern is All About</h3>
        <p className="text-[#555551]">
          AI-powered career recommendation platform helping students discover
          personalized career paths, explore detailed roadmaps, and make
          confident decisions about their future.
        </p>
      </div>
      <div className="border-b border-r rounded-br-xl p-5 w-full h-full flex flex-col justify-between">
        <h3 className="footer-h">Write Us</h3>

        <form action="" className="space-y-5">
          <div className="flex w-full">
            <div>
              <label className="block border-t border-b py-2 text-sm" htmlFor="">
                Name
              </label>
              <label className="block border-b py-2 text-sm" htmlFor="">
                Email
              </label>
              <label className="block border-b py-2 text-sm" htmlFor="">
                Phome
              </label>
            </div>
            <div className="">
              <input
                className="pl-20 border-t border-b py-2 w-full text-sm"
                type="text"
                placeholder="Full Name"
              />
              <input
                className="pl-20 border-b py-2 w-full text-sm"
                type="text"
                placeholder="your@email.com"
              />
              <input
                className="pl-20 border-b py-2 w-full text-sm"
                type="text"
                placeholder="(+977) 1234567890"
              />
            </div>
          </div>
          <div className="w-full flex justify-end">
            <button className="border rounded-full px-5 py-1 text-sm bg-black text-white ">
              Send
            </button>
          </div>
        </form>
      </div>
    </footer>
  );
}
