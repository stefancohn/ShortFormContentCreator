interface Props {
    Options: {
        [key: string]: string;
    };
}

function OptionsForm (options: Props) {
    return (
    <>
        <div className="blue-glass flex flex-col collapsible">
            <button type="submit"></button>
        </div>
    </>
    );
}

export default OptionsForm;