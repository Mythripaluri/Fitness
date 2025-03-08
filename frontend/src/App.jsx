import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
    const [message, setMessage] = useState("");

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api")
            .then(response => setMessage(response.data.message))
            .catch(error => console.error("Error fetching API:", error));
    }, []);

    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="flex flex-col items-center justify-center w-96 border-2 border-gray-300 rounded-lg p-2">
                <h1 className="scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0">Pose Detection App</h1>
                <p className="mb-4">{message}</p>

                {/* Buttons to start video feeds */}
                <div className="flex flex-col gap-4 text-gray-500">
                    <button className="w-full px-12 py-2 rounded border-2 border-gray-400 hover:bg-slate-200 hover:text-black transition duration-300"
                        onClick={() => window.open("http://127.0.0.1:5000/video_feed_left")}>
                        Left Curl
                    </button>
                    <button className="w-full px-12 py-2 rounded border-2 border-gray-400 hover:bg-slate-200 hover:text-black transition duration-300"
                        onClick={() => window.open("http://127.0.0.1:5000/video_feed_right")}>
                        Right Curl
                    </button>
                    <button className="w-full px-12 py-2 rounded border-2 border-gray-400 hover:bg-slate-200 hover:text-black transition duration-300"
                        onClick={() => window.open("http://127.0.0.1:5000/video_feed_pushup")}>
                        Pushup
                    </button>
                    <button className="w-full px-12 py-2 rounded border-2 border-gray-400 hover:bg-slate-200 hover:text-black transition duration-300"
                        onClick={() => window.open("http://127.0.0.1:5000/video_feed_squat")}>
                        Squat
                    </button>
                </div>
            </div>
        </div>
    );
}

export default App;
