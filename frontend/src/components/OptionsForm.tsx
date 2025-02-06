import { useState } from "react";

interface Props {
    inputOptions: {
        [key: string]: string;
    };

    selectOptions: {
        [key: string]: string[];
    }

    onOptionsChange: (key: string, value: string) => void;

}

function OptionsForm ({inputOptions, selectOptions, onOptionsChange}: Props) {
    const [collapse, setCollapse] = useState<boolean>(true);

    function handleOptionsChange(key: string, value: string) {
        onOptionsChange(key, value);
    }

    return (
    <>
        <div className="blue-glass flex flex-col justify-center items-center">
            <button onClick={()=>setCollapse(!collapse)} className={`underline font-extrabold pb-2 transition-all ease-in duration-1000`}>Options&nbsp;&nbsp;<strong>{collapse ? '+' : '-'}</strong></button>

            {/* Our form that iterates over options 
            Needs lots of conditionals on the collapse so the styling is proper for expansion*/}
            <div className={`${collapse ? "gap-0" : "gap-8"} flex flex-col justify-center items-center transition-all ease-in duration-1000`}>

                {/* Iterate over all the inputs, place them in template */}
                {Object.entries(inputOptions).map(([key, value]) => (
                <div key={key} className={`${collapse ? "invisible opacity-0 h-0" : "opacity-100 h-8"} items-center transition-all ease-in duration-1000 flex flex-col`}>
                    <label>{key}</label>
                    <input type={value} className="text-black" onChange={(e) => handleOptionsChange(key, e.target.value)}></input>
                </div>
                ))}

                {/* Iterate over all select options */}
                {Object.entries(selectOptions).map(([key, value]) => (
                <div className={`${collapse ? "opacity-0 h-0" : "opacity-100 h-12"} flex flex-col items-center transition-all ease-in duration-1000`}>
                    <label>{key}</label>
                    <select className="text-black" onChange={(e) => handleOptionsChange(key, e.target.value)}>
                        {value.map((value) => (
                            <option>{value}</option>
                        ))}
                    </select>
                </div>
                ))}

            </div>
            
        </div>
    </>
    );
    }

export default OptionsForm;

{/*<>
    <div className="blue-glass flex flex-col justify-center items-center">
        <button onClick={()=>setCollapse(!collapse)} className={`transition-all ease-in duration-1000`}>Options&nbsp;&nbsp;<strong>{collapse ? '+' : '-'}</strong></button>
        <input type="number" className={`${collapse ? "h-0" : "h-8"} text-black transition-all ease-in duration-1000`}></input>
    </div>
</>*/}