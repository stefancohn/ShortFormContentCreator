interface Props {
    caption: string,
}

function CaptionDisplay({ caption }: Props) {
    const handleCopy = () => {
        navigator.clipboard.writeText(caption);
    };
    
    return <>
    <div className="blue-glass text-white whitespace-pre-wrap flex flex-col items-center justify-center p-4 m-4">
        {caption}
        <div className={`m-2`}>
            <button className="blue-button font-bold" onClick={handleCopy}>Copy</button>
        </div>
    </div>
    </>
}

export default CaptionDisplay