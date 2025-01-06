//construct our form component
function Form() {
    return (
        <form className="flex flex-col space-y-4">
            <label className="self-center" >
                URL:<input type="text" name="name" className="bg-blue-500 rounded ml-4"/>
            </label>
            <button type="submit">Submit</button>
        </form>
    );
}

export default Form