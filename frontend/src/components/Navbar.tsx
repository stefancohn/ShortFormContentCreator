import logo from '../assets/logo.png'
import wordLogo from '../assets/wordLogo.png'

function Navbar() {
    return(
    <>
    <nav className="bg-blue-600 p-2 mb-4">
        <div className='flex flex-row items-center justify-evenly '>
            <div className="flex flex-row space-x-5 items-center group">
                <img src={logo} className="size-11 group-hover:animate-spin-slow"></img>
                <img src={wordLogo} className="w-18 h-12"></img>
            </div>
            <a href="" className="nav-item">Home</a>
            <a href="" className="nav-item">About</a>
            <a href="" className="nav-item">Contact</a>
        </div>
    </nav>
    </>)
}

export default Navbar