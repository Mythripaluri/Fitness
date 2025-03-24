import { useState, useEffect } from "react";
import axios from "axios";

const Work = () => {
    const [message, setMessage] = useState("");
    const [reps, setReps] = useState("");
    const [counts, setCounts] = useState("");
    const [selectedExercise, setSelectedExercise] = useState("left"); // Default exercise

    // Load initial message from Flask API
    useEffect(() => {
        axios
            .get("http://127.0.0.1:5000/api")
            .then((response) => setMessage(response.data.message))
            .catch((error) => console.error("Error fetching API:", error));
    }, []);

    // Submit handler to trigger video feed
    const handleSubmit = (e) => {
        e.preventDefault();
        const url = `http://127.0.0.1:5000/video_feed_${selectedExercise}?reps=${reps || 10}&sets=${counts || 3}`;
        window.open(url, "_blank"); // Open video feed in a new tab
    };

    return (
        <div
            className="flex items-center justify-center min-h-screen bg-cover bg-center bg-no-repeat"
            style={{ backgroundImage: "url('/bg-image.jpg')", backgroundSize: "1600px 1000px" }}
        >
            <div className="flex flex-col items-center justify-center w-96 border-2 border-gray-300 rounded-lg p-4 bg-opacity-80 shadow-lg">
                <h1 className="scroll-m-0 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0">
                    Pose Detection App
                </h1>
                <p className="mb-4">{message}</p>

                {/* Form to handle inputs */}
                <form
                    onSubmit={handleSubmit}
                    className="flex flex-col w-full gap-4"
                >
                    {/* Select Exercise */}
                    <select
                        value={selectedExercise}
                        onChange={(e) => setSelectedExercise(e.target.value)}
                        className="w-full p-2 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
                    >
                        <option value="left">Left Curl</option>
                        <option value="right">Right Curl</option>
                        <option value="pushup">Pushup</option>
                        <option value="squat">Squat</option>
                        <option value="kneetaps">Knee Taps</option>
                        <option value="op">Overhead Pendulum</option>
                        <option value="lunges">Lunges</option>
                    </select>

                    {/* Input for Reps */}
                    <input
                        type="number"
                        placeholder="Enter reps"
                        value={reps}
                        onChange={(e) => setReps(e.target.value)}
                        className="w-full p-2 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
                    />
                    
                    {/* Input for Sets */}
                    <input
                        type="number"
                        placeholder="Enter sets"
                        value={counts}
                        onChange={(e) => setCounts(e.target.value)}
                        className="w-full p-2 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
                    />
                    
                    {/* Submit Button */}
                    <button
                        type="submit"
                        className="w-full px-4 py-2 mt-2 rounded bg-gradient-to-r from-cyan-600 to-cyan-900 text-white hover:bg-cyan-200 transition duration-300"
                    >
                        Start Exercise
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Work;

