import { useState } from "react";

interface Props {
    options: {
        [key: string]: string;
    };
}

function OptionsForm ({options}: Props) {
    const [collapse, setCollapse] = useState<boolean>(true);
    return (
    <>
        <div className="blue-glass flex flex-col justify-center items-center">
            <button onClick={()=>setCollapse(!collapse)} className={`transition-all ease-in duration-1000`}>Options&nbsp;&nbsp;<strong>{collapse ? '+' : '-'}</strong></button>
            <input type="number" className={`${collapse ? "h-0" : "h-8"} text-black transition-all ease-in duration-1000`}></input>
        </div>
    </>
    );
}

export default OptionsForm;