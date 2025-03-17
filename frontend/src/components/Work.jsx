import React, { useState, useEffect } from "react";
import axios from "axios";

const Work = () => {
    const [message, setMessage] = useState("");
    const [reps, setReps] = useState("");
    const [counts, setCounts] = useState("");

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api")
            .then(response => setMessage(response.data.message))
            .catch(error => console.error("Error fetching API:", error));
    }, []);

    const handleSubmit = () => {
        console.log(`Reps: ${reps}, Counts: ${counts}`);
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-cover bg-center bg-no-repeat"
            style={{ backgroundImage: "url('/bg-image.jpg')", backgroundSize: "1600px 1000px" }}>

            <div className="flex flex-col items-center justify-center w-96 border-2 border-gray-300 rounded-lg p-4  bg-opacity-80 shadow-lg">
                <h1 className="scroll-m-0 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0">
                    Pose Detection App
                </h1>
                <p className="mb-4">{message}</p>

                {/* Input Fields */}
                <div className="flex flex-col w-full gap-4">
                    <input
                        type="number"
                        placeholder="Enter reps"
                        value={reps}
                        onChange={(e) => setReps(e.target.value)}
                        className="w-full p-2 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
                    />
                    <input
                        type="number"
                        placeholder="Enter counts"
                        value={counts}
                        onChange={(e) => setCounts(e.target.value)}
                        className="w-full p-2 border border-gray-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
                    />
                    <button
                        onClick={handleSubmit}
                        className="w-full px-4 py-2 mt-2 rounded bg-gradient-to-r from-cyan-600 to-cyan-900 text-white hover:bg-cyan-200 transition duration-300"
                    >
                        Submit
                    </button>
                </div>

                {/* Buttons to start video feeds */}
                <div className="flex flex-col gap-6 py-4 text-gray-100">
                    <button className="w-[300px] px-12 py-2 rounded border-4 border-gray-400 hover:bg-slate-200 hover:text-black transition duration-300"
                        onClick={() => window.open("http://127.0.0.1:5000/video_feed_left")}>
                        Left Curl
                    </button>
                    <button className="w-[300px] px-12 py-2 rounded border-4 border-gray-400 hover:bg-slate-200 hover:text-black transition duration-300"
                        onClick={() => window.open("http://127.0.0.1:5000/video_feed_right")}>
                        Right Curl
                    </button>
                    <button className="w-[300px] px-12 py-2 rounded border-4 border-gray-400 hover:bg-slate-200 hover:text-black transition duration-300"
                        onClick={() => window.open("http://127.0.0.1:5000/video_feed_pushup")}>
                        Pushup
                    </button>
                    <button className="w-[300px] px-12 py-2 rounded border-4 border-gray-400 hover:bg-slate-200 hover:text-black transition duration-300"
                        onClick={() => window.open("http://127.0.0.1:5000/video_feed_squat")}>
                        Squat
                    </button>
                </div>
            </div>
        </div>
    )
}

export default Work;
